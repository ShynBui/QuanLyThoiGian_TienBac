import math
from flask import render_template, request, redirect, session, jsonify, url_for
from saleapp import app, admin, login, untils, socketio
from saleapp.models import UserRole
from flask_login import login_user, logout_user, login_required, current_user
import cloudinary.uploader
from flask_socketio import SocketIO, emit, join_room
import requests
import openpyxl
from saleapp.decoding import decoding_no1
from datetime import datetime, date
from saleapp.time import *

from saleapp.time import *
import feedparser

@app.route("/")
def home():
    return render_template('index.html')

# socket
@app.route("/chatroom")
def chat_room():
    if current_user.is_authenticated:
        pass
    else:
        return redirect(url_for('user_signin'))

    user_name = (current_user.name)
    room = untils.get_chatroom_by_user_id(id=current_user.id)
    list_user = untils.load_message(room.room_id)

    # print(room.room_id)

    user_send = [decoding_no1(untils.get_user_by_id(x.user_id).name) for x in list_user]

    user_image = [untils.get_user_by_id(x.user_id).avatar for x in list_user]

    user_id = [x.user_id for x in list_user]

    host_avatar = untils.get_host_room_avatar(room.room_id);

    user_send.pop(0)
    user_image.pop(0)
    user_id.pop(0)

    # print(user_send)

    if user_name and room:

        # print(untils.load_message(room.room_id)[0].content)

        return render_template('chatroom.html', user_name=decoding_no1(user_name), room=room.room_id, name=current_user.name,
                               message=list_user, room_id=int(room.room_id),
                               user_send=user_send, n=len(user_send), user_image=user_image, user_id=user_id,
                               room_name=untils.get_chatroom_by_id(room.room_id),
                               host_avatar=host_avatar);
    else:
        return redirect(url_for('home'))


@app.route("/admin/chatadmin/<int:room_id>")
def chat_room_admin(room_id):
    if current_user.userRole == UserRole.SYSADMIN or current_user.userRole == UserRole.ADMIN:
        # print(room_id)
        user_name = decoding_no1(current_user.name)
        room = untils.get_chatroom_by_room_id(id=room_id)
        list_user = untils.load_message(room.room_id)

        user_send = [decoding_no1(untils.get_user_by_id(x.user_id).name) for x in list_user]

        user_image = [untils.get_user_by_id(x.user_id).avatar for x in list_user]

        user_id = [x.user_id for x in list_user]

        user_send.pop(0)
        user_image.pop(0)
        user_id.pop(0)

        host_avatar = untils.get_host_room_avatar(room.room_id);

        if user_name and room:
            return render_template('chatroom.html', user_name=(user_name), room=room.room_id, name=current_user.name,
                                   message=list_user, room_id=int(room.room_id),
                                   user_send=user_send, n=len(user_send), user_image=user_image, user_id=user_id,
                                   room_name=untils.get_chatroom_by_id(room.room_id),
                                   host_avatar=host_avatar);

    return redirect(url_for('home'));


@socketio.on('send_message')
def handle_send_message_event(data):
    app.logger.info("{} has sent message to the room {}: {}".format(data['username'],
                                                                    data['room'],
                                                                    data['message']))

    app.logger.info("{}".format(data['user_avatar']))
    socketio.emit('receive_message', data, room=data['room'])


@socketio.on('save_message')
def handle_save_message_event(data):
    # app.logger.info("2.all_mess: " + str(data['all_message']))
    app.logger.info("2.room_id: " + str(data['room']))

    untils.save_chat_message(room_id=int(data['room']), message=data['message'], user_id=current_user.id)

    if (current_user.userRole == UserRole.SYSADMIN or current_user.userRole == UserRole.ADMIN):
        untils.change_room_status(data['room'], 1)

    if (current_user.userRole == UserRole.USER):
        untils.change_room_status(data['room'], 0)


@socketio.on('join_room')
def handle_send_room_event(data):
    app.logger.info(data['username'] + " has sent message to the room " + data['room'] + ": ")
    join_room(data['room'])

    socketio.emit('join_room_announcement', data, room=data['room'])


