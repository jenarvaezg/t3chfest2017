import smtplib

from email.mime.text import MIMEText

def send_mail(address, content):
    msg = MIMEText(content)
    msg['Subject'] = "Hue Status"
    msg['From']    = "HueBot@sandbox62a59026785245a3b1618ae2fb90b9d5.mailgun.org"
    msg['To']      = address

    s = smtplib.SMTP('smtp.mailgun.org', 587)

    s.login('postmaster@sandbox62a59026785245a3b1618ae2fb90b9d5.mailgun.org', '10cf9480b0fb0c9ade5b493be366ab33')
    s.sendmail(msg['From'], msg['To'], msg.as_string())
    s.quit()
