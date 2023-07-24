from flask import Flask, render_template, redirect, request, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import pytz

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ab#1867$@817'  # Replace with a strong random key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'  # Database filename

db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

# User model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return "<User {}>".format(self.username)

# Load user function required by Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Topic model for the database table
class Topic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    topic_image = db.Column(db.String(200), nullable=False)
    topic_name = db.Column(db.String(100), nullable=False)
    topic_details = db.Column(db.Text, nullable=False)
    pdf_link = db.Column(db.String(200), nullable=False)

# Create the database and the tables
db.create_all()

# Admin Page - Add New Topic
@app.route('/admin', methods=['GET', 'POST'])
def admin_page():
    if request.method == 'POST':
        if current_user.is_authenticated and current_user.username == "admin":
            topic_image = request.form['topicImage']
            topic_name = request.form['topicName']
            topic_details = request.form['topicDetails']
            pdf_link = request.form['pdfLink']

            # Store the topic data in the database
            new_topic = Topic(
                topic_image=topic_image,
                topic_name=topic_name,
                topic_details=topic_details,
                pdf_link=pdf_link
            )
            db.session.add(new_topic)
            db.session.commit()

            return redirect(url_for('main_page'))

    return render_template('admin.html')

# Main Website Page
@app.route('/')
def main_page():
    # Fetch all topics from the database
    topics = Topic.query.all()
    return render_template('main.html', topics=topics)

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

        user = User.query.filter_by(username=username).first()

        if user:
            flash('Username already exists. Please choose a different username.', 'error')
        else:
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                flash('Email already exists. Please choose a different email.', 'error')
            else:
                hashed_password = generate_password_hash(password)
                new_user = User(username=username, email=email, password=hashed_password)
                db.session.add(new_user)
                db.session.commit()
                flash('Registration successful. You can now log in.', 'success')
                return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.', 'success')
    return redirect(url_for('login'))

@app.route('/users')
@login_required
def list_users():
    if current_user.username == "admin":
        users = User.query.all()
        return render_template('user_list.html', users=users)
    else:
        flash("You do not have permission to access the Admin page.", 'error')
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
                flash("User '{}' has been deleted.".format(user.username), 'success')
            else:
                flash("User not found.", 'error')
    else:
        flash("You do not have permission to perform this action.", 'error')
    return redirect(url_for('list_users'))

if __name__ == '__main__':
    app.run(debug=True)