@app.route('/register', methods=['get', 'post'])
def user_register():
    err_msg = ""
    if request.method == 'POST':
        name = request.form.get('firstname') + " " + request.form.get('lastname')
        password = request.form.get('password')
        email = request.form.get('email')
        username = email
        sex = request.form.get('sex')
        dob = request.form.get('dob')
        phone = request.form.get('phone')
        diachi = request.form.get('diachi')
        queQuan = request.form.get('hometown')

        confirm = request.form.get('confirm')
        avatar_path = None
        # user = User(name="Bui Tien Hoang", username="u1",
        #             password=password,
        #             avatar='https://scontent.fsgn2-5.fna.fbcdn.net/v/t1.6435-9/191455455_1236939360069997_5418463114445577817_n.jpg?_nc_cat=106&ccb=1-7&_nc_sid=8bfeb9&_nc_ohc=rcajabo0f74AX9qvH8y&_nc_ht=scontent.fsgn2-5.fna&oh=00_AfBoXfETYQ2MJIS8cYaTUQDAix3LXAwX2UK0Vz-P8P1M1w&oe=645FD60B',
        #             email="20512052047hoang@ou.edu.vn", joined_date=datetime.now(),
        #             diachi="Gò Vấp", queQuan='Dong Lak', facebook='https://www.facebook.com/d8.ndh',
        #             dob=datetime.strptime("22-06-1990", '%d-%m-%Y').date(), sex=0, userRole=UserRole.SYSADMIN,
        #             idtaikhoan=taiKhoan.id)
    try:
        if str(password) == str(confirm):
            avatar = request.files.get('avatar')
            if avatar:
                res = cloudinary.uploader.upload(avatar)
                avatar_path = res['secure_url']

            untils.add_user(name=name,
                            username=username,
                            password=password,
                            diachi=diachi,
                            queQuan=queQuan,
                            email=email,
                            avatar=avatar_path,
                            sex=sex,
                            dob=dob,
                            phone=phone)
            return redirect(url_for('user_signin'))
        else:
            err_msg = "Mat khau khong khop"
            # print(err_msg)
    except Exception as ex:
        pass
        # err_msg = 'He thong ban' + str(ex)
        # print(err_msg)

    return render_template('register.html', err_msg=err_msg)


@app.route('/user-login', methods=['get', 'post'])
def user_signin():
    err_msg = ""

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = untils.check_login(username=username, password=password)
        if user:
            login_user(user=user)
            next = request.args.get('next', 'home')
            return redirect(url_for(next))
        else:
            err_msg = "Sai tên đăng nhập hoặc mật khẩu"

    return render_template('login.html', err_msg=err_msg)


@app.route('/admin-login', methods=['post'])
def signin_admin():
    username = request.form.get('username')
    password = request.form.get('password')

    # user = untils.check_login(username=username, password=password, role=UserRole.ADMIN)
    user = untils.check_admin_login(username=username, password=password)
    if user:
        login_user(user=user)

    return redirect('/admin')


@app.route('/user-logout')
def user_signout():
    logout_user()
    return redirect(url_for('home'))


@login.user_loader
def user_load(user_id):
    return untils.get_user_by_id(user_id=user_id)

#Tài chính
@app.route('/taichinh')
def taichinh():

    topchitieu = untils.get_top_loai_chi_tieu(current_user.idtaikhoan)

    tenloai = []
    tongtien = []

    for i in topchitieu:
        tenloai.append(untils.get_ten_loai_theo_id_loai(i.idLoaiChiTieu).name)
        tongtien.append(untils.get_tong_tien_theo_id_loai(i.idLoaiChiTieu))


    data = untils.sort_ten_tongtien(tenloai, tongtien)
    ten = data[0]
    tien = data[1]

    #Chi tieu gan day

    chitieuganday = untils.get_top_chi_tieu_gan_day(current_user.idtaikhoan)

    ten2 = chitieuganday[0]
    time2 = chitieuganday[1]
    tien2 = chitieuganday[2]

    #Chi tieu hom nay

    datahomnay = untils.get_ten_chi_tieu_va_tien(current_user.idtaikhoan)
    tien3 = datahomnay[1]
    ten3 = datahomnay[0]

    sotien = untils.get_tai_khoan_tai_chinh(current_user.idtaikhoan).soTien
    return render_template('taichinh.html', sotien=str(sotien), topchitieu=topchitieu, tenloai=ten,
                           n=len(tenloai), tongtien=tien, chitieuganday=chitieuganday,
                           ten2=ten2, time2=time2, tien2=tien2, n2=len(ten2), ten3=ten3, tien3=tien3,
                           n3=len(ten3))

@app.route('/taichinhtuan', methods=['get', 'post'])
def taichinh_tuan():

    sotien = untils.get_tai_khoan_tai_chinh(current_user.idtaikhoan).soTien

    tientuannay = untils.get_all_tien_tuan_truoc_va_tuan_nay(current_user.idtaikhoan)

    topchitieu = untils.get_top_loai_chi_tieu(current_user.idtaikhoan)

    tenloai = []
    tongtien = []

    for i in topchitieu:
        tenloai.append(untils.get_ten_loai_theo_id_loai(i.idLoaiChiTieu).name)
        tongtien.append(untils.get_tong_tien_theo_id_loai(i.idLoaiChiTieu))


    data = untils.sort_ten_tongtien(tenloai, tongtien)
    ten = data[0]
    tien = data[1]

    #Chi tieu gan day

    chitieuganday = untils.get_top_chi_tieu_gan_day(current_user.idtaikhoan)

    ten2 = chitieuganday[0]
    time2 = chitieuganday[1]
    tien2 = chitieuganday[2]

    # Chi tieu hom nay

    datahomnay = untils.get_ten_chi_tieu_va_tien(current_user.idtaikhoan)
    tien3 = datahomnay[1]
    ten3 = datahomnay[0]

    return render_template('taichinh.html', sotien=str(sotien), tien= tientuannay,
                           ten=['Tuần trước', 'Tuần này'], topchitieu=topchitieu, tenloai=ten,
                           n=len(tenloai), tongtien=tien, chitieuganday=chitieuganday,
                           ten2=ten2, time2=time2, tien2=tien2, n2=len(ten2), ten3=ten3, tien3=tien3,
                           n3=len(ten3))

