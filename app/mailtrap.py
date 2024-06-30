import mailtrap as mt
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
reset_pass_template_path = os.path.join(script_dir, 'templates', 'email-reset-password-template.html')
welcome_template_path = os.path.join(script_dir, 'templates', 'email-welcome-template.html')
contact_email_path = os.path.join(script_dir, 'templates', 'email-contact-template.html')
approve_submited_quest_path = os.path.join(script_dir, 'templates', 'email-approve-submited-quest-template.html')
reject_submited_quest_path = os.path.join(script_dir, 'templates', 'email-reject-submited-quest-template.html')
email_request_changes_quest_path = os.path.join(script_dir, 'templates', 'email-request-changes-submited-quest-template.html')

# Read welcome mail template from file
def read_file_content(file_path):
    with open(file_path, "r") as file:
        return file.read()

# Send welcome mail to new users
def send_welcome_mail(recipient, username):
    html_content = read_file_content(welcome_template_path)
    html_content = html_content.replace("{{ username }}", username)
    
    mail = mt.Mail(
        sender=mt.Address(email="support@stratios.net", name="Skill Forge Support"),
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
        sender=mt.Address(email="support@stratios.net", name="Skill Forge Support"),
        to=[mt.Address(email=email)],
        subject="Skill-Forge Password Reset",
        html=html_content,
        category="Password Resets",
    )

    client = mt.MailtrapClient(token=os.getenv("MAILTRAP_API_TOKEN"))
    client.send(mail)


# Send email from the contact form
def send_contact_email(username, email, subject, message):
    html_content = read_file_content(contact_email_path)
    html_content = html_content.replace("{{ username }}", username)
    html_content = html_content.replace("{{ message }}", message)
    
    support_email = os.getenv("SUPPORT_EMAIL")
    mail = mt.Mail(
        sender=mt.Address(email="support@stratios.net", name="Skill Forge Support"),
        to=[mt.Address(email=email)],
        bcc=[mt.Address(email=support_email)],
        subject=f"Contact Form - {subject}",
        html = html_content.replace("{{ message }}", message),
        category="SignUps",)
    client = mt.MailtrapClient(token=os.getenv("MAILTRAP_API_TOKEN"))
    client.send(mail)


# Send email to notify the user that their quest has been approved
def send_quest_approved_email(recipient, username, quest_name, quest_language, quest_id):
    html_content = read_file_content(approve_submited_quest_path)
    html_content = html_content.replace("{{ username }}", username)
    html_content = html_content.replace("{{ quest_name }}", quest_name)
    html_content = html_content.replace("{{ quest_language }}", quest_language)
    html_content = html_content.replace("{{ quest_id }}", quest_id)
    
    
    mail = mt.Mail(
        sender=mt.Address(email="support@stratios.net", name="Skill Forge Support"),
        to=[mt.Address(email=recipient)],
        subject="Your Quest has been approved!",
        html=html_content,
        category="Quests Approved")
    client = mt.MailtrapClient(token=os.getenv("MAILTRAP_API_TOKEN"))
    client.send(mail)

# Send email to notify the user that their quest has been rejected
def send_quest_rejected_email(recipient, username, quest_name, quest_language):
    html_content = read_file_content(reject_submited_quest_path)
    html_content = html_content.replace("{{ username }}", username)
    html_content = html_content.replace("{{ quest_name }}", quest_name)
    html_content = html_content.replace("{{ quest_language }}", quest_language)
    
    mail = mt.Mail(
        sender=mt.Address(email="support@stratios.net", name="Skill Forge Support"),
        to=[mt.Address(email=recipient)],
        subject="Your Quest has been rejected!",
        html=html_content,
        category="Quests Rejected")
    client = mt.MailtrapClient(token=os.getenv("MAILTRAP_API_TOKEN"))
    client.send(mail)
    
# Send email to notify the user that changes are requested for their quest
def send_quest_changes_requested_email(recipient, username, quest_name, quest_language, comments):
    print("Sending email")
    html_content = read_file_content(email_request_changes_quest_path)
    html_content = html_content.replace("{{ username }}", username)
    html_content = html_content.replace("{{ quest_name }}", quest_name)
    html_content = html_content.replace("{{ quest_language }}", quest_language)
    html_content = html_content.replace("{{ specific_comments }}", comments)
    
    mail = mt.Mail(
        sender=mt.Address(email="support@stratios.net", name="Skill Forge Support"),
        to=[mt.Address(email=recipient)],
        subject="Changes requested for your Quest",
        html=html_content,
        category="Quests Changes Requested")
    client = mt.MailtrapClient(token=os.getenv("MAILTRAP_API_TOKEN"))
    client.send(mail)
    print("Email sent")
