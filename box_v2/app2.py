from flask import Flask, jsonify,request, render_template, redirect, url_for
import ast
import json
import collections
from datetime import datetime

from flask.ext.wtf import Form
from wtforms.fields import TextField, BooleanField
from wtforms.validators import Required
from wtforms.ext.appengine.db import model_form
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

class Post(db.Model):
    '''
    We are trying to map all the endpoint details and store them as is
    '''
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    body = db.Column(db.Text)
    pub_date = db.Column(db.DateTime)

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category',
        backref=db.backref('posts', lazy='dynamic'))

    def __init__(self, title, body, category, pub_date=None):
        self.title = title
        self.body = body
        if pub_date is None:
            pub_date = datetime.utcnow()
        self.pub_date = pub_date
        self.category = category

    def __repr__(self):
        return '<Post %r>' % self.title


class Category(db.Model):
    '''
    user can define as many number of projects as possible and create endpoints that will be 
    stored in endpoint table.
    '''
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50),  unique=True)
    version = db.Column(db.String(50))

    def __init__(self, name,version):
        self.name = name
        self.version= version

    def __repr__(self):
        return '<Category %r>' % self.name

from flask_wtf import Form
from wtforms.fields import StringField, DateTimeField
from wtforms.widgets import TextArea
from wtforms.validators import DataRequired
from wtforms.ext.sqlalchemy.orm import model_form
from wtforms.ext.sqlalchemy.fields import QuerySelectField


def enabled_categories():
    return Category.query.all()

def tract(file_name, title, project):
    try:
        obj = json.loads(file_name.strip()) 
        d = convert(obj)
        endpoints_list = d["endpoints"]
        enp_path = []
        dfp = {}
        methods = {}
        for i in endpoints_list:
            enp_path.append(str(project)+'/'+title+'/'+d['api']['prefix']+i["path"])
            # try:
            #     dfp[i["path"]]=i['method']
            # except: pass
        print enp_path
        return enp_path
    except Exception,e: 
        print e
        return "Given Json is having some errors Please Correct It"

class PostForm(Form):
    title = StringField(u'title', validators=[DataRequired()])
    body = StringField(u'Text', widget=TextArea())
    pub_date = DateTimeField(u'date create')
    category = QuerySelectField(query_factory=enabled_categories,
                                allow_blank=True)

@app.route('/',methods=['POST','GET'])
def home():

    if request.method=='POST':
        results =[]
        try:
            print "entered post"
            project_name = request.form['p_name']
            api_version = request.form['api_ver']
            category  = Category(name= project_name, version=api_version)        
            db.session.add(category)
            db.session.commit()
        except Exception, e:
            print "Unable to add the data provided ... " +str(request.data) 
            print e

    form = PostForm()
    results = Category.query.all()
    endpoints = Post.query.all()
    print "getting data from category" , str(results)
    return render_template('index.html', results=results,endpoints=endpoints, form=form)


# @app.route('/new/project')

@app.route('/subprojects', methods= ['POST','GET'])
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, pub_date=form.pub_date.data,
                    body=form.body.data, category=form.category.data)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('home'))
    posts = Post.query.all()
    return render_template('eps.html', posts=posts)


@app.route('/sub/<path:sname>', methods= ['POST','GET'])
def sub_post(sname):
    form = PostForm()
    if not sname.startswith('qo'):
        post = Post.query.filter_by(title= sname).all()
    else:
        post = Post.query.filter_by(category_id = sname.split('qo')[1]).all()
    kk ={}
    for p in post:
        enp = tract(p.body, p.title, p.category_id)
        k= []
        if type(enp)==list:
            for ep in enp:
                k.append(ep)
        if len(k) >1:
        # k.append("")
            kk[p.title] = k
        else: 
            kk[p.title] = ["We couldn't Understand what you have submitted",]
    
    results = Category.query.all()
    return render_template('sub.html', post=kk,form= form, results=results)




'''
converts json object to dictionary
Input:
- data: json onject
Return:
'''
def convert(data):
    if isinstance(data, basestring):
        return str(data)
    elif isinstance(data, collections.Mapping):
        return dict(map(convert, data.iteritems()))
    elif isinstance(data, collections.Iterable):
        return type(data)(map(convert, data))
    else:
        return data





