import os
from flask import Flask, url_for, redirect, render_template, request, jsonify
from flask.ext.sqlalchemy import SQLAlchemy
from wtforms import form, fields, validators
from flask.ext import admin, login
from flask.ext.admin.contrib import sqla
from flask.ext.admin import helpers, expose
from werkzeug.security import generate_password_hash, check_password_hash
import json
import ast
import datetime
import time
# Create Flask application
app = Flask(__name__)

# Create dummy secrey key so we can use sessions
app.config['SECRET_KEY'] = '123456790'

# Create in-memory database

# collect = Collect()
# collect.init_app(app)
# collect.collect(verbose=True)
app.config['DATABASE_FILE'] = 'sample_db.sqlite'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + app.config['DATABASE_FILE']
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


# Create user model.
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    login = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120))
    password = db.Column(db.String(64))
    data = db.relationship('Data', backref='author', lazy='dynamic')

    # Flask-Login integration
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def get_mail(self):
        return self.email

    def get_data(self):
        return Data.query.filter_by(user_id= self.id).first()

    # Required for administrative interface
    def __unicode__(self):
        return self.username



class Data(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    datapoints = db.Column(db.Text())
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def get_ep(self):
        return self.datapoints

    def __repr__(self):
        return '%r' % (self.datapoints)


# Define login and registration forms (for flask-login)
class LoginForm(form.Form):
    login = fields.TextField(validators=[validators.required()])
    password = fields.PasswordField(validators=[validators.required()])

    def validate_login(self, field):
        user = self.get_user()

        if user is None:
            raise validators.ValidationError('Invalid user')

        # we're comparing the plaintext pw with the the hash from the db
        if not check_password_hash(user.password, self.password.data):
        # to compare plain text passwords use
        # if user.password != self.password.data:
            raise validators.ValidationError('Invalid password')

    def get_user(self):
        return db.session.query(User).filter_by(login=self.login.data).first()


class RegistrationForm(form.Form):
    login = fields.TextField(validators=[validators.required()])
    email = fields.TextField()
    password = fields.PasswordField(validators=[validators.required()])

    def validate_login(self, field):
        if db.session.query(User).filter_by(login=self.login.data).count() > 0:
            raise validators.ValidationError('Duplicate username')
# parsing the json created by user



def parse(d):
    d = ast.literal_eval(d)
    endpoints_list = d["endpoints"]
    enp_path = []
    dfp = {}
    for i in endpoints_list:
        enp_path.append(i["path"])
        try:
            dfp[i["path"]]=i['result']
        except: pass
    print type(dfp) , "hey this is dfp before sendign"
    return dfp


def parse_enp(d):
    d = ast.literal_eval(d)
    endpoints_list = d["endpoints"]
    enp_path = []
    for i in endpoints_list:
        enp_path.append(i["path"])
    return enp_path



# Initialize flask-login
def init_login():
    login_manager = login.LoginManager()
    login_manager.init_app(app)

    # Create user loader function
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.query(User).get(user_id)


# Create customized model view class
class MyModelView(sqla.ModelView):

    def is_accessible(self):
        return login.current_user.is_authenticated()


# Create customized index view class that handles login & registration
class MyAdminIndexView(admin.AdminIndexView):

    @expose('/')
    def index(self):
        if not login.current_user.is_authenticated():
            return redirect(url_for('.login_view'))
        return super(MyAdminIndexView, self).index()

    @expose('/login/', methods=('GET', 'POST'))
    def login_view(self):
        # handle user login
        form = LoginForm(request.form)
        if helpers.validate_form_on_submit(form):
            user = form.get_user()
            login.login_user(user)

        if login.current_user.is_authenticated():
            return redirect(url_for('.index'))
        link = '<p>Don\'t have an account? <a href="' + url_for('.register_view') + '">Click here to register.</a></p>'
        self._template_args['form'] = form
        self._template_args['link'] = link
        return super(MyAdminIndexView, self).index()

    @expose('/register/', methods=('GET', 'POST'))
    def register_view(self):
        form = RegistrationForm(request.form)
        if helpers.validate_form_on_submit(form):
            user = User()

            form.populate_obj(user)
            # we hash the users password to avoid saving it as plaintext in the db,
            # remove to use plain text:
            user.password = generate_password_hash(form.password.data)

            db.session.add(user)
            db.session.commit()

            login.login_user(user)
            return redirect(url_for('.index'))
        link = '<p>Already have an account? <a href="' + url_for('.login_view') + '">Click here to log in.</a></p>'
        self._template_args['form'] = form
        self._template_args['link'] = link
        return super(MyAdminIndexView, self).index()

    @expose('/logout/')
    def logout_view(self):
        login.logout_user()
        return redirect(url_for('.index'))

# Flask views
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/boxit', methods=["POST","GET"])
def boxit():
    d= {}
    if request.method== "POST":
        d["name"] = str(request.form["cname"]).strip().replace(' ','')
        d["api"] ={'verion':str(request.form["api_version"]).strip(), 'prefix':str(request.form["api_prefix"]).strip()}
        d["data"] = str(request.form).count('path')
        ep = []

        for i in range(str(request.form).count('path')):
            try:
                k ={}
                k['path'] = str(d['name']+'/'+d['api']['prefix']+''+request.form['path'+str(i)]).replace('///','/').replace('//','/')
                k['methods'] = str(request.form['methods'+str(i)]).upper()
                k['req_body'] = ast.literal_eval(str(request.form['req_body'+str(i)]).strip())
                k['result'] = {'success': ast.literal_eval(request.form['result_s'+str(i)].strip()),'failure':ast.literal_eval(request.form['result_f'+str(i)].strip())}
                
                ep.append(k)
            except Exception, e: print e; pass;
        d["endpoints"] = ep

        print login.current_user.get_id(), "hey this is d"
        epsps = Data(datapoints=str(d), timestamp=datetime.datetime.utcnow(), author=login.current_user)
        db.session.add(epsps)
        db.session.commit()
        k= ['<a>'+k+'</a>' for k in parse_enp(str(d))]
        return  '<p>'+ str(k) +'</p>' # request.data #redirect(url_for('boxit')))
    # if len(d)>5:
    #     return str(d)
    # return "got the message",str(d


@app.route('/',defaults={'path': ''})
@app.route('/<path:path>',methods = ["GET","POST","PUT","DELETE"])
def catch_all(path):
    k = path
    print k
    ud = Data.query.filter_by(user_id= login.current_user.id).first()

    modified_data = []
    print type(ud.datapoints)
    enp_path = [str(l).strip().replace(' ','')  for l in parse_enp(str(ud.datapoints))]
    dfp = parse(str(ud.datapoints) )
    print dfp, "hey this is dfp"
    if request.method == "POST":
        print "just entered post"
        print enp_path, "in endpoint", k
        if k in enp_path:
            print "checking path"
            existing_data = list(str(dfp[k]['success']))
            print existing_data
            if len(existing_data)>1:
                existing_data.append(str(requestself.data))
                dfp[k]['success'] = existing_data
                ud.datapoints = dfp
                return str(dfp)
            else:
                print request.data, "this is post man"
                modified_data.append(existing_data)
                modified_data.append(request.data)
                dfp[k]['success'] = modified_data   
                return str(dfp)
                        
        else:
            return "invalid endpoint"


    if request.method == "GET":
        print "came to get"
        if k in enp_path:
            print "reaching inside get"
            return str(dfp[k]["success"])
                    
        else:
            return "invalid endpoint"

    if request.method == "DELETE":
        if k in enp_path:
            b =  ast.literal_eval(request.data)
            existing_data = dfp[k]["success"]
            if len(existing_data)>1:
                for i in range(0,len(existing_data)):
                    if b == existing_data[i]:
                        del existing_data[i]
                        break
                dfp[k]['success'] = existing_data
                return str(dfp)
            else:
                return "No values in this end point"
        else:
            return "invalid endpoint"
            
                        
            
            
# Initialize flask-login
init_login()

# Create admin
admin = admin.Admin(app, 'Haywire Box', index_view=MyAdminIndexView(), base_template='my_master.html')

# Add view
# admin.add_view(MyModelView(User, db.session))


def build_sample_db():
    """
    Populate a small db with some example entries.
    """

    import string
    import random

    db.drop_all()
    db.create_all()
    # passwords are hashed, to use plaintext passwords instead:
    # test_user = User(login="test", password="test")
    test_user = User(login="test", password=generate_password_hash("test"))
    db.session.add(test_user)

    first_names = [
        'Harry', 'Amelia', 'Oliver', 'Jack', 'Isabella', 'Charlie','Sophie', 'Mia',
        'Jacob', 'Thomas', 'Emily', 'Lily', 'Ava', 'Isla', 'Alfie', 'Olivia', 'Jessica',
        'Riley', 'William', 'James', 'Geoffrey', 'Lisa', 'Benjamin', 'Stacey', 'Lucy'
    ]
    last_names = [
        'Brown', 'Smith', 'Patel', 'Jones', 'Williams', 'Johnson', 'Taylor', 'Thomas',
        'Roberts', 'Khan', 'Lewis', 'Jackson', 'Clarke', 'James', 'Phillips', 'Wilson',
        'Ali', 'Mason', 'Mitchell', 'Rose', 'Davis', 'Davies', 'Rodriguez', 'Cox', 'Alexander'
    ]

    for i in range(len(first_names)):
        user = User()
        user.first_name = first_names[i]
        user.last_name = last_names[i]
        user.login = user.first_name.lower()
        user.email = user.login + "@example.com"
        user.password = generate_password_hash(''.join(random.choice(string.ascii_lowercase + string.digits) for i in range(10)))
        db.session.add(user)

    db.session.commit()
    return

if __name__ == '__main__':

    # Build a sample db on the fly, if one does not exist yet.
    app_dir = os.path.realpath(os.path.dirname(__file__))
    database_path = os.path.join(app_dir, app.config['DATABASE_FILE'])
    if not os.path.exists(database_path):
        build_sample_db()

    # Start app
    app.run(debug=True)