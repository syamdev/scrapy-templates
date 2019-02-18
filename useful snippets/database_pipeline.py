#
# This file was created by Attila Toth - http://scrapingauthority.com
#
#
# This snippet contains a MySQL database pipeline
# You have to add your database settings and enable the pipeline in scrapy settings.py in order to use it
#
# Define the db settings like this:
#
# DB_SETTINGS = {
#     'db': "my_db",
#     'user': 'root',
#     'passwd': 'my_pass',
#     'host': '0.0.0.0',
# }
#
#


import MySQLdb
from scrapy.exceptions import NotConfigured


class DatabasePipeline(object):

    def __init__(self, db, user, passwd, host):
        self.db = db
        self.user = user
        self.passwd = passwd
        self.host = host

    @classmethod
    def from_crawler(cls, crawler):
        db_settings = crawler.settings.getdict("DB_SETTINGS")
        if not db_settings:
            raise NotConfigured
        db = db_settings['db']
        user = db_settings['user']
        passwd = db_settings['passwd']
        host = db_settings['host']
        return cls(db, user, passwd, host)

    def open_spider(self, spider):
        self.conn = MySQLdb.connect(db=self.db,
                               user=self.user, passwd=self.passwd,
                               host=self.host,
                               charset='utf8', use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        sql = "INSERT INTO table (field1, field2, field3) VALUES (%s, %s, %s)"
        self.cursor.execute(sql,
                            (
                                item.get("field1"),
                                item.get("field2"),
                                item.get("field3"),
                            )
                            )
        self.conn.commit()
        return item


    def close_spider(self, spider):
        self.conn.close()
