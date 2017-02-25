# 課搜（curso）

*`curso`* 是西班牙文的課程，諧音為中文的 *`課搜`*（課程搜尋）  
因此得名

*`課搜`* 使用中興資工 [`普及資料與智慧運算實驗室`](http://web.nchu.edu.tw/~yfan/) 所開發的`KCM、KEM`等文字探勘模型作為輔助工具  
當使用者所搜尋的名稱在資料庫查無符合資料時  
系統會找出 `近似` 於使用者所查詢的 `關鍵字`   
再次查詢資料庫  並且回傳`最符合的相關課程給使用者`

## API usage and Results

api domain：*`http://www.campass.com.tw/`*  
請在api domain後面接上正確的url pattern以及query string  
詳細的參數以及結果請參閱下面介紹

### parameter

* `keyword`：the word you want to query.
* `school`：Cours of school you want to search. Below are schools which is available.
  * `NCHU`：中興大學

### API usage and Results

API使用方式（下面所寫的是api的URL pattern）<br>
Usage of API (pattern written below is URL pattern)：

1. 簡稱、課程名稱、老師、課號搜尋：  
取得課程在資料庫的該課程在該校的課程代碼

  - 範例 (Example)：
    - `http://www.campass.com.tw/search/?keyword=狼人&school=NCHU`：

        ```
        ["6686", "6694", "6673"]
        ```
    - `http://www.campass.com.tw/search/?keyword=西方+電影&school=NCHU`

      ```
      ["0302"]
      ```

2. 複數關鍵字查詢：

  - 範例 (Example)：`http://www.campass.com.tw/search/?keyword=電影+西方&school=NCHU`

    ```
    ["0302"]
    ```

3. 累積關鍵字權重：需要給使用者查詢了哪個`關鍵字`、`課程代碼`、`學校`。例如`普物`這個key在mongodb裏面有非常多堂課程，透過指定`課程代碼`累積權重，下次使用者查詢時，權重高的課程會優先出現。

  - 範例 (Example)：`http://www.campass.com.tw/incWeight/?keyword=普物&code=1108&school=NCHU`
  - result：

    ```
    {
    "_id": "58562b5caaa5b630c0c70e76",
    "普物": {
    "NCHU": [
    {
      "DBid": 2349,
      "weight": 55575
    },
    {
      "DBid": 2433,
      "weight": 700
    },
    {
      "DBid": 2434,
      "weight": 300
    }
    ]
    },
    "NCHUCourseID": [
    "1108",
    "2277"
    ]
    }
    ```

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

## Prerequisities

1. OS：Ubuntu / OSX would be nice
2. environment：need `python3`

  - Linux：`sudo apt-get update; sudo apt-get install; python3 python3-dev`
  - OSX：`brew install python3`

3. service：need `mongodb`：

  - Linux：`sudo apt-get install mongodb`

## Installing

1. `pip install curso`

## Running & Testing

## Run

1. `settings.py`裏面需要新增curso這個app：
  * add this:
  ```
    INSTALLED_APPS=[
        ...
        ...
        ...
        'curso',
    ]
  ```

2. `urls.py`需要新增下列代碼  把所有search開頭的request都導向到curso這個app：
  * add this:
  ```
  import curso.urls
  urlpatterns += [
      url(r'^search/', include(curso.urls))
  ]
  ```

3. `python manage.py runserver`：即可進入頁面測試curso是否安裝成功。

### Break down into end to end tests

目前還沒寫測試...

### And coding style tests

目前沒有coding style tests...

## Deployment

`curso` is a django-app, so depends on django project.

`課搜` 是一般的django插件，所以必須依存於django專案

## Built With

- djangoApiDec==1.2,
- jieba==0.38,
- pymongo==3.4.0,
- PyPrind==2.9.9,
- requests==2.12.3,
- simplejson==3.10.0,

## Contributors

- **張泰瑋** [david](https://github.com/david30907d)

## License

This package use `MIT` License.

## Acknowledgments

感謝`范耀中`老師的指導
