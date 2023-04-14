import math
from flask import render_template, request, redirect, session, jsonify, url_for
from saleapp import app, admin, login, untils, socketio
from saleapp.models import UserRole
from flask_login import login_user, logout_user, login_required, current_user
import cloudinary.uploader
from flask_socketio import SocketIO, emit, join_room
import requests
import openpyxl
from datetime import datetime, date

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

    print(room.room_id)

    user_send = [(untils.get_user_by_id(x.user_id).name) for x in list_user]

    user_image = [untils.get_user_by_id(x.user_id).avatar for x in list_user]

    user_id = [x.user_id for x in list_user]

    host_avatar = untils.get_host_room_avatar(room.room_id);

    user_send.pop(0)
    user_image.pop(0)
    user_id.pop(0)

    print(user_send)

    if user_name and room:

        # print(untils.load_message(room.room_id)[0].content)

        return render_template('chatroom.html', user_name=(user_name), room=room.room_id, name=current_user.name,
                               message=list_user, room_id=int(room.room_id),
                               user_send=user_send, n=len(user_send), user_image=user_image, user_id=user_id,
                               room_name=untils.get_chatroom_by_id(room.room_id),
                               host_avatar=host_avatar);
    else:
        return redirect(url_for('home'))


@app.route("/admin/chatadmin/<int:room_id>")
def chat_room_admin(room_id):
    if current_user.userRole == UserRole.SYSADMIN or current_user.userRole == UserRole.ADMIN:
        print(room_id)
        user_name = current_user.name
        room = untils.get_chatroom_by_room_id(id=room_id)
        list_user = untils.load_message(room.room_id)

        user_send = [(untils.get_user_by_id(x.user_id).name) for x in list_user]

        user_image = [untils.get_user_by_id(x.user_id).avatar for x in list_user]

        user_id = [x.user_id for x in list_user]

        user_send.pop(0)
        user_image.pop(0)
        user_id.pop(0)

        host_avatar = untils.get_host_room_avatar(room.room_id);

        if user_name and room:
            return render_template('chatroom.html', user_name=user_name, room=room.room_id, name=current_user.name,
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
        confirm = request.form.get('confirm')
        avatar_path = None

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

    sotien = untils.get_tai_khoan_tai_chinh(current_user.idtaikhoan).soTien
    return render_template('taichinh.html', sotien=str(sotien))

@app.route('/giaodich', methods=['post', 'get'])
def giaodich():

    sotien = 0
    nhom = 0
    all_nhom = untils.get_all_nhom()
    if request.method == 'POST':
        sotien = request.form.get('sotien')
        nhom = request.form.get('nhom')
        loai = request.form.get('loai')
        ngay = request.form.get('ngay')
        note = request.form.get('note')

        if sotien == '':
            sotien = 0
        if ngay == '':
            ngay = '2023-04-15'
        if not loai:
            loai = '0'
        if nhom == '':
            nhom = 0

        print(loai, ngay, nhom, sotien)

        all_loai =untils.get_all_loai_theo_nhom(nhom)

        return render_template('giaodich.html', all_nhom=all_nhom, all_loai=all_loai, nhomselect=int(nhom),
                           sotien=sotien, ngay=ngay, loai=int(loai), note=note.strip(), date=datetime.strptime(ngay, '%Y-%m-%d').date())

    return render_template('giaodich.html', all_nhom=all_nhom, all_loai=untils.get_all_loai_theo_nhom(nhom), nhomselect=int(nhom),
                           sotien=sotien, ngay=datetime.now(), loai=int(0), note='',
                           date=datetime.now())

@app.route('/process_giaodich')
def process_giaodich():

    print('ss')
    return redirect(url_for('taichinh'))

if __name__ == '__main__':
    socketio.run(app, debug=True)
