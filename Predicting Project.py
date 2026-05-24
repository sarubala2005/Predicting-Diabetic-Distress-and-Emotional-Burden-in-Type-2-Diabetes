import sqlite3 as sql
import os
import pickle
import numpy as np
app = Flask(__name__)
app.secret_key = "secret key"
DATABASE = 'stressdb.db'
filename = 'model_CB.pkl'
model = pickle.load(open(filename, 'rb'))
if not os.path.exists(DATABASE):
conn = sql.connect(DATABASE)
c = conn.cursor()
c.execute('''
CREATE TABLE tbladmin (
id INTEGER PRIMARY KEY AUTOINCREMENT,
uname TEXT NOT NULL,
lid TEXT NOT NULL UNIQUE,
lpass TEXT NOT NULL
)
''')
conn.commit()
conn.close()
56
def get_db():
conn = sql.connect(DATABASE)
conn.row_factory = sql.Row
return conn
@app.route('/')
def index():
return render_template('index.html')
@app.route('/login', methods=['GET', 'POST'])
def login():
if request.method == 'POST':
username = request.form['lid']
password = request.form['lpass']
conn = get_db()
cur=conn.cursor()
cur.execute("select * from tbladmin where lid=? and
lpass=?",(username,password))
data=cur.fetchone()
conn.close()
if data:
session['loggedin'] = True
session["aname"]=data["uname"]
return redirect(url_for('dashboard'))
else:
flash('Admin Login ID and Password Incorrect...!','danger')
return redirect(url_for("index"))
return redirect(url_for("index"))
@app.route('/dashboard')
57
def dashboard():
if 'loggedin' in session:
return render_template('dashboard.html', aname=session['aname'])
return redirect(url_for('logout'))
@app.route('/eda')
def eda():
if 'loggedin' in session:
return render_template('eda.html', aname=session['aname'])
return redirect(url_for('logout'))
@app.route('/prediction')
def prediction():
if 'loggedin' in session:
return render_template('prediction.html', aname=session['aname'])
return redirect(url_for('logout'))
@app.route('/actionresult', methods=['GET', 'POST'])
def actionresult():
if 'loggedin' in session:
temp_array = list()
if request.method == 'POST':
gender = int(request.form['gender'])
age = int(request.form['age'])
smoke = int(request.form['smoke'])
food = int(request.form['food'])
marital = int(request.form['marital'])
dsince = int(request.form['dsince'])
fbs = int(request.form['fbs'])
eb = float(request.form['eb'])
58
prd = float(request.form['prd'])
rrd = float(request.form['rrd'])
interd = float(request.form['interd'])
temp_array = temp_array +
[gender,age,smoke,food,marital,dsince,fbs,eb,prd,rrd,interd]
data = np.asarray([temp_array])
input_data = data.reshape(1,-1)
result = int(model.predict(input_data)[0])
return render_template('result.html', result=result)
return redirect(url_for('logout'))
@app.route('/logout')
def logout():
session.pop('loggedin', None)
session.pop('aname', None)
return redirect(url_for('index'))
if __name__ == "__main__":
app.run(debug=True)
dashboard.html
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Artificial Intelligence</title>
<link rel="icon" href="images/favicon.png"/>
<link rel="stylesheet"
href="https://use.fontawesome.com/releases/v5.4.1/css/all.css">
<link rel="stylesheet" href="../static/css/bootstrap.css" />
59
<link rel="stylesheet" href="../static/css/bootstrap.min.css">
<link rel="stylesheet" href="../static/css/sidebar.css">
</head>
<body>
<div class="wrapper">
<!-- Sidebar -->
<nav id="sidebar">
<div class="sidebar-header d-flex flex-column py-2">
<img src="../static/images/admin.png" class="rounded-circle border borderdark mx-auto" style="width:100px; height:100px;">
<h6 class="text-center pt-3"></h6>
</div>
<ul class="list-unstyled components">
<li class="active">
<a href="{{url_for('dashboard')}}">Dashboard</a>
</li>
<li>
<a href="{{url_for('eda')}}">EDA Analysis</a>
</li>
<li>
<a href="{{url_for('prediction')}}">Diabetic Distress Prediction</a>
</li>
<li>
<a href="{{url_for('logout')}}">Logout</a>
</li>
</ul>
</nav>
60
<!-- Page Content -->
<div id="content">
<nav class="navbar navbar-expand-lg navbar-dark bg-primary">
<div class="container-fluid">
<button type="button" id="sidebarCollapse" class="btn btn-dark">
<i class="fas fa-align-left"></i>
</button>
<button class="btn btn-dark d-inline-block d-lg-none ml-auto" type="button"
data-toggle="collapse" data-target="#navbarSupportedContent" ariacontrols="navbarSupportedContent" aria-expanded="false" aria-label="Toggle
navigation">
<i class="fas fa-align-justify"></i>
</button>
<div class="collapse navbar-collapse" id="navbarSupportedContent">
<ul class="nav navbar-nav ml-auto">
<li class="nav-item">
<a class="nav-link text-white"
href="{{url_for('logout')}}">Logout</a>
</li>
</ul>
</div>
</div>
</nav>
<div class="container-fluid">
<div class="row">
<div class="col-12"></div>
<h3 class="mb-4 text-center">Predicting Diabetic Distress and Emotional
Burden in Type-2 Diabetes</h3>
61
<img src="../static/images/arch.png" class="img-fluid img-thumbnail mxauto d-block" style="width:500px; height:450px;" alt="Arch">
</div>
</div>
</div>
</div>
</div><!-- End wrapper -->
<script src="../static/js/jquery.min.js"></script>
<script src="../static/js/bootstrap.min.js"></script>
<script src="../static/js/sidebar.js"></script>
</body>
</html>
prediction.html
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Artificial Intelligence</title>
<link rel="icon" href="images/favicon.png"/>
<link rel="stylesheet"
href="https://use.fontawesome.com/releases/v5.4.1/css/all.css">
<link rel="stylesheet" href="../static/css/bootstrap.css" />
<link rel="stylesheet" href="../static/css/bootstrap.min.css">
<link rel="stylesheet" href="../static/css/sidebar.css">
</head>
<body>
<div class="wrapper">
62
<!-- Sidebar -->
<nav id="sidebar">
<div class="sidebar-header d-flex flex-column py-2">
<img src="../static/images/admin.png" class="rounded-circle border borderdark mx-auto" style="width:100px; height:100px;">
<h6 class="text-center pt-3"></h6>
</div>
<ul class="list-unstyled components">
<li>
<a href="{{url_for('dashboard')}}">Dashboard</a>
</li>
<li>
<a href="{{url_for('eda')}}">EDA Analysis</a>
</li>
<li class="active">
<a href="{{url_for('prediction')}}">Diabetic Distress Prediction</a>
</li>
<li>
<a href="{{url_for('logout')}}">Logout</a>
</li>
</ul>
</nav>
<!-- Page Content -->
<div id="content">
<nav class="navbar navbar-expand-lg navbar-dark bg-primary">
<div class="container-fluid">
<button type="button" id="sidebarCollapse" class="btn btn-dark">
63
<i class="fas fa-align-left"></i>
</button>
<button class="btn btn-dark d-inline-block d-lg-none ml-auto"
type="button" data-toggle="collapse" data-target="#navbarSupportedContent" ariacontrols="navbarSupportedContent" aria-expanded="false" aria-label="Toggle
navigation">
<i class="fas fa-align-justify"></i>
</button>
<div class="collapse navbar-collapse" id="navbarSupportedContent">
<ul class="nav navbar-nav ml-auto">
<li class="nav-item">
<a class="nav-link text-white"
href="{{url_for('logout')}}">Logout</a>
</li>
</ul>
</div>
</div>
</nav>
<div class="container-fluid">
<h3 class="mb-4 text-center">Predicting Diabetic Distress</h3>
<form name="form1" action="{{url_for('actionresult')}}"
method="post">
<div class="row">
<div class="col-lg-6 col-sm-12">
<div class="form-group">
<label class="control-label">Gender:</label>
<select name="gender" class="form-control border" required>
<option value=""> Select Gender</option>
<option value="0">Male</option>
64
<option value="1">Female</option>
</select>
</div>
<div class="form-group">
<label class="control-label">Enter Age:</label>
<input type="text" name="age" class="form-control border"
required>
</div>
<div class="form-group">
<label class="control-label">Smoking:</label>
<select name="smoke" class="form-control border" required>
<option value=""> Select Smoking</option>
<option value="1">Yes</option>
<option value="0">No</option>
</select>
</div>
<div class="form-group">
<label class="control-label">Food Type:</label>
<select name="food" class="form-control border" required>
<option value=""> Select Food Type</option>
<option value="1">Veg</option>
<option value="0">Non-Veg</option>
</select>
</div>
<div class="form-group">
<label class="control-label">Marital Status:</label>
<select name="marital" class="form-control border" required>
65
<option value=""> Select Marital Status</option>
<option value="1">Married</option>
<option value="0">Un-Married</option>
</select>
</div>
<div class="form-group">
<label class="control-label">Disease Since:</label>
<input type="text" name="dsince" class="form-control border"
required>
</div>
</div><!--End Col-1-->
<div class="col-lg-6 col-sm-12">
<div class="form-group">
<label class="control-label">Fasting Blood Sugar (FBS):</label>
<input type="text" name="fbs" class="form-control border"
required>
</div>
<div class="form-group">
<label class="control-label">Emotional Burden,:</label>
<input type="text" name="eb" class="form-control border" required>
</div>
<div class="form-group">
<label class="control-label">Physician-Related Distress:</label>
<input type="text" name="prd" class="form-control border" required>
</div>
<div class="form-group">
<label class="control-label">Regimen-Related Distress:</label>
<input type="text" name="rrd" class="form-control border" required>
66
</div>
<div class="form-group">
<label class="control-label">Interpersonal Distress:</label>
<input type="text" name="interd" class="form-control border"
required>
</div>
<div class="form-group">
<button type="submit" class="btn btn-success btn-block">
PREDICTION </button>
</div>
<div class="form-group">
<button type="reset" class="btn btn-success btn-block"> CLEAR
</button>
</div>
</div><!-- End Col-2 -->
</div><!-- End Row -->
</form>
</div>
</div>
</div><!-- End wrapper -->
<script src="../static/js/jquery.min.js"></script>
<script src="../static/js/bootstrap.min.js"></script>
<script src="../static/js/sidebar.js"></script>
</body>
</html>