import requests
from bs4 import BeautifulSoup as BS
import os
import random

os.system('cls')
extensions = []
links = []
ids = []
errors = []
folders = ['sonnets']
# fill = lists
# write = txts
# populate = dicts

base = 'https://shakespeare.folger.edu/shakespeares-works/shakespeares-sonnets/'

def find_all_idx(main, sub):
  res = [i for i in range(len(main)) if main.startswith(sub, i)]
  return res

def unicodetoascii(text):
  TEXT = (text.replace('\\xe2\\x80\\x99', "'").replace('\\xc3\\xa9', 'e').replace('\\xc3\\xa8', 'e').replace('⌜','@').replace('⌝','$').replace('\\xc2\\xa0', '').replace('\\xe2\\x8c\\x9c','').replace('\\xe2\\x8c\\x9d','').replace('\\xe2\\x80\\x90','-').replace('\\xe2\\x80\\x91', '-').replace('\\xe2\\x80\\x92','-').replace('\\xe2\\x80\\x93', '-').replace('\\xe2\\x80\\x94','-').replace('\\xe2\\x80\\x94', '-').replace('\\xe2\\x80\\x98',"'").replace('\\xe2\\x80\\x9b', "'").replace('\\xe2\\x80\\x9c','"').replace('\\xe2\\x80\\x9c', '"').replace('\\xe2\\x80\\x9d','"').replace('\\xe2\\x80\\x9e', '"').replace('\\xe2\\x80\\x9f','"').replace('\\xe2\\x80\\xa6', '...').replace('\\xe2\\x80\\xb2',"'").replace('\\xe2\\x80\\xb3', "'").replace('\\xe2\\x80\\xb4', "'").replace('\\xe2\\x80\\xb5', "'").replace('\\xe2\\x80\\xb6', "'").replace('\\xe2\\x80\\xb7', "'").replace('\\xe2\\x81\\xba', "+").replace('\\xe2\\x81\\xbb', "-").replace('\\xe2\\x81\\xbc',"=").replace('\\xe2\\x81\\xbd',"(").replace('\\xe2\\x81\\xbe', ")"))
  return TEXT

def write_ext():
  with open('extensions.txt', 'w'):
    pass
  for x in range(1, 155):
    with open('extensions.txt', 'a') as f:
      f.write(f'sonnet-{x}')
      f.write('\n')

def fill_ext():
  with open('extensions.txt') as f:
    for ext in f:
      extensions.append(ext.strip('\n'))

def write_ids():
  with open('ids.txt', 'a') as f:
    for x in range(1,155):
      f.write(f'{str(x).rjust(3,"0")}\n')

def fill_ids():
  with open('ids.txt') as f:
    for line in f:
      ids.append(line.strip('\n'))

def write_txt_and_synopsi(extnum):
  r = requests.get(f'{base+str(extnum)}/')
  soup = BS(r.content, 'html.parser')
  extid = ''
  for x in range(0, 4):
    if extnum[-x::].isdigit() == True:
      extid = (extnum[-x::])
  extid = extid.rjust(3, '0')
  for link in soup.find_all('div', class_="div1", id=f'Son-{extid}'):
    with open(f'sonnets/{extid}.txt', 'w', encoding='utf-8') as f:
      print('---', extid)
      f.write(unicodetoascii(str(str(link))))
    links.append(link)


def clean_brid(extid):
  with open(f'sonnets/{extid}.txt') as f:
    for line in f:
      newline = line
  for x in range(len(find_all_idx(newline, '<span'))):
    stt = find_all_idx(newline, '<span')
    end = find_all_idx(newline, '</span>')
    try:
      newline = newline.replace(line[stt[x]:end[x] + 7], '')
    except:
      pass
    with open(f'sonnets/{extid}.txt', 'w') as h:
      h.write(newline)
  return extid, len(find_all_idx(line, '<span'))

def clean(folder, extid):
  with open(f'{folder}/{extid}.txt') as f:
    for line in f:
      line = line
  line = unicodetoascii(line)
  line = line.replace('\\n', ' ')
  line = line.strip('\'b')
  line = line.replace('<br/>', '#')
  ope = line.index('<')
  clse = line.index('>')
  to_remove = line[ope:clse + 1]
  if 'lineNbr' in to_remove:
    lne = line.replace(to_remove, '')
  else:
    lne = line.replace(to_remove, '')
  with open(f'{folder}/{extid}.txt', 'w') as f:
    f.write(lne)

def clean_up(extid):
  for x in range(100):
    try:
      clean('sonnets', extid)
    except:
      break

def cleaning():
  for id in ids:
    clean_up(id)
    with open(f'sonnets/{id}.txt', encoding="utf-8") as f:
      for line in f:
        if '\\' in line:
          print(id)
          errors.append(line)
  nonumsing()
  print('No Nums')

def nonums(extid):
  newline = ''
  with open(f'sonnets/{extid}.txt', 'r', encoding='utf-8') as f:
    for line in f:
      for char in line:
        if char.isnumeric() == False:
          newline += char
  with open(f'sonnets/{extid}.txt', 'w') as h:
    h.write(newline.strip().strip('#'))

def nonumsing():
  for id in ids:
    nonums(id)

def startup():
  #os.system('cls')
  for name in folders:
    newpath = name
    if not os.path.exists(newpath):
      os.makedirs(newpath)
  with open('extensions.txt','r') as f:
    if len(f.read()) == 0:
      write_ext()
  fill_ext()
  with open('ids.txt','r') as h:
    if len(h.read()) == 0:
      with open('ids.txt','a') as r:
        for x in range(1,155):
          r.write(f'{str(x).rjust(3,"0")}\n')  
  fill_ids()             
  rewriteq = input('Resest Sonnet Txts?\ny\\n\n')
  if rewriteq.lower() == 'y':
    write_txt_and_synopsi(id)
       
startup()
