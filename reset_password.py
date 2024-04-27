"""
This file handles the functionality for resetting the user password.
- open_forgot_password routes open the form for password reset
"""


# Route to handle sending a token to the user's email
@forgot_password_bp.route('/send_token', methods=['POST'])
def send_token():
    print("Sending token")
    email = request.form.get('email_address')
    
    email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'

    if email and re.match(email_regex, email):
        # Generate a unique token
        token = secrets.token_urlsafe(32)
        # Calculate expiration time (60 minutes from now)
        expiration_time = datetime.datetime.now() + datetime.timedelta(minutes=60)
        # Associate the token with the email address
        reset_tokens[token] = {'email': email, 'expiration_time': expiration_time}
        print(reset_tokens)
        # Send email with reset link containing the token
        send_reset_email(email, token, expiration_time)
        flash('An email with instructions to reset your password has been sent.')
        return redirect(url_for('forgot_password.open_reset_password'))
    else:
        flash('Please provide an email address.')
        return redirect(url_for('forgot_password.open_forgot_password'))


# Route to handle resetting the password using the token CREATE NEW PAGE WHERE THE USER CAN ENTER NEW PASSWORD
@forgot_password_bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password_with_token(token):
    if token in reset_tokens:
        email = reset_tokens[token]['email']
        expiration_time = reset_tokens[token]['expiration_time']
        
        if datetime.datetime.now() > expiration_time:
            # Token has expired
            del reset_tokens[token]
            flash('The token has expired. Please request a new password reset.')
            return redirect(url_for('forgot_password.open_forgot_password'))
        
        if request.method == 'POST':
            new_password = request.form.get('new_password')
            # Update user's password in the database (implement this function)
            update_password(email, new_password)
            # Remove token after use
            del reset_tokens[token]
            flash('Your password has been reset successfully.')
            return redirect(url_for('auth.login'))  # Redirect to login page
        
        return render_template('reset_password.html', token=token)
    else:
        flash('Invalid or expired token.')
        return redirect(url_for('forgot_password.open_forgot_password'))  # Redirect to forgot password page

# Function to update user's password in the database (implement this function)
def update_password(email, new_password):
    print(f"Updating password for {email} to {new_password}")

# Function to generate token (if needed)
def generate_token():
    return secrets.token_urlsafe(16)