# Sleep Science Bot - Setup Instructions

This guide will help you set up the Sleep Science Explainer Bot project on your local machine.

## Prerequisites

- Python 3.9 or higher
- Node.js 18 or higher
- PostgreSQL (free tier available)
- AWS Account with Bedrock access

## 1. Database Setup (PostgreSQL)

### Option A: Local PostgreSQL Installation

1. **Install PostgreSQL:**
   - **macOS:** `brew install postgresql`
   - **Ubuntu/Debian:** `sudo apt-get install postgresql postgresql-contrib`
   - **Windows:** Download from [postgresql.org](https://www.postgresql.org/download/windows/)

2. **Start PostgreSQL service:**
   - **macOS:** `brew services start postgresql`
   - **Ubuntu/Debian:** `sudo systemctl start postgresql`
   - **Windows:** PostgreSQL service should start automatically

3. **Create database:**
   ```bash
   # Connect to PostgreSQL
   psql -U postgres
   
   # Create database
   CREATE DATABASE sleep_science_bot;
   
   # Create user (optional)
   CREATE USER sleepbot WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE sleep_science_bot TO sleepbot;
   
   # Exit
   \q
   ```

### Option B: Free Cloud PostgreSQL (Recommended for Demo)

1. **Sign up for a free PostgreSQL service:**
   - [Neon](https://neon.tech) - Free tier with 3GB storage
   - [Supabase](https://supabase.com) - Free tier with 500MB storage
   - [Railway](https://railway.app) - Free tier available

2. **Get your database URL** (it will look like):
   ```
   postgresql://username:password@host:port/database
   ```

## 2. AWS Bedrock Setup

### Step 1: AWS Account Setup
1. Go to [AWS Console](https://aws.amazon.com/console/)
2. Sign in or create an account
3. Navigate to **Amazon Bedrock** service

### Step 2: Enable Bedrock Access
1. In the Bedrock console, click **"Get started"**
2. Accept the terms and conditions
3. Request access to the models you need:
   - **Anthropic Claude 3 Sonnet** (recommended)
   - **Anthropic Claude 3 Haiku** (faster, cheaper)
   - **Amazon Titan** (alternative)

### Step 3: Create IAM User (for API access)
1. Go to **IAM Console** → **Users** → **Create user**
2. Name: `sleep-science-bot`
3. Select **"Programmatic access"**
4. Attach policy: `AmazonBedrockFullAccess` (or create custom policy)
5. **Save the Access Key ID and Secret Access Key**

### Step 4: Configure AWS CLI (Optional but Recommended)
```bash
# Install AWS CLI
pip install awscli

# Configure credentials
aws configure

# Enter your credentials:
# AWS Access Key ID: [your_access_key]
# AWS Secret Access Key: [your_secret_key]
# Default region name: us-east-1
# Default output format: json
```

## 3. Project Setup

### Step 1: Clone and Setup Backend
```bash
# Navigate to project directory
cd SleepScience

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Configure Environment Variables
```bash
# Copy example environment file
cp env.example .env

# Edit .env file with your settings
nano .env  # or use your preferred editor
```

**Required .env configuration:**
```env
# Database (replace with your PostgreSQL URL)
DATABASE_URL=postgresql://username:password@localhost:5432/sleep_science_bot

# AWS Credentials (from Step 2)
AWS_ACCESS_KEY_ID=your_aws_access_key_id
AWS_SECRET_ACCESS_KEY=your_aws_secret_access_key
AWS_DEFAULT_REGION=us-east-1
AWS_BEDROCK_REGION=us-east-1

# Application Settings
SECRET_KEY=your_secret_key_here_make_it_long_and_random_at_least_32_characters
DEBUG=True
ENVIRONMENT=development
```

### Step 3: Initialize Database
```bash
# Create database tables
python -c "from backend.database.connection import db_manager; db_manager.create_tables()"

# Or use Alembic for migrations (optional)
alembic upgrade head
```

### Step 4: Setup Frontend
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

## 4. Running the Application

### Start Backend
```bash
# From project root (with venv activated)
python app.py
```
Backend will be available at: http://localhost:8000

### Start Frontend
```bash
# From frontend directory
npm start
```
Frontend will be available at: http://localhost:3000

### Verify Installation
1. Visit http://localhost:3000
2. Try the chat interface
3. Check the recommendations page
4. View analytics dashboard

## 5. API Documentation

Once the backend is running, you can access:
- **Interactive API docs:** http://localhost:8000/docs
- **Alternative API docs:** http://localhost:8000/redoc
- **Health check:** http://localhost:8000/api/v1/health

## 6. Troubleshooting

### Common Issues

**Database Connection Error:**
```bash
# Check if PostgreSQL is running
psql -U postgres -c "SELECT version();"

# Verify connection string in .env
# Test connection
python -c "from backend.database.connection import db_manager; print('Database connected!')"
```

**AWS Bedrock Access Error:**
```bash
# Verify AWS credentials
aws sts get-caller-identity

# Check Bedrock access
aws bedrock list-foundation-models --region us-east-1
```

**Frontend Build Error:**
```bash
# Clear npm cache
npm cache clean --force

# Reinstall dependencies
rm -rf node_modules package-lock.json
npm install
```

**Port Already in Use:**
```bash
# Find process using port 8000
lsof -i :8000

# Kill process
kill -9 <PID>
```

## 7. Development Tips

### Backend Development
- Use `DEBUG=True` in .env for detailed error messages
- Check logs in console for debugging
- Use the `/docs` endpoint for API testing

### Frontend Development
- React dev tools available in browser
- Hot reload enabled for development
- Check browser console for errors

### Database Development
- Use `psql` for direct database access
- Consider using a GUI like pgAdmin or DBeaver
- Backup your data regularly

## 8. Production Deployment

For production deployment, consider:
- Using environment variables for all secrets
- Setting up proper logging
- Using a production database
- Setting up monitoring and alerts
- Using HTTPS
- Implementing proper authentication

## Support

If you encounter issues:
1. Check the troubleshooting section above
2. Review the logs for error messages
3. Verify all environment variables are set correctly
4. Ensure all services (PostgreSQL, AWS) are accessible

