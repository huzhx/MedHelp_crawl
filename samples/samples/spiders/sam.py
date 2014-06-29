from scrapy.spider import BaseSpider
from scrapy.spider import Spider
from scrapy.contrib.spiders import SitemapSpider
from scrapy.selector import Selector
from samples.items import GItem
from samples.items import CItem
from scrapy.utils.response import get_base_url
import re
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from samples.items import TItem
from scrapy.utils.url import urljoin_rfc
from scrapy.http import Request
from samples.items import UItem
from urlparse import urljoin
from samples.items import SItem
from samples.items import JItem
from samples.items import JItem2
from samples.items import NItem
from samples.items import CommunityItem
from samples.items import TrackerItem
from samples.items import FriendItem
from samples.items import GroupItem
from samples.items import ForumItem
 
class MedHelp_general(SitemapSpider):
    sitemap_urls = ['http://www.medhelp.org/sitemaps/mh_smi_general.xml']
    name = 'mhg'
    def parse(self, response):
        print response.url
        return

class WebPageContent(BaseSpider):
    name = "mhg_parser"
    def __init__(self, filename=None):
        if filename:
            data = open(filename).read().split("\n")
            for i in data:
                self.start_urls.append(i)
    allowed_domains = ['medhelp.org']
    start_urls = []
    def parse(self,response):
        sel = Selector(response)
        item = GItem()
        item['url'] = get_base_url(response)
        item['question_page_id'] = response.url.split('/')[-1]
        item['question_forum_name'] = sel.xpath('//div[@class="contentalign"]/text()').extract()[0].strip()
        item['question_forum_id'] = sel.xpath('//div[@class="bar"]/div[@class="back header_link"]/a/@href').extract()[0].split('/')[-1]
        item['question_title'] = sel.xpath('//div[@class="desc"]/text()').extract()[0].strip()
        item['question_post_id'] = sel.xpath('//div[@id="new_posts_show_middle"]/div[@class="post_data has_bg_color"]/@id').extract()[0]
        item['user_id'] = sel.xpath('//div[@class="user_info"]/div/span/a/@href').extract()[0].split('/')[-1]
        item['user_name'] = sel.xpath('//div[@class="user_info"]/div/span/a/text()').extract()[0]
        item['question_time'] = ''.join(sel.xpath('//div[@class="user_info"]/div/text()').extract()[1:]).strip()
        
        x = len(sel.xpath('//div[@class="subject_comments_number"]/span[@class="comments_num"]/a/text()').extract())
        if(x == 0):
            item['comment_num'] = re.compile('\d*').findall(sel.xpath('//div[@class="subject_comments_number"]/span[@class="comments_num"]/span/text()').extract()[0])[0]
        else:
            item['comment_num'] = re.compile('\d*').findall(sel.xpath('//div[@class="subject_comments_number"]/span[@class="comments_num"]/a/text()').extract()[0])[0]
        
        question_post_id = item['question_post_id']
        question_content_raw0 =  ''.join(sel.xpath('//div[@id="'+question_post_id+'"]/div[@class="post_desc_top"]/div[@id="'+question_post_id+'_message_text_false"]/div[@class="frm_post_msg"]/div[@class="KonaBody"]/text()|//div[@id="'+question_post_id+'"]/div[@class="post_desc_top"]/div[@id="'+question_post_id+'_message_text_false"]/div[@class="frm_post_msg"]/div[@class="KonaBody"]/a/@href').extract()).strip()
        question_content_raw1 = re.sub(r'(\xa0|\r|\t)','',question_content_raw0).encode("utf-8")
        question_content_raw2 = re.sub('\xe2\x80\x99',"'", question_content_raw1)
        question_content_raw3 = re.sub("\xe2\x80\x93","-",question_content_raw2)
        item['question_content'] = question_content_raw3 
        
        item['question_tags'] = sel.xpath('//span[@class="post_question_tags"]/a/text()').extract()
        yield item
        
