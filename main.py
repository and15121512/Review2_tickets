import os

from flask import Flask
from flask import render_template
from flask import request, make_response

from flask_sqlalchemy import SQLAlchemy

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "database.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file

db = SQLAlchemy(app)

from sqlalchemy import Column, Integer, String, DateTime, DECIMAL, ForeignKey

class User(db.Model):
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
        self.login_code = login
        self.password_code = password
        self.sum_amt = summ

    def __repr__(self):
        return '<User %i %s %s %s %s %i>' % (self.id, self.last_name_txt, self.first_name_txt, self.login_code,
                                             self.password_code, self.sum_amt)


class Flight(db.Model):
    __tablename__ = 'FLIGHT'
    id = Column(Integer, primary_key=True)
    from_txt = Column(String(255))
    where_txt = Column(String(255))
    departure_dttm = Column(String)
    arriving_dttm = Column(String)
    cost_amt = Column(Integer)
    departure_date = Column(String)

    def __init__(self, from_txt=None, where_txt=None, departure_dttm=None, arriving_dttm=None,
                 cost_amt=0, departure_date=None):
        self.from_txt = from_txt
        self.where_txt = where_txt
        self.departure_dttm = departure_dttm
        self.arriving_dttm = arriving_dttm
        self.departure_date = departure_dttm.split(' ')[0]
        self.cost_amt = cost_amt

    def __repr__(self):
        return '<Flight %i %s %s %s %s %i>' % (self.id, self.from_txt, self.where_txt, self.departure_dttm,
                                                   self.arriving_dttm, self.cost_amt)

    def __str__(self):
        return '%i %s %s %s %s %i' % (self.id, self.from_txt, self.where_txt, self.departure_dttm,
                                                   self.arriving_dttm, self.cost_amt)


class User_X_Flight(db.Model):
    __tablename__ = 'USER_X_FLIGHT'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("USER.id"))
    flight_id = Column(Integer, ForeignKey("FLIGHT.id"))

    def __init__(self, user_id=None, flight_id=None):
        self.user_id = user_id
        self.flight_id = flight_id

    def __repr__(self):
        return '<User_X_Flight>' % ()


##############################

#from database import init_db, db_session
#from models import User
#from models import Flight


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html",
                           title="Sign in")


@app.route('/validation/', methods=['POST'])
def validation():
    login = request.form['login']
    password = request.form['password']

    tmp = list()
    for user in User.query.filter_by(login_code=login):
        tmp.append(user)

    u = None
    if len(tmp) == 0:
        return render_template("sign_in.html")
    #elif tmp[0].password == password:
    #    u = tmp[0]
    else: # пользователь не найден
        #return render_template("index.html", title="Sign in")
        u = tmp[0]

    #print(str(u.sum_amt))
    resp = make_response(render_template("main_window.html", login_code=u.login_code, sum_amt=str(u.sum_amt)))
    resp.set_cookie('user_login', login)
    resp.set_cookie('user_sum', str(u.sum_amt))
    return resp
    #return render_template("main_window.html", login_code=u.login_code, sum_amt=u.sum_amt)


@app.route('/sign_in/', methods=['POST'])
def sign_in():
    last_name = request.form['last_name']
    first_name = request.form['first_name']
    login = request.form['login']
    password = request.form['password']
    summ = request.form['sum']

    u = User(last_name, first_name, login, password, summ)
    db.session.add(u)
    db.session.commit()

    resp = make_response(render_template("main_window.html", login_code=u.login_code, sum_amt=str(u.sum_amt)))
    resp.set_cookie('user_login', login)
    resp.set_cookie('user_sum', str(summ))
    return resp



