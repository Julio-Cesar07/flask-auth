from flask import Flask, request, jsonify
from database import db
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from models.user import User

app = Flask(__name__)

app.config['SECRET_KEY'] = "your_secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.sqlite3"

login_manager = LoginManager()

login_manager.login_view = 'login'

db.init_app(app)
login_manager.init_app(app)

@app.route('/api')
def api():
    return 'ok'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route('/login', methods=["POST"])
def login():
    data = request.json
    
    username = data.get('username')
    password = data.get('password')

    if username and password:
        user = User.query.filter_by(username=username).first()
                
        if user and user.password == password:
            login_user(user)
            return jsonify({'message': "Authenticate"}), 200
    
    return jsonify({'message': "Invalid Credentials"}), 400

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logout"})

@app.route('/user', methods=["POST"])
def create_user():
    data = request.json
    
    username = data.get('username')
    password = data.get('password')

    if username and password:
        usernameAlreadyExist = User.query.filter_by(username=username).first()

        if usernameAlreadyExist:
            return jsonify({"message": "Username already exist."}), 409

        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return jsonify({'message': 'User registered.'})
        
    return jsonify({'message': f"Invalid data{', password' if username else (', username' if password else ', username and password')} not provided."}), 400  

@app.route('/me', methods=["GET"])
@login_required
def get_user():
    user = User.query.get(current_user.id)
    
    if user:
        return {"username": user.username}
        
    return jsonify({'message': 'User not found'}), 404

@app.route('/user', methods=["PUT"])
@login_required
def update_user():
    data = request.json
    
    password = data.get('password')
    
    if password:
        user = User.query.get(current_user.id)

        if user:
            user.password = password
            
            db.session.commit()
            return jsonify({'message': 'Updated successfully'})
        
        return jsonify({'message': 'User not found'}), 404
    
    return jsonify({'message': f"Invalid data, password not provided."}), 400  

@app.route('/user', methods=["DELETE"])
@login_required
def delete_user():
    user = User.query.get(current_user.id)

    if user:
        logout_user()
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'Deleted successfully'})
    
    return jsonify({'message': 'User not found'}), 404

with app.app_context():
    db.create_all()
    db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)