class CommentContent(BaseSpider):
    name = "comments"
    def __init__(self, filename=None):
        if filename:
            data = open(filename).read().split("\n")
            for i in data:
                self.start_urls.append(i)
    allowed_domains = ['medhelp.org']
    start_urls = []
    
    def parse(self, response):
        sel = Selector(response)
        item = CItem()
        item['url'] = get_base_url(response)
        item['question_page_id'] = response.url.split('/')[-1]
        item['question_post_id'] = sel.xpath('//div[@id="new_posts_show_middle"]/div[@class="post_data has_bg_color"]/@id').extract()[0]
        x = len(sel.xpath('//div[@class="subject_comments_number"]/span[@class="comments_num"]/a/text()').extract())
        if(x == 0):
            item['comment_num'] = re.compile('\d*').findall(sel.xpath('//div[@class="subject_comments_number"]/span[@class="comments_num"]/span/text()').extract()[0])[0]
        else:
            item['comment_num'] = re.compile('\d*').findall(sel.xpath('//div[@class="subject_comments_number"]/span[@class="comments_num"]/a/text()').extract()[0])[0]
            
        comment_num = item['comment_num']
        if (comment_num>0):
            item['comment_post_id'] = sel.xpath('//div[@id="new_posts_show_middle"]/div[@class="post_data has_bg_color"]/@id').extract()[1:]
            
            item['comment_time'] = []
            item['comment_user_id'] = []
            item['comment_content'] = []
            for a_comment_id in item['comment_post_id']:
                a_comment_time = "%s|"%a_comment_id + ''.join(sel.xpath('//div[@id="'+a_comment_id+'"]/div[@class="post_desc_top"]/div[@class="float_fix"]/div[@class="user_info user_info_comment"]/div[@class="float_fix"]/div/text()').extract()).strip()
                item['comment_time'].append(a_comment_time)
                a_comment_user_id = "%s|"%a_comment_id + sel.xpath('//div[@id="'+a_comment_id+'"]/div[@class="post_desc_top"]/div[@class="float_fix"]/div[@class="user_info user_info_comment"]/div[@class="float_fix"]/div[@class="question_by"]/span/a/@href').extract()[0].split('/')[-1]
                item['comment_user_id'].append(a_comment_user_id)
                
                a_comment_content_raw0 =  ''.join(sel.xpath('//div[@id="'+a_comment_id+'"]/div[@class="post_desc_top"]/div[@id="'+a_comment_id+'_message_text_false"]/div[@class="frm_post_msg"]/div[@class="KonaBody"]/text()|//div[@id="'+a_comment_id+'"]/div[@class="post_desc_top"]/div[@id="'+a_comment_id+'_message_text_false"]/div[@class="frm_post_msg"]/div[@class="KonaBody"]/a/@href').extract()).strip()
                a_comment_content_raw1 = re.sub(r'(\xa0|\r|\t)','',a_comment_content_raw0).encode("utf-8")
                a_comment_content_raw2 = re.sub('\xe2\x80\x99',"'", a_comment_content_raw1)
                a_comment_content_raw3 = "%s|"%a_comment_id + re.sub("\xe2\x80\x93","-",a_comment_content_raw2) 
                item['comment_content'].append(a_comment_content_raw3)
                
        yield item


class MedHelp_tags(SitemapSpider):
    sitemap_urls = ['http://www.medhelp.org/sitemaps/mh_smi_tags.xml']
    name = 'mht'
    def parse(self, response):
        print response.url
        return
    
class Commentmore(BaseSpider):      
    name = "turls"
    def __init__(self, filename=None):
        if filename:
            data = open(filename).read().split("\n")
            for i in data:
                self.start_urls.append(i)
    allowed_domains = ['medhelp.org']
    start_urls = []
    def parse(self, response):
        sel = Selector(response)
        list1 = sel.xpath('//div[@class="cp_panel_exp_link"]/a/@href').extract()
        list2 = sel.xpath('//div[@class="nav"]/a/@href').extract()
        if len(list1)>0:
            relativeURL1 = sel.xpath('//div[@class="cp_panel_exp_link"]/a/@href').extract()[0]
            url1 = urljoin_rfc('http://www.medhelp.org',relativeURL1)
            print url1
            return Request(url1, callback=self.parse) 
        elif len(list2)==1:
            if sel.xpath('//div[@class="nav"]/a/text()').extract()[0] == "Next":
                relativeURL2 = sel.xpath('//div[@class="nav"]/a/@href').extract()[0]
                url2 = urljoin_rfc('http://www.medhelp.org',relativeURL2)
                print url2
                return Request(url2, callback=self.parse)
            else:
                pass
        elif len(list2)==2:
            if sel.xpath('//div[@class="nav"]/a/text()').extract()[1] == "Next":
                relativeURL3 = sel.xpath('//div[@class="nav"]/a/@href').extract()[1]
                url3 = urljoin_rfc('http://www.medhelp.org',relativeURL3)
                print url3
                return Request(url3, callback=self.parse)
            else:
                pass
        else:
            pass
        return

