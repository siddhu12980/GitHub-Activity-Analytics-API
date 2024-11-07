# 🚀 GitHub Activity Analytics API

A powerful FastAPI-based backend service that provides detailed insights into your GitHub activities, social connections, and repository interactions.

## 🎯 Features

### 📊 Activity Tracking
- Track pull requests, commits, and code reviews
- View activity summaries and trends
- Monitor issue interactions and comments
- Repository contribution analytics

### 👥 Social Integration
- Follow/Following management
- Track followers and network growth
- View starred repositories
- Monitor repository subscriptions

### TODO
 #### 📈 Event Monitoring
- Real-time GitHub event tracking
- Personalized event timelines


## 🛠️ Tech Stack
- FastAPI
- Python 
- GitHub OAuth2
- RESTful API

## 🚀 Getting Started

### Prerequisites
- Python 3.7+
- GitHub Account
- GitHub OAuth App credentials

### Environment Variables
```env
GITHUB_CLIENT_ID=your_client_id
GITHUB_CLIENT_SECRET=your_client_secret
GITHUB_REDIRECT_URI=your_redirect_uri
```

### Installation
```bash
# Clone the repository
git clone {reoi}

# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn main:app --reload
```

## 📍 API Endpoints

### Authentication
- `GET /login` - Initiate GitHub OAuth login
- `GET /auth/callback/github` - OAuth callback handler

### User Information
- `GET /user` - Get authenticated user's profile
- `GET /user/repo` - List user's repositories

### Activity Analytics
- `GET /events` - View GitHub activities grouped by type
- `GET /user/events` - View activity feed from followed users
- `GET /user/activity` - Get activity summary with metrics

### Social Network
- `GET /user/followers` - List your followers
- `GET /user/following` - List users you follow
- `GET /user/starred` - View starred repositories
- `GET /user/subscriptions` - List watched repositories

## 🔒 Security
- OAuth2 authentication with GitHub
- Secure token handling
- Protected endpoint access

## 🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License
This project is licensed under the MIT License - see the LICENSE file for details

## 🙋‍♂️ Author
[Your Name]

## 🌟 Acknowledgments
- GitHub API
- FastAPI framework
- Python community
