# 使用手册

## 1.0

### 项目包含了三个爬虫

- a39net.py
  - ` scrapy crawl a39net`
- haodaifu.py
  - ` scrapy crawl haodaifu`
- xywy.py
  - ` scrapy crawl xywy`

### 使用前需要自己配置Mysql数据库

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



### Pipeline

每个爬虫对应一个管道

```python
custom_settings = {
        'ITEM_PIPELINES': {
            'data.pipelines.a39netDataPipeline': 300,
        }
    }
```

**pipeline中只预置了存储到mysql数据库的管道**

**数据库生成语句**

- Xywy

  ```sql
  CREATE TABLE Xywy (
      name VARCHAR(255),
      introduction TEXT,
      department VARCHAR(255),
      population VARCHAR(255),
      complication VARCHAR(255),
      symptom TEXT,
      inspect TEXT,
      medication TEXT,
      cause TEXT
  );
  ```

- Haodaifu

  ```sql
  CREATE TABLE Haodaifu (
      name VARCHAR(255), 
      altname VARCHAR(255), 
      department VARCHAR(255), 
      introduction TEXT, 
      cause TEXT, 
      symptom TEXT, 
      prevent TEXT, 
      inspect TEXT, 
      treatment TEXT, 
      nutrition_and_diet TEXT, 
      notice TEXT, 
      prognosis TEXT
  );
  ```

- A39net

  ```sql
  CREATE TABLE A39net (
    `name` VARCHAR(255) NOT NULL,
    `introduction` TEXT,
    `altname` VARCHAR(255),
    `pathogenic_site` VARCHAR(255),
    `department` VARCHAR(255),
    `population` VARCHAR(255),
    `symptom` TEXT,
    `inspect` TEXT,
    `complication` TEXT,
    `treatment` TEXT
  )
  ```

  



### 中间件

**UA池和代理IP**

已在settings.py中打开

```python
DOWNLOADER_MIDDLEWARES = {
   "data.middlewares.DownloaderMiddleware": 543,
}
```



## 2.0更新

通过run_spiders.py即可运行整个爬虫项目

