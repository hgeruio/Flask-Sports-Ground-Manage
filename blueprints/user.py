import re
from re import match

import xlrd as xlrd
import xlwt as xlwt

import app
from flask import Blueprint, render_template, request, session, redirect, url_for
from sqlalchemy.sql.functions import user

from blueprints.forms import LoginForm, AddUser
from exts import db
from models import User, Area, Fellow, Data

bp = Blueprint("user", __name__, url_prefix="/user")


# 场地管理
@bp.route("/user_index", methods=['GET', 'POST'])
def user_index():
    if request.method == 'POST':
        name1 = request.form.get('name')
        area1 = float(request.form.get('area'))
        money1 = float(request.form.get('money'))
        number1 = int(request.form.get('number'))
        a = Area.query.filter(Area.area_name == name1).first()
        try:
            if a is None or (a.area_range != area1 or a.money != money1):
                area = Area(area_name=name1, area_range=area1, number=number1, money=money1)
                db.session.add(area)
                db.session.commit()
            else:
                a.number = number1 + a.number
                db.session.merge(a)
                db.session.commit()
            return redirect(url_for("user.user_index"))
        except Exception as e:
            print(f"错误:{e}")
            return redirect(url_for("user.user_index"))
    else:
        areas = Area.query.all()
        # print(users)
        return render_template("user_index.html", areas=areas)


# 会员管理
@bp.route("/user_member", methods=['GET', 'POST'])
def user_member():
    if request.method == 'POST':
        name1 = request.form.get('name')
        sex = request.form.get('sex1')
        if sex is None:
            sex = request.form.get('sex2')
        print('sex=' + sex)
        phone = request.form.get('phone')
        a = Fellow.query.filter(Fellow.fellow_phone == phone).first()
        try:
            if a is None:
                fellow = Fellow(fellow_name=name1, fellow_sex=sex, fellow_phone=phone)
                db.session.add(fellow)
                db.session.commit()
            else:
                return render_template("user_member.html")
        except Exception as e:
            print(f"错误:{e}")
        return redirect(url_for("user.user_member"))
    else:
        member = Fellow.query.all()
        # print(users)
        return render_template("user_member.html", members=member)
    # /return render_template("user_member.html")


# 删除会员
@bp.route("/delete_member/<id>")
def delete_member(id):
    print(id)
    member = Fellow.query.get(id)
    Fellow.query.filter(Fellow.id == id).delete()
    db.session.delete(member)
    db.session.commit()
    return redirect('/user/user_member')


# 费用管理
@bp.route("/user_money", methods=['GET', 'POST'])
def user_money():
    if request.method == 'GET':
        areas = Area.query.all()
        datas = Data.query.all()
        return render_template("user_money.html", datas=datas, areas=areas)
    if request.method == 'POST':
        user_search = request.form.get("user_search")
        print(user_search)
        submit = request.form.get("user_searchs")
        if submit == "user_searchs":
            areas = Area.query.all()
            datas = Data.query.filter(Data.user.like("%" + user_search + "%")).all()
            return render_template("user_money.html", datas=datas, areas=areas)
        area_search = request.form.get("area_search")
        print(area_search)
        submit = request.form.get("area_searchs")
        if submit == "area_searchs":
            areas = Area.query.all()
            datas = Data.query.filter(Data.data_area.like("%" + area_search + "%")).all()
            return render_template("user_money.html", datas=datas, areas=areas)
        submit = request.form.get("searchs")
        if submit == "searchs":
            areas = Area.query.all()
            datas = Data.query.all()
            return render_template("user_money.html", datas=datas, areas=areas)
        submit = request.form.get("addsubmit")
        print(submit)
        if submit == "addsubmit":
            print("submit")
            name1 = request.form.get('name')
            phone = request.form.get('phone')
            data_area = request.form.get('data_area')
            time = request.form.get('time')
            # 获取用户会员信息
            print(name1, phone, data_area, time)
            u = Fellow.query.filter(Fellow.fellow_phone == phone).first()
            if u is not None:
                member = 1
            else:
                member = 0
            # 获取所选场地的费用，数量
            t = Area.query.filter(Area.area_name == data_area).first()
            if t is not None and t.number > 0:
                money = t.money
                t.number -= 1
                db.session.merge(t)
            else:
                areas = Area.query.all()
                datas = Data.query.all()
                return render_template("user_money.html", datas=datas, areas=areas,n=0)
            print(t.number)
            # 获取时长,费用
            time1 = int(re.findall('\d+', time)[0])
            if member == 1:
                money = money * time1 * 0.8
            else:
                money = money * time1
            try:
                data = Data(user=name1, phone=phone, data_area=data_area, fellow=member, money=money, time=time)
                db.session.add(data)
                db.session.commit()
                return redirect(url_for("user.user_money"))
            except Exception as e:
                print(f"错误:{e}")
                return redirect(url_for("user.user_money"))
    return redirect(url_for("user.user_money"))


