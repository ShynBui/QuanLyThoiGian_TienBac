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
    note = Column(Text)

    def __str__(self):
        return self.idkhoanchitieu



if __name__ == '__main__':
    with app.app_context():


        db.drop_all()
        db.create_all()
        db.session.commit()
        password = str(hashlib.md5('1'.encode('utf-8')).hexdigest())

        #Nhom chi tieu
        nhom1 = NhomChiTieu(name="Chi tiêu hàng tháng",isGain=False)
        nhom2 = NhomChiTieu(name="Chi tiêu cần thiết", isGain=False)
        nhom3 = NhomChiTieu(name="Vui chơi giải trí", isGain=False)
        nhom5 = NhomChiTieu(name="Nợ", isGain=False)
        nhom6 = NhomChiTieu(name="Khoản thu", isGain=False)

        db.session.add_all([nhom1,nhom2,nhom3,nhom5, nhom6])
        db.session.commit()

        #Loai chi tieu
        #nhom2
        loai1 = LoaiChiTieu(name="Sửa nhà", idnhomchitieu=nhom2.id)
        loai2 = LoaiChiTieu(name="Bảo dưỡng xe", idnhomchitieu=nhom2.id)
        loai3 = LoaiChiTieu(name="Khám sức khỏe", idnhomchitieu=nhom2.id)
        loai4 = LoaiChiTieu(name="Bảo hiểm", idnhomchitieu=nhom2.id)
        loai5 = LoaiChiTieu(name="Giáo dục", idnhomchitieu=nhom2.id)
        loai6 = LoaiChiTieu(name="Đồ gia dụng", idnhomchitieu=nhom2.id)
        loai7 = LoaiChiTieu(name="Đồ dùng cá nhân", idnhomchitieu=nhom2.id)
        loai8 = LoaiChiTieu(name="Vật nuôi", idnhomchitieu=nhom2.id)
        loai9 = LoaiChiTieu(name="Dịch vụ gia đình", idnhomchitieu=nhom2.id)
        loai10 = LoaiChiTieu(name="Chi phí khác", idnhomchitieu=nhom2.id)

        db.session.add_all([loai1,loai2,loai3,loai4,loai5,loai6,loai7,loai8,loai9, loai10])
        db.session.commit()

        # Loai chi tieu
        # nhom1
        loai1 = LoaiChiTieu(name="Ăn uống", idnhomchitieu=nhom1.id)
        loai2 = LoaiChiTieu(name="Thuê nhà", idnhomchitieu=nhom1.id)
        loai3 = LoaiChiTieu(name="Hóa đơn nước", idnhomchitieu=nhom1.id)
        loai4 = LoaiChiTieu(name="Hóa đơn điện thoại", idnhomchitieu=nhom1.id)
        loai5 = LoaiChiTieu(name="Hóa đơn điện", idnhomchitieu=nhom1.id)
        loai6 = LoaiChiTieu(name="Hóa đơn gas", idnhomchitieu=nhom1.id)
        loai7 = LoaiChiTieu(name="Hóa đơn TV", idnhomchitieu=nhom1.id)
        loai8 = LoaiChiTieu(name="Hóa đơn Internet", idnhomchitieu=nhom1.id)
        loai9 = LoaiChiTieu(name="Hóa đơn khác", idnhomchitieu=nhom1.id)

        db.session.add_all([loai1, loai2, loai3, loai4, loai5, loai6, loai7, loai8, loai9])
        db.session.commit()


        # Loai chi tieu
        # nhom3
        loai1 = LoaiChiTieu(name="Thể dục thể thao", idnhomchitieu=nhom3.id)
        loai2 = LoaiChiTieu(name="Làm đẹp", idnhomchitieu=nhom3.id)
        loai3 = LoaiChiTieu(name="Quà tặng và quyên góp", idnhomchitieu=nhom3.id)
        loai4 = LoaiChiTieu(name="Dịch vụ trực tuyến", idnhomchitieu=nhom3.id)
        loai5 = LoaiChiTieu(name="Vui - chơi", idnhomchitieu=nhom3.id)

        db.session.add_all([loai1, loai2, loai3, loai4, loai5])
        db.session.commit()

        # Loai chi tieu
        # nhom5 Nợ
        loai1 = LoaiChiTieu(name="Trả nợ", idnhomchitieu=nhom5.id)
        loai2 = LoaiChiTieu(name="Trả lãi", idnhomchitieu=nhom5.id)

        db.session.add_all([loai1, loai2])
        db.session.commit()

        # Loai chi tieu
        # nhom6 Nợ
        loai1 = LoaiChiTieu(name="Lương", idnhomchitieu=nhom6.id)
        loai2 = LoaiChiTieu(name="Thu nhập khác", idnhomchitieu=nhom6.id)

        db.session.add_all([loai1, loai2])
        db.session.commit()


        #admin
        #tk: u1
        #mk: 1
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

        # user
        # tk: u2
        # mk: 1
        room2 = Room(name='ccv', is_reply=False, date=datetime.now())
        db.session.add_all([room2])
        db.session.commit()
        taiKhoan2 = TaiKhoan()
        db.session.add_all([taiKhoan2])
        db.session.commit()
        user2 = User(name="Bui Tien Thanh", username="u2",
                    password=password,
                    avatar='https://scontent.fsgn2-5.fna.fbcdn.net/v/t39.30808-6/275665854_949509355934005_7586877570851118227_n.jpg?_nc_cat=106&ccb=1-7&_nc_sid=09cbfe&_nc_ohc=o_zqYzGKu58AX-dndCH&_nc_ht=scontent.fsgn2-5.fna&oh=00_AfCpQf0QSxLtDvv6zCRY63_QLvXyVAmMx15h56a-fFGT9w&oe=643DD79A',
                    email="20512052047hoang@ou.edu.vn", joined_date=datetime.now(),
                    diachi="Gò Vấp", queQuan='Dong Lak', facebook='https://www.facebook.com/d8.ndh',
                    dob=datetime.strptime("22-06-1990", '%d-%m-%Y').date(), sex=0, userRole=UserRole.USER,
                    idtaikhoan=taiKhoan2.id)
        db.session.add_all([user2])
        db.session.commit()
        message2 = Message(room_id=room2.id, user_id=user2.id, content='', date=datetime.now())
        db.session.add_all([message2])
        db.session.commit()


        db.session.commit()
