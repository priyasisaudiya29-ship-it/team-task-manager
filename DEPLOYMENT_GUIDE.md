# Complete Deployment Checklist & Setup Guide

## ✅ Local Testing (Before Pushing to Railway)

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run Migrations

```bash
python manage.py migrate
```

### 3. Create Superuser

```bash
python manage.py createsuperuser
```

### 4. Run Development Server

```bash
python manage.py runserver
```

Access:

- Frontend: http://localhost:8000/
- Admin: http://localhost:8000/admin/

### 5. Test All Features

- [ ] Sign up new account
- [ ] Login with credentials
- [ ] Create a project
- [ ] Create a task in the project
- [ ] View dashboard
- [ ] Access admin panel
- [ ] Test API endpoints at /api/

---

## 🚀 Deploy to Railway

### Prerequisites

- [ ] All local tests passing
- [ ] Code committed to GitHub
- [ ] No errors in local test run

### Deployment Steps

1. **Push to GitHub**

   ```bash
   git add .
   git commit -m "Ready for production deployment"
   git push origin main
   ```

2. **Connect to Railway**
   - Visit https://railway.app
   - Create new project from GitHub repo
   - Select `team-task-manager`

3. **Set Environment Variables in Railway**

   Go to Railway Dashboard → Your Service → Variables tab

   **Required Variables:**

   ```
   DEBUG=False
   SECRET_KEY=<GENERATE NEW STRONG KEY>
   ALLOWED_HOSTS=.railway.app,your-domain.com
   SECURE_SSL_REDIRECT=False
   SESSION_COOKIE_SECURE=False
   CSRF_COOKIE_SECURE=False
   ```

4. **Generate Strong SECRET_KEY**
   Run locally:

   ```bash
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

   Copy output and paste into Railway `SECRET_KEY` variable

5. **Deploy**
   - Railway automatically deploys on push
   - Check "Deployments" tab for build status
   - Wait 2-5 minutes for build to complete

6. **Verify Deployment**
   - Open the provided Railway URL
   - Should see login page
   - Admin panel at /admin/

---

## 🐛 Troubleshooting

### Issue: "ModuleNotFoundError: No module named X"

**Solution:**

- Add package to `requirements.txt`
- Push changes: `git push origin main`
- Railway will rebuild automatically

### Issue: Templates not loading (500 error)

**Solution:**

- Check `TEMPLATES['DIRS']` in settings.py
- Verify all templates exist in `core/templates/core/`
- Check Railway logs for details

### Issue: Static files not loading (CSS/JS broken)

**Solution:**

- Run locally: `python manage.py collectstatic`
- Verify `STATIC_ROOT` and `STATIC_URL` in settings.py
- Railway runs this automatically during deployment

### Issue: Database errors (migrate failing)

**Solution:**

- Check Railway logs under "Release" tab
- Verify migrations in `core/migrations/`
- Local test: `python manage.py migrate`

### Issue: Can't access admin panel

**Solution:**

- Create superuser in Railway shell or locally
- SSH into Railway container and run:
  ```bash
  python manage.py createsuperuser
  ```

### View Deployment Logs

In Railway Dashboard:

1. Click your service
2. "Deployments" tab → Select deployment
3. "Build" tab - See build logs
4. "Runtime" tab - See app logs

---

## 🔐 Security Checklist

Before deploying to production:

- [ ] `DEBUG=False` in Railway
- [ ] Strong `SECRET_KEY` set (not default)
- [ ] `ALLOWED_HOSTS` configured correctly
- [ ] Database backups enabled (if using Railway Postgres)
- [ ] Admin users created with strong passwords
- [ ] HTTPS enabled (Railway provides this automatically)
- [ ] Sensitive data in environment variables (not code)

---

## 📊 Monitoring

After deployment:

1. **Check Application Health**
   - Visit your Railway URL
   - Test login/signup
   - Create test project/task

2. **Monitor Logs**
   - Railway Dashboard → Logs tab
   - Watch for errors in real-time

3. **Database Health**
   - Railway Dashboard → Data tab (if using Railway Postgres)
   - Check storage usage

---

## 🔄 Updates & Redeploy

To update code on production:

```bash
git add .
git commit -m "Update description"
git push origin main
```

Railway automatically redeploys on push.

---

## 🛑 Rollback

If deployment fails:

1. Go to Railway Dashboard
2. Deployments tab
3. Select previous working version
4. Click "Rollback"

---

## 📞 Support

- Railway Docs: https://docs.railway.app
- Django Docs: https://docs.djangoproject.com
- Check logs for detailed error messages

---

**Last Updated:** May 2026  
**Status:** ✅ Ready for Production
