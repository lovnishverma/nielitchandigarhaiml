from flask import Flask, render_template, redirect, request, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import pytz
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ab#1867$@817'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

# Ensure visitor count file exists
if not os.path.exists("visitor_count.txt"):
    with open("visitor_count.txt", "w") as f:
        f.write("0")

# Initialize extensions
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# ---------------------- MODELS ----------------------
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"<User {self.username}>"

class Topic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    topic_image = db.Column(db.String(200), nullable=False)
    topic_name = db.Column(db.String(100), nullable=False)
    topic_details = db.Column(db.Text, nullable=False)
    pdf_link = db.Column(db.String(200), nullable=False)

# ---------------------- LOGIN MANAGER ----------------------
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ---------------------- ROUTES ----------------------
@app.route('/')
@login_required
def dashboard():
    def get_visitor_count():
        with open("visitor_count.txt", "r") as f:
            count = int(f.read())
        count += 1
        with open("visitor_count.txt", "w") as f:
            f.write(str(count))
        return count

    utc_now = datetime.utcnow()
    tz = pytz.timezone('Asia/Kolkata')
    india_time = utc_now + timedelta(seconds=tz.utcoffset(utc_now).total_seconds())
    date = india_time.strftime("%Y-%m-%d")
    time = india_time.strftime("%I:%M %p")
    year = india_time.strftime("%Y")
    india_hour = india_time.hour

    if 5 <= india_hour < 12:
        time_of_day = 'Morning'
    elif 12 <= india_hour < 17:
        time_of_day = 'Afternoon'
    elif 17 <= india_hour < 21:
        time_of_day = 'Evening'
    else:
        time_of_day = 'Night'

    visitor_count = get_visitor_count()
    username = current_user.username
    topics = Topic.query.all()

    return render_template("main.html", topics=topics, username=username, time_of_day=time_of_day,
                           date=date, time=time, year=year, visitor_count=visitor_count)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Logged in successfully.', 'success')
            return redirect(url_for('dashboard'))

        flash('Invalid username or password.', 'error')

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        if User.query.filter_by(username=username).first():
            flash('Username already exists.', 'error')
        elif User.query.filter_by(email=email).first():
            flash('Email already exists.', 'error')
        else:
            hashed_password = generate_password_hash(password)
            new_user = User(username=username, email=email, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful. You can now log in.', 'success')
            return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/users')
@login_required
def list_users():
    if current_user.username == "admin":
        users = User.query.all()
        return render_template('user_list.html', users=users)
    flash("Access denied.", 'error')
    return redirect(url_for('dashboard'))

@app.route('/delete_user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    if current_user.username == "admin":
        if current_user.id == user_id:
            flash("You cannot delete your own account.", 'error')
        else:
            user = User.query.get(user_id)
            if user:
                db.session.delete(user)
                db.session.commit()
                flash(f"User '{user.username}' deleted.", 'success')
            else:
                flash("User not found.", 'error')
    else:
        flash("Action not permitted.", 'error')
    return redirect(url_for('list_users'))

@app.route('/admin')
@login_required
def admin_panel():
    if current_user.username == "admin":
        return render_template('admin_panel.html')
    flash("Access denied.", 'error')
    return redirect(url_for('dashboard'))

@app.route('/admin/add_topic', methods=['GET', 'POST'])
@login_required
def add_topic():
    if current_user.username == "admin":
        if request.method == 'POST':
            topic = Topic(
                topic_image=request.form['topicImage'],
                topic_name=request.form['topicName'],
                topic_details=request.form['topicDetails'],
                pdf_link=request.form['pdfLink']
            )
            db.session.add(topic)
            db.session.commit()
            flash("Topic added.", 'success')
            return redirect(url_for('admin_panel'))
        return render_template('add_topic.html')
    flash("Access denied.", 'error')
    return redirect(url_for('dashboard'))

@app.route('/admin/list_topics')
@login_required
def list_topics():
    if current_user.username == "admin":
        topics = Topic.query.all()
        return render_template('list_topics.html', topics=topics)
    flash("Access denied.", 'error')
    return redirect(url_for('dashboard'))

@app.route('/admin/modify_topic/<int:topic_id>', methods=['GET', 'POST'])
@login_required
def modify_topic(topic_id):
    if current_user.username == "admin":
        topic = Topic.query.get(topic_id)
        if not topic:
            flash("Topic not found.", 'error')
            return redirect(url_for('admin_panel'))

        if request.method == 'POST':
            topic.topic_image = request.form['topicImage']
            topic.topic_name = request.form['topicName']
            topic.topic_details = request.form['topicDetails']
            topic.pdf_link = request.form['pdfLink']
            db.session.commit()
            flash("Topic updated.", 'success')
            return redirect(url_for('admin_panel'))

        return render_template('modify_topic.html', topic=topic)
    flash("Access denied.", 'error')
    return redirect(url_for('dashboard'))

@app.route('/admin/delete_topic/<int:topic_id>', methods=['POST'])
@login_required
def delete_topic(topic_id):
    if current_user.username == "admin":
        topic = Topic.query.get(topic_id)
        if topic:
            db.session.delete(topic)
            db.session.commit()
            flash("Topic deleted.", 'success')
        else:
            flash("Topic not found.", 'error')
    return redirect(url_for('admin_panel'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out.', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
