import base64
import requests

client_id = 'eda12a570bbc45acb1838434b482f684'
client_secret = '0cb0b76eb9594ebcac2f507f01b139d9'
final = client_id + ':' + client_secret
final = str(base64.b64encode(bytes(final, 'utf-8'))).strip('b\'').strip('\'')


headers = {'Authorization': 'Basic ' + final, 
            'Content-Type': 'application/x-www-form-urlencoded'}
data = {'grant_type': 'client_credentials'}



def get():
    try:
        r = requests.post('https://accounts.spotify.com/api/token', headers=headers, data=data)
    except:
        print(r.status_code, r.reason)

    headin = {'Authorization': 'Bearer ' + r.json().get('access_token')}

    try:
        d = requests.get('https://api.spotify.com/v1/playlists/7kbAloN1ujbSFdb19XWHag', headers=headin)
    except:
        print(d.status_code, d.reason)
    
    tracks = []
    for track in d.json()['tracks']['items']:
        search = track['track']['name'] + '' + track['track']['artists'][0]['name']
        tracks.append(search)

    print('No.of tracks to be downloaded : '+str(len(tracks)))
    return tracks

# help