class CommentContent(BaseSpider):
    name = "mht_parser"
    def __init__(self, filename=None):
        if filename:
            data = open(filename).read().split("\n")
            for i in data:
                self.start_urls.append(i)
    allowed_domains = ['medhelp.org']
    start_urls = []
    
    def parse(self, response):
        sel = Selector(response)
        item = TItem()
        item['url'] = get_base_url(response)
        item['subject_id'] = response.url.split('/')[-2]
        item['subject_title'] =  sel.xpath('//div[@id="content_page_title"]/h1[@class="title"]/text()').extract()[0]
        item['postsOnTopic_urls'] = []
        if len(sel.xpath('//div[@class="post_summary_title"]/a/@href').extract()) >0:
            for i in sel.xpath('//div[@class="post_summary_title"]/a/@href').extract():
                item['postsOnTopic_urls'].append('http://www.medhelp.org%s'%i)
        yield item
        
class MedHelp_userjournals(SitemapSpider):
    sitemap_urls = ['http://www.medhelp.org/sitemaps/mh_smi_userjournals.xml']
    name = 'mhu'
    def parse(self, response):
        print response.url
        return
        
class CommentContent(BaseSpider):
    name = "mhu_parser"
    def __init__(self, filename=None):
        if filename:
            data = open(filename).read().split("\n")
            for i in data:
                self.start_urls.append(i)
    allowed_domains = ['medhelp.org']
    start_urls = []
    def parse(self, response):
        sel = Selector(response)
        relativeURL = sel.xpath('//span[@class="pp_r_txt_sel"]/a/@href|//span[@class="pp_r_txt"]/a/@href').extract()[0]
        url = urljoin_rfc('http://www.medhelp.org',relativeURL)
        print url
        return

class CommentContent2(BaseSpider):
    name = "mhu_parser2"
    def __init__(self, filename=None):
        if filename:
            data = open(filename).read().split("\n")
            for i in data:
                self.start_urls.append(i)
    allowed_domains = ['medhelp.org']
    start_urls = []
    def parse(self, response):
        sel = Selector(response)
        item = UItem()
        item['url'] = get_base_url(response)
        item['user_id'] = response.url.split('/')[-1]
        item['user_name'] = sel.xpath('//div[@id="header"]/div[@id="page_heading"]/div[@class="page_title"]/text()').extract()[0].strip().split("'s")[0]
        item['user_profile_id'] = sel.xpath('//div[@class="float_fix"]/span/span[@class="pp_r_txt_sel"]/a/@href').extract()[0].split('=')[1]
        status = sel.xpath('//div[@id="mood"]/text()').extract()
        if len(status) >0:
            if status[0] != '...' :
                status_raw0 = status[0]
                status_raw1 = re.sub(r'(\xa0|\r|\t)','',status_raw0).encode("utf-8")
                status_raw2 = re.sub('\xe2\x80\x99',"'",status_raw1)
                status_raw3 = re.sub("\xe2\x80\x93","-",status_raw2)
                item['user_about_me_status'] = status_raw3
            else:
                item['user_about_me_status'] = ""
        else:
            item['user_about_me_status'] = ""
        item['user_about_me_intro'] = ''
        part1 = sel.xpath('//div[@id= "about_me_wg"]/div[@class="bottom float_fix"]/div[@class="section"]/span/text()').extract()
        part2 = sel.xpath('//div[@id= "about_me_wg"]/div[@class="bottom float_fix"]/div[@class="section"]/text()').extract()
        part3 = sel.xpath('//div[@id="about_me_text"]/span[@class="about_me"]/span[@class="about_me_show"]/text()').extract()
        part4 = sel.xpath('//div[@id="about_me_text"]/span[@class="about_me"]/span[@id="about_me_less"]/text()').extract()
        if len(part1) > 0:
            item['user_about_me_intro'] += ''.join(part1).strip() +' '
        if len(part2) > 0:
            item['user_about_me_intro'] += ' '+ ''.join(part2).strip()
        if len(part3) > 0:
            item['user_about_me_intro'] += ' ' + part3[0]
        if len(part4) > 0:
            item['user_about_me_intro'] += ' ' + part4[0]
        tags1 = sel.xpath('//div[@class="section"]/span[@class="interests"]/span[@class="interests_show"]/a/text()|//div[@class="section"]/span[@class="interests"]/span[@class="interests_show"]/text()').extract()
        tags2 = sel.xpath('//div[@class="section"]/span[@class="interests"]/span[@id="interests_less"]/a/text()|//div[@class="section"]/span[@class="interests"]/span[@id="interests_less"]/text()').extract()
        tagsAll = tags1+tags2
        tagsAll = [s.strip(',') for s in tagsAll]
        tagsAll = [s.strip('\n') for s in tagsAll]
        tagsAll = [s.replace(' ', '') for s in tagsAll]
        tagsAll = filter(None, tagsAll)
        item['user_about_me_interest_tag_name'] = tagsAll
        numlist = sel.xpath('//div[@id="best_answers_hover"]/div/text()').extract()
        if len(numlist) >0:
            item['user_about_me_best_answer'] = numlist[0]
        else:
            item['user_about_me_best_answer'] = '0'
        item['user_about_me_top_answer'] = sel.xpath('//div[@class="stars section"]/div[@class="stars extra_info float_fix"]/div[@class="subcategory_name"]/text()').extract()     
        yield item

