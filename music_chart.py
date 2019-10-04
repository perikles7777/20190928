import requests
from bs4 import BeautifulSoup


from pymongo import MongoClient          
client = MongoClient('localhost', 27017) 
db = client.dbmusic                 


headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://www.genie.co.kr/chart/top200',headers=headers)


soup = BeautifulSoup(data.text, 'html.parser')


music_chart = soup.select('div.newest-list > div.music-list-wrap > table.list-wrap > tbody > tr.list')


rank = 1
for music in music_chart:
    a_tag = music.select_one('td > a.title')
    if a_tag is not None:
       

        title = a_tag.text
        artist = music.select_one('td > a.artist').text

        doc = {
            'rank' : rank,
            'title' : title,
            'artist' : artist
        }
        db.music_chart.insert_one(doc)
        #print(rank, title, artist)
        rank += 1



