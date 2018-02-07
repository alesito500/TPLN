import re 

urls = re.compile(r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)')
correos = re.compile(r'[^@]+@[^@]+\.[^@]+')

   
if re.match(urls, 'https://thepiratebay.org/torrent/19954542/Keep_Watching_2017_DVDR'):
    print('Sí filtra urls')

if re.match(correos, 'alejandro12@gmail.com'):
    print('Sí filtra correos')


