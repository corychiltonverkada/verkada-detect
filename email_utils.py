import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_email(gmail_app_password, receiver_email, subject, body):
    sender_email = "verkadadetectalerts@gmail.com"
    # Create a MIMEText object for the email content
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))
    # SMTP server configuration for Gmail
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    # Connect to the SMTP server
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()  # Start TLS encryption
        # Log in to the SMTP server using your Gmail credentials
        server.login(sender_email, gmail_app_password)
        # Send the email
        server.sendmail(sender_email, receiver_email, message.as_string())
        print("Email sent successfully.")