class GetURLsforP(BaseSpider):
    name = "userid"
    def __init__(self, filename=None):
        if filename:
            data = open(filename).read().split("\n")
            for i in data:
                self.start_urls.append(i)
    allowed_domains = ['medhelp.org']
    start_urls = []
    def parse(self,response):
        sel = Selector(response)
        user_id = sel.xpath('//div[@class="user_info"]/div/span/a/@href').extract()[0].split('/')[-1]
        user_url = urljoin_rfc('http://www.medhelp.org/personal_pages/user/',user_id)
        print user_url
        
class Status(BaseSpider):
    name = "status"
    def __init__(self, filename=None):
        if filename:
            data = open(filename).read().split("\n")
            for i in data:
                self.start_urls.append(i)
    allowed_domains = ['medhelp.org']
    start_urls = []
    def parse(self,response):
        sel = Selector(response)
        l = sel.xpath('//div[@class="mood"]/span[@class="summary_value"]/div/a/@href').extract()
        if len(l)>0:
            statusl = l[0].split('/')[:-1]
            statusurl = '/'.join(statusl)
            statuswholeurl = urljoin_rfc('http://www.medhelp.org',statusurl)
        else:
            statuswholeurl = ''
        print statuswholeurl

class Status_extend(BaseSpider):
    name = "status2"
    def __init__(self, filename=None):
        if filename:
            data = open(filename).read().split("\n")
            for i in data:
                if i != '':
                    self.start_urls.append(i)
    allowed_domains = ['medhelp.org']
    start_urls = []
    def parse(self,response):
        sel = Selector(response)    
        nextl = sel.xpath('//div[@class="pagination"]/a[@class="next_page"]/@href').extract()
        if len(nextl)>0:
            nextp = nextl[0]
            nexturl = urljoin('http://www.medhelp.org',nextp)
            print nexturl
            return Request(nexturl, callback=self.parse)
        else:
            pass
        return
        
