# Anubha Barve , ab4285@drexel.edu
# CS530: DUI, Assignment 1 

from flask import Flask, render_template, send_file, g, request, jsonify, session, escape, redirect
import os,sys
from Database import Database

app = Flask(__name__, static_folder='public', static_url_path='')
app.secret_key = b'lkj98t&%$3rhfSwu3D'

# Handle the index (home) page
@app.route('/')
def index():
    return render_template('index.html')


# Handle any files that begin "/course" by loading from the course directory
@app.route('/course/<path:path>')
def base_static(path):
    return send_file(os.path.join(app.root_path, '..', 'course', path))


# Handle any unhandled filename by loading its template
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = Database()
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/create_user', methods=['GET', 'POST'])
def create_user():
    message = None
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['mail']
        username = request.form['uname']
        typed_password = request.form['psw']
        retyped_password = request.form['cpsw']
        if name and email and username and typed_password and retyped_password:
            if typed_password == retyped_password:
                get_db().userSignUp(name, email, username, typed_password)
                return redirect('/')
            else:
                message = "Passwords do not match! Please enter again"
    return render_template('/',message = message)


@app.route('/login', methods=['GET', 'POST'])
def login():
    message = None
    if request.method == 'POST':
        username = request.form['uname']
        typed_password = request.form['psw']
        if username and typed_password:
            user = get_db().userLogin(username)
            if user:
                if typed_password == user['password']:
                    session['user'] = user
                    return redirect('userLogin')
                else:
                    message = "Incorrect password, please try again"
            else:
                message = "Unknown user, please try again"
        elif username and not typed_password:
            message = "Missing password, please try again"
        elif not username and typed_password:
            message = "Missing username, please try again"
    return render_template('/', message=message)


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

@app.route('/addexpense', methods=['GET', 'POST'])
def add_expense():
    message = None
    if request.method == 'POST':
        description = request.form['description']
        category = request.form['category']
        amount = request.form['amount']
        username = session['user']['username']
        if description and category and amount and username:
            get_db().expense(description, category, amount, username)
            message = "Expense added Succesfully!"
            return render_template('userLogin.html',message = message)
        else:
            message = "Please enter again !! "
    return render_template('userLogin.html',message = message)

@app.route('/addaccount', methods=['GET', 'POST'])
def add_account():
    message = None
    if request.method == 'POST':
        account = request.form['account']
        balance = request.form['balance']
        username = session['user']['username']
        if account and balance and username:
            get_db().add_account(account, balance, username)
            message = "Account added Succesfully!"
            return render_template('userLogin.html',message = message)
        else:
            message = "Please enter again !! "
    return render_template('userLogin.html',message = message)

@app.route('/addbudget', methods=['GET', 'POST'])
def add_budget():
    message = None
    if request.method == 'POST':
        category = request.form['category']
        budget = request.form['budget']
        username = session['user']['username']
        if category and budget and username:
            get_db().add_budget(category, budget, username)
            message = "Budget added Succesfully!"
            return render_template('userLogin.html',message = message)
        else:
            message = "Please enter again !! "
    return render_template('userLogin.html',message = message)

@app.route('/api/table')
def get_table():
    message = None
    if 'user' in session:
        username = session['user']['username']
        response = get_db().table(username)
        return jsonify(response)
    else:
        message = "No expenses added !! "
    return render_template('userLogin.html', message=message)

@app.route('/api/piechart')
def get_piechart():
    message = None
    if 'user' in session:
        username = session['user']['username']
        response = get_db().chart(username)
        return jsonify(response)
    else:
        message = "No expenses added !! "
    return render_template('userLogin.html', message=message)

@app.route('/api/barchart')
def get_barchart():
    message = None
    if 'user' in session:
        username = session['user']['username']
        response = get_db().chart(username)
        return jsonify(response)
    else:
        message = "No expenses added !! "
    return render_template('userLogin.html', message=message)

@app.route('/changeUser', methods=['GET', 'POST'])
def change_user():
    message = None
    if request.method == 'POST':
        name = session['user']['username']
        username = request.form['newU']
        cUsername = request.form['cnewU']
        if username and cUsername:
            if username == cUsername:
                get_db().changeUser(username,name)
                message = "Username Changed Successfully !! "
                return render_template('userLogin.html',message = message)
            else:
                message = "Usernames do not match! Please enter again"
    return render_template('userLogin.html',message = message)

@app.route('/changePwd', methods=['GET', 'POST'])
def change_pwd():
    message = None
    if request.method == 'POST':
        name = session['user']['username']
        pwd = request.form['newP']
        cPwd = request.form['cnewP']
        if pwd and cPwd:
            if pwd == cPwd:
                get_db().changePwd(pwd,name)
                message = "Password Changed Successfully !! "
                return render_template('userLogin.html',message = message)
            else:
                message = "Passwords do not match! Please enter again"
    return render_template('userLogin.html',message = message)

@app.route('/api/budget')
def budget_check():
    message = None
    if 'user' in session:
        username = session['user']['username']
        bud = get_db().budgetCheck(username)
        return jsonify(bud)
    else:
        message = "No Budget Added !! "
    return render_template('userLogin.html',message = message)

@app.route('/about')
def about():
    return render_template('about.html')    


@app.route('/<name>')
def generic(name):
    if 'user' in session:
        return render_template(name + '.html')
    else:
        return redirect('/')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8012, debug=False)
