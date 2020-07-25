from flask import Flask, request
import os
import requests
app = Flask(__name__)

@app.route('/', methods=['POST'])
def parse():
    base_url = 'https://api.mailgun.net/v3'
    token = os.environ.get('MAILGUN_TOKEN', None)
    dest_inbox = os.environ.get('DESTINATION_INBOX', None)
    if not (token and dest_inbox):
        return None

    msg = request.form
    sender = msg['sender']
    recipient = msg['recipient']
    mailbox = recipient.split('@')[0]
    subject = msg['subject']
    text = msg['stripped-text']
    html = msg['stripped-html']

    auth = ('api', token)
    data = {
        'from': sender,
        'to': dest_inbox,
        'subject': f'[{mailbox.upper()}] {subject}',
        'text': text,
        'html': html
    }

    response = requests.post(f'{base_url}/mauricio.cc/messages', data, auth=auth)

    print(response.text, response.status_code)
    return f'{response.text}', response.status_code
