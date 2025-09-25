import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from datetime import datetime

def send_vc_outreach_email():
    """
    Send a professional VC outreach email offering founder compatibility meeting
    """
    # Email configuration
    sender_email = "mafteiandreiiulian@gmail.com"
    sender_password = os.getenv("EMAIL_PASSWORD")  # Set this environment variable
    recipient_email = "sparshtyagi26@gmail.com"
    
    # Create message
    message = MIMEMultipart("alternative")
    message["Subject"] = "Investment Opportunity - Founder Compatibility Discussion"
    message["From"] = sender_email
    message["To"] = recipient_email
    
    # Create the email content
    email_content = """
Dear Sparsh,

I hope this email finds you well. My name is Andrei Maftei, and I'm reaching out from Venture Capital Partners, a leading investment firm focused on innovative technology startups.

We've been following your work and recent developments, and I must say, we're genuinely impressed by what you've accomplished. Your approach to solving complex problems and the potential scalability of your solutions have caught our attention, and we believe there's significant synergy between your vision and our investment thesis.

After reviewing your profile and recent achievements, our investment committee has expressed strong interest in exploring a potential partnership. We'd love to schedule a founder compatibility discussion to better understand your goals, vision, and how we might support your journey.

To make this as convenient as possible for you, I'm offering two communication options:

🎥 **Virtual Meeting**: Join me for a video call where we can have a face-to-face conversation about your venture and our potential collaboration.
   Link: https://bey.chat/96a7d634-d54c-4804-9a66-a9b9b639f77a

📞 **Phone Conversation**: Prefer a more traditional approach? We can have an in-depth phone discussion about your startup and our investment opportunities.
   Link: https://elevenlabs.io/app/talk-to?agent_id=agent_7701k60ynmmvejyrk5wz40fjdvcj

Both options will allow us to explore:
• Your current business model and growth trajectory
• Strategic challenges you're facing
• How our resources and network can accelerate your success
• Potential investment structures that align with your goals

I'm excited about the possibility of working together and believe this could be the beginning of a transformative partnership for your venture.

Please let me know which communication method works best for you, and feel free to reach out if you have any questions before our discussion.

Looking forward to hearing from you soon.

Best regards,

Andrei Maftei
Senior Investment Partner
Venture Capital Partners
Email: mafteiandreiiulian@gmail.com

P.S. We typically move quickly on opportunities that align with our investment criteria, so I'd encourage you to reach out at your earliest convenience.
"""

    # Create plain text version
    text_part = MIMEText(email_content, "plain")
    
    # Create HTML version for better formatting
    html_content = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
            <p>Dear Sparsh,</p>
            
            <p>I hope this email finds you well. My name is <strong>Andrei Maftei</strong>, and I'm reaching out from <strong>Venture Capital Partners</strong>, a leading investment firm focused on innovative technology startups.</p>
            
            <p>We've been following your work and recent developments, and I must say, we're genuinely impressed by what you've accomplished. Your approach to solving complex problems and the potential scalability of your solutions have caught our attention, and we believe there's significant synergy between your vision and our investment thesis.</p>
            
            <p>After reviewing your profile and recent achievements, our investment committee has expressed strong interest in exploring a potential partnership. We'd love to schedule a founder compatibility discussion to better understand your goals, vision, and how we might support your journey.</p>
            
            <p>To make this as convenient as possible for you, I'm offering two communication options:</p>
            
            <div style="margin: 20px 0; padding: 15px; background-color: #f8f9fa; border-left: 4px solid #007bff;">
                <p><strong>🎥 Virtual Meeting</strong>: Join me for a video call where we can have a face-to-face conversation about your venture and our potential collaboration.</p>
                <p><a href="https://bey.chat/96a7d634-d54c-4804-9a66-a9b9b639f77a" style="color: #007bff; text-decoration: none; font-weight: bold;">Click here to join virtual meeting</a></p>
            </div>
            
            <div style="margin: 20px 0; padding: 15px; background-color: #f8f9fa; border-left: 4px solid #28a745;">
                <p><strong>📞 Phone Conversation</strong>: Prefer a more traditional approach? We can have an in-depth phone discussion about your startup and our investment opportunities.</p>
                <p><a href="https://elevenlabs.io/app/talk-to?agent_id=agent_7701k60ynmmvejyrk5wz40fjdvcj" style="color: #28a745; text-decoration: none; font-weight: bold;">Click here to start phone conversation</a></p>
            </div>
            
            <p>Both options will allow us to explore:</p>
            <ul>
                <li>Your current business model and growth trajectory</li>
                <li>Strategic challenges you're facing</li>
                <li>How our resources and network can accelerate your success</li>
                <li>Potential investment structures that align with your goals</li>
            </ul>
            
            <p>I'm excited about the possibility of working together and believe this could be the beginning of a transformative partnership for your venture.</p>
            
            <p>Please let me know which communication method works best for you, and feel free to reach out if you have any questions before our discussion.</p>
            
            <p>Looking forward to hearing from you soon.</p>
            
            <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #dee2e6;">
                <p><strong>Best regards,</strong></p>
                <p><strong>Andrei Maftei</strong><br>
                Senior Investment Partner<br>
                Venture Capital Partners<br>
                Email: <a href="mailto:mafteiandreiiulian@gmail.com" style="color: #007bff;">mafteiandreiiulian@gmail.com</a></p>
            </div>
            
            <p style="font-style: italic; color: #6c757d; margin-top: 20px;"><strong>P.S.</strong> We typically move quickly on opportunities that align with our investment criteria, so I'd encourage you to reach out at your earliest convenience.</p>
        </div>
    </body>
    </html>
    """
    
    html_part = MIMEText(html_content, "html")
    
    # Attach parts to message
    message.attach(text_part)
    message.attach(html_part)
    
    try:
        # Connect to Gmail's SMTP server
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()  # Enable encryption
        
        # Check if password is available
        if not sender_password:
            print("Warning: EMAIL_PASSWORD environment variable not set.")
            print("Please set it using: set EMAIL_PASSWORD=your_app_password")
            print("Note: You'll need to use an App Password, not your regular Gmail password.")
            print("To generate an App Password:")
            print("1. Go to your Google Account settings")
            print("2. Select Security")
            print("3. Under 'Signing in to Google,' select 2-Step Verification")
            print("4. At the bottom, select App passwords")
            print("5. Generate a password for 'Mail'")
            return False
            
        # Login and send email
        server.login(sender_email, sender_password)
        text = message.as_string()
        server.sendmail(sender_email, recipient_email, text)
        server.quit()
        
        print(f"✅ Email sent successfully!")
        print(f"From: {sender_email}")
        print(f"To: {recipient_email}")
        print(f"Subject: {message['Subject']}")
        print(f"Sent at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error sending email: {str(e)}")
        print("\nTroubleshooting tips:")
        print("1. Make sure EMAIL_PASSWORD environment variable is set with your Gmail App Password")
        print("2. Enable 2-factor authentication on your Gmail account")
        print("3. Generate an App Password (not your regular password)")
        print("4. Check your internet connection")
        return False

def send_custom_email(subject=None, recipient=None, custom_message=None):
    """
    Send a custom email with specified parameters
    """
    sender_email = "mafteiandreiiulian@gmail.com"
    sender_password = os.getenv("EMAIL_PASSWORD")
    
    # Use defaults if not provided
    if not subject:
        subject = "Investment Opportunity - Founder Compatibility Discussion"
    if not recipient:
        recipient = "sparshtyagi26@gmail.com"
    
    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = recipient
    
    if custom_message:
        text_part = MIMEText(custom_message, "plain")
        message.attach(text_part)
    else:
        # Use default VC outreach message
        return send_vc_outreach_email()
    
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        
        if not sender_password:
            print("❌ EMAIL_PASSWORD environment variable not set.")
            return False
            
        server.login(sender_email, sender_password)
        text = message.as_string()
        server.sendmail(sender_email, recipient, text)
        server.quit()
        
        print(f"✅ Custom email sent successfully!")
        print(f"From: {sender_email}")
        print(f"To: {recipient}")
        print(f"Subject: {subject}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error sending custom email: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 Starting VC Outreach Email Sender...")
    print("=" * 50)
    
    # Send the VC outreach email
    success = send_vc_outreach_email()
    
    if success:
        print("\n🎉 Mission accomplished! Your professional VC outreach email has been sent.")
    else:
        print("\n❌ Email sending failed. Please check the troubleshooting tips above.")
