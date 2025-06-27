# civic_dashboard.py

import streamlit as st
import pandas as pd
import requests
from datetime import datetime
import json
import re
import os
from typing import Dict, List, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Streamlit page config
st.set_page_config(
    page_title="Civic.AI Dashboard", 
    layout="wide",
    page_icon="🏛️"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #2E86AB;
        font-size: 2.5rem;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 0.5rem 0;
    }
    .status-success {
        background: #d4edda;
        color: #155724;
        padding: 0.5rem;
        border-radius: 5px;
        border-left: 4px solid #28a745;
    }
    .status-error {
        background: #f8d7da;
        color: #721c24;
        padding: 0.5rem;
        border-radius: 5px;
        border-left: 4px solid #dc3545;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-header">🏛️ Civic.AI Dashboard</h1>', unsafe_allow_html=True)
st.markdown("### Automated Civic Reporting via AI Call Agent & Telegram Integration")

# Configuration Section
with st.expander("⚙️ System Configuration", expanded=False):
    col1, col2 = st.columns(2)
    with col1:
        telegram_token = st.text_input(
            "Telegram Bot Token", 
            value=os.getenv("TELEGRAM_BOT_TOKEN", ""),
            type="password",
            help="Your Telegram bot token from environment variables"
        )
        telegram_channel = st.text_input(
            "Telegram Channel/Chat ID", 
            value=os.getenv("TELEGRAM_CHANNEL_ID", ""),
            help="Your Telegram channel/chat ID from environment variables"
        )
    
    with col2:
        telnyx_webhook_url = st.text_input(
            "Telnyx Webhook URL", 
            value=os.getenv("TELNYX_WEBHOOK_URL", ""),
            placeholder="https://yourapp.com/webhook"
        )
        admin_contacts = st.text_area(
            "Admin Contacts (comma-separated)", 
            value=os.getenv("ADMIN_EMAILS", ""),
            placeholder="admin1@gov.ng, admin2@gov.ng"
        )

# Security validation functions
def validate_telegram_token(token: str) -> bool:
    """Validate Telegram bot token format"""
    if not token:
        return False
    pattern = r'^\d+:[A-Za-z0-9_-]+$'
    return bool(re.match(pattern, token))

def validate_chat_id(chat_id: str) -> bool:
    """Validate Telegram chat ID format"""
    if not chat_id:
        return False
    return chat_id.isdigit() or chat_id.startswith('-')

# AI Call Processing Functions
def extract_civic_info(transcript: str) -> Dict:
    """Extract structured civic information from call transcript using simple NLP"""
    
    # Keywords for different issue types
    issue_keywords = {
        'infrastructure': ['road', 'bridge', 'water', 'electricity', 'power', 'drainage'],
        'security': ['crime', 'theft', 'violence', 'unsafe', 'robbery', 'security'],
        'health': ['hospital', 'clinic', 'medical', 'health', 'disease', 'sanitation'],
        'education': ['school', 'teacher', 'education', 'student', 'classroom'],
        'waste': ['garbage', 'waste', 'dump', 'refuse', 'sanitation', 'dirty'],
        'other': []
    }
    
    # Priority keywords
    priority_keywords = {
        'urgent': ['emergency', 'urgent', 'immediate', 'critical', 'danger'],
        'high': ['serious', 'important', 'major', 'significant'],
        'medium': ['moderate', 'concern', 'issue'],
        'low': ['minor', 'small', 'slight']
    }
    
    transcript_lower = transcript.lower()
    
    # Determine issue category
    issue_category = 'other'
    for category, keywords in issue_keywords.items():
        if any(keyword in transcript_lower for keyword in keywords):
            issue_category = category
            break
    
    # Determine priority
    priority = 'medium'  # default
    for pri, keywords in priority_keywords.items():
        if any(keyword in transcript_lower for keyword in keywords):
            priority = pri
            break
    
    # Extract location (simple pattern matching)
    location_patterns = [
        r'in\s+([A-Za-z\s]+)',
        r'at\s+([A-Za-z\s]+)',
        r'from\s+([A-Za-z\s]+)',
        r'area\s+([A-Za-z\s]+)'
    ]
    
    location = "Location not specified"
    for pattern in location_patterns:
        matches = re.findall(pattern, transcript)
        if matches:
            location = matches[0].strip().title()
            break
    
    return {
        'category': issue_category,
        'priority': priority,
        'location': location,
        'summary': transcript[:200] + "..." if len(transcript) > 200 else transcript,
        'full_transcript': transcript
    }

def format_telegram_message(civic_info: Dict, call_metadata: Dict = None) -> str:
    """Format civic report for Telegram with emojis and structure"""
    
    category_emojis = {
        'infrastructure': '🏗️',
        'security': '🚨',
        'health': '🏥',
        'education': '🎓',
        'waste': '🗑️',
        'other': '📝'
    }
    
    priority_emojis = {
        'urgent': '🔴',
        'high': '🟠',
        'medium': '🟡',
        'low': '🟢'
    }
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    message = f"""
🏛️ **CIVIC VOICE REPORT**

{category_emojis.get(civic_info['category'], '📝')} **Category:** {civic_info['category'].title()}
{priority_emojis.get(civic_info['priority'], '🟡')} **Priority:** {civic_info['priority'].title()}
📍 **Location:** {civic_info['location']}
🕒 **Received:** {timestamp}

📞 **Report Summary:**
{civic_info['summary']}

{'📱 **Call Duration:** ' + str(call_metadata.get('duration', 'N/A')) + ' seconds' if call_metadata else ''}
{'📞 **Caller ID:** ' + str(call_metadata.get('caller_id', 'N/A')) if call_metadata else ''}

---
*Report ID: CVC-{timestamp.replace('-', '').replace(':', '').replace(' ', '-')}*
""".strip()
    
    return message

def send_to_telegram(message: str, token: str, chat_id: str) -> bool:
    """Send formatted message to Telegram with validation"""
    
    # Validate inputs
    if not validate_telegram_token(token):
        st.error("Invalid Telegram bot token format")
        return False
    
    if not validate_chat_id(chat_id):
        st.error("Invalid Telegram chat ID format")
        return False
    
    telegram_url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id, 
        "text": message,
        "parse_mode": "Markdown"
    }
    
    try:
        response = requests.post(telegram_url, json=payload, timeout=10)
        if response.status_code == 200:
            return True
        else:
            st.error(f"Telegram API Error: {response.status_code} - {response.text}")
            return False
    except requests.exceptions.Timeout:
        st.error("Request timed out. Please try again.")
        return False
    except Exception as e:
        st.error(f"Telegram Error: {str(e)}")
        return False

