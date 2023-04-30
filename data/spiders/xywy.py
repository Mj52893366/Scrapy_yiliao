import scrapy

from data.items import XywyDataItem

class XywySpider(scrapy.Spider):
    name = "xywy"
    allowed_domains = ["jib.xywy.com"]
    url_header = "http://jib.xywy.com/"
    start_urls = ["https://jib.xywy.com/html/neike.html"]
    custom_settings = {
        'ITEM_PIPELINES': {
            'data.pipelines.XywyDataPipeline': 200,
        }
    }
    # 例如  在主页面进入内科->呼吸内科页面
    def parse(self, response):
        ul = response.xpath("//div[@class='jblist-nav fl']/ul/li")
        for li in ul:
            li_list_in_ul = li.xpath("./ul/li")
            for li_c in li_list_in_ul:
                href = self.url_header + li_c.xpath("./a/@href").extract_first()
                yield scrapy.Request(url=href, callback=self.department_classification )

    # 进入呼吸内科后，按照字母顺序列出了所有疾病
    def department_classification(self, response):
        divs = response.xpath("//div[@class='ks-ill-txt mt20']")
        for div in divs:
            li_list = div.xpath("./ul/li")
            for li in li_list:
                url = self.url_header + li.xpath("./a/@href").extract_first()
                url_gaishu = url.replace("il_sii_", "il_sii/gaishu/")
                yield scrapy.Request(url=url_gaishu, callback=self.gaishu_information)

    def gaishu_information(self, response):
        # 疾病名称
        name = response.xpath('//div[@class="jb-name fYaHei gre"]/text()').extract_first()
        # print(name)
        # 疾病简介
        introduction = response.xpath(
            "//div[@class='jib-articl-con jib-lh-articl']/p/text()").extract_first().replace(" ", "").replace("\n",
                                                                                                              "").replace(
            "\t", "").replace("\r", "")
        # print(introduction)
        # 易感人群
        population = response.xpath(
            "//div[@class='mt20 articl-know'][1]/p[3]/span[2]/text()").extract_first().replace(" ", "").replace("\n",
                                                                                                                "").replace(
            "\t", "").replace("\r", "")
        # print(population)
        # 并发症
        complication = response.xpath("//div[@class='mt20 articl-know'][1]/p[5]/span[2]/a/text()").extract()  # 数组处理
        complication = ','.join(complication)
        # print(complication)
        # 科室
        department = response.xpath("//div[@class='mt20 articl-know'][2]/p[1]/span[2]/text()").extract_first().replace(
            "  ", ",")
        # print(department)
        # 常用药品
        medication = response.xpath("//div[@class='mt20 articl-know'][2]/p[5]/span[2]/a/text()").extract()
        medication = ','.join(medication).strip()
        # print(medication)
        # 存储到Item
        item = XywyDataItem()
        item['name'] = name
        item['introduction'] = introduction
        item['population'] = population
        item['complication'] = complication
        item['department'] = department
        item['medication'] = medication
        # print(self.item.items())
        # yield item
        url = response.request.url
        url_cause = url.replace("il_sii/gaishu/", "il_sii/cause/")
        yield scrapy.Request(url=url_cause,callback=self.cause_information,meta={'item':item})


    def cause_information(self, response):
        # 病因
        cause = response.xpath("//div[@class=' jib-articl fr f14 jib-lh-articl']//text()").extract()
        cause = ''.join(cause).replace(" ", "").replace("\n", "").replace("\t", "").replace("\r", "")
        # print(response)
        # print(cause)
        item = response.meta['item']
        item['cause'] = cause
        url = response.request.url
        url_symptom = url.replace("il_sii/cause/", "il_sii/symptom/")
        yield scrapy.Request(url=url_symptom, callback=self.symptom_information, meta={'item': item})


    def symptom_information(self, response):
        # 症状
        symptom = response.xpath("//div[@class='jib-articl fr f14 jib-lh-articl']//text()").extract()
        symptom = ''.join(symptom).replace(" ", "").replace("\n", "").replace("\t", "").replace("\r", "")
        item = response.meta['item']
        item['symptom'] = symptom
        url = response.request.url
        url_inspect = url.replace("il_sii/symptom/", "il_sii/inspect/")
        yield scrapy.Request(url=url_inspect, callback=self.inspect_information, meta={'item': item})


    def inspect_information(self, response):
        # 常用检查
        inspect = response.xpath("//div[@class='jib-articl fr f14 jib-lh-articl']//text()").extract()
        inspect = ''.join(inspect).replace(" ", "").replace("\n", "").replace("\t", "").replace("\r", "")
        item = response.meta['item']
        item['inspect'] = inspect
        yield item
