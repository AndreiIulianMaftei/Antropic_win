# Email Sender Setup Guide

## Prerequisites

Before running the email sender, you need to set up Gmail App Password authentication:

### Step 1: Enable 2-Factor Authentication
1. Go to your Google Account settings (https://myaccount.google.com/)
2. Select "Security" from the left menu
3. Under "Signing in to Google," select "2-Step Verification"
4. Follow the prompts to enable 2FA if not already enabled

### Step 2: Generate App Password
1. In the same Security section, scroll down to "App passwords"
2. Click "App passwords"
3. Select "Mail" as the app
4. Select "Windows Computer" as the device
5. Click "Generate"
6. Copy the 16-character password (it will look like: `abcd efgh ijkl mnop`)

### Step 3: Set Environment Variable
Open PowerShell and run:
```powershell
$env:EMAIL_PASSWORD = "your_16_character_app_password"
```

Or set it permanently:
```powershell
[Environment]::SetEnvironmentVariable("EMAIL_PASSWORD", "your_16_character_app_password", "User")
```

### Step 4: Run the Email Sender
```powershell
python backend\app\agents\send_email.py
```

## Email Content Preview

The email will be sent from: `mafteiandreiiulian@gmail.com`
To: `sparshtyagi26@gmail.com`

Subject: **Investment Opportunity - Founder Compatibility Discussion**

The email presents a professional VC outreach with:
- Professional introduction from Venture Capital Partners
- Explanation of interest in the recipient's work
- Two meeting options:
  - Virtual meeting: https://bey.chat/96a7d634-d54c-4804-9a66-a9b9b639f77a
  - Phone conversation: https://elevenlabs.io/app/talk-to?agent_id=agent_7701k60ynmmvejyrk5wz40fjdvcj
- Professional closing and call-to-action

## Security Notes

- Never commit your App Password to version control
- The App Password is different from your regular Gmail password
- Keep your App Password secure and don't share it
- You can revoke App Passwords anytime from your Google Account settings

## Troubleshooting

If you get authentication errors:
1. Double-check that 2FA is enabled
2. Make sure you're using the App Password, not your regular password
3. Verify the EMAIL_PASSWORD environment variable is set correctly
4. Check that the App Password doesn't have any spaces (remove them)

## Functions Available

- `send_vc_outreach_email()`: Sends the predefined VC outreach email
- `send_custom_email(subject, recipient, custom_message)`: Sends a custom email with specified parameters