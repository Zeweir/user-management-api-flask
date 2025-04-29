from config import Config
import mysql.connector
from flask import jsonify
def connect_db():
    return mysql.connector.connect(
        host=Config.MySQL_HOST,
        user=Config.MySQL_USER,
        password=Config.MySQL_PASSWORD,
        database=Config.MySQL_DB
    )

def success_response(data=None):
    return jsonify({
        'code': 200,
        'data': data or {}
    }), 200

def error_response(code, message):
    return jsonify({
        'code': code,
        'error': message
    }), code
