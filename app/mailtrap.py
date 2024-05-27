import mailtrap as mt
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
reset_pass_template_path = os.path.join(script_dir, 'templates', 'email-reset-password-template.html')
welcome_template_path = os.path.join(script_dir, 'templates', 'email-welcome-template.html')

# Read welcome mail template from file
def read_file_content(file_path):
    with open(file_path, "r") as file:
        return file.read()

# Send welcome mail to new users
def send_welcome_mail(recipient, username):
    html_content = read_file_content(welcome_template_path)
    html_content = html_content.replace("{{ username }}", username)
    
    mail = mt.Mail(
        sender=mt.Address(email="support@stratios.net", name="Skill-Forge Support"),
        to=[mt.Address(email=recipient)],
        subject="Welcome to Skill-Forge!",
        html=html_content,
        category="SignUps",
    )

    client = mt.MailtrapClient(token=os.getenv("MAILTRAP_API_TOKEN"))
    client.send(mail)


# Send password reset email with a generated token valid for 60 minutes
def send_reset_email(token, username, email, expiration_time):
    html_content = read_file_content(reset_pass_template_path)
    html_content = html_content.replace("{{ username }}", username)
    html_content = html_content.replace("{{ token }}", token)
    html_content = html_content.replace("{{ expiration_time }}", expiration_time.strftime("%d-%m-%Y %H:%M:%S"))

    mail = mt.Mail(
        sender=mt.Address(email="support@stratios.net", name="Skill-Forge Support"),
        to=[mt.Address(email=email)],
        subject="Skill-Forge Password Reset",
        html=html_content,
        category="Password Resets",
    )

    client = mt.MailtrapClient(token=os.getenv("MAILTRAP_API_TOKEN"))
    client.send(mail)


# Send email from the contact form
def send_contact_email(email, subject, message):
    support_email = os.getenv("SUPPORT_EMAIL")
    mail = mt.Mail(
        sender=mt.Address(email="support@stratios.net", name="Skill-Forge Support"),
        to=[mt.Address(email=email)],
        bcc=[mt.Address(email=support_email)],
        subject=f"Contact Form - {subject}",
        html = f"<p>{message}</p>",
        category="SignUps",)
    client = mt.MailtrapClient(token=os.getenv("MAILTRAP_API_TOKEN"))
    client.send(mail)
