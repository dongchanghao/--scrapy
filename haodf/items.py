# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field

class HaodfItem(scrapy.Item):
    table = 'haodf'
    # define the fields for your item here like:
    # name = scrapy.Field()
    illness = Field()#疾病
    sick_time = Field()#患病时间
    allergy = Field()#过敏史
    description = Field()#病情描述
    want_help = Field()
    last_treatment = Field()
    hospital = Field()
    help = Field()#希望提供的帮助
    medication = Field()#用药情况
    office = Field()#所就诊医院科室
    anamnesis = Field()#既往病史
    title = Field()#标题
    test_results = Field()#化验结果
    content = Field() #所有内容
    respond = Field()
