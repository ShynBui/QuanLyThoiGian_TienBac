from saleapp.models import User, UserRole, Room, Message, TaiKhoan, LoaiChiTieu, NhomChiTieu, TaiKhoanChiTieu, KhoanChiTieu
from flask_login import current_user
from sqlalchemy import func, and_, desc, or_
from saleapp import app, db
import json
from datetime import datetime
import hashlib
from sqlalchemy.sql import extract



def get_id_by_username(username):
    id = User.query.filter(User.username.__eq__(username))

    return id.first()


def add_user(name, username, password, diachi, queQuan, **kwargs):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    # print(kwargs.get('dob'))
    maSo1 = kwargs.get('email').split('@')[0]
    # maso = ''
    # for i in maSo1:
    #     if i.isnumeric():
    #         maso = maso + i
    #
    # print(maso)

    db.session.commit()
    taiKhoan3 = TaiKhoan()
    print(taiKhoan3.id)
    db.session.add_all([taiKhoan3])
    db.session.commit()
    print(diachi)
    print(queQuan)
    user = User(name=name.strip(), username=username, password=password, email=kwargs.get('email'),diachi=diachi, queQuan=queQuan,
                 avatar=kwargs.get('avatar'), userRole=UserRole.USER,
                dob=kwargs.get('dob'), idTaiKhoan=taiKhoan3.id)
    # user2 = User(name="Bui Tien Hoang", username="u1",
    #             password=password,
    #             avatar='https://scontent.fsgn2-5.fna.fbcdn.net/v/t1.6435-9/191455455_1236939360069997_5418463114445577817_n.jpg?_nc_cat=106&ccb=1-7&_nc_sid=8bfeb9&_nc_ohc=rcajabo0f74AX9qvH8y&_nc_ht=scontent.fsgn2-5.fna&oh=00_AfBoXfETYQ2MJIS8cYaTUQDAix3LXAwX2UK0Vz-P8P1M1w&oe=645FD60B',
    #             email="20512052047hoang@ou.edu.vn", joined_date=datetime.now(),
    #             diachi="Gò Vấp", queQuan='Dong Lak', facebook='https://www.facebook.com/d8.ndh',
    #             dob=datetime.strptime("22-06-1990", '%d-%m-%Y').date(), sex=0, userRole=UserRole.SYSADMIN,
    #             idtaikhoan=taiKhoan3.id)
    # print(user2)


    db.session.add(user)
    db.session.commit()

    room = Room(name="Room của " + name.strip())

    db.session.add(room)

    db.session.commit()

    message = Message(room_id=room.id, user_id=user.id)

    db.session.add(message)

    db.session.commit()


def save_chat_message(room_id, message, user_id):
    message = Message(content=message, room_id=room_id, user_id=user_id)

    db.session.add(message)

    db.session.commit()


def load_message(room_id):
    message = Message.query.filter(Message.room_id.__eq__(room_id))

    return message.all()


def load_user_send(room_id):
    message = Message.query.filter(Message.room_id.__eq__(room_id))

    return message.all()


def get_chatroom_by_user_id(id):
    id_room = Message.query.filter(Message.user_id.__eq__(id))

    print(id_room)
    return id_room.first()


def get_chatroom_by_room_id(id):
    id_room = Message.query.filter(Message.room_id.__eq__(id))

    print(id_room.first())
    return id_room.first()


def get_chat_room_by_user_id(id):
    message = Message.query.filter(Message.user_id == id).first()

    room = Room.query.filter(Room.id == message.room_id)

    return room.first()


def change_room_status(id, change):
    id_room = Room.query.filter(Room.id.__eq__(id)).first()

    id_room.is_reply = change

    db.session.commit()


def check_login(username, password, role=UserRole.USER):
    if username and password:
        password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

        return User.query.filter(User.username.__eq__(username),
                                 User.password.__eq__(password),
                                 User.userRole.__eq__(role)).first()


def check_admin_login(username, password):
    if username and password:
        password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

        return User.query.filter(User.username.__eq__(username),
                                 User.password.__eq__(password),
                                 User.userRole != UserRole.USER).first()


def get_unreply_room():
    room = Room.query.filter(Room.is_reply.__eq__(False)) \
        .order_by(Room.date.desc())

    return room.all()


def get_user_by_id(user_id):
    return User.query.get(user_id)


def get_host_room_avatar(room_id):
    user = Message.query.filter(Message.room_id.__eq__(room_id),
                                Message.content.__eq__('')).first()

    username = get_user_by_id(user.user_id);

    return username.avatar


def get_chatroom_by_id(id):
    id_room = Room.query.filter(Room.id.__eq__(id))
    # id_room[0]

    return id_room.first();


def get_tai_khoan_tai_chinh(id_taikhoan):
    taichinh = TaiKhoan.query.filter(TaiKhoan.id.__eq__(id_taikhoan))

    return taichinh.first()

def get_all_nhom():
    loai = NhomChiTieu.query.all()

    return loai

def get_all_loai_theo_nhom(id_nhom):
    loai = LoaiChiTieu.query.filter(LoaiChiTieu.idnhomchitieu == id_nhom)

    return loai.all()

def add_giao_dich(idtaikhoan, idloaichitieu, sotien, idnhomchitieu, note, ngay, name):

    khoanchitieu = KhoanChiTieu(name=name, ngayChiTieu=ngay, idLoaiChiTieu=idloaichitieu)
    db.session.add(khoanchitieu)
    db.session.commit()

    taikhoanchitieu = TaiKhoanChiTieu(idkhoanchitieu=khoanchitieu.id, idtaikhoan=idtaikhoan, tienChi=sotien,
                                      note=note)

    db.session.add(taikhoanchitieu)
    db.session.commit()

    #trừ tiền
    nhomchitieu = NhomChiTieu.query.filter(NhomChiTieu.id == idnhomchitieu).first()
    taikhoan = TaiKhoan.query.filter(TaiKhoan.id == idtaikhoan).first()

    if(nhomchitieu.isGain == True):
        taikhoan.soTien = taikhoan.soTien + sotien
        db.session.commit()
    else:
        taikhoan.soTien = taikhoan.soTien - sotien
        db.session.commit()

    db.session.commit()