# @bp.route("/user_search/<user_search>")
# def user_search(user_search):
#     search = Data.query.filter(Data.user == user_search).all()
#     return redirect('/user/user_money', datas=search)

# 工作人员管理
@bp.route("/user_manage", methods=['GET', 'POST'])
def user_manage():
    if request.method == 'POST':
        name_form = AddUser(request.form)
        if name_form.validate():
            name1 = name_form.name.data
            password1 = name_form.password.data
            email1 = name_form.email.data
            user = User(username=name1, password=password1, email=email1, is_admin=0)
            try:
                db.session.add(user)
                db.session.commit()
                return redirect(url_for("user.user_manage"))
            except Exception as e:
                print(f"错误:{e}")
                return redirect(url_for("user.user_manage"))
        else:
            return redirect(url_for("user.user_manage"))
    else:
        users = User.query.all()
        # print(users[0].username)
        return render_template("user_manage.html", users=users)


# 导入excel
@bp.route("/user_manage/to-excel/<id>", methods=['GET', 'POST'])
def to_excel(id):
    if request.method == 'POST':
        file = request.files.get('file')
        f = file.read()
        clinic_file = xlrd.open_workbook(file_contents=f)
        # sheet1
        table = clinic_file.sheet_by_index(0)
        nrows = table.nrows
        # print(nrows)
        db.session.query(User).filter(User.id != id).delete()
        user1 = User.query.filter(User.id == id).first()
        db.session.commit()
        for i in range(1, nrows):
            # print(i)
            row_date = table.row_values(i)
            # print(row_date)
            if user1.email != str(row_date[3]):
                user = User(username=str(row_date[1]), password=str(row_date[2]), email=str(row_date[3]),
                            is_admin=int(row_date[4]))
                db.session.add(user)
                db.session.commit()
            db.session.close()
        return redirect(url_for("user.user_manage"))


# 导出excel
@bp.route("/user_manage/get-excel", methods=['GET', 'POST'])
def get_excel():
    users = User.query.all()
    book = xlwt.Workbook(encoding='utf-8', style_compression=0)
    sheet = book.add_sheet('user表单')
    col = ('序号', '用户名', '用户密码', '邮箱', '用户角色')
    for i in range(0, 5):
        sheet.write(0, i, col[i])  # 第0行第i列为col[i]的值
    for i in range(1, len(users) + 1):
        sheet.write(i, 0, users[i - 1].id)
        sheet.write(i, 1, users[i - 1].username)
        sheet.write(i, 2, users[i - 1].password)
        sheet.write(i, 3, users[i - 1].email)
        sheet.write(i, 4, users[i - 1].is_admin)
    book.save('C:/Users/admin/Desktop/工作人员.xls')
    # print("文件已导出")
    return redirect(url_for("user.user_manage"))


# 删除工作人员
@bp.route("/delete_user/<id>")
def delete_user(id):
    print(id)
    user1 = User.query.get(id)
    User.query.filter(User.id == id).delete()
    db.session.delete(user1)
    db.session.commit()
    return redirect('/user/user_manage')


# 修改工作人员信息
@bp.route("edit_user/<id>", methods=['GET', 'POST'])
def edit_user(id):
    submit = request.form.get('addOk')
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        user1 = User.query.get(id)
        user1.username = name
        user1.email = email
        print(name, email, "111")
        try:
            print(name, email)
            db.session.merge(user1)
            db.session.commit()
        except Exception as e:
            print(f"错误:{e}")
            db.session.rollback()
        return redirect('/user/user_manage')
    elif submit == 'addOk':
        return redirect('/user/user_manage')
    else:
        user2 = User.query.filter(User.id == id).first()
        return render_template("edit_user.html", user2=user2)


# 修改密码
@bp.route('/user_password', methods=['GET', 'POST'])
def user_password():
    if request.method == 'POST':
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        name = app.user_context()['user']
        print(name.username)
        user1 = User.query.filter_by(username=name.username).first()
        if user1.password == password1:
            user1.email = email
            user1.password = password2
            try:
                db.session.merge(user1)
                db.session.commit()
            except Exception as e:
                print(f"错误:{e}")
                db.session.rollback()
            return render_template("user_password.html", data=0)
        else:
            return render_template("user_password.html", data=1)
    else:
        return render_template("user_password.html")
