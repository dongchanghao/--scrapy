import pymysql.cursors

class MySQLPipeline(object):
    def __init__(self):
        self.connect = pymysql.connect(
            host = 'localhost',
            port = 3306,
            db = 'haodfce',
            user = 'root',
            passwd = '1333',
            charset = 'utf8',
            use_unicode=True)
        self.cursor = self.connect.cursor()
    def process_item(self, item, spider):
        sql = 'insert into miniaoxitongjiehe(illness,sick_time,allergy,description,help,office,anamnesis,respond,medication,title,test_results,content,last_treatment,hospital,want_help)VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        params = (item['illness'],item['sick_time'],item['allergy'],item['description'],item['help'],item['office'],item['anamnesis'],item['respond'],item['medication'],item['title'],item['test_results'],item['content'],item['last_treatment'],item['hospital'],item['want_help'])
        self.cursor.execute(sql, params)
        self.connect.commit()
        return item