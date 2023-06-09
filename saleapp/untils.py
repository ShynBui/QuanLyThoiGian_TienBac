from saleapp.models import User, UserRole, Room, Message, TaiKhoan, LoaiChiTieu, NhomChiTieu, TaiKhoanChiTieu, KhoanChiTieu
from flask_login import current_user
from sqlalchemy import func, and_, desc, or_
from saleapp import app, db, summarizer
import json
from datetime import datetime, timedelta
import hashlib
from sqlalchemy.sql import extract
from saleapp.encoding import encoding_no1



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
    taiKhoan = TaiKhoan()
    # print(taiKhoan)
    db.session.add_all([taiKhoan])
    db.session.commit()
    # print(diachi)
    # print(queQuan)
    user = User(name=name.strip(), username=username, password=password, email=kwargs.get('email'),diachi=diachi, queQuan=queQuan,
                 dob=kwargs.get('dob'), sdt=kwargs.get('phone'), idtaikhoan = taiKhoan.id)
    user.name = encoding_no1(user.name)
    user.email = encoding_no1(user.email)
    db.session.add_all([user])

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

    # print(id_room)
    return id_room.first()


def get_chatroom_by_room_id(id):
    id_room = Message.query.filter(Message.room_id.__eq__(id))

    # print(id_room.first())
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
    # room = Room.query.filter(Room.is_reply.__eq__(False)) \
    #     .order_by(Room.date.desc())

    room = Room.query.all()

    return room


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

def get_all_tien_tuan_truoc_va_tuan_nay(idtaikhoan):
    khoanchitieutuannay = KhoanChiTieu.query.filter(extract('week', KhoanChiTieu.ngayChiTieu) == datetime.now().isocalendar()[1]).all()
    khoanchitieutuantruoc = KhoanChiTieu.query.filter(extract('week', KhoanChiTieu.ngayChiTieu) == datetime.now().isocalendar()[1] - 1).all()

    taikhoanchitieutuannay = []
    taikhoanchitieutuantruoc = []

    for i in khoanchitieutuannay:
        taikhoanchitieutuannay.append(TaiKhoanChiTieu.query.filter(i.id == TaiKhoanChiTieu.idkhoanchitieu,
                                                                   TaiKhoanChiTieu.isRecoment.__eq__(False)).first())

    for i in khoanchitieutuantruoc:
        taikhoanchitieutuantruoc.append(TaiKhoanChiTieu.query.filter(i.id == TaiKhoanChiTieu.idkhoanchitieu,
                                                                   TaiKhoanChiTieu.isRecoment.__eq__(False)).first())

    tongtienchituannay = 0
    tongtienchituantruoc = 0

    for i in taikhoanchitieutuannay:
        tongtienchituannay = tongtienchituannay + i.tienChi

    for i in taikhoanchitieutuantruoc:
        tongtienchituantruoc = tongtienchituantruoc + i.tienChi

    # print("a:", tongtienchituantruoc, "b:", tongtienchituannay)

    return [tongtienchituantruoc, tongtienchituannay]


def get_all_tien_thang_truoc_va_thang_nay(idtaikhoan):
    khoanchitieutuannay = KhoanChiTieu.query.filter(
        extract('month', KhoanChiTieu.ngayChiTieu) == datetime.now().month).all()
    khoanchitieutuantruoc = KhoanChiTieu.query.filter(
        extract('month', KhoanChiTieu.ngayChiTieu) == datetime.now().month - 1).all()

    taikhoanchitieutuannay = []
    taikhoanchitieutuantruoc = []

    for i in khoanchitieutuannay:
        taikhoanchitieutuannay.append(TaiKhoanChiTieu.query.filter(i.id == TaiKhoanChiTieu.idkhoanchitieu,
                                                                   TaiKhoanChiTieu.isRecoment.__eq__(False)).first())

    for i in khoanchitieutuantruoc:
        taikhoanchitieutuantruoc.append(TaiKhoanChiTieu.query.filter(i.id == TaiKhoanChiTieu.idkhoanchitieu,
                                                                   TaiKhoanChiTieu.isRecoment.__eq__(False)).first())

    tongtienchituannay = 0
    tongtienchituantruoc = 0

    for i in taikhoanchitieutuannay:
        tongtienchituannay = tongtienchituannay + i.tienChi

    for i in taikhoanchitieutuantruoc:
        tongtienchituantruoc = tongtienchituantruoc + i.tienChi

    # print("a:", tongtienchituantruoc, "b:", tongtienchituannay)

    return [tongtienchituantruoc, tongtienchituannay]

