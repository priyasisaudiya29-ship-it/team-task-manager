# Railway Deployment Guide

## Prerequisites

- GitHub account with the repository pushed
- Railway account (railway.app)
- Git installed

## Deployment Steps

### 1. Push to GitHub

```bash
git add .
git commit -m "Prepare for Railway deployment"
git push origin main
```

### 2. Connect to Railway

1. Go to [railway.app](https://railway.app)
2. Sign up / Login with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your `team-task-manager` repository
5. Click "Deploy"

### 3. Configure Environment Variables

In Railway Dashboard:

1. Go to your project
2. Click on the service (web)
3. Go to "Variables" tab
4. Add the following environment variables:
   - `DEBUG=False`
   - `SECRET_KEY=<generate-a-strong-secret-key>`
   - `ALLOWED_HOSTS=your-app-name.up.railway.app`
   - `SECURE_SSL_REDIRECT=False`
   - `SESSION_COOKIE_SECURE=False`
   - `CSRF_COOKIE_SECURE=False`

### 4. Generate Secret Key

Run this locally and copy the output to `SECRET_KEY`:

```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

### 5. Database Setup

Railway will automatically run migrations via the `release` command in Procfile.

### 6. Verify Deployment

- Wait for the build to complete (check logs)
- Click on the generated URL to access your app
- Admin panel: `https://your-app.up.railway.app/admin`

## Troubleshooting

### Build Failures

- Check Railway logs: Dashboard → Logs tab
- Ensure all requirements in `requirements.txt` are correct
- Verify Python version in `runtime.txt`

### Static Files Not Loading

- Railway automatically runs `python manage.py collectstatic`
- Check `STATIC_ROOT` and `STATIC_URL` in settings.py

### Database Issues

- Check if migrations ran: Dashboard → Deployments → Release logs
- Manually run migrations via Railway CLI if needed

### Port Issues

- Railway automatically assigns `$PORT` environment variable
- Procfile uses `$PORT` binding

## Post-Deployment

### Update SECRET_KEY

1. Generate a new secure key (see step 4)
2. Update `SECRET_KEY` variable in Railway dashboard
3. Restart the deployment

### Enable HTTPS (Auto)

Railway automatically provides HTTPS for your custom domain.

### Custom Domain

1. Go to Railway Dashboard
2. Select your service
3. Go to "Settings" → "Domain"
4. Add your custom domain and configure DNS

## Rollback

If deployment fails:

1. Railway keeps previous builds
2. Go to "Deployments" tab
3. Select a previous stable version
4. Click "Rollback"

## Support

- Railway Docs: https://docs.railway.app
- Django Deployment: https://docs.djangoproject.com/en/stable/howto/deployment/

---

**Last Updated**: May 2026