class statusparse(BaseSpider):
    name = "s_parser"
    def __init__(self, filename=None):
        if filename:
            data = open(filename).read().split("\n")
            for i in data:
                if i != '':
                    self.start_urls.append(i)
    allowed_domains = ['medhelp.org']
    start_urls = []
    def parse(self,response):
        sel = Selector(response)
        item = SItem()
        item['url'] = get_base_url(response)
        item['status_id'] = sel.xpath('//div[@class="status float_fix "]/@data-status-id').extract()
        item['user_id'] = {}
        item['status_time'] = {}
        item['status_content'] = {}
        item['status_reply'] = {}
        if len(item['status_id']) >0:
            for i in item['status_id']:
                item['user_id'][i] = sel.xpath('//div[@data-status-id="'+i+'"]/@data-user-id').extract()[0]
                item['status_time'][i] = sel.xpath('//div[@data-status-id="'+i+'"]/div/div/div/span[@class="time"]/text()').extract()[0].strip().split('-')[0].strip()
                item['status_content'][i] = sel.xpath('//div[@data-status-id="'+i+'"]/div/div/div/span[@class="text "]/text()').extract()[0]
                item['status_reply'][i] = sel.xpath('//div[@data-status-id="'+i+'"]/div/div/div/span[@class="comment_count"]/text()').extract()[0]      
        else:
            pass
        yield item  

class userJournal(BaseSpider):
    name = "j_parser"
    def __init__(self, filename=None):
        if filename:
            data = open(filename).read().split("\n")
            for i in data:
                if i != '':
                    self.start_urls.append(i)
    allowed_domains = ['medhelp.org']
    start_urls = []
    def parse(self,response):
        sel = Selector(response)
        item = JItem2()
        item['url'] = get_base_url(response)
        item['journal_id'] = response.url.split('/')[-2]
        item['journal_title'] = sel.xpath('//h1/text()').extract()[0].strip()
        item['journal_time'] = sel.xpath('//span[@class="date"]/text()').extract()[0].strip()
        item['journal_content'] = ''.join(sel.xpath('//div[@class="journal_content"]/text()').extract()).strip()
        item['journal_reply'] = sel.xpath('//span[@class="comment_count"]/text()').extract()[0]
        profileRelativeURL = sel.xpath('//span[@class="pp_r_txt_sel"]/a/@href').extract()[0]
        item['user_p_id'] = urljoin_rfc('http://www.medhelp.org', profileRelativeURL)
        yield item
        
class GetURLsforN(BaseSpider):
    name = "urlsforn"
    def __init__(self, filename=None):
        if filename:
            data = open(filename).read().split("\n")
            for i in data:
                self.start_urls.append(i)
    allowed_domains = ['medhelp.org']
    start_urls = []
    def parse(self,response):
        sel = Selector(response)
        user_id = sel.xpath('//div[@class="user_info"]/div/span/a/@href').extract()[0].split('/')[-1]
        user_url = urljoin_rfc('http://www.medhelp.org/notes/list/',user_id)
        print user_url

class Notes_extend(BaseSpider):
    name = "urlsforn2"
    def __init__(self, filename=None):
        if filename:
            data = open(filename).read().split("\n")
            for i in data:
                if i != '':
                    self.start_urls.append(i)
    allowed_domains = ['medhelp.org']
    start_urls = []
    def parse(self,response):
        sel = Selector(response)    
        nextl = sel.xpath('//div[@id="pagination_nav"]/a[@class="msg_next_page"]/@href').extract()
        if len(nextl)>0:
            nextp = nextl[0]
            nexturl = urljoin('http://www.medhelp.org',nextp)
            print nexturl
            return Request(nexturl, callback=self.parse)
        else:
            pass
        return
 
class statusparse(BaseSpider):
    name = "n_parser"
    def __init__(self, filename=None):
        if filename:
            data = open(filename).read().split("\n")
            for i in data:
                if i != '':
                    self.start_urls.append(i)
    allowed_domains = ['medhelp.org']
    start_urls = []
    def parse(self,response):
        sel = Selector(response)
        item = NItem()
        item['url'] = get_base_url(response)
        item['note_id'] = sel.xpath('//div[@class="note_entries"]/div[@class="note_entry float_fix note_sep"]/@id').extract()
        item['user_id_sender'] = {}
        item['user_id_receiver'] = {}
        item['note_time'] = {}
        item['note_content'] = {}
        if len(item['note_id']) >0:
            for i in item['note_id']:
                item['user_id_sender'][i] = sel.xpath('//div[@id="'+i+'"]/div[@class="note_desc"]/div/span/a/@id').extract()[0].split('_')[1]
                item['user_id_receiver'][i] = sel.xpath('//div[@id="'+i+'"]/div[@class="note_desc"]/div/span/a/@id').extract()[0].split('_')[2]
                item['note_time'][i] = sel.xpath('//div[@id="'+i+'"]/div[@class="note_desc"]/div[2]/text()').extract()[0]
                item['note_content'][i] = sel.xpath('//div[@id="'+i+'"]/div[@class="note_desc"]/div[@class="note_msg"]/text()').extract()[0]
        yield item
        
