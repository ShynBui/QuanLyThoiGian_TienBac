from saleapp.models import User, UserRole, Room, Message
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


def add_user(name, username, password, diachi, **kwargs):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    print(kwargs.get('dob'))
    maSo1 = kwargs.get('email').split('@')[0]
    maso = ''
    for i in maSo1:
        if i.isnumeric():
            maso = maso + i

    print(maso)

    db.session.commit()

    user = User(name=name.strip(), username=username, password=password, diachi=diachi,
                email=kwargs.get('email'), avatar=kwargs.get('avatar'), maSo=maso, userRole=UserRole.USER,
                dob=kwargs.get('dob'))

    # user1 = User(name="Bùi Tiến Phát", maSo="2051052096", username="2051052096phat@ou.edu.vn",
    #              password=password, email="2051052096phat@ou.edu.vn", joined_date=datetime.now(),
    #              diachi="Gò Vấp", userRole=UserRole.SINHVIEN, idPerson=sv1.id,
    #              dob=datetime.strptime("24-06-2002", '%d-%m-%Y').date(), avatar='')

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
