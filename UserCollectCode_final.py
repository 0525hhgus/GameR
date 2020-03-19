import re
import requests
import json
import datetime
import time
import csv
from fake_useragent import UserAgent

def steam_crawling(steamID, ID_Range, fileNum):
    userCount=int(fileNum)
    for n in range(ID_Range):
        time.sleep(35)
        steamID = steamID+1
        string_ID = str(steamID)

        ua = UserAgent()
        headers = {'User-Agent':str(ua.random)}

        url='https://steamcommunity.com/profiles/'+string_ID+'/games/?tab=all&sort=playtime'
        print(url)
        
        try:
            html=requests.get(url, headers=headers).text
            
            if 'An error was encountered' in html:
                #steamID = steamID + 1
                print('429 Error')
                time.sleep(1800)
                continue
            
            
            htmlSearch = re.search(r'var rgGames =(.+?);', html, re.S)

            gameList = htmlSearch.group(1)

            SteamGame = json.loads(gameList)


        except:
            continue
        
        if (str(SteamGame) != "[]" and 'hours_forever' in gameList):  #Private library Check
            userCount = userCount+1
            f = open('D:/Project/'+str(userCount)+'n'+'.csv', 'w', newline='')
            wr=csv.writer(f)
            
            for course in SteamGame:
                try:
                    gameName = '{name}'.format(**course)
                    gameName = gameName.replace(',',' ') #if 'comma' inside GameName, replace 'space'
                    gameTime = '{hours_forever}'.format(**course)
                    gameTime = gameTime.replace(',','') #if'comma' inside playtime, replace 'space'
                    print(gameName)
                    print(gameTime)
                    wr.writerow([string_ID, gameName, gameTime])
                    
                except:
                    continue
                    
            f.close()

        else:
            print('Private account')
            continue

# 76561198363008705 end

#76561197960266728+1000 +10
#steamID=76561197960266738+100 complete
#+100+30+20+50+?+10+100
#+100+100+100+100+100+80
#+100+50+218+3+72 + 926 + 430 + 107 + 29 + 369 end
steamID=76561198293008336

now = datetime.datetime.now()

steam_crawling(steamID, 369, 49)
