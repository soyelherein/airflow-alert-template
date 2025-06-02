import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Email credentials and details
sender_email = ''
receiver_email = ''
password = ""  # Use App Password, not your real password
subject = "Test Email from Python"
body = "Hello, this is a test email sent from Python!"

# Create email message
message = MIMEMultipart()
message["From"] = ''
message["To"] = ''
message["Subject"] = subject

# Attach body content
message.attach(MIMEText(body, "plain"))

# Send email via Gmail's SMTP server
try:
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()  # Secure the connection
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        print("✅ Email sent successfully.")
except Exception as e:
    print("❌ Failed to send email:", e)
