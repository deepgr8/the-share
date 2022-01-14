import pymongo
import bcrypt


from flask import Flask,render_template,request,url_for, redirect, session
from flask_pymongo import PyMongo

app = Flask(__name__)

app.secret_key = 'keynotknown'

client = pymongo.MongoClient(
    "mongodb+srv://whale-crawl:binomo123@cluster0.w1jbe.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

# get the database name
db = client.get_database('clustergr8')
# get the particular collection that contains the data
records = db.users

@app.route('/')
def ho():
    return render_template("/index.html")



@app.route("/signup", methods=['post', 'get'])
def signup():
    print("message",request.form)
    message = 'Signup to your account'
   
    if request.method == "POST":
        name = request.form.get("name")
        
        email = request.form.get("email")
        password1 = request.form.get("password")
       
        # if found in database showcase that it's found
        email_found = records.find_one({"email": email})
        if email_found:
            message = 'This email already exists in database'
            return render_template("create.html", message=message)
  
        else:
            # hash the password and encode it
            hashed = bcrypt.hashpw(password1.encode('utf-8'), bcrypt.gensalt())
            # assing them in a dictionary in key value pairs
            user_input = {'name': name, 'email': email,'password': hashed}
            # insert it in the record collection
            records.insert_one(user_input)

            # find the new created account and its email
            user_data = records.find_one({"email": email})
            new_email = user_data['email']
            # if registered redirect to logged in as the registered user
            session["email"] = new_email
            return render_template("/dashboard.html")
    return render_template("/dashboard.html", message=message)


@app.route("/login", methods=["POST", "GET"])
def login():
    
    message = 'Please login to your account'
    # if "email" in session:
    #     return render_template("/index.html")

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        # check if email exists in database
        email_found = records.find_one({"email": email})
        if email_found:
            email_val = email_found['email']
            passwordcheck = email_found['password']
            # encode the password and check if it matches
            if bcrypt.checkpw(password.encode('utf-8'), passwordcheck):
                session["email"] = email_val
                return render_template("/dashboard.html")
            else:
                if "email" in session:
                    return redirect(url_for("logged_in"))
                message = 'Wrong password'
                return render_template("/create.html", message=message)
        else:
            message = 'Email not found'
            return render_template("/create.html", message=message)
    return render_template("/create.html", message=message)




@app.route("/create")
def createaccount():
    return render_template('create.html')



# Uploading files by drag and drop


app.config['MONGO_URI'] =  "mongodb+srv://whale-crawl:binomo123@cluster0.w1jbe.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"

mongo = PyMongo(app)
db = client[ "myFirstDatabase" ]
col = db[ "fs.files" ]

@app.route('/uploader', methods=['POST', 'GET'])
def uploader():
    if request.method == 'POST':
        f = request.files['fileinput']
        
        # print(n)
        # mongo.save_file(f.filename, f)
        col.insert_one({'file': f.filename})
        print("successfully")

    return render_template("index.html")
@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        name=request.form.get('name')
        f = request.files['fileinput']
        
        # mongo.save_file(f.filename, f)
        col.insert_one({'file':f.filename})
        # print("successfully")

    return render_template("dashboard.html")
@app.route('/search',methods=['GET', 'POST'])
def download():
    
        a=col.find({},{'_id':0,'file':1})
        
        print(a)
        return render_template("downloads.html",a=a)
    
    

@app.route("/logout", methods=['POST','GET'])
def logout():
    session.pop('username',None)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
