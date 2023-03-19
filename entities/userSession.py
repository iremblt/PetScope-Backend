from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
class UserSession(db.Model):
    __tablename__ = 'UserSession'
    user_session_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    login_date = db.Column(db.DateTime, nullable=False)
    expire_date = db.Column(db.DateTime, nullable=False)
    logged_out = db.Column(db.Boolean, nullable=False)
    jw_token = db.Column(db.String(4000), nullable=False)

    def __init__(__self__,user_id,login_date,expire_date,logged_out,jw_token):
        __self__.user_id = user_id
        __self__.login_date = login_date
        __self__.expire_date = expire_date
        __self__.logged_out = logged_out
        __self__.jw_token = jw_token
