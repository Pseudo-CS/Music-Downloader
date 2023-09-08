from ytmusicapi import YTMusic
from tqdm import tqdm
import requests, re, sys, time
from urllib.parse import unquote
from pathlib import Path
import spot

search = sys.argv[1]
headers = {
    'authority': 'ytmp3cut.com',
    'method': 'POST',   
    'path': '/ajax',
    'scheme': 'https',
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'content-length': '168',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'sec-fetch-dest': 'empty',
    'origin': 'https://ytmp3cut.com',
#    'sec-fetch-mode': 'cors',
#    'sec-fetch-site': 'none',
#    'sec-gpc': '1',
    'x-requested-with': 'XMLHttpRequest',
    'upgrade-insecure-requests': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.87 '
                  'Safari/537.36',
    'cookie': '_y_uid=84216db14db6547ffcd33cac0de75752; _y_cnt__clix=1; _y_dlx=1360:768:; _PWA=done; _y_cnt__PWAC_=2; dl_signal=on; _clid=done'
}

downloadValues = {'purpose': 'download', 'token': 'UOGsT-3s5_w:b2ea081fd6b23e6c381581107f8f4738','f': '0', 'd': '0', 'b': '320', 'c': '1', '_': '16454497922496338955573719192964', 'r': 'https://ytmp3cut.com/UOGsT-3s5_w'}
reqValues = {'purpose': 'audio', 'token':''}



def connect(vid, heads):
    heads['method'] = 'GET'
    heads['path'] = '/'+vid
    heads['accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
    # heads['sec-fetch-dest'] = 'document'
    # heads['sec-fetch-mode'] = 'navigate'
    if 'x-requested-with' in heads.keys():
        heads.pop('x-requested-with')
        heads.pop('content-length') 

    print('retrieving download token...')
    try:
        r = requests.get('https://ytmp3cut.com/'+vid, headers=heads)
    except:
        print('error occured, retrying....')
        time.sleep(2)
        r = requests.get('https://ytmp3cut.com/'+vid, headers=heads)
        print(r.status_code, r.reason)
    
    
    patter = re.compile(r'.token.:"([^"]|\\")*"')
    matches = patter.search(r.text)
    r.close()
    return matches.group().replace('"token":', '').strip('"')



def ajax(values): #request for retreiving download url
    print('executing ajax request ... ')
    try:
        r = requests.post('https://ytmp3cut.com/ajax', headers=headers, data=values)
    except:
        print('error occured retrying....')
        time.sleep(2)
        r = requests.post('https://ytmp3cut.com/ajax', headers=headers, data=values)
        print(r.status_code, r.reason)
    return r



def download(r): #opens download stream and returns file
    try:
        d = requests.get(r.json().get('mp3url'), stream=True)
    except:
        print('error occured, retrying...')
        time.sleep(2)
        d = requests.get(r.json().get('mp3url'), stream=True)
        print(d.status_code, d.reason)

    title = d.url
    patter = re.compile(r'.*\.mp3')
    matches = patter.search(title.split('/')[-1])
    title = unquote(matches.group())
        
    print('Downloading '+title)

    total = int(d.headers.get('content-length', 0))
    blocksz = 1024
    progress_bar = tqdm(total=total, unit='iB', unit_scale=True)
    
    with open(str(Path.home()) + "/Downloads/Music/" + title, 'wb') as file:
        for dat in d.iter_content(blocksz):
            progress_bar.update(len(dat))
            file.write(dat)
    progress_bar.close()



def token(id): #returns download token
    # heads['content-length'] = '66'
    reqValues['token'] = connect(id, headers)
    token = ajax(reqValues).json().get('audio')
    return token


ytmusic = YTMusic()



def execute(sec):
    print('searching youtube music.....')
    data = ytmusic.search(sec, 'songs')
    for cat in data:
        for tist in cat.get('artists'):
            print('Artist: ' + tist.get('name'))

        print('-------------------')
        downloadValues['token'] = token(cat.get('videoId')) #setting the token for accessing download servers 
        download(ajax(downloadValues))
        break

if search == 'spotify':
    for song in spot.get():
        execute(song)
        print('....................................................')
        time.sleep(3)
else:
    execute(search)