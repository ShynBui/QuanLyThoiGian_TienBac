from saleapp.models import User, UserRole, Room, Message, Priority, LoiNhac, Task
from flask_login import current_user
from sqlalchemy import func, and_, desc, or_
from saleapp import app, db
import json
from datetime import datetime
import hashlib
from sqlalchemy.sql import extract

from flask_mail import Mail, Message
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'quythanh.test@gmail.com'
app.config['MAIL_PASSWORD'] = 'pfuhlpfddrmuwnjh'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

def NhacNhoSuKien(ten, email):
    msg = Message('Nhắc nhở', sender = 'quythanh.test@gmail.com', recipients = [email])
    mail.body = f"hello {ten}"
    msg.html = mail.body
    mail.send(msg)


def add_task(user_id, name, task, deadline, startAt, des, loop):
    pri = Priority.query.get(1)

    loinhac = LoiNhac(hour=loop, name=name, description=des)
    db.session.add(loinhac)
    db.session.commit()

    task = Task(name=name, description= des, startAt=startAt, deadline=deadline, idPriority=pri.id, idUser=user_id,
                idLoiNhac=loinhac.id)
    db.session.add(task)
    db.session.commit()
    print(task)


def get_su_kien(id_user):

    loinhac = Task.query.filter(Task.idUser == id_user)

    return loinhac.all()