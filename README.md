# Blog API with Authentication

[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/fastapi-0.104.1-green.svg)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/postgresql-15-blue.svg)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://img.shields.io/badge/tests-passing-green.svg)](https://github.com/dera-delis/blog-api)
[![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-blue.svg)](https://github.com/dera-delis/blog-api/actions)

A secure, production-ready Blog API built with FastAPI, PostgreSQL, and JWT authentication. This project demonstrates modern backend development practices and is perfect for portfolio projects.

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect_with_Me-blue?style=for-the-badge&logo=linkedin)](https://www.linkedin.com/in/dera-delis/)

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   FastAPI App   │    │   PostgreSQL    │    │   Docker        │
│   (Port 8000)   │◄──►│   Database      │    │   Compose       │
│                 │    │                 │    │                 │
│ • JWT Auth      │    │ • User Data     │    │ • Containerized │
│ • REST API      │    │ • Post Data     │    │ • Easy Deploy   │
│ • Auto Docs     │    │ • Migrations    │    │ • Dev/Prod      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │   Pytest        │
                    │   Tests         │
                    │                 │
                    │ • Unit Tests    │
                    │ • Integration   │
                    │ • Coverage      │
                    └─────────────────┘
```

## 🚀 Features

- **User Authentication**: JWT-based authentication with secure password hashing
- **User Management**: Sign up, login, profile management
- **Blog Posts**: Full CRUD operations for blog posts
- **Authorization**: Role-based access control (users can only modify their own content)
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Migrations**: Alembic for database schema management
- **Testing**: Comprehensive unit tests with pytest
- **Docker**: Containerized application with docker-compose
- **API Documentation**: Auto-generated with FastAPI

## 🛠 Tech Stack

- **Backend**: FastAPI (Python 3.11+)
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Authentication**: JWT with python-jose
- **Password Hashing**: bcrypt with passlib
- **Migrations**: Alembic
- **Testing**: pytest
- **Containerization**: Docker & Docker Compose
- **Documentation**: FastAPI auto-generated docs

## 📋 Prerequisites

- Python 3.11 or higher
- Docker and Docker Compose (for containerized setup)
- PostgreSQL (if running locally)

## 🚀 Quick Start

### Option 1: Docker (Recommended)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd blog-api
   ```

2. **Start the application**
   ```bash
   docker-compose up --build
   ```

3. **Access the application**
   - API: http://localhost:8000
   - Interactive API docs: http://localhost:8000/docs
   - Alternative API docs: http://localhost:8000/redoc

### Option 2: Local Development

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd blog-api
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp env.example .env
   # Edit .env with your database credentials
   ```

5. **Set up database**
   ```bash
   # Start PostgreSQL locally or use Docker
   docker run --name postgres -e POSTGRES_PASSWORD=password -e POSTGRES_DB=blog_api -p 5432:5432 -d postgres:15
   ```

6. **Run migrations**
   ```bash
   alembic upgrade head
   ```

7. **Start the application**
   ```bash
   uvicorn app.main:app --reload
   ```

## 🎯 Live Demo

> **🚀 LIVE NOW**: Your Blog API is deployed and ready for recruiters to test!

**Interactive API Documentation**: Test all endpoints directly at:
- **Swagger UI**: `https://blog-api-qnzg.onrender.com/docs`
- **ReDoc**: `https://blog-api-qnzg.onrender.com/redoc`

### 🌐 **Live API Endpoints**

[![Live API](https://img.shields.io/badge/Live_API-Test_Now-green?style=for-the-badge&logo=api)](https://blog-api-qnzg.onrender.com/)

**Click the button above to test your live API!**

**Available at**: `https://blog-api-qnzg.onrender.com/`

## 📸 Screenshots

### FastAPI Swagger UI
![Swagger UI](screenshots/swagger-ui.png)

*Interactive API documentation with automatic request/response examples*

### Docker Containers Running
![Docker Containers](screenshots/docker-containers.png)

*FastAPI app and PostgreSQL database running in Docker containers*

### API Testing Example
![API Testing](screenshots/api-testing.png)

*Example of creating a blog post via API with authentication*

> **📝 To capture these screenshots:**
> 1. **Swagger UI**: Visit `http://localhost:8000/docs` and use browser Dev Tools (F12 → Ctrl+Shift+P → "Capture full size screenshot")
> 2. **Docker**: Run `docker ps` and screenshot the terminal output
> 3. **API Testing**: Use Postman, curl, or browser dev tools to test endpoints

## 📚 API Documentation

### Authentication Endpoints

#### Register User
```http
POST /api/v1/auth/signup
Content-Type: application/json

{
  "email": "user@example.com",
  "username": "username",
  "password": "password123"
}
```

#### Login
```http
POST /api/v1/auth/login
Content-Type: application/x-www-form-urlencoded

username=username&password=password123
```

#### Get Current User
```http
GET /api/v1/auth/me
Authorization: Bearer <access_token>
```

### User Endpoints

#### Get All Users
```http
GET /api/v1/users/?skip=0&limit=100
```

#### Get User by ID
```http
GET /api/v1/users/{user_id}
```

#### Update User
```http
PUT /api/v1/users/{user_id}
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "email": "newemail@example.com",
  "username": "newusername"
}
```

#### Delete User
```http
DELETE /api/v1/users/{user_id}
Authorization: Bearer <access_token>
```

### Post Endpoints

#### Create Post
```http
POST /api/v1/posts/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "title": "My Blog Post",
  "content": "This is the content of my blog post.",
  "published": true
}
```

#### Get All Posts
```http
GET /api/v1/posts/?skip=0&limit=100&published_only=false
```

#### Get Post by ID
```http
GET /api/v1/posts/{post_id}
```

#### Update Post
```http
PUT /api/v1/posts/{post_id}
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "title": "Updated Title",
  "content": "Updated content.",
  "published": true
}
```

#### Delete Post
```http
DELETE /api/v1/posts/{post_id}
Authorization: Bearer <access_token>
```

#### Get User's Posts
```http
GET /api/v1/posts/user/{user_id}?skip=0&limit=100
```

#### Get My Posts
```http
GET /api/v1/posts/my/posts?skip=0&limit=100
Authorization: Bearer <access_token>
```

## 🧪 Testing

### Local Testing

Run the test suite:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_auth.py

# Run with verbose output
pytest -v
```

### Continuous Integration

This project uses **GitHub Actions** for automated testing and code quality checks:

- ✅ **Automated Tests**: Runs on every push and pull request
- ✅ **Code Quality**: Linting with flake8, black, and isort
- ✅ **Coverage Reports**: Test coverage tracking
- ✅ **Database Testing**: PostgreSQL integration tests

**CI/CD Status**: ![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-blue.svg)

## 📁 Project Structure

```
blog-api/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration settings
│   ├── database.py          # Database connection
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   ├── auth.py              # Authentication logic
│   ├── crud.py              # CRUD operations
│   └── routers/
│       ├── __init__.py
│       ├── auth.py          # Authentication routes
│       ├── users.py         # User management routes
│       └── posts.py         # Post management routes
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Test configuration
│   ├── test_auth.py         # Authentication tests
│   └── test_posts.py        # Post tests
├── alembic/                 # Database migrations
├── requirements.txt         # Python dependencies
├── Dockerfile              # Docker configuration
├── docker-compose.yml      # Docker Compose setup
├── alembic.ini             # Alembic configuration
└── README.md               # This file
```

## 🔧 Configuration

The application uses environment variables for configuration. Copy `env.example` to `.env` and modify as needed:

```env
# Database Configuration
DATABASE_URL=postgresql://postgres:password@localhost:5432/blog_api

# JWT Configuration
SECRET_KEY=your-secret-key-here-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Application Configuration
DEBUG=True
API_V1_STR=/api/v1
PROJECT_NAME=Blog API
```

## 🚀 Deployment

### Production Considerations

1. **Security**:
   - Change the default `SECRET_KEY`
   - Use environment variables for sensitive data
   - Configure CORS properly for your domain
   - Use HTTPS in production

2. **Database**:
   - Use a managed PostgreSQL service
   - Set up proper backups
   - Configure connection pooling

3. **Performance**:
   - Use a production ASGI server (Gunicorn + Uvicorn)
   - Set up reverse proxy (Nginx)
   - Configure caching (Redis)

### Docker Production Build

```bash
# Build production image
docker build -t blog-api:prod .

# Run with production settings
docker run -d \
  -p 8000:8000 \
  -e DATABASE_URL=your_production_db_url \
  -e SECRET_KEY=your_production_secret_key \
  blog-api:prod
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) for the amazing web framework
- [SQLAlchemy](https://www.sqlalchemy.org/) for the ORM
- [Alembic](https://alembic.sqlalchemy.org/) for database migrations
- [Pytest](https://docs.pytest.org/) for testing framework

## 📞 Support

If you have any questions or need help, please open an issue on GitHub.

---

## 💼 Portfolio Project

This project is part of my **Backend + AI Portfolio** showcasing modern software development practices. 

### 🎯 What This Demonstrates

- **Backend Development**: Building secure, scalable APIs with FastAPI
- **Database Design**: PostgreSQL with proper relationships and migrations
- **Authentication & Security**: JWT implementation with password hashing
- **Testing**: Comprehensive unit and integration tests
- **DevOps**: Docker containerization and deployment readiness
- **Documentation**: Professional README and API documentation
- **Best Practices**: Clean architecture, error handling, and code organization

### 🔗 More Projects

Check out my other portfolio projects:
- **[GitHub Profile](https://github.com/dera-delis)** - View all my projects
- **[LinkedIn](https://www.linkedin.com/in/dera-delis/)** - Connect with me professionally

### 🚀 Ready for Production

This API is designed to be production-ready with:
- ✅ Security best practices
- ✅ Comprehensive error handling
- ✅ Database migrations
- ✅ Containerized deployment
- ✅ Automated testing
- ✅ Professional documentation

**Perfect for demonstrating backend development skills to potential employers!** 🎯
