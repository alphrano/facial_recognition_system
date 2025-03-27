import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv  # Import dotenv

# Load environment variables from .env
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path)

def send_email_notification(admin_email, subject, message):
    # Load email credentials from environment variables
    sender_email = os.getenv("EMAIL_USER")
    sender_password = os.getenv("EMAIL_PASS")

    if not sender_email or not sender_password:
        print("Error: Email credentials are missing. Set EMAIL_USER and EMAIL_PASS environment variables.")
        return

    # Create the email
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = admin_email
    msg["Subject"] = subject
    msg.attach(MIMEText(message, "plain"))

    # Send the email
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, admin_email, msg.as_string())
        print("Email notification sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Test sending an email
if __name__ == "__main__":
    send_email_notification("a3809261@example.com", "Test Email", "This is a test!")
