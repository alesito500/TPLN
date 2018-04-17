import re
def getNUM():
  dic = {}
  dic_path = open('Dictionaries/LIWC2007_English131104.dic', 'r')
  cat = 0
  for line in dic_path.readlines():
      if cat < 65 and cat > 0:
          num = line.split('\t')
          dic[num.pop(0)] = 0
      cat = cat + 1
  dic_path.close()
  return dic

def getWORDS():
    dic = {}
    dic_path = open('Dictionaries/LIWC2007_English131104.dic', 'r')
    patron1 = re.compile(r'[0-9]{1,3}\t[a-z]')
    patron2 = re.compile(r'%')
    for line in dic_path.readlines():
        if not re.match(patron1,line) and not re.match(patron2, line):
            ac = line.split('\t')
            ac[-1] = ac[-1].replace('\n','')
            ac[0] = ac[0].replace('*', '.*')
            ac[0] = ac[0].replace('\'', '\\\'')
            dic[ac.pop(0)] = ac
    dic_path.close()
    return dic
