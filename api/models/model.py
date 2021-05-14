from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_,update
from sqlalchemy.sql.expression import func
from sqlalchemy.orm import sessionmaker

db = SQLAlchemy()

class Artist(db.Model):
    __tablename__ = 'artist'
    pid = db.Column(db.Integer, primary_key=True)
    cid = db.Column(
        db.String(45), unique=True, nullable=False)
    name = db.Column(
        db.String(45), nullable=False)
    pic = db.Column(
        db.String(200), nullable='none')
    allfirst = db.Column(
        db.String(100), nullable='none')
    # add the data

    def __init__(self, cid, name, pic='none', allfirst='none'):
        self.name = name
        self.cid = cid
        self.pic = pic
        self.allfirst = allfirst
    def add_artist(self):
        db.session.add(self)
        db.session.commit()
    def update_artist(self):
        db.session.commit()
    @classmethod
    def check_data(cls,cid):
        data = Artist.query.filter_by(cid=cid).first()
        # print(data.cid,data.name,data.pic)
        return data


class Song(db.Model):
    __tablename__ = 'song'
    pid = db.Column(db.Integer, primary_key=True)
    cid = db.Column(
        db.String(100),nullable=False)
    cname = db.Column(
        db.String(100))
    sid = db.Column(
        db.String(60), unique=True, nullable=False)
    sname = db.Column(
        db.String(100))
    aid = db.Column(
        db.String(80), nullable=False)
    aname = db.Column(
        db.String(100))
    pic = db.Column(
        db.String(200))
    def __init__(self, cid, cname, sid, sname,pic,aid='none', aname='none'):
        self.cid = cid
        self.cname = cname
        self.sid = sid
        self.sname = sname
        self.aid = aid
        self.aname = aname
        self.pic = pic
    def add_song(self):
        db.session.add(self)
        db.session.commit()
    def update_song(self):
        db.session.commit()
    @classmethod
    def get_data(cls,sname,cname=None):
        sname=sname.lower()
        if cname ==None:
            data=Song.query.filter(func.lower(Song.sname)==sname).first()
        else:
            data=Song.query.filter(and_(Song.sname.ilike(sname+'%'),Song.cname.ilike(cname+'%'))).first()
        if data ==None:
            return None
        print(data.sname)
        return data

    @classmethod
    def check_data(cls,sid):
        data =None
        data=Song.query.filter_by(sid=sid).first()
        return data

    @classmethod
    def get_singer_song(cls,cname):
        print(cname)
        data=None
        cid=Song.query.filter_by(cname=cname).first()
        if cid !=None:
            cid=cid.cid
            data=Song.query.filter_by(cid=cid).order_by(func.rand()).limit(25).all()    #test just return at most 25 songs
            print(cname,len(data))
        return data
    @classmethod
    def updatepic(cls,aid,piclink):
        session = sessionmaker(db.engine)
        db_session = session()
        affected_rows = db_session.query(Song).filter(Song.aid == aid).update({"pic":piclink})
        db_session.commit()
        # db.engine.commit()
        print('Affected rows:', affected_rows)
        # print("update ok")
    @classmethod
    def update_album(cls,sid,aname):
        session = sessionmaker(db.engine)
        db_session = session()
        db_session.query(Song).filter(Song.sid == sid).update({"aname":aname})
        db_session.commit()
        print("update the album!")
        
        
class Opinion(db.Model):
    __tablename__ = 'opinion'
    id = db.Column(db.Integer, primary_key=True)
    songname = db.Column(db.String(50))
    opnum = db.Column(db.Integer)
    feeling = db.Column(db.String(50))
    date = db.Column(db.DateTime)
    # add the data

    def __init__(self,songname,opnum,feeling):
        self.songname = songname
        self.opnum = opnum
        self.feeling = feeling
    def add_opinion(self):
        db.session.add(self)
        db.session.commit()     
    @classmethod
    def get_data(cls,d):
        data=Opinion.query.all()
        return data

