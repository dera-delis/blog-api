# 🚀 Deployment Guide for Recruiters

This guide will help you deploy your Blog API live so recruiters can see it in action!

## 🌟 **Quick Deploy to Render.com (Recommended)**

### **Step 1: Prepare Your Repository**
1. Make sure your code is pushed to GitHub
2. Ensure you have these files in your repo:
   - `render.yaml` ✅
   - `requirements.txt` ✅
   - `app/main.py` ✅

### **Step 2: Deploy to Render**
1. Go to [render.com](https://render.com) and sign up/login
2. Click **"New +"** → **"Blueprint"**
3. Connect your GitHub repository
4. Render will automatically detect the `render.yaml` file
5. Click **"Apply"** and wait for deployment

### **Step 3: Access Your Live API**
- **API Base URL**: `https://your-app-name.onrender.com`
- **Interactive Docs**: `https://your-app-name.onrender.com/docs`
- **Health Check**: `https://your-app-name.onrender.com/health`

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
curl https://your-app-name.onrender.com/health
```

### **2. Create a User**
```bash
curl -X POST "https://your-app-name.onrender.com/api/v1/auth/signup" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "username": "testuser",
    "password": "password123"
  }'
```

### **3. Login**
```bash
curl -X POST "https://your-app-name.onrender.com/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=testuser&password=password123"
```

### **4. Create a Blog Post**
```bash
curl -X POST "https://your-app-name.onrender.com/api/v1/posts/" \
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
- **Live API**: `https://your-app-name.onrender.com`
- **Interactive Docs**: `https://your-app-name.onrender.com/docs`
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
1. **Build Fails**: Check `requirements.txt` and Python version
2. **Database Connection**: Ensure `DATABASE_URL` is set correctly
3. **Port Issues**: Render uses `$PORT` environment variable
4. **CORS Errors**: Check CORS configuration in `main.py`

### **Get Help**
- Check Render deployment logs
- Review GitHub Actions CI/CD
- Test locally with Docker first

## 🎉 **Success!**

Once deployed, your Blog API will be live and accessible to recruiters worldwide! They can:
- Test all endpoints interactively
- See your code quality and architecture
- Understand your technical skills
- Experience your API in real-time

**Perfect for showcasing your backend development skills!** 🚀