@app.route('/taichinhthang', methods=['get', 'post'])
def taichinh_thang():

    sotien = untils.get_tai_khoan_tai_chinh(current_user.idtaikhoan).soTien

    tientuannay = untils.get_all_tien_thang_truoc_va_thang_nay(current_user.idtaikhoan)

    topchitieu = untils.get_top_loai_chi_tieu(current_user.idtaikhoan)

    tenloai = []
    tongtien = []

    for i in topchitieu:
        tenloai.append(untils.get_ten_loai_theo_id_loai(i.idLoaiChiTieu).name)
        tongtien.append(untils.get_tong_tien_theo_id_loai(i.idLoaiChiTieu))


    data = untils.sort_ten_tongtien(tenloai, tongtien)
    ten = data[0]
    tien = data[1]

    #Chi tieu gan day

    chitieuganday = untils.get_top_chi_tieu_gan_day(current_user.idtaikhoan)

    ten2 = chitieuganday[0]
    time2 = chitieuganday[1]
    tien2 = chitieuganday[2]

    # Chi tieu hom nay

    datahomnay = untils.get_ten_chi_tieu_va_tien(current_user.idtaikhoan)
    tien3 = datahomnay[1]
    ten3 = datahomnay[0]

    return render_template('taichinh.html', sotien=str(sotien), tien= tientuannay,
                           ten=['Tháng trước', 'Tháng này'], topchitieu=topchitieu, tenloai=ten,
                           n=len(tenloai), tongtien=tien, chitieuganday=chitieuganday,
                           ten2=ten2, time2=time2, tien2=tien2, n2=len(ten2), ten3=ten3, tien3=tien3,
                           n3=len(ten3))

@app.route('/process_addtien', methods=['post', 'get'])
def procees_addtien():

    tien = request.form.get('themtien')

    print(tien)
    untils.add_tien(current_user.idtaikhoan, int(tien))

    print("a")
    return redirect(url_for('taichinh'))

@app.route('/giaodich', methods=['post', 'get'])
def giaodich():
    sotien = 0
    name = ''
    nhom = 1
    loai = 1
    all_nhom = untils.get_all_nhom()
    all_loai = untils.get_all_loai_theo_nhom(1)
    if request.method == 'POST':
        sotien = request.form.get('sotien')
        nhom = request.form.get('nhom')
        loai = request.form.get('loai')
        ngay = request.form.get('ngay')
        note = request.form.get('note')
        name = request.form.get('name')

        # print(sotien, nhom, loai, ngay)

        if float(sotien) > 0 and ngay:
            untils.add_giao_dich(current_user.idtaikhoan, int(loai), float(sotien),
                                 int(nhom), note, datetime.strptime(ngay, '%Y-%m-%d').date(), name)

            # sotien = untils.get_tai_khoan_tai_chinh(current_user.idtaikhoan).soTien
            return redirect(url_for('taichinh'))

        all_loai = untils.get_all_loai_theo_nhom(nhom)

        return render_template('giaodich.html', all_nhom=all_nhom, all_loai=all_loai, nhomselect=int(nhom),
                           sotien=sotien, ngay=ngay, loai=int(loai), note=note.strip(),
                               date=datetime.strptime(ngay, '%Y-%m-%d').date(), name=name)


    return render_template('giaodich.html', all_nhom=all_nhom, all_loai=all_loai, nhomselect=int(nhom),
                           sotien=sotien, ngay=datetime.now(), loai=int(0), note='',
                           date=datetime.strptime('2023-04-15', '%Y-%m-%d').date(), name=name)


