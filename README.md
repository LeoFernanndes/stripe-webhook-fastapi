# Stripe Webhook Fastapi

Webserver to help with development of Stripe integration by listening to stripe events and posting them to a user defined webhook url

### Steps to spin the server up
1. Clone the repository
2. Create and activate virtual environenment (optional)\
    python3 -m venv venv\
    source venv/bin/activate
3. Install dependencies
    pip install -r requirements.txt
4. Create a .env file following .example.env template


### Runserver command
python3 main.py
