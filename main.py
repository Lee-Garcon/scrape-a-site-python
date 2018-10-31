import requests
from bs4 import BeautifulSoup
import os
from os.path import join

while True:
  print('Enter Site:')
  url = input('> ')
  r = requests.get(url)
  print(r.__dict__.keys())
  try:
    res = requests.get(url)
  except Exception as e:
    print(e)
  if r.status_code == 200:

    selfdir = os.path.dirname(os.path.realpath('__file__'))
    dirname = url.replace('/', '-').replace('.', '-').replace(':', '_')
    print('name: %s' % join(selfdir, dirname))
    try:
      os.mkdir(join(selfdir, dirname))
    except:
      pass
    dirpath = join(selfdir, dirname)

    out = res.content
    soup = BeautifulSoup(out, 'html.parser')

    sp = [x for x in url.split('/') if x != ''] #disregard http/https
    print(sp)
    fullurl = sp[0]+'//'+sp[1]
    rootdir = '/'.join([fullurl] + sp[2:-1]) + '/'
    rootrootdir = '/'.join([fullurl] + sp[2:-2]) + '/'
    #print([link.get('href') for link in soup.find_all('a')])

    imgsrc = {}
    
    for x in [link.get('src') for link in soup.find_all('img')]:
      if not x:
      elif x.startswith('http'):
        imgsrc[x] = x
      elif x.startswith('/'):
        imgsrc[x] = join(fullurl, x[1:])
      elif x.startswith('../'):
        imgsrc[x] = join(rootrootdir, x[3:])
      elif x.startswith('./'):
        imgsrc[x] = join(rootdir, x)
      else:
        imgsrc[x] = join(rootdir, x)

    imgid = 0
    replacedict = {}
    corrupt_items = []
    for link in imgsrc.keys():
      corrupt = False
      imgurl = imgsrc[link]
      if imgurl.startswith('//'):
        imgurl = 'http:' + imgurl
      elif imgurl.startswith('/') and not imgurl.startswith('//'):
        imgurl = fullurl + imgurl

      r = requests.get(imgurl)
      print(':%s' % imgsrc[link])
      print(join(dirpath, str(imgid) + '.' + imgsrc[link].split('.')[-1]))
      print('type: %s' % r.headers['Content-Type'])
      try:
        f = open(join(dirpath, str(imgid) + '.' + imgsrc[link].split('.')[-1]), 'wb')
      except:
        if r.headers['Content-Type'].split('/')[0] == 'image':
          f = open(join(dirpath,str(imgid) + '.' + r.headers['Content-Type'].split('/')[-1]), 'wb')
        else:
          corrupt = True
        #f = open(join(dirpath, str(imgid)) + )
      if not corrupt:
        f.write(r.content)
        f.close()
        replacedict[link] = join(dirpath, str(imgid) + '.' + imgsrc[link].split('.')[-1])
        imgid += 1
      else:
        corrupt_items.append(link) 
      
      
    for x in soup.find_all('img'):
      if x.get('src') not in corrupt_items:
        x['src'] = replacedict[x.get('src')]

    outtext = str(soup)
    ext = url.split('.')[-1]
    if len(url.split('.')[-1]) > 5:
      ext = 'html'
    fname = dirname + '.' + ext
    f = open(join(dirpath, fname), 'w')
    f.write(outtext)
    f.close()
    print('finalized: %s' % join(dirpath, fname))
    #print('go to https://%s--%s.repl.co/%s/%s' % ())


    
