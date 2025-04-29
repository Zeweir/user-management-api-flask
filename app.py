from flask import Flask
from routes import register_router

# 初始化Flask应用
app = Flask(__name__)

# 注册所有路由
register_router(app)

if __name__ == '__main__':
    app.run(debug=True)