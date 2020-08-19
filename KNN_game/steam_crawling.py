import re
import requests
import json
import time
from fake_useragent import UserAgent

# web crawling
def steam_crawling(baseUrl):
    time.sleep(30)

    newGame = dict()

    ua = UserAgent()
    headers = {'User-Agent': str(ua.random)}

    # url='https://steamcommunity.com/profiles/'+string_ID+'/games/?tab=all&sort=playtime'
    url = baseUrl + 'games/?tab=all&sort=playtime'
    print(url)

    try:
        html = requests.get(url, headers=headers).text

        if 'An error was encountered' in html:
            print('429 Error')

        htmlSearch = re.search(r'var rgGames =(.+?);', html, re.S)

        gameList = htmlSearch.group(1)

        SteamGame = json.loads(gameList)


    except:
        print('error')

    if (str(SteamGame) != "[]" and 'hours_forever' in gameList):  # Private library Check

        for course in SteamGame:
            try:
                gameName = '{name}'.format(**course)
                gameName = gameName.replace(',', ' ')  # if 'comma' inside GameName, replace 'space'
                gameTime = '{hours_forever}'.format(**course)
                gameTime = gameTime.replace(',', '')  # if'comma' inside playtime, replace 'space'
                print(gameName)
                print(gameTime)
                newGame[gameName] = float(gameTime)

            except:
                print('error')


    else:
        print('비공개 계정입니다. 계정을 공개로 변경해주세요!')

    return newGame

