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
        item['postsOnTopic_urls'] = sel.xpath('//div[@class="post_summary_title"]/a/@href').extract()
        yield item