'''
takes path as url and method as one of the  methods and return the appropriate value
Inputs: 
- path: endpoint path
- method: enum value ["GET","POST","DELETE","PUT"]
'''
def url_methods(path,method,dfp):

    if method in dfp[path][0]:
        return dfp[path][0][method]["success"]
    else:
        return "This method is not supported"


def get_datafield_in_method(path,method,dfp):
    data = dfp[path][0][method]["data"]
    return data

def compare_dictionaries(data,dict2):
    keys_of_data = data.keys()
    keys2 = dict2.keys()
    if len(keys_of_data)==len(keys2):
        count = 0
        for i in range(len(keys_of_data)):
            if data[keys_of_data[i]].keys() == dict2[keys2[i]].keys():
                count = count +1
        if count == len(keys_of_data):
            return True
        else:
            return False
    else:
        return False



def post_method(data,path, dfp):
    key = ast.literal_eval(data)
    existing_data = dfp[path][0]["GET"]["success"]
    #if len(existing_data)>1:
    existing_data.append(key)
    dfp[path][0]["GET"]["success"] = existing_data
    return str(dfp)
    #else:
       # modified_data.append(existing_data)
        #modified_data.append(key)
       # dfp["/benchmark"][0]["GET"]["success"] = modified_data
       # return dfp["/benchmark"][0]["GET"]["success"]

def extract_enp(cat_id, prj_name):
    po = Post.query.filter_by(title= prj_name, category_id=cat_id).first()
    file_name= po.body
    try:
        obj = json.loads(file_name.strip()) 
        d = convert(obj)
        endpoints_list = d["endpoints"]
        enp_path = []
        original = []
        dfp = {}
        methods = {}
        for i in endpoints_list:
            original.append(i["path"])
            enp_path.append('box'+'/'+str(cat_id)+'/'+str(prj_name)+'/'+d["api"]["prefix"]+i["path"])
            # print enp_path, "i'm printingthis"
            try:
                dfp[i["path"]]=i['method']
            except: pass
        
        return (enp_path, dfp, original)
    except Exception,e: 
        print e
        return "something went really wrong"


# def extract_enp():
#     try:
#         obj = json.loads(file_name.strip()) 
#         d = convert(obj)
#         endpoints_list = d["endpoints"]
#         enp_path = []
#         dfp = {}
#         methods = {}
#         for i in endpoints_list:
#             enp_path.append(i["path"])
#             try:
#                 dfp[i["path"]]=i['method']
#             except: pass
        
#         return dfp
#     except Exception,e: 
#         print e
#         return "something went really wrong"

def check(ori, enp_path):
    for path in enp_path:
        if ori in path:
            return True
    return False

@app.route('/',defaults={'path': ''})
@app.route('/<path:path>',methods = ["GET","POST","DELETE","PUT"])
def catch_all(path):
    cat_id= path.split('/')[0]
    proj_name = path.split('/')[1]
    enp_path  = extract_enp(cat_id,proj_name)[0]
    ori = [a for a in extract_enp(cat_id,proj_name)[2] if a in path][0]
    print ori,"this is original"

    # print enp_path , "this is enp_path"
    dfp  = extract_enp(cat_id,proj_name)[1]
    print enp_path,"this is dfp"
    # return str(cat_id)
    k = "/" + path
    if request.method == "POST":
        print type(request.data)
        key = ast.literal_eval(request.data)
        data = get_datafield_in_method(ori,request.method,dfp)
        print data
        if compare_dictionaries(data,key):
            post_method(request.data,ori,dfp)
        else:
            return "Invalid Key pair" +str(request.data)
    if check(ori, enp_path):
        print str(request.method),"thjis is the menthod"
        return str(url_methods(ori,request.method,dfp))
    else:
        return "Invalid end point"
  
import os   
    
if __name__ == '__main__':
    if not os.path.exists('test.db'):
        db.create_all()
    app.run(debug=True, host='0.0.0.0')
