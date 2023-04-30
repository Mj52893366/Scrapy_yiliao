# 使用手册

## 项目包含了三个爬虫

- a39net.py
  - ` scrapy crawl a39net`
- haodaifu.py
  - ` scrapy crawl haodaifu`
- xywy.py
  - ` scrapy crawl xywy`

## 使用前需要自己配置Mysql数据库

在data.settings.py中配置Mysql信息

```python
MYSQL = {
    "host": "x.xx.xx.xx",
    "port": 3306,
    "user": "xxx",
    "password": "xxx",
    "database": "xxx"
}
```



## Pipeline

每个爬虫对应一个管道

```python
custom_settings = {
        'ITEM_PIPELINES': {
            'data.pipelines.a39netDataPipeline': 300,
        }
    }
```

**pipeline中只预置了存储到mysql数据库的管道**



## 中间件

**UA池和代理IP**

已在settings.py中打开

```python
DOWNLOADER_MIDDLEWARES = {
   "data.middlewares.DownloaderMiddleware": 543,
}
```

