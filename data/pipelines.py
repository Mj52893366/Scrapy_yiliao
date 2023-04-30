# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pymysql
from data.settings import MYSQL

# class DataPipeline:
#     def process_item(self, item, spider):
#         #在process中 是每条数据执行一次 所以mode="a"
#         print(item['name']+'888888888888888888888888888888888888')


class XywyDataPipeline:
    def open_spider(self, spider):
        self.conn = pymysql.connect(
            host=MYSQL['host'],
            port=MYSQL['port'],
            user=MYSQL['user'],
            password=MYSQL['password'],
            database=MYSQL['database']
        )

    def close_spider(self, spider):
        if self.conn:
            self.conn.close()

    def process_item(self, item, spider):
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "insert into xywy(name,introduction,department,population,complication,medication,cause,inspect,symptom) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                (item['name'], item['introduction'], item['department'], item['population'],
                 item['complication'], item['medication'], item['cause'], item['inspect'], item['symptom']))
            print('insert ok')
            self.conn.commit()
        except:
            self.conn.rollback()
            print('插入失败')
        finally:
            if cursor:
                cursor.close()

        return item


class haodaifuDataPipeline:
    def open_spider(self, spider):
        self.conn = pymysql.connect(
            host=MYSQL['host'],
            port=MYSQL['port'],
            user=MYSQL['user'],
            password=MYSQL['password'],
            database=MYSQL['database']
        )


    def close_spider(self, spider):
        if self.conn:
            self.conn.close()

    def process_item(self, item, spider):
        try:
            cursor = self.conn.cursor()
            sql = "insert into haodaifu(name, altname, department, introduction, cause, symptom, prevent, inspect, " \
                  "treatment, nutrition_and_diet, notice, prognosis) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                  " %s ,%s)"
            if item['cause'] != 'None':
                cursor.execute(sql, (item['name'], item['altname'], item['department'], item['introduction'],
                                     item['cause'], item['symptom'], item['prevent'], item['inspect'], item['treatment'],
                                     item['nutrition_and_diet'], item['notice'], item['prognosis']))
                self.conn.commit()
                print('成功')
        except pymysql.Error as e:
            self.conn.rollback()
        finally:
            if cursor:
                cursor.close()
        return item


class a39netDataPipeline:
    def open_spider(self, spider):
        self.conn = pymysql.connect(
            host=MYSQL['host'],
            port=MYSQL['port'],
            user=MYSQL['user'],
            password=MYSQL['password'],
            database=MYSQL['database']
        )

    def close_spider(self, spider):
        if self.conn:
            self.conn.close()

    def process_item(self, item, spider):
        try:
            cursor = self.conn.cursor()
            sql = sql = "INSERT INTO a39net(`name`, `introduction`, `altname`, `pathogenic_site`, `department`," \
                        " `population`, `symptom`, `inspect`, `complication`, `treatment`) VALUES (%s, %s, %s, %s, %s," \
                        " %s, %s, %s, %s, %s)"
            cursor.execute(sql, (item['name'], item['introduction'], item['altname'], item['pathogenic_site'],
                                 item['department'], item['population'], item['symptom'], item['inspect'],
                                 item['complication'], item['treatment']))
            print('ok')
            self.conn.commit()
        except:
            print('写入异常')
            self.conn.rollback()
        finally:
            if cursor:
                cursor.close()
        return item
