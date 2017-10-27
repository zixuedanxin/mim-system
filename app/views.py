import datetime

from flask import render_template, url_for, request, flash, redirect
from manage import app, db
from .models import Medicine, Agency, Client
from .user import User
from .forms import LoginForm
from flask_login import login_user, login_required, logout_user
from app.config import FLASK_ADMIN_USERNAME, FLASK_ADMIN_PASSWORD


@app.route("/home", methods=["POST", "GET"])
@login_required
def home():
    return render_template("home.html", title="首页")


@app.route('/', methods=["POST", "GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.username.data == FLASK_ADMIN_USERNAME and \
           form.password.data == FLASK_ADMIN_PASSWORD:
            login_user(user=User(FLASK_ADMIN_USERNAME), remember=True)
            return redirect(url_for("home"))
        else:
            flash("账号或密码错误！")
            return redirect(url_for("login"))
    return render_template("login.html", title="登录", form=form)


@app.route('/logout')
@login_required
def logout():
    """ 登出账户
    """
    logout_user()
    flash('您已退出登录')
    return redirect(url_for('login'))


@app.route("/insert-client", methods=["POST", "GET"])
def insert_client():
    if request.method == "POST":
        cname = request.values.get("cname")
        csex = request.values.get("csex")
        cage = request.values.get("cage")
        try:
            _cage = int(cage)
        except:
            flash("年龄需为整数！")
            return redirect(url_for("insert_client"))
        caddress = request.values.get("caddress")
        cphone = request.values.get("cphone")
        csymptom = request.values.get("csymptom")
        ano = request.values.get("ano")
        if Agency.query.filter_by(ano=ano).first() is None:
            flash(ano + "：该经办人编号不存在！")
            return redirect(url_for("insert_client"))
        mno = request.values.get("mno")
        if Medicine.query.filter_by(mno=mno).first() is None:
            flash(mno + "：该药品编号不存在！")
            return redirect(url_for("insert_client"))
        cremark = request.values.get("cremark")

        _client = Client(
            cname=cname,
            csex=csex,
            cage=_cage,
            caddress=caddress,
            cphone=cphone,
            csymptom=csymptom,
            cdate=datetime.datetime.now(),
            ano=ano,
            mno=mno,
            cremark=cremark
        )

        db.session.add(_client)
        db.session.commit()
    return render_template("insert_client.html",
                           title="新增顾客",
                           client_info={
                               "cname": "",
                               "csex": "",
                               "cage": "",
                               "caddress": "",
                               "cphone": "",
                               "csymptom": "",
                               "ano": "",
                               "mno": "",
                           })


@app.route("/insert-agency", methods=["POST", "GET"])
def insert_agency():
    if request.method == "POST":
        aname = request.values.get("aname")
        asex = request.values.get("asex")
        aphone = request.values.get("aphone")
        aremark = request.values.get("aremark")
        _agency = Agency(
            aname=aname,
            asex=asex,
            aphone=aphone,
            aremark=aremark
        )
        db.session.add(_agency)
        db.session.commit()
    return render_template("insert_agency.html",
                           title="新增经办人",
                           agency_info={
                               "aname": "",
                               "asex": "",
                               "aphone": "",
                               "aremark": ""
                           })


@app.route("/insert-medicine", methods=["POST", "GET"])
def insert_medicine():
    if request.method == "POST":
        mname = request.values.get("mname")
        mmode = request.values.get("mmode")
        mefficacy = request.values.get("mefficacy")
        _medicine = Medicine(
            mname=mname,
            mmode=mmode,
            mefficacy=mefficacy
        )

        db.session.add(_medicine)
        db.session.commit()
    return render_template("insert_medicine.html",
                           title="新增药品",
                           medicine_info={
                               "mname": "",
                               "mmode": "",
                               "mefficacy": ""
                           })


@app.route("/insert-client/<int:id>", methods=["POST", "GET"])
def edit_client(id):
    _client = Client.query.filter_by(cno=id).first()
    cname = _client.cname
    csex = _client.csex
    cage = _client.cage
    caddress = _client.caddress
    cphone = _client.cphone
    csymptom = _client.csymptom

    if request.method == "POST":
        cname = request.values.get("cname")
        csex = request.values.get("csex")
        cage = request.values.get("cage")
        try:
            _cage = int(cage)
        except:
            flash("年龄需为整数！")
            return redirect(url_for("insert_client"))
        caddress = request.values.get("caddress")
        cphone = request.values.get("cphone")
        csymptom = request.values.get("csymptom")
        ano = request.values.get("ano")
        if Agency.query.filter_by(ano=ano).first() is None:
            flash(ano + "：该经办人编号不存在！")
            return redirect(url_for("insert_client"))
        mno = request.values.get("mno")
        if Medicine.query.filter_by(mno=mno).first() is None:
            flash(mno + "：该药品编号不存在！")
            return redirect(url_for("insert_client"))
        cremark = request.values.get("cremark")

        _client.cname = cname
        _client.csex = csex
        _client.cage = _cage
        _client.caddress = caddress
        _client.csymptom = csymptom
        _client.ano = ano
        _client.mno = mno
        _client.cremark = cremark

        db.session.add(_client)
        db.session.commit()
    return render_template("insert_client.html",
                           title="编辑顾客信息",
                           client_info={
                               "cname": cname,
                               "csex": csex,
                               "cage": cage,
                               "caddress": caddress,
                               "cphone": cphone,
                               "csymptom": csymptom
                           })


@app.route("/insert-agency/<int:id>", methods=["POST", "GET"])
def edit_agency(id):
    _agency = Agency.query.filter_by(ano=id).first()
    aname = _agency.aname
    asex = _agency.asex
    aphone = _agency.aphone

    if request.method == "POST":
        aname = request.values.get("aname")
        asex = request.values.get("asex")
        aphone = request.values.get("aphone")
        aremark = request.values.get("aremark")

        _agency.aname = aname
        _agency.asex = asex
        _agency.aphone = aphone
        _agency.aremark = aremark

        db.session.add(_agency)
        db.session.commit()
    return render_template("insert_agency.html",
                           title="编辑经办人信息",
                           agency_info={
                               "aname": aname,
                               "asex": asex,
                               "aphone": aphone
                           })


@app.route("/edit-medicine/<int:id>", methods=["POST", "GET"])
def edit_medicine(id):
    _medicine = Medicine.query.filter_by(mno=id).first()
    mname = _medicine.mname
    mmode = _medicine.mmode
    mefficacy = _medicine.mefficacy

    if request.method == "POST":
        mname = request.values.get("mname")
        mmode = request.values.get("mmode")
        mefficacy = request.values.get("mefficacy")

        _medicine.mname = mname
        _medicine.mmode = mmode
        _medicine.mefficacy = mefficacy

        db.session.add(_medicine)
        db.session.commit()
    return render_template("insert_medicine.html",
                           title="编辑药品信息",
                           medicine_info={
                               "mname": mname,
                               "mmode": mmode,
                               "mefficacy": mefficacy
                           })


@app.route("/query-client", methods=["POST", "GET"])
def query_client():
    query = request.values.get("cQuery")
    if query == "#all":
        client = Client.query.all()
    else:
        if request.values.get("queryBy") == "搜编号":
            client = Client.query.filter_by(cno=query)
        else:
            client = Client.query.filter_by(cname=query)
    return render_template("query_client.html",
                           title="查询顾客",
                           forms=client)


@app.route("/query-agency", methods=["POST", "GET"])
def query_agency():
    query = request.values.get("aQuery")
    if query == "#all":
        agency = Agency.query.all()
    else:
        if request.values.get("queryBy") == "搜编号":
            agency = Agency.query.filter_by(ano=query)
        else:
            agency = Agency.query.filter_by(aname=query)
    return render_template("query_agency.html",
                           title="查询经办人",
                           forms=agency)


@app.route("/query-medicine", methods=["POST", "GET"])
def query_medicine():
    query = request.values.get("mQuery")
    if query == "#all":
        medicine = Medicine.query.all()
    else:
        if request.values.get("queryBy") == "搜编号":
            medicine = Medicine.query.filter_by(mno=query)
            print("do")
        else:
            medicine = Medicine.query.filter_by(mname=query)
    return render_template("query_medicine.html",
                           title="查询药品",
                           forms=medicine)


@app.route("/delete-client/<int:id>")
def delete_client(id):
    query = Client.query.filter_by(cno=id).first()
    db.session.delete(query)
    db.session.commit()


@app.route("/delete-agency/<int:id>")
def delete_agency(id):
    query = Agency.query.filter_by(ano=id).first()
    db.session.delete(query)
    db.session.commit()


@app.route("/delete-medicine/<int:id>")
def delete_medicine(id):
    query = Medicine.query.filter_by(mno=id).first()
    db.session.delete(query)
    db.session.commit()


@app.errorhandler(401)
def page_not_found(e):
    return render_template("401.html"), 401


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500