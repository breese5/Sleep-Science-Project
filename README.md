# Sleep Science Explainer Bot

A conversational AI designed to interpret, summarize, and explain publicly available sleep-related academic papers, clinical guidelines, and trusted recommendations from sleep experts. This bot provides layperson-friendly explanations and helps users quickly grasp key insights about sleep, health, and longevity research.

## 🎯 Project Overview

The Sleep Science Explainer Bot leverages AWS Bedrock's generative AI capabilities to:
- Process and summarize sleep science research papers from NIH PubMed
- Explain complex medical concepts in simple, accessible terms
- Provide evidence-based sleep recommendations from experts
- Monitor and analyze user interaction patterns
- Offer curated advice from Bryan Johnson, Andrew Huberman, EightSleep, and CDC

## 🎯 Architecture

### System Architecture
```mermaid
graph TB
    subgraph "Frontend Layer"
        UI[React Frontend]
        UI --> |HTTP Requests| API
    end
    
    subgraph "API Layer"
        API[FastAPI Backend]
        API --> |Health Check| HC[Health Endpoint]
        API --> |Chat| CB[Chat Bot]
        API --> |Analytics| AS[Analytics Service]
        API --> |Papers| PC[Paper Client]
        API --> |Recommendations| RC[Recommendations]
    end
    
    subgraph "AI Layer"
        CB --> |AWS Bedrock| AI[AWS Bedrock<br/>Claude 3 Sonnet]
    end
    
    subgraph "Data Sources"
        PC --> |NIH PubMed API| NIH[NIH PubMed]
        RC --> |Expert Data| EXP[Expert Recommendations<br/>Bryan Johnson, Huberman, etc.]
    end
    
    subgraph "Data Layer"
        API --> |ORM| DB[(PostgreSQL Database)]
        DB --> |Users| U[Users Table]
        DB --> |Conversations| C[Conversations Table]
        DB --> |Interactions| I[Interactions Table]
        DB --> |Analytics| A[Analytics Table]
    end
    
    subgraph "Monitoring"
        API --> |Structured Logs| LOG[Structured Logging]
        AS --> |Metrics| MET[Analytics Dashboard]
    end
    
    style UI fill:#e1f5fe
    style API fill:#f3e5f5
    style AI fill:#fff3e0
    style DB fill:#e8f5e8
    style LOG fill:#ffebee
    style MET fill:#fff8e1
```

### Core Components
- **Conversational AI Interface**: Built with AWS Bedrock (Claude 3 Sonnet)
- **Data Ingestion Pipeline**: NIH PubMed API and expert recommendations integration
- **Interactive Analytics Dashboard**: User interaction monitoring and topic popularity analysis
- **PostgreSQL Database**: Persistent storage for conversations, users, and analytics
- **React Frontend**: Modern, responsive web interface
- **Security Layer**: Privacy controls and responsible AI practices

### Technology Stack
- **Backend**: FastAPI, SQLAlchemy, PostgreSQL, AWS Bedrock
- **Frontend**: React, Tailwind CSS, Axios
- **Database**: PostgreSQL with Alembic migrations
- **Cloud Services**: AWS Bedrock, AWS Lambda (future), AWS S3 (future)
- **Monitoring**: Structured logging, analytics tracking

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Node.js 18+
- PostgreSQL (local or cloud)
- AWS Account with Bedrock access

### 1. Clone and Setup
```bash
git clone <your-repo-url>
cd SleepScience

# Backend setup
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Frontend setup
cd frontend
npm install
cd ..
```

### 2. Configure Environment
```bash
cp env.example .env
# Edit .env with your database and AWS credentials
```

### 3. Database Setup
```bash
# Option A: Local PostgreSQL
brew install postgresql  # macOS
brew services start postgresql
psql -U postgres -c "CREATE DATABASE sleep_science_bot;"

# Option B: Cloud PostgreSQL (recommended)
# Use Neon, Supabase, or Railway for free tier
```

