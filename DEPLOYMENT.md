# 🚀 Deployment Guide for Recruiters

This guide will help you deploy your Blog API live so recruiters can see it in action!

## 🌟 **Quick Deploy to Northflank (Recommended)**

### **Step 1: Prepare Your Repository**
1. Make sure your code is pushed to GitHub
2. Ensure you have these files in your repo:
   - `Dockerfile` ✅
   - `requirements.txt` ✅
   - `app/main.py` ✅
   - `northflank.yaml` ✅ (configuration reference)

### **Step 2: Deploy to Northflank**

#### **Option A: Using Northflank Web UI (Easiest)**

1. Go to [northflank.com](https://northflank.com) and sign up/login
2. Click **"New Project"** or select an existing project
3. Click **"Add Service"** → **"Container Service"**
4. Connect your GitHub repository
5. Configure the service:
   - **Name**: `blog-api`
   - **Build Type**: Dockerfile
   - **Dockerfile Path**: `Dockerfile`
   - **Port**: `8000`
   - **Public Port**: Enable (for HTTP access)
6. Add environment variables:
   - `DATABASE_URL` (will be set after creating database)
   - `SECRET_KEY` (generate a secure random string)
   - `ALGORITHM=HS256`
   - `ACCESS_TOKEN_EXPIRE_MINUTES=30`
   - `DEBUG=false`
   - `API_V1_STR=/api/v1`
   - `PROJECT_NAME=Blog API`
7. Create a PostgreSQL database:
   - Click **"Add Service"** → **"Database"** → **"PostgreSQL"**
   - **Name**: `blog-api-db`
   - **Version**: `15`
   - **Database Name**: `blog_api`
8. Link the database to your service:
   - In your service settings, set `DATABASE_URL` to the connection string provided by Northflank
9. Click **"Deploy"** and wait for deployment

#### **Option B: Using Northflank CLI**

1. Install Northflank CLI:
   ```bash
   npm install -g @northflank/cli
   # or
   curl -fsSL https://cli.northflank.com/install.sh | sh
   ```

2. Login to Northflank:
   ```bash
   nf login
   ```

3. Create a project:
   ```bash
   nf project create blog-api-project
   ```

4. Create the database service:
   ```bash
   nf service create database blog-api-db \
     --type postgresql \
     --version 15 \
     --database blog_api
   ```

5. Create the application service:
   ```bash
   nf service create container blog-api \
     --dockerfile Dockerfile \
     --port 8000 \
     --public \
     --env DATABASE_URL=<database-connection-string> \
     --env SECRET_KEY=<your-secret-key> \
     --env ALGORITHM=HS256 \
     --env ACCESS_TOKEN_EXPIRE_MINUTES=30 \
     --env DEBUG=false \
     --env API_V1_STR=/api/v1 \
     --env PROJECT_NAME="Blog API"
   ```

6. Deploy:
   ```bash
   nf service deploy blog-api
   ```

### **Step 3: Access Your Live API**
- **API Base URL**: `https://your-service-name.northflank.app`
- **Interactive Docs**: `https://your-service-name.northflank.app/docs`
- **Health Check**: `https://your-service-name.northflank.app/health`

## 🎯 **What Recruiters Will See**

### **Live API Endpoints**
- ✅ **Authentication**: `/api/v1/auth/signup`, `/api/v1/auth/login`
- ✅ **User Management**: `/api/v1/users/`
- ✅ **Blog Posts**: `/api/v1/posts/`
- ✅ **Interactive Documentation**: Swagger UI at `/docs`

### **Professional Features**
- 🔐 **JWT Authentication** with secure password hashing
- 🗄️ **PostgreSQL Database** with proper relationships
- 📝 **Database Migrations** using Alembic
- 🧪 **Comprehensive Testing** with pytest
- 🐳 **Docker Containerization**
- 📚 **Auto-generated API Documentation**

## 🔧 **Alternative Deployment Options**

### **Railway.app**
- Free tier: $5 monthly credit
- Very simple deployment
- PostgreSQL included

### **Fly.io**
- Free tier: 3 shared-cpu VMs
- Global deployment
- PostgreSQL available

### **Heroku**
- Free tier discontinued
- Paid plans available
- Very reliable

## 📱 **Testing Your Live API**

### **1. Health Check**
```bash
curl https://your-service-name.northflank.app/health
```

### **2. Create a User**
```bash
curl -X POST "https://your-service-name.northflank.app/api/v1/auth/signup" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "username": "testuser",
    "password": "password123"
  }'
```

### **3. Login**
```bash
curl -X POST "https://your-service-name.northflank.app/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=testuser&password=password123"
```

### **4. Create a Blog Post**
```bash
curl -X POST "https://your-service-name.northflank.app/api/v1/posts/" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My First Blog Post",
    "content": "This is the content of my blog post.",
    "published": true
  }'
```

## 🌐 **Share with Recruiters**

### **Portfolio Links**
- **Live API**: `https://your-service-name.northflank.app`
- **Interactive Docs**: `https://your-service-name.northflank.app/docs`
- **GitHub Repo**: `https://github.com/yourusername/blog-api`
- **README**: `https://github.com/yourusername/blog-api#readme`

### **What This Demonstrates**
- ✅ **Backend Development**: FastAPI with modern Python practices
- ✅ **Database Design**: PostgreSQL with SQLAlchemy ORM
- ✅ **Authentication**: JWT implementation with security
- ✅ **API Design**: RESTful endpoints with proper documentation
- ✅ **Testing**: Comprehensive test coverage
- ✅ **DevOps**: Containerization and deployment
- ✅ **Documentation**: Professional README and API docs

## 🚨 **Troubleshooting**

### **Common Issues**
1. **Build Fails**: Check `requirements.txt` and Python version in Dockerfile
2. **Database Connection**: Ensure `DATABASE_URL` is set correctly and database is running
3. **Port Issues**: Northflank automatically handles port mapping
4. **CORS Errors**: Check CORS configuration in `main.py`
5. **Migrations**: Run Alembic migrations after database is created:
   ```bash
   # In Northflank, use the service shell or add a one-time job
   alembic upgrade head
   ```

### **Get Help**
- Check Northflank deployment logs in the dashboard
- Review GitHub Actions CI/CD
- Test locally with Docker first
- Northflank Support: [support.northflank.com](https://support.northflank.com)

## 🎉 **Success!**

Once deployed, your Blog API will be live and accessible to recruiters worldwide! They can:
- Test all endpoints interactively
- See your code quality and architecture
- Understand your technical skills
- Experience your API in real-time

**Perfect for showcasing your backend development skills!** 🚀

## 📝 **Northflank Advantages**

- ✅ **Multi-Cloud Support**: Deploy across AWS, GCP, Azure, and more
- ✅ **Kubernetes Simplified**: Automatic Kubernetes management
- ✅ **Great Developer Experience**: UI, CLI, and API interfaces
- ✅ **CI/CD Integration**: Automatic builds and deployments
- ✅ **High-Quality Support**: Excellent customer support
- ✅ **Scalable**: Easy to scale as your project grows
