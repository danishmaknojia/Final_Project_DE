import os
from dotenv import load_dotenv
from flask import Flask
from flask_mail import Mail

app = Flask(__name__)

# Load environment variables from a .env file
load_dotenv()

# Get mail server details from environment variables
mailServer = os.getenv("SERVER")
mailPort = os.getenv("PORT")
mailUser = os.getenv("USERNAME")
mailPass = os.getenv("PASSWORD")

# Validate MAIL_PORT
try:
    mailPort = int(mailPort) if mailPort else 465  # Default to 587 if not set
except ValueError:
    print(f"Invalid MAIL_PORT value: {mailPort}")
    mailPort = 465  # Fallback to default

# Configure Flask-Mail
app.config['MAIL_SERVER'] = mailServer
app.config['MAIL_PORT'] = mailPort
app.config['MAIL_USERNAME'] = mailUser
app.config['MAIL_PASSWORD'] = mailPass
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_DEBUG'] = True


# Initialize the Mail object
mail = Mail(app)