@app.route('/search_flights/', methods=['POST'])
def search_flights():
    from_ = request.form['from']
    where_ = request.form['where']
    dep_date = request.form['departure_date']
    user_login = request.cookies.get('user_login')
    user_summ = request.cookies.get('user_sum')

    result_list = list()
    for result in Flight.query.filter_by(
            from_txt=from_, where_txt=where_, departure_date=dep_date):
        result_list.append([str(result.id), str(result.from_txt), str(result.where_txt),
                            str(result.departure_dttm), str(result.arriving_dttm), str(result.cost_amt)])

    resp = make_response(render_template("search_results.html", result=result_list,
                                         login_code=user_login, sum_amt=user_summ))
    result_list = ['|'.join(elem) for elem in result_list]

    resp.set_cookie('user_login', user_login)
    resp.set_cookie('user_sum', user_summ)
    resp.set_cookie('searching_result', '!'.join(result_list))
    return resp
    #return render_template("search_results.html", result=result_list)


@app.route('/view_more/', methods=['POST'])
def view_more():
    chosen_id = request.form['v_more']
    user_login = request.cookies.get('user_login')
    user_summ = request.cookies.get('user_sum')
    searching_result = request.cookies.get('searching_result')

    chosen_flight = None
    for result in Flight.query.filter_by(id=chosen_id):
        chosen_flight = [str(result.id), str(result.from_txt), str(result.where_txt),
                            str(result.departure_dttm), str(result.arriving_dttm), str(result.cost_amt)]

    resp = make_response(render_template("confrim.html", flight=chosen_flight,
                                         login_code=user_login, sum_amt=user_summ))
    resp.set_cookie('user_login', user_login)
    resp.set_cookie('user_sum', user_summ)
    resp.set_cookie('searching_result', searching_result)
    return resp
    #return render_template("confrim.html", flight=chosen_flight)


def insert_to_db(user_login, flight_id):
    tmp = list()
    for user in User.query.filter_by(login_code=user_login):
        tmp.append(user)
    user = tmp[0]
    tmp = list()
    for flight in Flight.query.filter_by(id=flight_id):
        tmp.append(flight)
    flight = tmp[0]
    if user.sum_amt < flight.cost_amt:
        return -1

    u_f = User_X_Flight(user.id, flight_id)
    db.session.add(u_f)

    res = user.sum_amt-flight.cost_amt
    User.query.filter_by(id=user.id).update({'sum_amt': user.sum_amt-flight.cost_amt})
    db.session.commit()
    return res


@app.route('/confrim/', methods=['POST'])
def confrim():
    user_login = request.cookies.get('user_login')
    user_summ = request.cookies.get('user_sum')
    searching_result = request.cookies.get('searching_result')

    answer = (request.form['confrim_ans']).split()
    print(answer)
    answer_str = answer[0]
    answer_id = answer[1]
    if answer_str == 'yes':
        print('YES!!!', answer_id)
        new_summ = insert_to_db(user_login, answer_id)
        if new_summ != -1:
            print('Success')
            resp = make_response(render_template("success.html", login_code=user_login, sum_amt=str(new_summ),
                                                 what_happened='success'))
            resp.set_cookie('user_login', user_login)
            resp.set_cookie('user_sum', str(new_summ))
            return resp
        else:
            print('No money!!!')
            resp = make_response(render_template("success.html", login_code=user_login, sum_amt=user_summ,
                                                 what_happened='no_money'))
            resp.set_cookie('user_login', user_login)
            resp.set_cookie('user_sum', user_summ)
            return resp
    elif answer_str == 'no':
        print('NO!!!', answer_id)

        result_list = searching_result.split('!')
        result_list = [elem.split('|') for elem in result_list]

        resp = make_response(render_template("search_results.html", result=result_list,
                                             login_code=user_login, sum_amt=user_summ))
        resp.set_cookie('user_login', user_login)
        resp.set_cookie('user_sum', user_summ)
        resp.set_cookie('searching_result', searching_result)
        return resp
    else:
        print('Something strange happened!!!')


@app.route('/go_home/', methods=['POST'])
def go_home():
    user_login = request.cookies.get('user_login')
    user_summ = request.cookies.get('user_sum')

    resp = make_response(render_template("main_window.html", login_code=user_login, sum_amt=user_summ))
    resp.set_cookie('user_login', user_login)
    resp.set_cookie('user_sum', user_summ)
    return resp