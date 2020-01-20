##  header2, <h2>

*   `Flask` is used as the backend of our website. 前端框架用的是 `Vue.js`. And `numpy, pandas, sklearn` are used as machine learning modules.

*   这是一个段落

*   This is another paragraph

*   This is a hyper-link to [flask](http://flask.pocoo.org/docs/1.0/api)

*   Here is an image

    ![a](https://flask.palletsprojects.com/en/1.0.x/_static/flask-icon.png)

##  quotation and codeblcok

这是一句引用

>this is a `quotation`, and a [link](123) within.

codeblock

```python
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'
```

<br>

#   header

*   代码块 `codeblock`

    ```
    Ubuntu 16.04
    Python 3.5+
    Flask 1.0.2
    Vue.js v2.5.13
    axios v0.17.1
    Bootstrap v4.0.0
    ```

*   `nested-list`

    *   sub-list

    *   123

    *   aaa

<br>

#   <h1>This is h1 header</h1>

This is a paragraph.

All html tags, e.g. `<h1>` in the first line, will be escaped unless there is only a `<br>` in a line, which could be used to add more space between two sections).

<br>

##  TODO

*   代码高亮颜色仍待实现

    ```bash
    $ export FLASK_APP=server
    $ python3 -m flask initdb
    python3 server.py &
    ```

*   有序列表 `ol`

<br>

