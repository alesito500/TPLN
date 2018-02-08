import re

urls = re.compile(r'(http)?s?\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)')
correos = re.compile(r'[^@]+@[^@]+\.[^@]+')


if re.match(urls, 'todo'):
    print('Si filtra urls')

if re.match(correos, 'alejandro12@gmail.com'):
    print('Si filtra correos')