### 4. AWS Bedrock Setup
1. Go to [AWS Bedrock Console](https://console.aws.amazon.com/bedrock/)
2. Request access to Claude 3 Sonnet
3. Create IAM user with Bedrock permissions
4. Add credentials to `.env` file

### 5. Run the Application

#### Option A: Using main.py (Recommended)
```bash
# Check dependencies and environment
python main.py check

# Start both backend and frontend servers
python main.py both

# Or start services individually
python main.py start      # Backend only
python main.py frontend   # Frontend only
```

#### Option B: Manual Start
```bash
# Terminal 1: Backend
python app.py

# Terminal 2: Frontend
cd frontend
npm start
```

Visit http://localhost:3000 to use the application!

### 6. Testing and Development
```bash
# Run tests
python main.py test

# Generate coverage report
python main.py coverage

# View coverage report
open htmlcov/index.html  # macOS
# or
start htmlcov/index.html # Windows
```

## 📁 Project Structure

```
SleepScience/
├── main.py                     # Main entry point (NEW!)
├── app.py                      # FastAPI application
├── requirements.txt            # Python dependencies
├── env.example                 # Environment variables template
├── alembic.ini                # Database migration config
├── SETUP.md                   # Detailed setup instructions
├── README.md                  # This file
├── sleep_science_plan.md      # Original project plan
│
├── tests/                     # Test suite
│   └── test_api.py           # API endpoint tests
│
├── htmlcov/                   # Coverage report (generated)
│   └── index.html            # Interactive coverage report
│
├── backend/                   # Backend application
│   ├── __init__.py
│   ├── core/                  # Core functionality
│   │   ├── config.py         # Configuration management
│   │   ├── logging.py        # Structured logging
│   │   └── middleware.py     # Request middleware
│   │
│   ├── api/                  # API endpoints
│   │   ├── routes/
│   │   │   ├── health.py     # Health checks
│   │   │   ├── chat.py       # Chat interface
│   │   │   ├── papers.py     # Research papers
│   │   │   ├── analytics.py  # Analytics data
│   │   │   └── monitoring.py # Monitoring dashboard
│   │
│   ├── data/                 # Data sources
│   │   ├── nih_client.py     # PubMed API client
│   │   └── sleep_recommendations.py  # Expert recommendations
│   │
│   ├── models/               # Business logic
│   │   ├── chat.py          # Chat bot implementation
│   │   └── analytics.py     # Analytics service
│   │
│   └── database/            # Database layer
│       ├── models.py        # SQLAlchemy models
│       └── connection.py    # Database connection
│
├── frontend/                # React frontend
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ChatInterface.js
│   │   │   ├── Recommendations.js
│   │   │   ├── Analytics.js
│   │   │   └── Navbar.js
│   │   ├── App.js
│   │   └── index.js
│   ├── package.json
│   └── tailwind.config.js
│
└── migrations/              # Database migrations
    └── env.py
```

## 🔧 Features

### 🤖 Conversational AI
- **Intelligent Responses**: Powered by AWS Bedrock Claude 3 Sonnet
- **Context Awareness**: Maintains conversation history
- **Sleep Science Expertise**: Specialized knowledge in sleep research
- **Layperson-Friendly**: Explains complex concepts simply

### 📚 Research Integration
- **NIH PubMed Access**: Real-time sleep science papers
- **Paper Summarization**: AI-generated summaries of research
- **Recent Publications**: Latest sleep research updates
- **Citation Support**: Proper source attribution

### 💡 Expert Recommendations
- **Bryan Johnson**: Blueprint protocol insights
- **Andrew Huberman**: Neuroscience-based advice
- **EightSleep**: Sleep optimization techniques
- **CDC Guidelines**: Clinical recommendations
- **Categorized Content**: Filter by topic and priority

### 📊 Analytics Dashboard
- **User Interactions**: Track conversation patterns
- **Popular Topics**: Identify trending sleep topics
- **Usage Metrics**: Monitor application performance
- **Data Export**: Download analytics reports

### 🎨 Modern Interface
- **Responsive Design**: Works on all devices
- **Real-time Chat**: Instant messaging interface
- **Search & Filter**: Find specific recommendations
- **Visual Analytics**: Charts and metrics display

## 📊 Analytics Dashboard Guide

The Sleep Science Bot includes a comprehensive analytics dashboard that provides insights into user interactions, popular topics, and system performance.

### Accessing the Analytics Dashboard

#### Frontend Analytics
- **URL**: Navigate to the Analytics tab in the main application
- **Real-time Data**: Updates automatically as users interact with the system
- **Interactive Charts**: Visual representations of key metrics

#### Monitoring Dashboard (External)
- **URL**: `http://localhost:8000/api/v1/monitoring/dashboard`
- **Purpose**: System monitoring and performance tracking
- **Auto-refresh**: Updates every 30 seconds automatically

### Key Metrics Explained

#### 📈 User Engagement Metrics
- **Total Interactions**: Number of chat messages exchanged
- **Unique Users**: Distinct users who have interacted with the system
- **Average Message Length**: Mean length of user messages (indicates engagement depth)
- **Session Duration**: Time users spend in conversations

#### 🎯 Topic Analytics
- **Popular Topics**: Most frequently discussed sleep-related subjects
- **Topic Trends**: How interest in different topics changes over time
- **User Preferences**: Which topics generate the most engagement

#### ⚡ System Performance
- **Response Time**: How quickly the AI responds to user queries
- **System Uptime**: Application availability and reliability
- **Database Performance**: Connection health and query efficiency

### Using the Analytics Dashboard

#### 1. Overview Section
```
📊 Daily Summary
├── Total Interactions: 1,247
├── Unique Users: 89
├── Avg Message Length: 23.4 characters
└── Popular Topics: Sleep Hygiene, Insomnia, Circadian Rhythm
```

#### 2. Time-based Analysis
- **Date Range Selector**: Choose custom time periods (1 day, 7 days, 30 days)
- **Trend Visualization**: See how metrics change over time
- **Peak Usage Times**: Identify when users are most active

#### 3. Topic Insights
- **Topic Breakdown**: Percentage distribution of conversation topics
- **Engagement by Topic**: Which topics generate the longest conversations
- **User Questions**: Common questions and concerns

#### 4. User Behavior Patterns
- **Session Analysis**: How users navigate through conversations
- **Drop-off Points**: Where users typically end conversations
- **Return User Rate**: Percentage of users who come back

### Interpreting the Data

#### High Engagement Indicators
- ✅ **Longer message lengths**: Users are asking detailed questions
- ✅ **Multiple interactions per session**: Users are engaged in conversation
- ✅ **Return visits**: Users find value and come back

#### Areas for Improvement
- ⚠️ **Short message lengths**: Users might not be getting detailed enough responses
- ⚠️ **High drop-off rates**: Users might be dissatisfied with responses
- ⚠️ **Low return rates**: Content might not be meeting user needs

#### Popular Topics Analysis
- **Sleep Hygiene**: Basic sleep practices (most common)
- **Insomnia**: Sleep disorders and treatments
- **Circadian Rhythm**: Natural sleep-wake cycles
- **Sleep Apnea**: Breathing-related sleep issues
- **Dream Analysis**: Understanding sleep patterns

### API Endpoints for Analytics

#### Get Overview Data
```bash
GET /api/v1/analytics/overview?days=7
```
**Response:**
```json
{
  "total_interactions": 1247,
  "unique_users": 89,
  "avg_message_length": 23.4,
  "popular_topics": ["Sleep Hygiene", "Insomnia", "Circadian Rhythm"],
  "period_days": 7
}
```

#### Get Topic Analytics
```bash
GET /api/v1/analytics/topics?days=30
```
**Response:**
```json
{
  "topics": [
    {
      "name": "Sleep Hygiene",
      "count": 456,
      "percentage": 36.6,
      "avg_engagement": 4.2
    }
  ]
}
```

#### Get User Analytics
```bash
GET /api/v1/analytics/users/{user_id}
```
**Response:**
```json
{
  "user_id": "user123",
  "total_interactions": 15,
  "favorite_topics": ["Sleep Hygiene", "Circadian Rhythm"],
  "avg_session_length": 8.5,
  "last_active": "2024-01-15T10:30:00Z"
}
```

### Exporting Analytics Data

#### CSV Export
```bash
GET /api/v1/analytics/export?format=csv&days=30
```
- Downloads comprehensive analytics data
- Includes all metrics and user interactions
- Suitable for external analysis tools

#### JSON Export
```bash
GET /api/v1/analytics/export?format=json&days=30
```
- Machine-readable format
- Includes detailed metadata
- Perfect for custom dashboards

### Best Practices for Analytics

#### 1. Regular Monitoring
- Check dashboard daily for system health
- Monitor for unusual patterns or spikes
- Track user satisfaction through engagement metrics

#### 2. Data Interpretation
- Consider context when analyzing metrics
- Look for trends rather than single data points
- Compare metrics across different time periods

#### 3. Actionable Insights
- Use topic popularity to guide content development
- Identify user pain points through conversation analysis
- Optimize response quality based on engagement patterns

#### 4. Privacy Considerations
- All analytics are anonymized
- No personal information is tracked
- Data is used only for system improvement

### Troubleshooting Analytics

#### Common Issues
- **No data showing**: Check if the application is running and users are active
- **Missing metrics**: Verify database connectivity and logging configuration
- **Stale data**: Ensure the dashboard is refreshing properly

#### Data Accuracy
- Analytics are based on actual user interactions
- Metrics update in real-time as users engage with the system
- Historical data is preserved for trend analysis

---

## 📄 API Documentation

### Core Endpoints

#### Chat Interface
- `POST /api/v1/chat` - Send message to AI assistant
- `GET /api/v1/chat/conversation/{id}` - Get conversation history
- `DELETE /api/v1/chat/conversation/{id}` - Delete conversation
- `GET /api/v1/chat/topics` - Get available topics

#### Research Papers
- `GET /api/v1/papers/search` - Search PubMed papers
- `GET /api/v1/papers/{id}` - Get paper details
- `GET /api/v1/papers/recent` - Get recent papers
- `POST /api/v1/papers/summarize` - Generate paper summary

#### Recommendations
- `GET /api/v1/recommendations` - Get sleep recommendations
- `GET /api/v1/recommendations/{id}` - Get specific recommendation
- `GET /api/v1/recommendations/categories` - Get categories

#### Analytics
- `GET /api/v1/analytics/overview` - Get analytics overview
- `GET /api/v1/analytics/topics` - Get topic analytics
- `GET /api/v1/analytics/users/{id}` - Get user analytics
- `GET /api/v1/analytics/trends` - Get usage trends

#### Health & Monitoring
- `GET /api/v1/health` - Basic health check
- `GET /api/v1/health/detailed` - Detailed health status
- `GET /api/v1/ready` - Readiness check

#### Monitoring Dashboard
- `GET /api/v1/monitoring/dashboard` - HTML monitoring dashboard
- `GET /api/v1/monitoring/metrics` - System performance metrics
- `GET /api/v1/monitoring/logs` - Recent application logs

### Interactive API Docs
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🎮 Application Management with main.py

The `main.py` script provides a unified interface for managing the Sleep Science Bot application. It handles dependency checking, environment validation, and service management.

### Available Commands

#### Service Management
```bash
# Start both backend and frontend servers
python main.py both

# Start backend server only
python main.py start

# Start frontend server only
python main.py frontend
```

#### Development Tools
```bash
# Run the test suite
python main.py test

# Generate test coverage report
python main.py coverage

# Check dependencies and environment
python main.py check
```

#### Help and Information
```bash
# Show help information
python main.py help
```

### Command Details

#### `python main.py both`
- Starts both backend (FastAPI) and frontend (React) servers
- Backend runs on http://localhost:8000
- Frontend runs on http://localhost:3000
- Automatically checks dependencies and environment first

#### `python main.py start`
- Starts only the backend server
- Useful for API development and testing
- Includes health checks and dependency validation

#### `python main.py frontend`
- Starts only the React frontend
- Assumes backend is already running
- Opens browser automatically

#### `python main.py test`
- Runs the complete test suite
- Includes health, chat, analytics, and recommendations tests
- Provides verbose output with test results

#### `python main.py coverage`
- Generates comprehensive test coverage report
- Creates HTML report in `htmlcov/` directory
- Shows coverage statistics in terminal

#### `python main.py check`
- Validates Python version (3.9+ required)
- Checks for required dependencies
- Verifies environment configuration
- Validates frontend dependencies

### Development Workflow
```bash
# 1. Initial setup
python main.py check

# 2. Start development servers
python main.py both

# 3. Run tests during development
python main.py test

# 4. Generate coverage for quality assurance
python main.py coverage
```

## 🗄️ Database Schema

### Core Tables
- **users**: User information and session data
- **conversations**: Chat session management
- **messages**: Individual chat messages
- **interactions**: Analytics tracking
- **research_papers**: Cached paper data
- **sleep_recommendations**: Expert recommendations
- **analytics_metrics**: Aggregated analytics

## 🔒 Security & Privacy

### Data Protection
- **User Anonymization**: No personal data collection
- **Secure API Endpoints**: Rate limiting and validation
- **Environment Variables**: Secure credential management
- **Input Validation**: Sanitized user inputs

### Responsible AI
- **Medical Disclaimer**: Educational purposes only
- **Source Attribution**: Proper citation of sources
- **Bias Mitigation**: Diverse expert perspectives
- **Content Filtering**: Safe and appropriate responses

## 🚀 Deployment

### Quick Start Checklist

#### ✅ Prerequisites
- [ ] Python 3.9+ installed
- [ ] Node.js 18+ installed
- [ ] PostgreSQL database (local or cloud)
- [ ] AWS Account with Bedrock access
- [ ] Git repository cloned

#### ✅ Setup Steps
- [ ] Virtual environment created and activated
- [ ] Backend dependencies installed (`pip install -r requirements.txt`)
- [ ] Frontend dependencies installed (`cd frontend && npm install`)
- [ ] Environment file configured (`cp env.example .env`)
- [ ] Database created and accessible
- [ ] AWS credentials configured

### Development Deployment

#### Using main.py (Recommended)
```bash
# Check system readiness
python main.py check

# Start both servers
python main.py both

# Run tests
python main.py test

# Generate coverage report
python main.py coverage
```

#### Manual Development
```bash
# Backend only
python app.py

# Frontend only
cd frontend && npm start

# Tests
pytest tests/ -v

# Coverage
pytest --cov=backend --cov-report=html tests/
```

### Production Deployment

#### Environment Configuration

Required environment variables:
```bash
DATABASE_URL=postgresql://user:pass@host:port/db
AWS_ACCESS_KEY_ID=your_aws_key
AWS_SECRET_ACCESS_KEY=your_aws_secret
AWS_DEFAULT_REGION=us-east-1
```

#### Database Setup

**Option A: Local PostgreSQL**
```bash
brew install postgresql  # macOS
brew services start postgresql
psql -U postgres -c "CREATE DATABASE sleep_science_bot;"
```

**Option B: Cloud Database (Recommended)**
- **Neon**: Free tier with 3GB storage
- **Supabase**: Free tier with 500MB
- **Railway**: Free tier with 1GB

#### AWS Bedrock Setup

1. **Request Access**: Go to [AWS Bedrock Console](https://console.aws.amazon.com/bedrock/)
2. **Model Access**: Request Claude 3 Sonnet access
3. **IAM User**: Create user with Bedrock permissions
4. **Credentials**: Add to `.env` file

#### Deployment Options

**Option A: Traditional VPS**
```bash
# Install dependencies
sudo apt update
sudo apt install python3 python3-pip nodejs npm postgresql

# Deploy application
git clone <repository>
cd SleepScience
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd frontend && npm install && npm run build
```

**Option B: Container Deployment**
```dockerfile
# Dockerfile example
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["python", "app.py"]
```

**Option C: Cloud Platforms**
- **Heroku**: Easy deployment with PostgreSQL addon
- **Railway**: Full-stack deployment platform
- **Vercel**: Frontend deployment with API routes

### Performance Monitoring

#### Key Metrics to Monitor
- Response time < 2 seconds
- Database connection pool usage
- Memory usage < 512MB
- CPU usage < 80%
- Error rate < 1%

#### Monitoring Commands
```bash
# Check system resources
curl http://localhost:8000/api/v1/monitoring/metrics

# View recent logs
curl http://localhost:8000/api/v1/monitoring/logs?limit=20

# Health check
curl http://localhost:8000/health
```

### Troubleshooting

#### Common Issues

**Backend Won't Start**
```bash
# Check dependencies
python main.py check

# Check environment
cat .env

# Check database connection
python -c "from backend.database.connection import db_manager; db_manager.create_tables()"
```

**Frontend Won't Start**
```bash
# Check Node.js version
node --version

# Reinstall dependencies
cd frontend
rm -rf node_modules package-lock.json
npm install
```

**Tests Failing**
```bash
# Check test environment
python main.py check

# Run tests with verbose output
pytest tests/ -v -s

# Check specific test
pytest tests/test_api.py::test_health_check -v -s
```

**Database Issues**
```bash
# Check connection
python -c "from backend.database.connection import db_manager; print(db_manager.engine.url)"

# Reset database (development only)
python -c "from backend.database.connection import db_manager; db_manager.drop_tables(); db_manager.create_tables()"
```

### Production Considerations
- Use production database (AWS RDS, etc.)
- Set up proper logging and monitoring
- Configure HTTPS and security headers
- Implement user authentication
- Set up CI/CD pipeline
- Regular database backups
- Keep dependencies updated
- Monitor application health regularly

## 🧪 Testing

### Test Suite Overview
The project includes a comprehensive test suite that validates core API functionality:

- **Health Check Tests**: Verify application status endpoints
- **Recommendations Tests**: Validate sleep recommendation data structure
- **Chat Interface Tests**: Test basic chat functionality (with graceful AWS/DB failure handling)
- **Analytics Tests**: Ensure analytics endpoints return proper data structure

### Running Tests

#### Prerequisites
```bash
# Install test dependencies
pip install pytest pytest-cov
```

#### Basic Test Execution
```bash
# Run all tests
pytest tests/

# Run with verbose output
pytest tests/ -v

# Run specific test file
pytest tests/test_api.py

# Run specific test function
pytest tests/test_api.py::test_health_check
```

#### Test Coverage
```bash
# Generate coverage report
pytest --cov=backend --cov-report=html tests/

# Generate coverage report with terminal output
pytest --cov=backend --cov-report=term-missing tests/

# Generate multiple report formats
pytest --cov=backend --cov-report=html --cov-report=term --cov-report=xml tests/
```

### Coverage Report
After running tests with coverage, you can view the detailed coverage report:

1. **HTML Report**: Open `htmlcov/index.html` in your web browser
   - Interactive coverage visualization
   - Line-by-line coverage analysis
   - File and directory coverage breakdown
   - Missing coverage highlighting

2. **Terminal Report**: Coverage summary displayed in terminal output
   - Overall coverage percentage
   - Missing lines summary
   - File-by-file coverage

### Test Structure
```
tests/
└── test_api.py              # API endpoint tests
    ├── test_health_check()           # Health endpoint validation
    ├── test_get_recommendations()    # Recommendations data structure
    ├── test_chat_endpoint_basic()    # Chat functionality (basic)
    └── test_analytics_endpoint()     # Analytics data structure
```

### Test Features
- **Isolated Testing**: Each test runs independently
- **Graceful Failure Handling**: Tests handle expected AWS/DB issues
- **Data Structure Validation**: Ensures API responses have correct format
- **Error State Testing**: Validates proper error handling
- **Coverage Tracking**: Monitors code coverage across backend modules

### Continuous Integration
For CI/CD pipelines, the tests can be run with:
```bash
# CI-friendly output
pytest --cov=backend --cov-report=xml --cov-report=term-missing tests/

# Exit on first failure
pytest -x tests/

# Run in parallel (if pytest-xdist installed)
pytest -n auto tests/
```

### Frontend Testing
```bash
cd frontend
npm test
npm run build
```

## 📈 Performance

### Optimization Features
- **Database Connection Pooling**: Efficient database connections
- **Response Caching**: Cached recommendations and papers
- **Rate Limiting**: API usage protection
- **Async Processing**: Non-blocking operations

### Monitoring
- **Structured Logging**: JSON-formatted logs
- **Health Checks**: Application status monitoring
- **Analytics Tracking**: Usage pattern analysis
- **Error Handling**: Graceful failure management

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 for Python code
- Use TypeScript for frontend components
- Write comprehensive tests
- Update documentation
- Follow conventional commits

### Code Quality
```bash
# Backend code quality checks
flake8 backend/
black backend/
mypy backend/
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚖️ Disclaimer

This is not meant to be medical advice and is made for educational purposes only. Consult with a doctor for further questions.

## 🆘 Support

### Documentation
- [Setup Guide](SETUP.md) - Detailed installation instructions
- [API Documentation](http://localhost:8000/docs) - Interactive API docs
- [Project Plan](sleep_science_plan.md) - Original project specifications

### Troubleshooting
- Check the [SETUP.md](SETUP.md) troubleshooting section
- Review application logs for error messages
- Verify environment variables are correctly set
- Ensure all services (PostgreSQL, AWS) are accessible

---

**Built for better sleep science education**

## 🤖 AI Assistance

This project was developed with the assistance of **Cursor**, an AI pair programming tool, to accelerate development, debugging, and documentation.