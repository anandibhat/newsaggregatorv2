from flask import Flask, render_template, request, redirect, url_for, session, flash
from newsapi import NewsApiClient
import re
from flask_mysqldb import MySQL

app = Flask(__name__)

app.secret_key = 'your secret key'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Nandi@1986'
app.config['MYSQL_DB'] = 'myapp'

mysql = MySQL(app)

newsapi = NewsApiClient(api_key='41f450e6eed6475398fb3ebcc136352c')

news_articles = newsapi.get_top_headlines(country='sg', category='technology')['articles']

for article in news_articles:
    print(article['title'])

@app.route('/', methods=['GET', 'POST'])
def home():
    # NewsAPI
    news_articles = newsapi.get_top_headlines(country='sg', category='technology')['articles']
    
    if 'loggedin' in session:
        return render_template('dashboard.html', name=session['name'], email=session['email'], news_articles=news_articles)
    else:
        return render_template('index.html', news_articles=news_articles)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST' and 'name' in request.form and 'email' in request.form and 'password' in request.form:
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        account = cursor.fetchone()
        if account:
            flash('Account already exists!')
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            flash('Invalid email address!')
        else:
            cursor.execute('INSERT INTO users(name, email, password) VALUES (%s, %s, %s)', (name, email, password))
            mysql.connection.commit()
            flash('You have successfully registered!')
    elif request.method == 'POST':
        flash('Please fill out the form!')
    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM users WHERE email = %s AND password = %s', (email, password))
        account = cursor.fetchone()

        if account:
            session['loggedin'] = True
            session['id'] = account[0]
            session['name'] = account[1]
            session['email'] = account[2]
            return redirect(url_for('home'))
        else:
            flash('Incorrect email/password!')
    
    return render_template('login.html')













