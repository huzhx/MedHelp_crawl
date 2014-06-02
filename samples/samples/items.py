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
    question_title = Field()
    question_post_id = Field()
    user_id = Field()
    user_name = Field()
    question_time = Field()
    comment_num = Field()
    question_content = Field()
    question_tags = Field()
    comment_post_id = Field()
    comment_time = Field()
    comment_user_id = Field()
    comment_to_user_id = Field()
    comment_to_user_name = Field()
    comment_content = Field()
    
    
    