def get_top_loai_chi_tieu(idUser):
    taikhoanchitieu = TaiKhoanChiTieu.query.filter(TaiKhoanChiTieu.idtaikhoan == idUser,
                                                                   TaiKhoanChiTieu.isRecoment.__eq__(False)).all()

    my_list = [x.idkhoanchitieu for x in taikhoanchitieu]

    # khoanchiteu = KhoanChiTieu.query.filter(KhoanChiTieu.id.in_(my_list)).all()

    loaichitieu = db.session.query(KhoanChiTieu.idLoaiChiTieu, db.func.count(KhoanChiTieu.id).label('soluong'))\
                    .filter(KhoanChiTieu.id.in_(my_list))\
                    .group_by(KhoanChiTieu.idLoaiChiTieu)\
                    .limit(5)

    # print(loaichitieu.all())

    return loaichitieu.all()


def get_ten_loai_theo_id_loai(idLoai):

    loai = LoaiChiTieu.query.filter(LoaiChiTieu.id == idLoai)

    return loai.first()


def get_tong_tien_theo_id_loai(idLoai):

    id = KhoanChiTieu.query.filter(KhoanChiTieu.idLoaiChiTieu == idLoai).all()

    list_id = []

    for i in id:
        list_id.append(i.id)

    taikhoanchitieu = TaiKhoanChiTieu.query.filter(TaiKhoanChiTieu.idkhoanchitieu.in_(list_id),
                                                                   TaiKhoanChiTieu.isRecoment.__eq__(False)).all()

    sotien = 0

    for i in taikhoanchitieu:
        sotien = sotien + i.tienChi

    return sotien

def sort_ten_tongtien(ten, tongtien):

    for i in range(len(tongtien)):
        for j in range(i + 1, len(tongtien)):
            if tongtien[j] > tongtien[i]:
                temp = tongtien[i]
                tongtien[i] = tongtien[j]
                tongtien[j] = temp
                temp = ten[i]
                ten[i] = ten[j]
                ten[j] = temp

    return [ten, tongtien]

def get_tien_by_idkhoanchitieu(id):

    return TaiKhoanChiTieu.query.filter(TaiKhoanChiTieu.idkhoanchitieu == id,
                                                                   TaiKhoanChiTieu.isRecoment.__eq__(False)).first().tienChi
def get_top_chi_tieu_gan_day(user_id):

    chitieu = TaiKhoanChiTieu.query.filter(TaiKhoanChiTieu.idtaikhoan == user_id,
                                                                   TaiKhoanChiTieu.isRecoment.__eq__(False)).all()

    id_chitieu = []

    for i in chitieu:
        id_chitieu.append(i.idkhoanchitieu)

    # print(id_chitieu)

    chitieuganday = KhoanChiTieu.query.filter(KhoanChiTieu.id.in_(id_chitieu))\
                    .order_by(KhoanChiTieu.ngayChiTieu.desc()).limit(5).all()

    ten = []
    time = []
    tien = []


    for i in chitieuganday:
        ten.append(i.name)
        time.append(i.ngayChiTieu)
        tien.append(get_tien_by_idkhoanchitieu(i.id))

    # print(ten)


    return [ten, time, tien]

def get_ten_chi_tieu_va_tien(idTaiKhoan):

    today = datetime.now() - timedelta(days=1)
    nextday = today + timedelta(days=1)
    taikhoanchitieu = TaiKhoanChiTieu.query.filter(TaiKhoanChiTieu.idtaikhoan == idTaiKhoan,
                                                                   TaiKhoanChiTieu.isRecoment.__eq__(False))

    list_tien = []
    list_ten = []


    for i in taikhoanchitieu:
        ten = KhoanChiTieu.query\
            .filter(KhoanChiTieu.id == i.idkhoanchitieu, KhoanChiTieu.ngayChiTieu.between(today, nextday)).first()
        if ten:
            list_ten.append(ten.name)
            list_tien.append(i.tienChi)

    # print(list_ten, list_tien)

    return [list_ten, list_tien]


def add_tien(idTaiKhoan, tien):
    taikhoan = TaiKhoan.query.filter(TaiKhoan.id == idTaiKhoan).first()


    taikhoan.soTien = taikhoan.soTien + tien
    db.session.commit()

    return True

def get_all_nhom_va_loai_chi_tieu():

    nhom = db.session.query(LoaiChiTieu.name.label('tenloai'), LoaiChiTieu.image, NhomChiTieu.name.label('tennhom'))\
            .join(LoaiChiTieu, NhomChiTieu.id == LoaiChiTieu.idnhomchitieu)\
            .order_by(NhomChiTieu.id).all()

    print(nhom)

    return nhom

def get_loai_chi_tieu_theo_nhom_id(nhomid):

    loaichitieu = LoaiChiTieu.query.filter(LoaiChiTieu.idnhomchitieu == nhomid).all()

    return loaichitieu

def get_all_loai():
    loai = LoaiChiTieu.query.all()

    return loai

def change_info(user_id, sdt, diachi):
    user = get_user_by_id(user_id)

    user.sdt = sdt
    user.diachi = diachi

    db.session.commit()

    return 1;

def summary(text):
    return summarizer(text, max_length=200, min_length=20, do_sample=False)[0]['summary_text']