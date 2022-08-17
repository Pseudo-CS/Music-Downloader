import subprocess, time, json

f = open('Music Downloader/data280.json')
music = ''

data = json.load(f)

for i, dat in enumerate(data['items']):
    
    music = str(dat['track']['uri'])
    music.replace(':', '%3A')
    p = subprocess.Popen('curl -X "POST" "https://api.spotify.com/v1/playlists/7kbAloN1ujbSFdb19XWHag/tracks?uris='+music+'" -H "Accept: application/json" -H "Content-Type: application/json" -H "Authorization: Bearer BQClPcScCnXmhQ293FoRGYryu-KW8gvB2v0abimVkm8aOemVHm1oDFmSaKDnX-37T1rRzs58Milx3Se3zn3GBbbTjkMsBUvEXX9Ap49HpuxqMa8ky01MUReMP-00J9sDOyd6oAEdhX9XbkUH1FYFa9K17nxKnUYi1K3Mx9L_8S6v7DpVRKk9bPcXU-UOYKsAtziObCLuX7crHltHTiMtfQhfKOmtwEoTCzwXeAFdTO_aWfQjlIpn8Izo-PGR"', stdout=subprocess.PIPE, shell=True)
    print(p.communicate)
    time.sleep(2)

    
