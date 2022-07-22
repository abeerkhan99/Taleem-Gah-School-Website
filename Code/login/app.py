from flask import Flask, render_template, url_for, request

# app instance
app = Flask(__name__)

# routing
@app.route('/')
def home():
    return render_template('welcome.html')
    # return 'Hello World!'

@app.route('/login')
def login():
    return render_template('login.html')
    # return 'Hello World!'

@app.route('/logout')
def logout():
    return render_template('login.html')
    # return 'Hello World!'

@app.route('/registration')
def register():
    return render_template('register.html')
    # return 'Hello World!'

@app.route('/verify-details')
def verify():
    return render_template('verify.html')
    # return 'Hello World!'

@app.route('/reset')
def reset_pass():
    return render_template('reset-pass.html')
    # return 'Hello World!'

@app.route('/submit', methods = ['POST'])
def submit():
    if request.method == 'POST':
        email = request.form['uname']
        password = request.form['pass']
        # print(email, password)
        if email == '' and password == '':
            return render_template('login.html', message = "Please enter required fields")
        elif email == '' and password != '':
            return render_template('login.html', message = "Please enter your email address")
        elif email != '' and password == '':
            return render_template('login.html', message = "Please enter your password")
        
        else:
            return render_template('homepage.html')


if __name__ == '__main__':
    app.run(debug=True)