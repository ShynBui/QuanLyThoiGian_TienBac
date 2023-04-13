from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship, backref
from saleapp import db, app
from datetime import datetime
from enum import Enum as UserEnum
from flask_login import UserMixin
import hashlib

class BaseModel(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)


class UserRole(UserEnum):
    USER = 1
    SYSADMIN = 2
    ADMIN = 3

class User(BaseModel, UserMixin):
    __tablename__ = 'user'
    __table_args__ = {'extend_existing': True}
    name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    avatar = Column(Text, default='https://antimatter.vn/wp-content/uploads/2022/11/anh-avatar-trang-fb-mac-dinh.jpg')
    email = Column(String(50))
    dob = Column(DateTime, nullable=False)
    is_active = Column(Boolean, default=True)
    joined_date = Column(DateTime, default=datetime.now())
    diachi = Column(String(100), nullable=False)
    userRole = Column(Enum(UserRole), default=UserRole.USER)
    sdt = Column(String(50), default="123456789")
    queQuan = Column(String(50), default="TP.HCM")
    sex = Column(Boolean, default=True)
    facebook = Column(String(255), default="https://www.facebook.com/phat.buitien.54")
    idtaikhoan = Column(Integer)

    message = relationship('Message', backref='user', lazy=True)
    userevent = relationship('UserEvent', backref='user', lazy=True)


    def __str__(self):
        return self.name

class Room(db.Model):
    __tablename__ = 'room'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    is_reply = Column(Boolean, default=True)
    date = Column(DateTime, default=datetime.now())
    message = relationship('Message', backref='room', lazy=True)

    def __str__(self):
        return self.name

class Message(db.Model):
    __tablename__ = 'message'

    id = id = Column(Integer, primary_key=True, autoincrement=True)
    room_id = Column(Integer, ForeignKey(Room.id), nullable=False, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False, primary_key=True)

    content = Column(String(255), default= '')
    date = Column(DateTime, default= datetime.now())

    def __str__(self):
        return self.content

class Priority(db.Model):
    __tablename__ = 'priority'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    mucDo = Column(Integer)
    task = relationship('Task', backref='priority', lazy=True)

    def __str__(self):
        return self.name

class Loai(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)

    def __str__(self):
        return self.name

#->>>>>>>>>>>>>>>>>>>>>>
class Event(Loai):
    __tablename__ = 'event'

    noiToChuc = Column(String(255), nullable=False)
    host = Column(Integer, nullable=False)
    userevent = relationship('UserEvent', backref='event', lazy=True)
    task = relationship('Task', backref='event', lazy=True)

    def __str__(self):
        return self.host

class LoiNhac(Loai):
    __tablename__ = 'loinhac'

    isLoop = Column(Boolean, default=True)
    hour = Column(Integer, nullable=False)

    def __str__(self):
        return self.id
class UserEvent(db.Model):
    __tablename__ = 'userevent'

    idEvent = Column(Integer, ForeignKey(Event.id), nullable=False, primary_key=True)
    idUser = Column(Integer, ForeignKey(User.id), nullable=False, primary_key=True)
    isJoin = Column(Boolean, default=False)

    def __str__(self):
        return self.idEvent

class Task(db.Model):
    __tablename__ = 'task'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    startAt = Column(DateTime, nullable=False)
    deadline = Column(DateTime, nullable=False)
    finish = Column(Boolean, default=False)
    idPriority = Column(Integer, ForeignKey(Priority.id), nullable=False, primary_key=True)
    idEvent = Column(Integer, ForeignKey(Event.id), nullable=False, primary_key=True)
    idUser = Column(Integer, ForeignKey(User.id), nullable=False, primary_key=True)

    def __str__(self):
        return self.name

class TaiKhoan(db.Model):
    __tablename__ = 'taikhoan'

    id = Column(Integer, primary_key=True, autoincrement=True)
    soTien = Column(Float, default=0)
    taikhoanchitieu = relationship('TaiKhoanChiTieu', backref='taikhoan', lazy=True)

    def __str__(self):
        return self.id

class NhomChiTieu(db.Model):
    __tablename__ = 'nhomchitieu'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    isGain = Column(Boolean, default=False)
    loaichitieu = relationship('LoaiChiTieu', backref='nhomchitieu', lazy=True)

    def __str__(self):
        return self.name

class LoaiChiTieu(db.Model):
    __tablename__ = 'loaichitieu'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    idnhomchitieu = Column(Integer, ForeignKey(NhomChiTieu.id), nullable=False, primary_key=True)
    khoanchitieu = relationship('KhoanChiTieu', backref='loaichitieu', lazy=True)
    def __str__(self):
        return self.name

class KhoanChiTieu(db.Model):
    __tablename__ = 'khoanchitieu'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    ngayChiTieu = Column(DateTime, default=datetime.now())
    idLoaiChiTieu = Column(Integer, ForeignKey(LoaiChiTieu.id), nullable=False, primary_key=True)
    taikhoanchitieu = relationship('TaiKhoanChiTieu', backref='khoanchitieu', lazy=True)

    def __str__(self):
        return self.name

class TaiKhoanChiTieu(db.Model):
    __tablename__ = 'taikhoanchitieu'

    idkhoanchitieu = Column(Integer, ForeignKey(KhoanChiTieu.id), nullable=False, primary_key=True)
    idtaikhoan = Column(Integer, ForeignKey(TaiKhoan.id), nullable=False, primary_key=True)
    tienChi = Column(Float)

    def __str__(self):
        return self.idkhoanchitieu



if __name__ == '__main__':
    with app.app_context():


        db.drop_all()
        db.create_all()
        db.session.commit()
        password = str(hashlib.md5('1'.encode('utf-8')).hexdigest())

        room = Room(name='ccv', is_reply=False, date=datetime.now())
        db.session.add_all([room])
        db.session.commit()
        taiKhoan = TaiKhoan()
        db.session.add_all([taiKhoan])
        db.session.commit()
        user = User(name="Bui Tien Hoang", username="u1",
                         password=password, avatar='https://scontent.fsgn2-5.fna.fbcdn.net/v/t1.6435-9/191455455_1236939360069997_5418463114445577817_n.jpg?_nc_cat=106&ccb=1-7&_nc_sid=8bfeb9&_nc_ohc=rcajabo0f74AX9qvH8y&_nc_ht=scontent.fsgn2-5.fna&oh=00_AfBoXfETYQ2MJIS8cYaTUQDAix3LXAwX2UK0Vz-P8P1M1w&oe=645FD60B',
                         email="20512052047hoang@ou.edu.vn", joined_date=datetime.now(),
                         diachi="Gò Vấp", queQuan='Dong Lak', facebook='https://www.facebook.com/d8.ndh',
                         dob=datetime.strptime("22-06-1990", '%d-%m-%Y').date(), sex=0, userRole=UserRole.SYSADMIN, idtaikhoan=taiKhoan.id)
        db.session.add_all([user])
        db.session.commit()
        message = Message(room_id=room.id, user_id=user.id, content='', date=datetime.now())
        db.session.add_all([message])
        db.session.commit()
        db.session.commit()
