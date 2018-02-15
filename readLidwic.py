import re
dic_path = open('Dictionaries/LIWC2007_English131104.dic', 'r')
def getNUM():
  dic = []
  cat = 0
  for line in dic_path.readlines():
      if cat < 65 and cat > 0:
          num = line.split('\t')
          dic.append(num.pop(0))
      cat = cat + 1
  dic_path.close()
  return dic

def getWORDS():
    dic = {}
    patron1 = re.compile(r'[0-9]{1,3}\t[a-z]')
    patron2 = re.compile(r'%')
    for line in dic_path.readlines():
        if not re.match(patron1,line) and not re.match(patron2, line):
            print line
            # ac = line.split('\t')
            # dic[ac.pop(0)] = ac
        cat = cat + 1
    return dic

getWORDS()
