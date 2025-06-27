# 🏛️ Civic Voice AI Dashboard

An automated civic reporting system that integrates AI call agents with real-time Telegram notifications to transform how citizens report issues to government authorities.

## 🎯 Overview

**Civic Voice AI** enables citizens to report civic issues through phone calls that are automatically transcribed, categorized, and forwarded to relevant government departments via Telegram alerts. The system operates 24/7 without human intervention, ensuring no civic issue goes unreported.

### Key Features
- **AI-Powered Call Processing**: Automatic transcription and issue categorization
- **Smart Prioritization**: Urgent issues get immediate attention
- **Instant Telegram Alerts**: Real-time notifications to government departments
- **Analytics Dashboard**: Track reports, response times, and trends
- **Multi-Language Support**: Works with local languages
- **24/7 Operation**: No human operators required

## 🛠️ Tech Stack

- **Frontend**: Streamlit (Python web framework)
- **AI Processing**: Telnyx AI Call Control
- **Messaging**: Telegram Bot API
- **Data Processing**: Pandas, Python NLP
- **Deployment**: Compatible with Heroku, AWS, Google Cloud

## 📋 Prerequisites

Before running this application, ensure you have:

1. **Python 3.8+** installed
2. **Telnyx Account** with Call Control enabled
3. **Telegram Bot Token** and Channel/Chat ID
4. **Webhook endpoint** accessible from the internet