class communityparse(BaseSpider):
    name = "community_parser"
    def __init__(self, filename=None):
        if filename:
            data = open(filename).read().split("\n")
            for i in data:
                if i != '':
                    self.start_urls.append(i)
    allowed_domains = ['medhelp.org']
    start_urls = []
    def parse(self,response):
        sel = Selector(response)
        item = CommunityItem()
        item['url'] = get_base_url(response)
        item['forum_id'] = []
        f_list = sel.xpath('//div[@class="comm_name "]/div/a/@href|//div[@class="comm_name separated"]/div/a/@href').extract()
        for i in f_list:
            item['forum_id'].append(i.split('/')[-1])
        item['user_id'] = {}
        if len(item['forum_id']) > 0:
            for i in item['forum_id']:
                item['user_id'][i] = response.url.split('/')[-1]
        yield item
        
class trackerparse(BaseSpider):
    name = "tracker_parser"
    def __init__(self, filename=None):
        if filename:
            data = open(filename).read().split("\n")
            for i in data:
                if i != '':
                    self.start_urls.append(i)
    allowed_domains = ['medhelp.org']
    start_urls = []
    def parse(self,response):
        sel = Selector(response)
        item = TrackerItem()
        item['url'] = get_base_url(response)
        item['tracker_id'] = []
        t_list = sel.xpath('//div[@class="ut_side_link"]/a/@href').extract()
        for i in t_list:
            item['tracker_id'].append(i.split('/')[-1])
        item['tracker_name'] = {}
        if len(item['tracker_id']) > 0:
            for i in item['tracker_id']:
                item['tracker_name'][i] = sel.xpath('//div[@class="ut_side_link"]/a[@href="/user_trackers/show/'+i+'"]/text()').extract()[0]
        item['user_id'] = {}
        if len(item['tracker_id']) > 0:
            for i in item['tracker_id']:
                item['user_id'][i] = response.url.split('/')[-1]
        yield item

class GetURLsforF(BaseSpider):
    name = "urlsforf"
    def __init__(self, filename=None):
        if filename:
            data = open(filename).read().split("\n")
            for i in data:
                self.start_urls.append(i)
    allowed_domains = ['medhelp.org']
    start_urls = []
    def parse(self,response):
        sel = Selector(response)
        user_id = response.url.split('/')[-1]
        user_url = urljoin_rfc('http://www.medhelp.org/friendships/list/',user_id)
        print user_url
       
class Friend_extend(BaseSpider):
    name = "urlsforf2"
    def __init__(self, filename=None):
        if filename:
            data = open(filename).read().split("\n")
            for i in data:
                if i != '':
                    self.start_urls.append(i)
    allowed_domains = ['medhelp.org']
    start_urls = []
    def parse(self,response):
        sel = Selector(response)    
        nextl = sel.xpath('//div[@id="pagination_nav"]/a[@class="msg_next_page"]/@href').extract()
        if len(nextl)>0:
            nextp = nextl[0]
            nexturl = urljoin('http://www.medhelp.org',nextp)
            print nexturl
            return Request(nexturl, callback=self.parse)
        else:
            pass
        return

class fparse(BaseSpider):
    name = "f_parser"
    def __init__(self, filename=None):
        if filename:
            data = open(filename).read().split("\n")
            for i in data:
                if i != '':
                    self.start_urls.append(i)
    allowed_domains = ['medhelp.org']
    start_urls = []
    def parse(self,response):
        sel = Selector(response)
        item = FriendItem()
        item['url'] = get_base_url(response)
        t = response.url.split('/')[-1]
        if '?' in t:
            item['user_id_i'] = t.split('?')[0]
        else:
            item['user_id_i'] = response.url.split('/')[-1]
        item['user_id_j'] = {}
        f_list = sel.xpath('//div[@class="mh_info_main"]/div[@class="login"]/span/a/@href').extract()
        if len(f_list) >0:
            for i in f_list:
                item['user_id_j'][i.split('/')[-1]] = item['user_id_i']
        yield item

