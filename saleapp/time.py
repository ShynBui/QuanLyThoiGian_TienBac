from saleapp.models import User, UserRole, Room, Message
from flask_login import current_user
from sqlalchemy import func, and_, desc, or_
from saleapp import app, db
import json
from datetime import datetime
import hashlib
from sqlalchemy.sql import extract



