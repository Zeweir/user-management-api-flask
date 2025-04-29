from flask import request, jsonify
from datetime import datetime
from models import connect_db,error_response,success_response
import mysql.connector
from werkzeug.security import generate_password_hash,check_password_hash
import re

def register_router(app):
    # 获取用户信息
    @app.route('/user/<int:id>', methods=['GET'])
    def get_user(id: int):
        try:
            with connect_db() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT id, username, email FROM users where id = %s", (id,))
                    result = cursor.fetchone()

                    if not result:
                        return jsonify({'error': 'User not found'}), 404

                    # 返回标准响应格式，包含用户ID和用户名，不包含密码
                    return success_response({
                        'id': result[0],
                        'username': result[1],
                        'email': result[2]
                    })
        except mysql.connector.Error as err:
            return jsonify({'error': f'Database error: {str(err)}'}), 500
        except Exception as e:
            return jsonify({'error': f'Server error: {str(e)}'}), 500

    # 注册接口
    @app.route('/register', methods=['POST'])
    def register():
        try:
            # 1. 获取并验证输入数据
            data = request.get_json()

            # 检查请求体是否为空或缺少必要字段
            request_fields = ['username', 'password', 'email']
            if not data or any(field not in data for field in request_fields):
                return jsonify({'error': 'Missing required input'}), 400

            # 用户名和密码
            username = data['username'].strip()
            password = data['password']
            email = data['email']

            # 检查用户名长度
            if len(username) < 3 or len(password) > 20:
                return jsonify({
                    'error': 'Username and password must be at least 3 and 20 characters long'
                }), 400

            # 检查密码长度
            if len(password) < 8 or len(password) > 128:
                return jsonify({
                    'error': 'Password must be at least 8 and 128 characters long'
                }), 400

            # 邮箱格式验证（基础正则）
            if not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
                return jsonify({'error': 'Invalid email format'}), 400

            # 账号密码如果为空 返回400
            if not username or not password:
                return jsonify({'error': 'Username and password cannot be empty'}), 400

            # 2. 密码哈希加密
            hashwd_pw = generate_password_hash(password)

            # 3. 数据库操作
            with connect_db() as conn:
                with conn.cursor() as cursor:
                    # 先检查用户是否存在
                    cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
                    if cursor.fetchone():
                        return jsonify({'error': 'Username already exists'}), 400

                    # 插入新用户
                    cursor.execute(
                        "INSERT INTO users (username, password, email, create_time, isadmin) VALUES (%s, %s, %s, %s, %s)",
                        (username, hashwd_pw, email ,datetime.now(), 0)
                    )
                    # 提交事务
                    conn.commit()
                    return success_response({
                        'message': 'User registered successfully',
                        'username': username
                    }), 201

        except mysql.connector.IntegrityError as e:
            if "Duplicate entry" in str(e) and "email" in str(e):
                return jsonify({'error': 'Email already exists'}), 400
            # 特殊处理唯一性约束冲突（如用户名重复）
            return jsonify({'error': 'Database integrity error: ' + str(e)}), 400
        except mysql.connector.Error as err:
            return jsonify({'error': 'Database error: ' + str(err)}), 500
        except Exception as e:
            return jsonify({'error': 'Server error: ' + str(e)}), 500

    # 登录接口
    @app.route('/login', methods=['POST'])
    def login():
        try:
            # 1. 获取并验证输入数据
            data = request.get_json()
            if not data or 'identity' not in data or 'password' not in data:
                return jsonify({'error': 'Invalid input'}), 400
            # 账号密码
            identity = data['identity'].strip()
            password = data['password']

            # 2. 查询数据库用户
            with connect_db() as conn:
                with conn.cursor() as cursor:
                    # 参数化查询防止SQL注入
                    cursor.execute(
                        "SELECT id,username,password FROM users WHERE username = %s OR email = %s",
                        (identity, identity)
                    )
                    user = cursor.fetchone()

                    # 用户不存在或密码验证失败 返回401
                    if not user or not check_password_hash(user[2],password):
                        return jsonify({
                            'error': 'Invalid username or password'
                        }), 401

                    # 登录成功
                    return success_response({
                        'message': 'Login successful',
                        'username': user[1]
                    }), 200

        except mysql.connector.Error as err:
            return jsonify({'error': 'Database error:' + str(err)}), 500
        except Exception as e:
            return jsonify({'error': 'Server error:' + str(e)}), 500


    @app.route('/user/<int:id>', methods=['PUT'])
    def update_user(id):
        try:
            # 1. 获取并验证输入数据
            data = request.get_json()
            if not data:
                return error_response(400, 'Invalid input')

            # 提取可更新字段
            email = data.get('email', None)

            with connect_db() as conn:
                with conn.cursor() as cursor:
                    # 3. 构建动态更新语句
                    update_fields = []
                    params = []

                    if email is not None:
                        # 验证邮箱格式
                        if not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
                            return error_response(400, 'Invalid email format')

                        # 检查邮箱唯一性
                        cursor.execute("SELECT id FROM users WHERE email = %s AND id != %s", (email, id))
                        if cursor.fetchone():
                            return error_response(400, 'Email already exists')

                        update_fields.append("email = %s")
                        params.append(email)

                    if not update_fields:
                        return error_response(400, 'No valid fields to update')

                    # 4. 执行更新操作
                    params.append(id)
                    sql = f"UPDATE users SET {', '.join(update_fields)} WHERE id = %s"
                    cursor.execute(sql, params)

                    if cursor.rowcount == 0:
                        return error_response(404, 'User not found')

                    conn.commit()
                    return success_response({'message': 'User updated successfully'})

        except mysql.connector.IntegrityError as e:
            return error_response(400, f'Database integrity error: {str(e)}')
        except mysql.connector.Error as err:
            return error_response(500, f'Database error: {str(err)}')
        except Exception as e:
            return error_response(500, f'Server error: {str(e)}')
