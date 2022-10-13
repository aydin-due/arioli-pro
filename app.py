from flask import Flask, render_template, request, Response, jsonify, url_for, redirect
import database as db
from models.user import User

db = db.dbConnection()
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/account')
def account():
    return render_template('account.html')

@app.errorhandler(404)
def not_found(error=None):
    message = {
        'message': 'Resource not found: ' + request.url,
        'status': '404 Not Found'
    }
    response = jsonify(message)
    response.status_code = 404
    return response

if __name__ == '__main__':
    app.run(debug=True, port=4000)