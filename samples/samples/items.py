# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class SamplesItem(Item):
    # define the fields for your item here like:
    # name = Field()
    pass
class GItem(Item):
    url = Field()
    question_page_id = Field()
    question_forum_name = Field()
    question_forum_id = Field()
    question_title = Field()
    question_post_id = Field()
    user_id = Field()
    user_name = Field()
    question_time = Field()
    comment_num = Field()
    question_content = Field()
    question_tags = Field()

class CItem(Item):
    url = Field()
    question_page_id = Field()
    question_post_id = Field()
    comment_post_id = Field()
    comment_time = Field()
    comment_num = Field()
    comment_user_id = Field()
    comment_to_user_id = Field()
    comment_to_user_name = Field()
    comment_content = Field()
    
class TItem(Item):
    url = Field()
    subject_id = Field()
    subject_title = Field()
    postsOnTopic_urls = Field()
    
class UItem(Item):
    url = Field()
    user_id = Field()
    user_name = Field()
    user_profile_id = Field()
    user_about_me_intro = Field()
    user_about_me_status = Field()
    user_about_me_best_answer = Field()
    user_about_me_top_answer = Field()
    user_about_me_interest_tag_name = Field()
    user_about_me_more = Field()
    
class SItem(Item):
    url = Field()
    status_id = Field()
    status_time = Field()
    status_content = Field()
    status_reply = Field()
    user_id = Field()

class JItem(Item):
    url = Field()
    journal_id = Field()
    journal_title = Field()
    journal_time = Field()
    journal_content = Field()
    journal_reply = Field()
    #user_id = Field()
	#user_p_id = Field()

class JItem2(Item):
    url = Field()
    journal_id = Field()
    journal_title = Field()
    journal_time = Field()
    journal_content = Field()
    journal_reply = Field()
    user_p_id = Field()

class NItem(Item):
    url = Field()
    note_id = Field()
    user_id_sender = Field()
    note_time = Field()
    note_content = Field()
    user_id_receiver = Field()
    
class CommunityItem(Item):
    url = Field()
    forum_id = Field()
    user_id = Field()

class TrackerItem(Item):
    url = Field()
    tracker_id = Field()
    tracker_name = Field()
    user_id = Field()
    
class FriendItem(Item):
    url = Field()
    user_id_i = Field()
    user_id_j = Field()
    
class GroupItem(Item):
    url = Field()
    group_id_text = Field()
    group_name = Field()
    group_type = Field()
    group_keyword = Field()
    group_members = Field()
    group_description = Field()
    
class ForumItem(Item):
    url = Field()
    forum_id = Field()
    forum_title = Field()
    forum_keywords = Field()
    forum_description = Field()