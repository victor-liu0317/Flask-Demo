from flask import Flask, render_template, request, redirect,url_for
import pymysql

app = Flask(__name__)


@app.route('/')
def hello():
    return render_template('home.html')

@app.route('/signin', methods=['POST', 'GET'])
def testlogin():
    username = str(request.form['username'])
    passwd = mymd5(str(request.form['password'])) # 一次MD5加密
    # 连接数据库
    conn = pymysql.connect(user='root', passwd='', host='localhost', db='pythonconnection')
    cur = conn.cursor()
    cur.execute("select psw from logintest where user='%s'" % username)
    try:
        data = cur.fetchall()
        if len(data) == 0:
            return render_template('home.html', message='该用户尚未注册！')
        for r in data:
            if str(r[0]) == passwd:
                return render_template('welcome.html', username=username)
            else:
                return render_template('home.html', message='错误的密码！')
    except:
        return render_template('home.html', message='数据库连接有问题！')
    cur.close()
    conn.close()

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/register', methods=['POST', 'GET'])
def adduser():
    username = str(request.form['username'])
    passwd = mymd5(str(request.form['password']))

    # 连接数据库
    conn = pymysql.connect(user='root', passwd='', host='localhost', db='pythonconnection')
    cur = conn.cursor()
    cur.execute("select * from logintest where user='%s'" % username)
    try:
        data = cur.fetchall()
        if len(data) != 0:
            return render_template('register.html', message='该用户已经注册！')
        else:
            cur.execute("insert into logintest VALUES ('%s','%s')" % (username, passwd))
            conn.commit()
            return render_template('home.html', message='注册成功！请登录')

    except:
        return render_template('home.html', message='数据库连接有问题！')

@app.route('/comment', methods=['POST', 'GET'])
def comment():
    conn = pymysql.connect(user='root', passwd='shiyanshi', host='localhost', db='pythonconnection', charset='utf8')
    cur = conn.cursor()
    if request.args:
        username = request.args.get('username')
        time = request.args.get('time')
        comment = request.args.get('comment')
        if username and time and comment:
            cur.execute("insert into comment VALUES ('%s','%s','%s')" % (username, time, comment))
            conn.commit()
    cur.execute("select * from comment order by time desc")
    data = cur.fetchall()
    mycomment = ""
    for r in data:
        textstr = "<div class='panel panel-primary'><div class='panel-heading'>" \
                  "<h3 class='panel-title'>" + "Name：" + r[0] + \
                  "&nbsp;&nbsp;&nbsp;&nbsp;Time：" + r[1] + \
                  "</h3></div><div class='panel-body'>" + r[2] + "</div></div>"
        mycomment += textstr
    cur.close()
    conn.close()
    return mycomment


def mymd5(str):
    # 定义自己的md5加密，用于数据库中密码的存储和校验
    import hashlib
    m = hashlib.md5()
    m.update(str.encode('utf-8')) # 注意这里的编码问题
    return m.hexdigest()

if __name__ == '__main__':
    app.run(host='0.0.0.0')
