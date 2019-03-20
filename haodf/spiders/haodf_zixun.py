# -*- coding: utf-8 -*-
import scrapy
from scrapy import Spider, Request
import time
import re
from ..items import HaodfItem
import requests

class HaodfZixunSpider(scrapy.Spider):
    name = 'haodf-zixun'
    allowed_domains = ['zixun.haodf.com']
    start_urls = ['https://zixun.haodf.com/dispatched/26.htm']
    def start_requests(self):
        base_url = 'https://zixun.haodf.com/dispatched/'#基础url
                #time.sleep(2)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}#请求头
        for p in range(1,8):
            url = base_url + '56' + '.htm?p='+str(p)#加载每一页
            print(url)
            req = requests.get(url, headers=headers)
            text = req.text
            results = re.findall('<a\shref="//(.*?)"\stitle=".*?"\starget=".*?"\sclass=".*?">', text, re.S)[1:]#正则匹配
            for result in results:
                print(result)
                time.sleep(2)
                yield Request('https://'+result,self.parse)

    def parse(self, response):
        result = response.text
        item = HaodfItem()
        illness = re.findall('<h2\sstyle=.*?>(.*?)</h2>',result,re.S)[0]
        s = re.sub(r'[a-z0-9<>=\'/_.]+', '',illness)
        s = s.replace(' ', '')
        s = s.replace('\n', '')
        item['illness'] = '疾病：'+s+'flag'
        title = re.findall('<h3\sclass="h_s_cons_info_title">(.*?)</h3>', result, re.S)
        all = re.findall('<strong\sclass="cblues1">.*?</strong>.*?h2\sstyle="font-weight:\snormal;font-size:\s14px;">.*?</h2>.*?<strong>.*?</strong>(.*?)</p>',result,re.S)
        if len(all) > 0 and '病情描述' in all[0]:
            if '曾经治疗情况和效果' in all[0]:
                last_result = all[0].find('曾经治疗情况和效果')
                if '想得到怎样的帮助：' in all[0]:
                    helps = all[0].find('想得到怎样的帮助：')
                    # print('曾经治疗情况和效果：'+all[0][last_result:helps])
                    if '检查结果' in all[0]:
                        test_results = all[0].find('化验、检查结果')

                        if '最后一次就诊的医院' in all[0]:
                            item['content']='内容:' + all[0][:last_result]+'flag'
                            item['last_treatment']= all[0][last_result:helps]+'flag' #anamnesis
                            hospital = all[0].find('最后一次就诊的医院')
                            item['want_help']=all[0][helps:test_results]+'flag'
                            item['test_results']=all[0][test_results:hospital]+ 'flag'
                            item['hospital']=all[0][hospital:]+'flag'#office
                        else:
                            item['content'] = '内容:' + all[0][:last_result] + 'flag'
                            item['last_treatment'] = all[0][last_result:helps] + 'flag'  # anamnesis
                            item['want_help'] = all[0][helps:test_results] + 'flag'
                            item['test_results'] = all[0][test_results:] + 'flag'
                            item['hospital'] = '最后一次就诊的医院：NONEflag'
                    else:
                        item['content'] = '内容:' + all[0][:last_result] + 'flag'
                        item['last_treatment'] = all[0][last_result:helps] + 'flag'  # anamnesis
                        item['want_help'] = all[0][helps:] + 'flag'
                        item['test_results'] = '化验、检查结果：NONEflag'
                        item['hospital'] = '最后一次就诊的医院：NONEflag'
                else:
                    helps = None
                    item['content'] = '内容:' + all[0][:last_result] + 'flag'
                    item['last_treatment'] = all[0][last_result:] + 'flag'  # anamnesis
                    item['want_help'] = '想得到怎样的帮助：NONEflag'
                    item['test_results'] = '化验、检查结果：NONEflag'
                    item['hospital'] = '最后一次就诊的医院：NONEflag'
        elif len(all)>0 and '曾经' not in all[0]and '冬日送暖活动已结束'not in all[0] and '主治医师' not in all[0] and '副主任医师'not in all[0]:
            item['content'] = '内容:'+all[0]+'flag'
            item['last_treatment'] = '曾经治疗情况和效果：NONEflag'
            item['want_help'] = '想得到怎样的帮助：NONEflag'
            item['test_results'] = '化验、检查结果：NONEflag'
            item['hospital'] = '最后一次就诊的医院：NONEflag'
        else:
            item['content']='内容：NONEflag'
            item['last_treatment']='曾经治疗情况和效果：NONEflag'
            item['want_help']='想得到怎样的帮助：NONEflag'
            item['test_results']='化验、检查结果：NONEflag'
            item['hospital']='最后一次就诊的医院：NONEflag'

        if len(title)>0:
            item['title'] = title[0]
        else:
            item['title'] = '咨询标题：NONEflag'
        is_sick_time = re.findall('<h2\sstyle=.*?>(.*?)</h2>',result,re.S)
        if len(is_sick_time)>1:
            item['sick_time'] = '患病时间：'+is_sick_time[1]+'flag'
        else:
            item['sick_time'] = '患病时间：NONE'+'flag'
        is_allergy = re.findall('<h2\sstyle=.*?>(.*?)</h2>',result,re.S)
        if len(is_allergy) == 3:
            item['allergy'] = '过敏史：'+is_allergy[2]+'flag'
        else:
            item['allergy'] = '过敏史：None'+'flag'
        description = re.findall('<strong\sclass="cblues1">[\u2E80-\u9FFF]{4}.*?/>(.*?)</div>',result,re.S)
        if len(description)>0:
            item['description'] = '病情描述'+description[0]+'flag'
        else:
            item['description'] = '病情描述：NONEflag'
        #item['description'] = re.findall('<strong\sclass="cblues1">[\u2E80-\u9FFF]{4}.*?/>(.*?)</div>',result,re.S)[0]
        help = re.findall('<strong\sclass="cblues1">[\u2E80-\u9FFF]{7}.*?/>\n(.*?)</p>',result,re.S)
        if len(help)>0:
            item['help'] = '寻求帮助'+help[0]+'flag'
        else:
            item['help'] = '寻求帮助：NONEflag'
        #item['help'] = re.findall('<strong\sclass="cblues1">[\u2E80-\u9FFF]{7}.*?/>\n(.*?)</p>',result,re.S)[0]
        is_office = re.findall('<strong\sclass="cblues1">[\u2E80-\u9FFF]{7}.*?/>\n(.*?)</p>',result,re.S)
        if len(is_office) == 2:
            item['office'] = '所就诊医院科室：'+is_office[1]+'flag'
        else:
            item['office'] = '所就诊医院科室：NONEflag'
        medication = re.findall('<strong\sclass="cblues1">[\u2E80-\u9FFF]{4}.*?</strong>.*?<b.*?>(.*?)</p>',result,re.S)
        if len(medication) == 3:
            result_2 = re.findall('([\u2E80-\u9FFF0-9]+).*>', medication[1])
            s = ''.join(result_2)
            item['medication'] = '用药情况：'+s+'flag'
        else:
            item['medication'] = '用药情况：NONEflag'
        anamnesis = re.findall('<p>.*?<strong\sclass="cblues1">[\u2E80-\u9FFF]{4}.</strong>.*?/>(.*?)</p>',result,re.S)
        if len(anamnesis)>1 and len(anamnesis[-1])>18:
            item['anamnesis'] = '既往病史：'+anamnesis[-1][-18:]+'flag'
        else:
            item['anamnesis'] = '既往病史：NONEflag'
        respond = re.findall(
            '<div\sclass="h_s_cons_.*?class="h_s_cons_title">(.*?)</h3>.*?class="h_s_cons_main\sseo2js"></p>', result,
            re.S)
        ill_respond = re.findall('<pre\sclass="h_s_cons_main">(.*?)</pre>', result, re.S)
        res = []
        dic = {}
        for i in respond:
            key = (result.find(i))
            i = re.sub(r'[a-zA-Z<>=\'/_.]+', '', i)
            i = i.replace('<br />', '').replace('\n', '').replace('\r', '').replace('"', '').replace(':', '').replace(
                '?', '').replace(' \n','')
            i ='flag'+ '医生回复：' + i
            res.append(i)
            dic[key] = i
        for i in ill_respond:
            key = result.find(i)
            i ='flag'+'患者提问：' + i.replace('\n','').replace(' \n','')
            dic[key] = i
        resu = ''''''
        for k in sorted(dic):
            resu += dic[k] + '\n'
        item['respond'] = resu+'flag'+'flag'
        yield item

