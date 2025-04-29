# 用户管理系统 API

基于 Flask 实现的 RESTful 用户管理系统，支持基础账号管理、身份认证和数据增删改查。

背景：大二软工专业、某个无聊的中午心血来潮想用Flask写个接口玩。

## 🌟 功能特点
- ✅ JWT 认证 (待实现)
- 📄 用户信息管理（CRUD）D还未实现因为身份认证还没写
- 🔐 密码加密存储
- 📧 邮箱字段验证
- 🧑‍💼 管理员角色控制
- ⚙️ 模块化架构设计

## ⚙️ 技术栈
| 类别       | 技术/工具          |
|------------|-------------------|
| 后端框架   | Flask             |
| 数据库     | MySQL             |
| 安全验证   | Werkzeug 密码安全 |
| 请求处理   | Request           |
| 架构设计   | MVC 模块分离      |

## 📦 环境依赖

```bash
安装依赖
pip install flask mysql-connector-python werkzeug
或者使用 requirements 文件
pip install -r requirements.txt
```

## 🛠️ 配置要求
在 `config.py` 中配置数据库连接：

```python
class Config: 
    MySQL_HOST = 'localhost' 
    MySQL_USER = 'root' 
    MySQL_PASSWORD = 'your_password' 
    MySQL_DB = 'user_db'
```
## 🚀 快速启动

```bash
创建数据库表（需提前创建 user_db 数据库）
CREATE TABLE users ( 
	id INT AUTO_INCREMENT PRIMARY KEY, 
	username VARCHAR(50) NOT NULL UNIQUE, 
	password VARCHAR(200) NOT NULL, 
	email VARCHAR(100) NOT NULL UNIQUE, 
	create_time DATETIME DEFAULT CURRENT_TIMESTAMP, 
	isadmin TINYINT(1) DEFAULT 0 );
	
启动服务
python app.py

服务器将在 http://127.0.0.1:5000 运行
```

## 🌐 API 文档

### 🔐 身份认证
#### `POST /register` 注册新用户

```json
{ 
    "username": "string (3-20)",
    "password": "string (8-128)",
    "email": "valid-email" 
}
```
**响应成功**: `201 Created`

```json
{ 
    "code": 200, 
    "data": {
        "message": "User registered successfully"
    } 
}
```
#### `POST /login` 登录获取凭证

```json
{ 
    "identity": "username/or email", 
 	"password": "string" 
}
```
**响应成功**: `200 OK`

```json
{ 
    "code": 200, 
    "data": {
        "message": "Login successful"
    } 
}
```
---

### 👥 用户管理
#### `GET /user/:id` 获取用户详情  
**响应成功**: `200 OK`

```json
{ 
	"code": 200, 
	"data": { 
	"id": 1, 
	"username": "testuser",
    "email": "test@example.com" 
    } 
}
```
#### `PUT /user/:id` 更新用户信息

```json
{ 
	"email": "new_email@example.com", 
}
```
**响应成功**: `200 OK`

```json
{ 
    "code": 200, 
    "data": {
        "message": "User updated successfully"
    } 
}
```

#### `DELETE /user/:id` 删除用户  
**响应成功**: `200 OK`

```json
{ 
	"code": 200, 
	"data": {
		"message": "User deleted successfully"
	} 
}
```

---

## 🛑 错误码约定
| Code | 说明                    |
|------|-------------------------|
| 400  | 参数缺失或格式错误      |
| 401  | 未授权访问              |
| 403  | 权限不足                |
| 404  | 资源未找到              |
| 500  | 服务内部异常            |

## 💡 开发建议
1. 生产环境关闭 `app.run(debug=False)`
2. 增加 Redis 缓存用户 sessions
3. 使用 JWT 扩展增强身份体系
4. 添加邮件验证码系统实现双因子认证

## ☕ 演进路线图
- [X] Created project structure
- [X] Implemented basic CRUD
- [ ] Add JWT authentication
- [ ] Integrate OpenAPI documentation
- [ ] Support frontend integration

---

如遇到问题欢迎提交 Issues 或联系作者 3530466993@qq.com
