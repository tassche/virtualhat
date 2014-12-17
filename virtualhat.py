"""Draw names from a virtual hat and email them."""

PARTICIPANTS = {
    'Person1': 'p1@example.com',
    'Person2': 'p2@example.com',
    'Person3': 'p3@example.com',
    'Person4': 'p4@example.com',
    'Person5': 'p5@example.com',
}

COUPLES = (
    ('Person1', 'Person2'),
    ('Person3', 'Person4'),
)

OCCASION = 'Virtual Hat Test'
SUBJECT = '{participant}, the draw has been made for {occasion}'
BODY = '''\
Hi {participant}

You drew {drawn_name}.
'''

FROM_ADDR = 'virtualhat@example.com'
SMTP_SERVER = 'smtp.example.com'
SMTP_PORT = 25


from email.mime.text import MIMEText
from smtplib import SMTP
import random


def random_permutation(iterable, r=None):
    pool = tuple(iterable)
    r = len(pool) if r is None else r
    return tuple(random.sample(pool, r))


def validate_draw(names, permutation, couples):
    for i in range(len(names)):
        if names[i] == permutation[i]:
            return False
        for couple in couples:
            if names[i] in couple and permutation[i] in couple:
                return False
    return True


def draw_names():
    names = tuple(PARTICIPANTS.keys())
    permutation = random_permutation(names)
    while(not validate_draw(names, permutation, COUPLES)):
        permutation = random_permutation(names)
    draw = {}
    for i in range(len(names)):
        draw[names[i]] = permutation[i]
    return draw


def send_email(from_addr, to_addr, subject, body, server, port):
    message = MIMEText(body)
    message['From'] = from_addr
    message['To'] = to_addr
    message['Subject'] = subject
    with SMTP(server, port) as smtp:
        smtp.send_message(message)


def send_draw(draw):
    for participant_name, drawn_name in draw.items():
        to_addr = PARTICIPANTS[participant_name]
        subject = SUBJECT.format(participant=participant_name,
                                 occasion=OCCASION)
        body = BODY.format(participant=participant_name,
                           drawn_name=drawn_name)
        send_email(FROM_ADDR, to_addr, subject, body, SMTP_SERVER, SMTP_PORT)


if __name__ == '__main__':
    draw = draw_names()
    send_draw(draw)
