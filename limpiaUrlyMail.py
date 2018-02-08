import re

urls = re.compile(r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)')
correos = re.compile(r'[^@]+@[^@]+\.[^@]+')


if re.match(urls, '//www.reddit.com/r/EatingDisorders/comments/2qt9q6/request_pregnancy_and_bn/'):
    print('Si filtra urls')

if re.match(correos, 'alejandro12@gmail.com'):
    print('Si filtra correos')
