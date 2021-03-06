from . import db


class Agency(db.Model):
    __tablename__ = "agencies"

    ano = db.Column(db.Integer, primary_key=True, autoincrement=True)
    aname = db.Column(db.String)
    asex = db.Column(db.String)
    aphone = db.Column(db.String)
    aremark = db.Column(db.String)

    def __repr__(self):
        return '<Agency {}>'.format(self.ano)


class Medicine(db.Model):
    __tablename__ = "medicines"

    mno = db.Column(db.Integer, primary_key=True, autoincrement=True)
    mname = db.Column(db.String)
    mmode = db.Column(db.String)
    mefficacy = db.Column(db.String)

    def __repr__(self):
        return '<Medicine {}>'.format(self.mno)


class Client(db.Model):
    __tablename__ = "clients"

    cno = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cname = db.Column(db.String)
    csex = db.Column(db.String)
    cage = db.Column(db.Integer)
    caddress = db.Column(db.String)
    cphone = db.Column(db.String)
    csymptom = db.Column(db.String)
    cdate = db.Column(db.DateTime)
    cremark = db.Column(db.String)

    # 与 Medicine 建立主外键关系
    medicine = db.relationship("Medicine",
                               backref=db.backref("client", lazy=True))
    mno = db.Column(db.Integer, db.ForeignKey("medicines.mno"))

    # 与 Agency 建立主外键关系
    agencies = db.relationship("Agency",
                               backref=db.backref("client", lazy=True))
    ano = db.Column(db.Integer, db.ForeignKey("agencies.ano"))

    def __repr__(self):
        return '<Client {}>'.format(self.cno)