class GetURLsforGroup(BaseSpider):
    name = "urlsforg"
    allowed_domains = ['medhelp.org']
    start_urls = ['http://www.medhelp.org/user_groups/list']
    print start_urls[0]
    def parse(self,response):
        sel = Selector(response)    
        nextl = sel.xpath('//div[@id="pagination_nav"]/a[@class="msg_next_page"]/@href').extract()
        if len(nextl)>0:
            nextp = nextl[0]
            nexturl = urljoin('http://www.medhelp.org',nextp)
            print nexturl
            return Request(nexturl, callback=self.parse)
        else:
            pass
        return

class groupparse(BaseSpider):
    name = "group_parser"
    def __init__(self, filename=None):
        if filename:
            data = open(filename).read().split("\n")
            for i in data:
                if i != '':
                    self.start_urls.append(i)
    allowed_domains = ['medhelp.org']
    start_urls = []
    def parse(self,response):
        sel = Selector(response)
        item = GroupItem()
        item['url'] = get_base_url(response)
        item['group_id_text'] = sel.xpath('//div[@class="ug_listing float_fix"]/div[@class="ug_top_info float_fix"]/div[@class="ug_title"]/a/@href').extract()
        item['group_name'] = {}
        item['group_type'] = {}
        item['group_keyword'] = {}
        item['group_members'] = {}
        item['group_description'] = {}
        if len(item['group_id_text'])>0:
            for i in item['group_id_text']:
                item['group_name'][i] = sel.xpath('//div[@class="ug_listing float_fix"]/div[@class="ug_top_info float_fix"]/div[@class="ug_title"]/a[@href="'+i+'"]/text()').extract()[0].strip()
                ginfo = sel.xpath('//div[@class="ug_listing float_fix"]/div[@class="ug_top_info float_fix"]/div[@class="ug_title"][a[@href="'+i+'"]]/div[@class="mh_info_main"]/text()').extract()[0].strip().split('-')
                if len(ginfo) >2:
                    item['group_type'][i] = ginfo[0].strip()
                    item['group_keyword'][i] = ginfo[1].strip()
                    item['group_members'][i] = ginfo[2].strip().split(' ')[0].strip()
                else:
                    item['group_type'][i] = '!Private'
                    item['group_keyword'][i] = ginfo[0].strip()
                    item['group_members'][i] = ginfo[1].strip().split(' ')[0].strip()
                item['group_description'][i] = sel.xpath('//div[@class="ug_listing float_fix"]/div[@class="ug_top_info float_fix"][./div[@class="ug_title"]/a[@href="'+i+'"]]/div[@class="forum_description float_fix"]/text()').extract()[0]
        yield item
        
class GetURLsforForum(BaseSpider):
    name = "urlsforfor"
    allowed_domains = ['medhelp.org']
    start_urls = ['http://www.medhelp.org/forums/list']
    def parse(self,response):
        sel = Selector(response)
        list = sel.xpath('//div[@id="A_support"]/div[@class="alpha_col"]/div[@class="forum"]/a/@href').extract()
        for i in list:
            print urljoin('http://www.medhelp.org',i)

class forumparse(BaseSpider):
    name = "forum_parser"
    def __init__(self, filename=None):
        if filename:
            data = open(filename).read().split("\n")
            for i in data:
                if i != '':
                    self.start_urls.append(i)
    allowed_domains = ['medhelp.org']
    start_urls = []
    def parse(self,response):
        sel = Selector(response)
        item = ForumItem()
        item['url'] = get_base_url(response)
        item['forum_id'] = response.url.split('/')[-1]
        item['forum_title'] = sel.xpath('//title/text()').extract()[0]
        keywords =  sel.xpath('//meta[@name="keywords"]/@content').extract()
        if len(keywords)>0:
            item['forum_keywords'] = keywords[0]
        else:
            item['forum_keywords'] = ''
        description = sel.xpath('//meta[@name="description"]/@content').extract()
        if len(description)>0:
            item['forum_description'] = description[0]
        else:
            item['forum_description'] = ''
        yield item