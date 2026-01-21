import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.config import Config

def send_confirmation_email(to_email, booking_details):
    """
    Sends a booking confirmation email.
    """
    if not Config.EMAIL_SENDER or not Config.EMAIL_PASSWORD:
        return False, "Email credentials not configured."
    
    msg = MIMEMultipart()
    msg['From'] = Config.EMAIL_SENDER
    msg['To'] = to_email
    msg['Subject'] = "Dental Appointment Confirmation"
    
    body = f"""
    Dear {booking_details['name']},
    
    Your appointment has been successfully booked!
    
    Service: {booking_details['service']}
    Date & Time: {booking_details['date']}
    
    Thank you for choosing our Dental Clinic.
    
    Best regards,
    Dental Clinic Team
    """
    
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        server = smtplib.SMTP(Config.SMTP_SERVER, Config.SMTP_PORT)
        server.starttls()
        server.login(Config.EMAIL_SENDER, Config.EMAIL_PASSWORD)
        text = msg.as_string()
        server.sendmail(Config.EMAIL_SENDER, to_email, text)
        server.quit()
        return True, "Email sent successfully."
    except Exception as e:
        return False, f"Failed to send email: {str(e)}"
