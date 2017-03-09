# SlothTw（怠惰）  
課程心得查詢的API

_`sloth`_ 是天主教中七原罪的怠惰之罪<br>
學生基本上就是想要偷懶，才會想要看學長姊的修課心得XD<br>
所以以此命名。無奈sloth在pypi上已經被註冊過了，所以後面加上Tw

![剛之煉金術師的怠惰](https://images2.alphacoders.com/231/231210.png)

## API

api domain：目前還沒架起來，所以暫定`127.0.0.1`<br>
請在api domain後面接上正確的url pattern以及query string<br>
詳細的參數以及結果請參閱下面介紹

### parameter

- `school`：要查詢的學校
- `teacher`：該堂課程的老師
- `name`：課程名稱
- `start`：在取得課程名稱陣列、課程心得留言時，因為筆數可能過多，所以每次統一回傳15個。`start`為起始的index，會回傳start~start+15的資料。  

### usage and Results

API使用方式（下面所寫的是api的URL pattern）<br>
Usage of API (pattern written below is URL pattern)：

1. 取得課程目錄的陣列：_`/sloth/get/clist/`_

  - 需要指定學校和起始index： `http://127.0.0.1:8000/sloth/get/clist?school=NCHU&start=1`

    ```
    [
      {
        "model": "slothTw.course",
        "fields": {
          "teacher": "李建福",
          "avatar": "",
          "name": "對聯欣賞及創作"
        },
        "pk": 2
      },
      {
        "model": "slothTw.course",
        "fields": {
          "teacher": "李衛民等",
          "avatar": "",
          "name": "動物福祉"
        },
        "pk": 3
      }
      ...
    ]
    ```

2. 取得課程的詳細評分資料：_`/sloth/get/cvalue`_

  - 需要指定`學校、名稱、老師`： `http://127.0.0.1:8000/sloth/get/cvalue?school=NCHU&name=倫理學與當代議題&teacher=翟挹`

    ```
    {
      "book": "",
      "feedback_amount": 2,
      "school": "NCHU",
      "teacher": "翟挹",
      "syllabus": "",
      "feedback_FU": 2.5,
      "id": 39,
      "feedback_freedom": 0.0,
      "feedback_easy": 2.62,
      "feedback_knowledgeable": 3.25,
      "avatar": null,
      "feedback_GPA": 3.5,
      "name": "倫理學與當代議題"
    }
    ```

3. _`/sloth/get/comment`_：取得課程評論的陣列

  - 需要指定學校、老師、課名、起始index： `http://127.0.0.1:8000/sloth/get/comment?school=NCHU&teacher=翟挹&name=倫理學與當代議題&start=1`

    ```
    [
      {
        "model": "slothTw.comment",
        "fields": {
          "raw": "考前會給考試範圍\r\n回答問題盡量不要有冗詞",
          "course": 39,
          "html": ""
        },
        "pk": 58
      }
    ]
    ```

4. _`/put/reply`_：留言到課程心得

  - 需要指定學校、老師、課名： `http://127.0.0.1:8000/put/reply?school=NCHU&teacher=翟挹&name=倫理學與當代議題&start=1`

    ```
    {'success':True}
    ```

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

## Prerequisities

1. OS：Ubuntu / OSX would be nice
2. environment：need `python3`

  - Linux：`sudo apt-get update; sudo apt-get install; python3 python3-dev`
  - OSX：`brew install python3`

## Installing

1. `pip install slothTw`

## Running & Testing

## Run

1. `settings.py`裏面需要新增`slothTw`這個app：

  - add this:

    ```
    INSTALLED_APPS=[
    ...
    ...
    ...
    'slothTw',
    ]
    ```

2. `urls.py`需要新增下列代碼 把所有search開頭的request都導向到`slothTw`這個app：

  - add this:

    ```
    import slothTw.urls
    urlpatterns += [
        url(r'^sloth/',include(slothTw.urls,namespace="slothTw") ),
    ]
    ```

3. `python manage.py runserver`：即可進入頁面測試 `slothTw` 是否安裝成功。

### Break down into end to end tests

目前還沒寫測試...

### And coding style tests

目前沒有coding style tests...

## Deployment

`slothTw` is a django-app, so depends on django project.

`怠惰` 是一般的django插件，所以必須依存於django專案

## Built With

- simplejson
- djangoApiDec==1.2,

## Contributors

- **張泰瑋** [david](https://github.com/david30907d)

## License

This package use `GPL3.0` License.

## Acknowledgments

感謝 `剛之煉金術師`給予命名靈感