@app.route('/chitieuhangthang', methods=['post', 'get'])
def chitieuhangthang():


    tennhom = untils.get_all_nhom()

    chitieu = []

    for i in tennhom:
        chitieu.append(untils.get_all_loai_theo_nhom(i.id))

    tien = []
    subN = []
    phepChia = []
    counting = 0
    tongTien = 0
    for i in chitieu:
        temp = []
        counting = 0
        for j in i:
            temp.append(untils.get_tong_tien_theo_id_loai(j.id))
            counting = counting + 1
            tongTien = tongTien + untils.get_tong_tien_theo_id_loai(j.id)
        tien.append(temp)
        subN = counting

    for i in chitieu:
        temp = []
        for j in i:
            try:
                temp.append(round(untils.get_tong_tien_theo_id_loai(j.id) / tongTien, 2) * 100)
            except:
                temp.append(0)
        phepChia.append(temp)

    # print(tien)

    return render_template('chitieuhangthang.html', chitieu=chitieu, tennhom=tennhom, n=len(tennhom), tien=tien,
                           subN=subN, tongTien=tongTien, phepChia=phepChia)

@app.route("/profile", methods=['post', 'get'])
def profile_user():
    # sdt = request.form.get('sdt')
    # email = request.form.get('email')
    # diachi = request.form.get('diachi')
    #
    profile = untils.get_user_by_id(current_user.id)
    profile.name = decoding_no1(profile.name)
    profile.email = decoding_no1(profile.email)
    hoten = profile.name.split(" ")
    #
    # if sdt:
    #     untils.change_info(user_id=current_user.id, sdt=sdt, diachi=diachi)
    #     return render_template('profile.html', user=user)

    ho = hoten[0]
    ten = ''
    for i in range(1, len(hoten)):
        ten = ten + " " + hoten[i]

    taikhoan = untils.get_tai_khoan_tai_chinh(current_user.idtaikhoan)

    return render_template('profile.html', profile=profile, ten=ten[1:], ho=ho, taikhoan=taikhoan)


@app.route('/summary', methods=['post', 'get'])
def summary():
    summary = ''
    text = ''

    if request.method == 'POST':
        text = request.form.get('text')

        if text:
            summary = untils.summary(text)
        else:
            summary = "Please input fully"

    return render_template('summary.html', summary=summary, text=text)

# CHATBOT
# @app.route('/chatbot', methods=["get"])
# def chatbot():
#     return render_template('tintuc.html')
#
# @app.route('/getBotResponse', methods=['post'])
# def chatbot_response():
#     msg = request.form["msg"]
#     response = chatbot.get_response(msg)
#     return str(response)

@app.route('/tintuc', methods=['get'])
def tintuc():
    return render_template('tintuc.html')


@app.route('/calendar', methods=['GET'])
def calendar():
    loinhac = get_su_kien(current_user.id)

    data = []

    for i in loinhac:
        data.append({
            "id": i.id,
            "name": i.name,
            "description": i.description,
            "badge": "Sự kiện",
            "date": i.startAt,
            "type": 'event',
        })

    return render_template('calendar.html', data=data)


@app.route('/create_task', methods=['Post', 'get'])
def create_task():
    name = request.form.get('name')
    task = request.form.get('task')
    deadline = request.form.get('deadline')
    startAt = request.form.get('startAt')
    des = request.form.get('des')
    loop = request.form.get('loop')

    hour_dl = deadline.split(':')[0]
    minute_dl = deadline.split(':')[1]

    hour_sa = startAt.split(':')[0]
    minute_sa = startAt.split(':')[1]

    deadline = datetime.now().replace(hour=int(hour_dl), minute=int(minute_dl), second=0, microsecond=0)
    startAt = datetime.now().replace(hour=int(hour_sa), minute=int(minute_sa), second=0, microsecond=0)

    add_task(user_id=current_user.id, name=name, task=task, deadline=deadline, startAt=startAt, des=des, loop=loop)

    return redirect(url_for('calendar'))


@app.route('/calendar', methods=['GET'])
def calendar():

    loinhac = get_su_kien(current_user.id)

    data = []

    for i in loinhac:
        data.append({
            "id": i.id,
            "name": i.name,
            "description": i.description,
            "badge": "Sự kiện",
            "date": i.startAt,
            "type": 'event',
        })

    return render_template('calendar.html', data=data)


@app.route('/create_task', methods=['Post', 'get'])
def create_task():


    name = request.form.get('name')
    task = request.form.get('task')
    deadline = request.form.get('deadline')
    startAt = request.form.get('startAt')
    des = request.form.get('des')
    loop = request.form.get('loop')

    hour_dl = deadline.split(':')[0]
    minute_dl = deadline.split(':')[1]

    hour_sa = startAt.split(':')[0]
    minute_sa = startAt.split(':')[1]

    deadline = datetime.now().replace(hour=int(hour_dl), minute=int(minute_dl), second=0, microsecond=0)
    startAt = datetime.now().replace(hour=int(hour_sa), minute=int(minute_sa), second=0, microsecond=0)

    add_task(user_id=current_user.id, name=name, task=task, deadline=deadline, startAt=startAt, des=des, loop=loop)
    

    return redirect(url_for('calendar'))

if __name__ == '__main__':
    socketio.run(app, debug=True)