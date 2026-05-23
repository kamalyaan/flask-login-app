from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User
from config import Config

# 1. Create app first
app = Flask(__name__)
app.config.from_object(Config)

# 2. Initialize db and login
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# 3. Create routes - after app is created
@app.route('/')
def home():
    return 'Server is running! ✅ <br><a href="/register">Register</a> | <a href="/login">Login</a>'

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        if User.query.filter_by(username=username).first():
            return 'Username already exists! <a href="/register">Go back</a>'
        
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return 'Account created successfully! <a href="/login">Login now</a>'
    
    return '''
    <form method="POST">
        <h2>Register</h2>
        Username: <input name="username" required><br><br>
        Email: <input name="email" type="email" required><br><br>
        Password: <input name="password" type="password" required><br><br>
        <button type="submit">Register</button>
        <br><br><a href="/login">Already have an account? Login</a>
    </form>
    '''

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            return f'Login successful! Welcome {username} <br><a href="/dashboard">Go to Dashboard</a>'
        return 'Invalid username or password <a href="/login">Try again</a>'
    
    return '''
    <form method="POST">
        <h2>Login</h2>
        Username: <input name="username" required><br><br>
        Password: <input name="password" type="password" required><br><br>
        <button type="submit">Login</button>
        <br><br><a href="/register">Create new account</a>
    </form>
    '''

@app.route('/dashboard')
@login_required
def dashboard():
    return f'''
    <h2>Welcome {current_user.username}!</h2>
    <p>Email: {current_user.email}</p>
    <p>This is a protected page. You cannot access it without login.</p>
    <a href="/logout">Logout</a>
    '''

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return 'Logged out successfully! <a href="/login">Login</a> | <a href="/">Home</a>'

# 4. Start server at the end
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("Database is ready")
    
    print("Starting server...")
    app.run(host='0.0.0.0', port=5000, debug=True)