### Required Accounts
- [Telnyx Account](https://telnyx.com) - For AI call processing
- [Telegram Bot](https://core.telegram.org/bots#botfather) - For notifications

## 🚀 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/civic-voice-ai.git
cd civic-voice-ai
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables
Create a `.env` file in the project root:
```env
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
TELEGRAM_CHANNEL_ID=your_telegram_channel_id_here
TELNYX_API_KEY=your_telnyx_api_key_here
WEBHOOK_URL=https://yourdomain.com/webhook
```

### 4. Run the Application
```bash
streamlit run civic_dashboard.py
```

The dashboard will be available at `http://localhost:8501`

## ⚙️ Configuration

### Telegram Bot Setup
1. Create a bot using [@BotFather](https://t.me/botfather)
2. Get your bot token
3. Add the bot to your government channel/group
4. Get the channel/chat ID using `https://api.telegram.org/bot<token>/getUpdates`

### Telnyx Configuration
1. Purchase a phone number in Telnyx
2. Enable Call Control for the number
3. Configure speech recognition
4. Set webhook URL to your deployed endpoint

### Webhook Deployment
Deploy the webhook endpoint to a cloud service:

**For Heroku:**
```bash
git push heroku main
```

**For AWS/Google Cloud:**
Follow their respective deployment guides for Python applications.

## 📁 Project Structure

```
civic-voice-ai/
├── civic_dashboard.py          # Main Streamlit application
├── webhook_handler.py          # Telnyx webhook endpoint
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── .env                        # Environment variables (create this)
├── utils/
│   ├── telegram_handler.py     # Telegram messaging functions
│   ├── nlp_processor.py        # Text processing and categorization
│   └── report_formatter.py     # Report formatting utilities
└── docs/
    ├── API_DOCS.md             # API documentation
    └── DEPLOYMENT.md           # Deployment guide
```

## 🎛️ Usage

### For Citizens
1. **Call the civic hotline number**
2. **Describe the issue** to the AI assistant
3. **Provide location details** when asked
4. **Receive confirmation** that the report was submitted

### For Government Officials
1. **Receive instant Telegram alerts** for new reports
2. **View categorized issues** with priority levels
3. **Access the dashboard** for analytics and trends
4. **Track response times** and resolution rates

### For Administrators
1. **Monitor system performance** through the dashboard
2. **Configure alert recipients** by department
3. **Analyze reporting patterns** for resource allocation
4. **Export data** for external analysis

## 📊 Dashboard Features

### Main Dashboard
- **Real-time report processing**
- **System configuration panel**
- **Test simulation tools**

### Analytics Tab
- Reports by category (Infrastructure, Security, Health, etc.)
- Priority distribution
- Response time metrics
- Citizen satisfaction scores

### Configuration Tab
- Webhook setup instructions
- Telegram bot configuration
- System integration guides

## 🔗 API Integration

### Webhook Endpoint
The system expects POST requests from Telnyx with this structure:
```json
{
  "data": {
    "event_type": "call.transcription.received",
    "payload": {
      "transcription_text": "Citizen's spoken report",
      "call_control_id": "unique_call_id",
      "call_duration": 120
    }
  }
}
```

### Response Format
Webhook responds with:
```json
{
  "status": "success",
  "report_id": "CVC-20240127-143022",
  "category": "infrastructure",
  "priority": "high"
}
```

## 🧪 Testing

### Unit Tests
```bash
python -m pytest tests/
```

### Manual Testing
1. Use the **"Simulate Call"** tab in the dashboard
2. Test with various report types and priorities
3. Verify Telegram messages are received correctly
4. Check data extraction accuracy

### Load Testing
```bash
python tests/load_test.py
```

## 🚨 Issue Categories

The system automatically categorizes reports into:

| Category | Examples |
|----------|----------|
| **Infrastructure** | Roads, bridges, water supply, electricity |
| **Security** | Crime, theft, unsafe areas, lighting |
| **Health** | Hospitals, sanitation, disease outbreaks |
| **Education** | Schools, teachers, student safety |
| **Waste** | Garbage collection, illegal dumping |
| **Other** | Issues not fitting other categories |

## 🔧 Troubleshooting

### Common Issues

**Telegram messages not sending:**
- Verify bot token is correct
- Check if bot is added to the target channel
- Ensure channel ID is accurate

**Webhook not receiving calls:**
- Confirm webhook URL is accessible
- Check Telnyx webhook configuration
- Verify SSL certificate is valid

**AI categorization errors:**
- Review and update keyword lists
- Check transcript quality
-- Improve speech recognition settings

### Logs and Debugging
```bash
# Enable debug logging
export DEBUG=True
streamlit run civic_dashboard.py
```

View logs in `logs/civic_voice.log`

## 📈 Scaling

### High Volume Deployment
- Use Redis for caching frequent requests
- Deploy multiple webhook instances behind load balancer
- Implement database storage for report persistence
- Set up monitoring with Prometheus/Grafana

### Multi-City Deployment
- Configure separate Telegram channels per city
- Use environment-specific configuration files
- Implement tenant-based routing
- Set up centralized logging and monitoring

## 🔒 Security

### Data Protection
- All transcripts are encrypted at rest
- No personal information stored unnecessarily
- GDPR compliance built-in
- Regular security audits recommended

### Access Control
- Telegram channel access controls
- Webhook endpoint authentication
- Dashboard admin authentication
- API rate limiting

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup
```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
python -m pytest

# Format code
black civic_dashboard.py

# Type checking
mypy civic_dashboard.py
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙋‍♂️ Support

### Documentation
- [API Documentation](docs/API_DOCS.md)
- [Deployment Guide](docs/DEPLOYMENT.md)
- [Telnyx Integration Guide](https://developers.telnyx.com/docs/api/v2/call-control)

### Community
- **GitHub Issues**: Bug reports and feature requests
- **Discussions**: General questions and ideas
- **Wiki**: Community-contributed guides and examples

### Commercial Support
For enterprise deployments and custom integrations, contact: [support@civicvoice.ai](mailto:support@civicvoice.ai)

## 🌟 Acknowledgments

- [Telnyx](https://telnyx.com) for AI call processing capabilities
- [Telegram](https://telegram.org) for reliable messaging infrastructure
- [Streamlit](https://streamlit.io) for the rapid dashboard development
- Nigerian civic tech communities for inspiration and feedback

## 📊 Usage Statistics

If you use this project, consider sharing anonymous usage statistics to help improve the system:

```python
# Optional: Enable anonymous usage analytics
ENABLE_ANALYTICS = True
```

---

**Made with ❤️ for better civic engagement**

*Transform your city's civic reporting with AI-powered automation*
