import scrapy
from data.items import HaoDaiFuItem


class HaodaifuSpider(scrapy.Spider):
    name = "haodaifu"
    allowed_domains = ["haodf.com"]
    start_urls = ["https://www.haodf.com/citiao/list-jibing-xinxueguanneike.html"]
    urls_header = 'https://www.haodf.com'
    custom_settings = {
        'ITEM_PIPELINES': {
            'data.pipelines.haodaifuDataPipeline': 300,
        }
    }

    def parse(self, response):
        hrefs = response.xpath("//div[@class='kstl']/a/@href").extract()
        for href in hrefs:
            href = self.urls_header + href
            yield scrapy.Request(
                url=href,
                callback=self.First_classification
            )

    # 进入内科外科等页面
    def First_classification(self, response):
        hrefs = response.xpath("//div[@class='ksbd']/ul/li/a/@href").extract()
        if not hrefs:
            href = response.request.url
            yield scrapy.Request(
                url=href,
                callback=self.Second_classification
            )
        else:
            for href in hrefs:
                href = self.urls_header + href
                yield scrapy.Request(
                    url=href,
                    callback=self.Second_classification
                )

    def Second_classification(self, response):
        divs = response.xpath("//div[@class='m_ctt_green']")
        for div in divs:
            hrefs = div.xpath("./ul/li/a/@href").extract()
            for href in hrefs:
                href = (self.urls_header + href)
                if href.split("/")[-1] == "tuijian-doctor.html":
                    href = href.replace("tuijian-doctor.html", "jieshao.html")
                else:
                    href = href.replace(".html", "/jieshao.html")
                yield scrapy.Request(
                    url=href,
                    callback=self.detailed_information
                )

    def detailed_information(self, response):
        name = response.xpath("//div[@class='info-title']/h1/text()").extract_first()
        altname = response.xpath("//div[@class='info-title']/span/text()").extract_first()
        if not altname:
            altname = 'None'
        else:
            altname = altname.split("：")[-1][0:-1]
        department = (",".join(response.xpath("//p[@class='info-faculty']/a/text()").extract())).replace('\xa0','')
        introduction = response.xpath(
            "//div[@data-key='介绍']/div[@class='l-c-text rich-text-content']/p/text()").extract()
        if not introduction:
            introduction = 'None'
        else:
            introduction = "".join(introduction)

        cause = response.xpath(
            "//div[@data-key='发病原因']/div[@class='l-c-text rich-text-content']//text()").extract()
        if not cause:
            cause = 'None'
        else:
            cause = ("".join(cause)).replace('\n','')

        symptom = response.xpath(
            "//div[@data-key='症状表现']/div[@class='l-c-text rich-text-content']//text()").extract()
        if not symptom:
            symptom = 'None'
        else:
            symptom = ("".join(symptom)).replace('\n','')

        prevent = response.xpath(
            "//div[@data-key='如何预防']/div[@class='l-c-text rich-text-content']//text()").extract()
        if not prevent:
            prevent = 'None'
        else:
            prevent = ("".join(prevent)).replace('\n','')

        inspect = response.xpath("//div[@data-key='检查']/div[@class='l-c-text rich-text-content']//text()").extract()
        if not inspect:
            inspect = 'None'
        else:
            inspect = ("".join(prevent)).replace('\n','')

        treatment = response.xpath(
            "//div[@data-key='治疗方式']/div[@class='l-c-text rich-text-content']//text()").extract()
        if not treatment:
            treatment = 'None'
        else:
            treatment = ("".join(prevent)).replace('\n','')

        nutrition_and_diet = response.xpath(
            "//div[@data-key='营养与饮食']/div[@class='l-c-text rich-text-content']//text()").extract()
        if not nutrition_and_diet:
            nutrition_and_diet = 'None'
        else:
            nutrition_and_diet = ("".join(nutrition_and_diet)).replace('\n','')

        notice = response.xpath(
            "//div[@data-key='注意事项']/div[@class='l-c-text rich-text-content']//text()").extract()
        if not notice:
            notice = 'None'
        else:
            notice = ("".join(notice)).replace('\n','')

        prognosis = response.xpath(
            "//div[@data-key='预后']/div[@class='l-c-text rich-text-content']//text()").extract()
        if not prognosis:
            prognosis = 'None'
        else:
            prognosis = ("".join(prognosis)).replace('\n','')

        item = HaoDaiFuItem()
        item['name'] = name
        item['altname'] = altname
        item['department'] = department
        item['introduction'] = introduction
        item['cause'] = cause
        item['symptom'] = symptom
        item['prevent'] = prevent
        item['inspect'] = inspect
        item['treatment'] = treatment
        item['nutrition_and_diet'] = nutrition_and_diet
        item['notice'] = notice
        item['prognosis'] = prognosis
        yield item