# Main Dashboard Layout
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="metric-card">
        <h3>📞 AI Call Agent</h3>
        <p>Automated transcription and civic issue extraction</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric-card">
        <h3>🤖 Smart Processing</h3>
        <p>AI categorizes and prioritizes reports automatically</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="metric-card">
        <h3>📱 Instant Alerts</h3>
        <p>Real-time notifications to civic authorities</p>
    </div>
    """, unsafe_allow_html=True)

# Configuration Status
if not os.getenv("TELEGRAM_BOT_TOKEN") or not os.getenv("TELEGRAM_CHANNEL_ID"):
    st.warning("⚠️ Missing environment variables. Please set TELEGRAM_BOT_TOKEN and TELEGRAM_CHANNEL_ID in your .env file or deployment environment.")

# Test Section
st.subheader("🧪 Test the System")

tab1, tab2, tab3 = st.tabs(["📞 Simulate Call", "📊 Analytics", "⚙️ Webhook Setup"])

with tab1:
    st.markdown("**Simulate an incoming civic report call:**")
    
    sample_transcripts = {
        "Infrastructure Issue": "Hello, I'm calling to report a major pothole on Ahmadu Bello Way in Kaduna Central. The road is really bad and causing damage to vehicles. This needs urgent attention as it's a main road.",
        
        "Security Concern": "There have been multiple theft cases in Barnawa area over the past week. The community is concerned about safety, especially at night. We need increased security patrol.",
        
        "Waste Management": "The garbage dump near Government College is overflowing and creating health hazards. The smell is terrible and attracting pests. This is an urgent health concern for the community.",
        
        "Water Supply": "Water supply has been cut off in Malali area for three days now. Residents are struggling and we need immediate intervention from the water board."
    }
    
    selected_sample = st.selectbox("Choose a sample report:", list(sample_transcripts.keys()))
    
    transcript_input = st.text_area(
        "Call Transcript:", 
        value=sample_transcripts[selected_sample],
        height=100
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔄 Process Call Transcript", type="primary"):
            if transcript_input and telegram_token and telegram_channel:
                with st.spinner("Processing civic report..."):
                    # Extract civic information
                    civic_info = extract_civic_info(transcript_input)
                    
                    # Format message
                    telegram_message = format_telegram_message(civic_info)
                    
                    # Send to Telegram
                    success = send_to_telegram(telegram_message, telegram_token, telegram_channel)
                    
                    if success:
                        st.markdown('<div class="status-success">✅ Report processed and sent successfully!</div>', unsafe_allow_html=True)
                        
                        # Display extracted information
                        st.subheader("📋 Extracted Information:")
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Category", civic_info['category'].title())
                        with col2:
                            st.metric("Priority", civic_info['priority'].title())
                        with col3:
                            st.metric("Location", civic_info['location'])
                        
                        st.text_area("Generated Telegram Message:", telegram_message, height=200)
                    else:
                        st.markdown('<div class="status-error">❌ Failed to send report. Check your configuration.</div>', unsafe_allow_html=True)
            else:
                st.warning("Please fill in all required fields (transcript, bot token, channel ID)")
    
    with col2:
        if st.button("📝 Custom Report"):
            custom_transcript = st.text_input("Enter your custom report:")
            if custom_transcript:
                civic_info = extract_civic_info(custom_transcript)
                st.json(civic_info)

with tab2:
    st.markdown("**System Analytics Dashboard**")
    
    # Mock analytics data
    mock_data = {
        'Today': [15, 8, 12, 5, 3],
        'This Week': [89, 45, 67, 23, 18],
        'This Month': [324, 198, 256, 87, 65]
    }
    
    categories = ['Infrastructure', 'Security', 'Health', 'Education', 'Waste']
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Reports by Category")
        df = pd.DataFrame(mock_data, index=categories)
        st.bar_chart(df)
    
    with col2:
        st.subheader("📈 Key Metrics")
        st.metric("Total Reports Today", "43", "+12%")
        st.metric("Average Response Time", "8 min", "-15%")
        st.metric("Resolution Rate", "87%", "+5%")
        st.metric("Citizen Satisfaction", "4.2/5", "+0.3")

with tab3:
    st.markdown("**Telnyx Webhook Configuration**")
    
    st.markdown("""
    ### 🔗 How to Set Up the Integration:
    
    1. **Telnyx Call Control Setup:**
       - Configure your Telnyx number to use Call Control
       - Set up speech recognition for call transcription
       - Point webhook to your server endpoint
    
    2. **Webhook Endpoint Example:**
    """)
    
    webhook_code = '''
# Example Flask webhook endpoint for Telnyx
from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route('/telnyx-webhook', methods=['POST'])
def handle_telnyx_webhook():
    data = request.json
    
    if data['data']['event_type'] == 'call.transcription.received':
        transcript = data['data']['payload']['transcription_text']
        call_id = data['data']['payload']['call_control_id']
        
        # Process with your civic dashboard
        process_civic_call(transcript, call_id)
        
    return jsonify({'status': 'success'})

def process_civic_call(transcript, call_id):
    # Send to your Streamlit app or process directly
    civic_info = extract_civic_info(transcript)
    send_to_telegram(format_telegram_message(civic_info))
'''
    
    st.code(webhook_code, language='python')
    
    st.markdown("""
    3. **Testing Your Setup:**
       - Use the "Simulate Call" tab above to test message formatting
       - Verify Telegram bot receives messages correctly
       - Test with actual calls through your Telnyx number
    
    4. **Production Deployment:**
       - Deploy webhook endpoint (Heroku, AWS, etc.)
       - Update Telnyx webhook URL
       - Configure monitoring and error handling
    """)

# Footer
st.markdown("---")
st.markdown("""
### 🎯 Use Cases for This System:

**Government Agencies:**
- Automated citizen complaint processing
- Real-time emergency response coordination
- Civic engagement monitoring

**NGOs & Community Organizations:**
- Community issue tracking
- Rapid response to citizen concerns
- Data-driven advocacy

**Smart City Initiatives:**
- 24/7 citizen service hotline
- Multi-channel reporting (voice, web, mobile)
- Analytics for urban planning

---

*Built with Streamlit, Telnyx AI, and Telegram Bot API*
""")