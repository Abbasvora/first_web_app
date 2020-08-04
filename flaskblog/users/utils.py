import os
import secrets
from PIL import Image
from flask import url_for, current_app
import smtplib

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


def send_reset_email(user):
    token = user.get_reset_token()
    email = os.environ.get('EMAIL_USER')
    password = os.environ.get('EMAIL_PASS')

    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(email, password)
    subject = 'Password Reset Request'
    body = f'''To reset your password visit following link.
     {url_for('users.reset_password', token=token, _external=True)}
     If you did not make this request then ignore this email. No changes will be made.
     '''
    msg = f'Subject: {subject}\n\n{body}'
    server.sendmail(
    "noreply@domain.com",
    user.email,
    msg)
    server.quit()
