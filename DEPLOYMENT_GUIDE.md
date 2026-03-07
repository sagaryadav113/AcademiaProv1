# AcademiaPro Deployment Guide

## ✅ Completed Security Improvements

Your application has been secured with:

1. **Environment Variables** - All API keys and secrets now use `.env` files
2. **Configuration Management** - Separate configs for development, testing, and production  
3. **CORS Security** - Restricted to specific origins (configurable)
4. **Security Headers** - Added X-Frame-Options, X-Content-Type-Options, and more
5. **Session Security** - HTTPOnly, Secure, and SameSite cookies configured
6. **Logging** - Added proper logging for monitoring
7. `.gitignore` - Prevents accidental commits of sensitive files
8. `requirements.txt` - Lock dependencies for reproducibility

---

## 🚀 Deployment Steps

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Create Production `.env` File
Copy `.env.example` to `.env` and update with production values:
```bash
cp .env.example .env
```

Edit `.env` with:
- Real Google API key
- Real SECRET_KEY (use a strong random key)
- Production domain in CORS_ORIGINS
- Production settings

**Generate a strong SECRET_KEY:**
```python
import secrets
print(secrets.token_hex(32))
```

### Step 3: Set Environment Variables for Production
```bash
set FLASK_ENV=production
set FLASK_DEBUG=False
```

Or in your hosting platform's environment settings.

### Step 4: Run with Gunicorn (Production Server)
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

Parameters:
- `-w 4`: Use 4 worker processes
- `-b 0.0.0.0:5000`: Bind to all interfaces on port 5000
- Adjust worker count based on CPU cores

### Step 5: Use Reverse Proxy (Nginx/Apache)
Example Nginx configuration:
```nginx
upstream academiapro {
    server 127.0.0.1:5000;
}

server {
    listen 80;
    server_name yourdomain.com;
    
    location / {
        proxy_pass http://academiapro;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Step 6: Enable HTTPS
Use Let's Encrypt with Certbot:
```bash
sudo certbot certonly --standalone -d yourdomain.com
```

### Step 7: Setup Database (Optional)
For production data persistence, consider:
- SQLite (simple)
- PostgreSQL (scalable)
- MongoDB (flexible)

---

## 📋 Pre-Deployment Checklist

- [ ] Change `SECRET_KEY` to a strong random value
- [ ] Update `CORS_ORIGINS` to your production domain
- [ ] Set `FLASK_ENV=production`
- [ ] Set `FLASK_DEBUG=False`
- [ ] Verify all API keys are in `.env`, not in code
- [ ] Test locally: `python app.py`
- [ ] Run with Gunicorn: `gunicorn app:app`
- [ ] Setup HTTPS/SSL certificate
- [ ] Configure database backups
- [ ] Setup logging/monitoring
- [ ] Test all features in production environment
- [ ] Review and test file upload limits
- [ ] Setup automated cleanup for temp files
- [ ] Monitor API usage/costs

---

## 🔒 Security Best Practices

1. **Never commit `.env` file** - It's in `.gitignore`
2. **Rotate API keys periodically** - Update GOOGLE_API_KEY every 90 days
3. **Monitor API usage** - Track quota usage at Google Cloud Console
4. **Use strong SECRET_KEY** - At least 32 characters of random data
5. **Enable HTTPS only** - Never serve over HTTP in production
6. **Regular backups** - Backup uploads/ and vault_storage/ folders
7. **Update dependencies** - Run `pip install --upgrade -r requirements.txt`
8. **Rate limiting** - Consider adding Flask-Limiter for API protection
9. **Input validation** - All file uploads are validated by extension and size
10. **Error handling** - Sensitive errors are not shown to users

---

## 📊 Monitoring & Logs

Logs are written to console. For production, redirect to file:
```bash
gunicorn app:app > logs/access.log 2>&1 &
```

Monitor these metrics:
- API error rates
- File upload success/failure
- Cleanup process execution  
- Database/storage usage

---

## ⚠️ Known Limitations

1. **Windows-specific**:
   - `win32com.client` requires Windows (PDF to PPTX conversion)
   - For Linux: Use `libreoffice` alternative or cloud service

2. **File System**:
   - Currently uses local file storage
   - For scalability, migrate to S3/Cloud Storage

3. **Single Server**:
   - Deploy to multiple servers with load balancer
   - Use Redis for session management

---

## 🆘 Troubleshooting

**Issue**: `GOOGLE_API_KEY not found`
- Solution: Ensure `.env` file exists with GOOGLE_API_KEY set

**Issue**: Pop unsupported format error
- Solution: Ensure Poppler is installed at POPPLER_PATH

**Issue**: CORS errors in browser
- Solution: Update CORS_ORIGINS to match frontend domain

**Issue**: File uploads fail
- Solution: Check MAX_FILE_SIZE and disk space

---

## 📞 Support

For issues:
1. Check logs first
2. Verify environment variables
3. Test API keys independently
4. Review error messages carefully

Good luck with your deployment! 🚀
