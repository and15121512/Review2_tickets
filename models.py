#from database import db_session
from main import app, db_session
@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()



from sqlalchemy import Column, Integer, String, DateTime, DECIMAL, ForeignKey
from main import Base

class User(Base):
    __tablename__ = 'USER'
    id = Column(Integer, primary_key=True)
    last_name_txt = Column(String(50))
    first_name_txt = Column(String(50))
    login_code = Column(String(120), unique=True)
    password_code = Column(String(120))
    sum_amt = Column(Integer)

    def __init__(self, last_name=None, first_name=None, login=None, password=None, summ=0):
        self.last_name_txt = last_name
        self.first_name_txt = first_name
        self.login = login
        self.password = password
        self.sum_amt = summ

    def __repr__(self):
        return '<User %r>' % (self.last_name_txt)


class Flight(Base):
    __tablename__ = 'FLIGHT'
    id = Column(Integer, primary_key=True)
    from_txt = Column(String(255))
    where_txt = Column(String(255))
    departure_dttm = Column(String(255))
    arriving_dttm = Column(String(255))
    cost_amt = Column(DECIMAL(10, 1))

    def __init__(self, from_txt=None, where_txt=None, departure_dttm=None, arriving_dttm=None, cost_amt=0):
        self.from_txt = from_txt
        self.where_txt = where_txt
        self.departure_dttm = departure_dttm
        self.arriving_dttm = arriving_dttm
        self.cost_amt = cost_amt

    def __repr__(self):
        return '<Flight %r>' % (self.from_txt)


class User_X_Flight(Base):
    __tablename__ = 'USER_X_FLIGHT'
    #id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("USER.id"), primary_key=True)
    flight_id = Column(Integer, ForeignKey("FLIGHT.id"), primary_key=True)

    def __init__(self):
        pass

    def __repr__(self):
        return '<User_X_Flight>' % ()
#User.query.all()