from flask import Flask, render_template, request, redirect
import pymysql as mysql
import pymysql

# 配置数据库用户名 密码 数据库名
con = mysql.connect(user='root', password='root', db="book")
# 开启数据库事务的自动提交功能
con.autocommit(True)
# 获取数据库的游标
cur = con.cursor()

# 主函数
app = Flask(__name__)


# 配置数据库名 账号 密码  端口号 数据库库名
def getdata(sql):
    connect = pymysql.connect(
        host="localhost",
        user="root",
        password="root",
        port=3306,
        database="book"
    )
    # 获取游标
    cursor = connect.cursor()
    # 执行通过函数传入的sql语句
    cursor.execute(sql)
    # 获取所有的数据库将参数赋给result
    result = cursor.fetchall()
    # 返回result参数
    return result


# 设置网址的路由
@app.route('/index')
def hello_world():
    # 执行userlist函数将返回值赋给data
    data = userlist()
    # 使用render_template渲染index.html并传入数据data到前端
    return render_template("index.html", data=data)


# 设置网址的路由
@app.route('/', methods=["post", "get"])
def login():
    if request.method == "POST":
        user = request.form.get('user')
        password = request.form.get('password')
        sql = 'select * from user where user ="{}" AND pwd="{}"'.format(user, password)
        b = cur.execute(sql)
        if b == 1:
            return redirect('/index')
        else:
            return render_template("login.html", data=0)
    else:
        return render_template("login.html", data=1)


# 定义一个函数 使用sql语句查询anthors表的所有数据
def userlist():
    sql = "select * from authors"
    # 执行通过函数传入的sql语句
    cur.execute(sql)
    # 获取所有的数据库将参数赋给data
    data = cur.fetchall()
    return data


# 设置路由为/add 使用的请求方式是post
@app.route('/add', methods=["post", "get"])
def add():
    if request.method == "POST":
        # 获取前端表单里key来获取value值
        id = request.form.get('id')
        name = request.form.get('name')
        books = request.form.get('books')
        price = request.form.get('price')
        # 数据库命令根据id来查询此id是否已经存在
        s = 'select * from authors where id=' + id
        a = cur.execute(s)
        # 如果存在
        if a == 1:
            return "编号已存在"
        # 否则
        else:
            # 数据库插入语句
            sql = 'insert  authors values(%s,%s,%s,%s)'
            # 传入语句与需要插入的值
            cur.execute(sql, [id, name, books, price])
            # 提交该事务
            con.commit()
            # 重定向路由为
            return redirect('/index')


# 根据id进行删除
@app.route('/dele', methods=["post", "get"])
def dele():
    # 从前端表单中获取id的值
    id = request.args.get("id")
    # 执行sql命令，根据id删除内容
    sql = "delete from authors where id=" + id
    cur.execute(sql)
    con.commit()
    return redirect('/index')

# 根据id进行查找
@app.route('/sele', methods=["post", "get"])
def sele():
    id = request.form.get("sele")
    sql = "select * from authors where id=" + id
    b = cur.execute(sql)
    sdata = cur.fetchall()
    if b == 1:
        return render_template("select.html", sdata=sdata)
    else:
        return render_template("select.html", d=0)


# 根据名称进行查找
@app.route('/sele1', methods=["post", "get"])
def sele1():
    name = request.form.get("name")
    sql = 'select * from authors where books like "%{}%"'.format(name)
    b = cur.execute(sql)
    sdata = cur.fetchall()
    print(b)
    if b == 1:
        return render_template("select.html", sdata=sdata)
    else:
        return render_template("select.html", d=0)


# # 根据id进行修改
@app.route('/updata', methods=['GET', 'POST'])
def updata():
    id = request.args.get('id')
    sql = "select * from authors where id = %s" % id
    data = getdata(sql)
    movie = []
    for i in data:
        movie.append(i)
    print(movie[0])
    print(movie)
    return render_template('updata.html', data=movie[0])


@app.route('/update', methods=['POST'])
def update():
    id = request.form.get('id')
    name = request.form.get('name')
    books = request.form.get('books')
    price = request.form.get('price')
    sql = 'update authors set name="{}",books="{}",price="{}" where id="{}"'.format(name, books, price, id)
    cur.execute(sql)
    con.commit()
    return redirect('/index')


# 主函数执行
if __name__ == '__main__':
    # 主动开启debug便于调试
    app.run(debug=True)
