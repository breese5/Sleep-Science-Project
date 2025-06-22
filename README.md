# Sleep Science Explainer Bot

A conversational AI designed to interpret, summarize, and explain publicly available sleep-related academic papers, clinical guidelines, and trusted recommendations from sleep experts. This bot provides layperson-friendly explanations and helps users quickly grasp key insights about sleep, health, and longevity research.

## 🎯 Project Overview

The Sleep Science Explainer Bot leverages AWS Bedrock's generative AI capabilities to:
- Process and summarize sleep science research papers from NIH PubMed
- Explain complex medical concepts in simple, accessible terms
- Provide evidence-based sleep recommendations from experts
- Monitor and analyze user interaction patterns
- Offer curated advice from Bryan Johnson, Andrew Huberman, EightSleep, and CDC

## 🏗️ Architecture

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
```bash
# Terminal 1: Backend
python app.py

# Terminal 2: Frontend
cd frontend
npm start
```

Visit http://localhost:3000 to use the application!

## 📁 Project Structure

```
SleepScience/
├── app.py                      # Main FastAPI application
├── requirements.txt            # Python dependencies
├── env.example                 # Environment variables template
├── alembic.ini                # Database migration config
├── SETUP.md                   # Detailed setup instructions
├── README.md                  # This file
├── sleep_science_plan.md      # Original project plan
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
│   │   │   └── analytics.py  # Analytics data
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

## 📚 API Documentation

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

### Interactive API Docs
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

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

### Development
```bash
# Backend
python app.py

# Frontend
cd frontend && npm start
```

### Production Considerations
- Use production database (AWS RDS, etc.)
- Set up proper logging and monitoring
- Configure HTTPS and security headers
- Implement user authentication
- Set up CI/CD pipeline

## 🧪 Testing

### Backend Testing
```bash
# Run tests
python -m pytest tests/

# Code quality
flake8 backend/
black backend/
mypy backend/
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

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

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

### Getting Help
- Create an issue in the GitHub repository
- Check the documentation links above
- Review the troubleshooting guide

## 🗺️ Roadmap

### Completed ✅
- [x] Basic conversational AI implementation
- [x] NIH PubMed integration
- [x] Expert recommendations system
- [x] Analytics dashboard
- [x] PostgreSQL database integration
- [x] React frontend with modern UI
- [x] AWS Bedrock integration
- [x] Comprehensive documentation

### Future Enhancements 🚀
- [ ] User authentication and profiles
- [ ] Advanced paper summarization
- [ ] Mobile app development
- [ ] Multi-language support
- [ ] Advanced analytics and ML insights
- [ ] Integration with wearable devices
- [ ] Personalized sleep recommendations
- [ ] Community features and sharing

## 🙏 Acknowledgments

- **Bryan Johnson** - Blueprint protocol insights
- **Andrew Huberman** - Neuroscience expertise
- **EightSleep** - Sleep optimization research
- **CDC** - Clinical guidelines and standards
- **NIH PubMed** - Research paper database
- **AWS Bedrock** - Generative AI capabilities

---

**Built with ❤️ for better sleep science education** 