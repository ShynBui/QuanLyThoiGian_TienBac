from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship, backref
from saleapp import db, app
from datetime import datetime
from enum import Enum as UserEnum
from flask_login import UserMixin
import hashlib
from saleapp.encoding import  encoding_no1
from saleapp.decoding import decoding_no1
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
    image = Column(Text)
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
    isRecoment = Column(Boolean, default=False)

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
        nhom6 = NhomChiTieu(name="Khoản thu", isGain=True)

        db.session.add_all([nhom1,nhom2,nhom3,nhom5, nhom6])
        db.session.commit()

        #Loai chi tieu
        #nhom2
        loai1 = LoaiChiTieu(name="Sửa nhà", idnhomchitieu=nhom2.id, image="https://xaynhangaviet.com/wp-content/uploads/2022/09/icon-sua-nha.png")
        loai2 = LoaiChiTieu(name="Bảo dưỡng xe", idnhomchitieu=nhom2.id, image="https://media.istockphoto.com/id/1215271982/vi/vec-to/bi%E1%BB%83u-t%C6%B0%E1%BB%A3ng-b%E1%BA%A3o-d%C6%B0%E1%BB%A1ng-xe-h%C6%A1i.jpg?s=1024x1024&w=is&k=20&c=LnAN5rqTkFQlJ_Mslj_f-Hpzjj5rTrG3gPl45upV0K8=")
        loai3 = LoaiChiTieu(name="Khám sức khỏe", idnhomchitieu=nhom2.id, image="https://vieclam123.vn/ckfinder/userfiles/images/images/mot-so-luu-y-khi-kham-suc-khoe-tai-vien-198.jpg")
        loai4 = LoaiChiTieu(name="Bảo hiểm", idnhomchitieu=nhom2.id, image="https://banner2.cleanpng.com/20180411/euw/kisspng-health-insurance-health-care-whole-5ace87e407a9a8.7638984515234846440314.jpg")
        loai5 = LoaiChiTieu(name="Giáo dục", idnhomchitieu=nhom2.id, image="https://www.shutterstock.com/image-vector/graduation-icon-260nw-696419326.jpg")
        loai6 = LoaiChiTieu(name="Đồ gia dụng", idnhomchitieu=nhom2.id, image="https://chatuchak.vn/image/cache/catalog/new/icon-dung-cu-lam-bep-200x200.png")
        loai7 = LoaiChiTieu(name="Đồ dùng cá nhân", idnhomchitieu=nhom2.id, image="https://img.lovepik.com/element/40154/8917.png_860.png")
        loai8 = LoaiChiTieu(name="Vật nuôi", idnhomchitieu=nhom2.id, image="https://png.pngtree.com/template/20191108/ourlarge/pngtree-love-cute-dog-pets-logo-icon-image_327863.jpg")
        loai9 = LoaiChiTieu(name="Dịch vụ gia đình", idnhomchitieu=nhom2.id, image="https://med247.vn/wp-content/uploads/2022/03/icon_tham-kham-tai-nha.png")
        loai10 = LoaiChiTieu(name="Chi phí khác", idnhomchitieu=nhom2.id, image="https://www.tsg.net.vn/wp-content/uploads/2016/03/icon-chi-phi-750x460.png")

        db.session.add_all([loai1,loai2,loai3,loai4,loai5,loai6,loai7,loai8,loai9, loai10])
        db.session.commit()

        # Loai chi tieu
        # nhom1
        loai1 = LoaiChiTieu(name="Ăn uống", idnhomchitieu=nhom1.id, image="https://img.pikbest.com/png-images/qiantu/vector-icon-hand-drawn-cartoon-catering-icon_2688650.png!w700wp")
        loai2 = LoaiChiTieu(name="Thuê nhà", idnhomchitieu=nhom1.id, image="https://media.istockphoto.com/id/1130481222/vi/vec-to/bi%E1%BB%83u-t%C6%B0%E1%BB%A3ng-thu%C3%AA-nh%C3%A0-tr%C3%AAn-n%E1%BB%81n-tr%E1%BA%AFng.jpg?s=612x612&w=is&k=20&c=nGNhiEt3-HblTrUTVfHoqDIFSH35AQAOSeQMZQG-hMM=")
        loai3 = LoaiChiTieu(name="Hóa đơn nước", idnhomchitieu=nhom1.id, image="https://banner2.cleanpng.com/20180702/hcp/kisspng-telegram-logo-computer-icons-foreign-water-5b3a4b6de4bb03.3372467615305470539369.jpg")
        loai4 = LoaiChiTieu(name="Hóa đơn điện thoại", idnhomchitieu=nhom1.id, image="https://www.pngkit.com/png/detail/22-220966_phone-icon-png-red-icon-in-thoi-png.png")
        loai5 = LoaiChiTieu(name="Hóa đơn điện", idnhomchitieu=nhom1.id, image="https://illin.vn/upload/h%C3%B3a%20%C4%91%C6%A1n_-11-04-2019-12-24-05.png")
        loai6 = LoaiChiTieu(name="Hóa đơn gas", idnhomchitieu=nhom1.id, image="https://cdn-icons-png.flaticon.com/512/234/234793.png")
        loai7 = LoaiChiTieu(name="Hóa đơn TV", idnhomchitieu=nhom1.id, image="https://png.pngtree.com/png-clipart/20190516/original/pngtree-tv-icon-png-image_3568212.jpg")
        loai8 = LoaiChiTieu(name="Hóa đơn Internet", idnhomchitieu=nhom1.id, image="https://cdn-icons-png.flaticon.com/512/364/364089.png")
        loai9 = LoaiChiTieu(name="Hóa đơn khác", idnhomchitieu=nhom1.id, image="https://timviec365.vn/pictures/news/2019/09/04/czp1567559203.jpg")

        db.session.add_all([loai1, loai2, loai3, loai4, loai5, loai6, loai7, loai8, loai9])
        db.session.commit()


        # Loai chi tieu
        # nhom3
        loai1 = LoaiChiTieu(name="Thể dục thể thao", idnhomchitieu=nhom3.id, image="https://img.lovepik.com/original_origin_pic/18/07/04/56174f903b65b242d5ecf9f0f06dec82.png_wh860.png")
        loai2 = LoaiChiTieu(name="Làm đẹp", idnhomchitieu=nhom3.id, image="https://png.pngtree.com/png-vector/20201224/ourlarge/pngtree-beauty-skin-care-icon-vector-png-image_2589305.jpg")
        loai3 = LoaiChiTieu(name="Quà tặng và quyên góp", idnhomchitieu=nhom3.id, image="https://png.pngtree.com/png-vector/20201109/ourmid/pngtree-gift-box-icon-design-template-illustration-png-image_2413411.jpg")
        loai4 = LoaiChiTieu(name="Dịch vụ trực tuyến", idnhomchitieu=nhom3.id, image="https://media.istockphoto.com/id/1144489611/vi/vec-to/hotline-icon-vector-d%E1%BB%AF-li%E1%BB%87u-nam-d%E1%BB%8Bch-v%E1%BB%A5-h%E1%BB%97-tr%E1%BB%A3-kh%C3%A1ch-h%C3%A0ng-h%E1%BB%93-s%C6%A1-avatar-v%E1%BB%9Bi-tai-nghe-v%C3%A0-%C4%91%E1%BB%93.jpg?s=1024x1024&w=is&k=20&c=DS-aaXhPY9osRxEOLw6IBTmvghkZGgTlfvdLeMTtEnU=")
        loai5 = LoaiChiTieu(name="Vui - chơi", idnhomchitieu=nhom3.id, image="https://banner2.cleanpng.com/20180421/req/kisspng-leisure-travel-computer-icons-hospitality-industry-leisure-and-entertainment-5adabec8272b98.6110896915242851281605.jpg")

        db.session.add_all([loai1, loai2, loai3, loai4, loai5])
        db.session.commit()

        # Loai chi tieu
        # nhom5 Nợ
        loai1 = LoaiChiTieu(name="Trả nợ", idnhomchitieu=nhom5.id, image="https://banner2.cleanpng.com/20180806/zjc/kisspng-debt-clip-art-money-computer-icons-investment-5b6918af1ae205.0498421215336142551101.jpg")
        loai2 = LoaiChiTieu(name="Trả lãi", idnhomchitieu=nhom5.id, image="https://timo.vn/wp-content/uploads/lai-suat-ngan-hang.png")

        db.session.add_all([loai1, loai2])
        db.session.commit()

        # Loai chi tieu
        # nhom6 Nợ
        loai1 = LoaiChiTieu(name="Lương", idnhomchitieu=nhom6.id, image="https://gp1.wac.edgecastcdn.net/802892/http_public_production/artists/images/6781721/original/resize:248x186/crop:x0y80w640h480/hash:1578983472/loan-icon-png_239807.jpg?1578983472")
        loai2 = LoaiChiTieu(name="Thu nhập khác", idnhomchitieu=nhom6.id, image="https://cdn.scb.com.vn/picture/icon_tien_gui_tiet_kiem_phat_loc_tai_1_.jpg")

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