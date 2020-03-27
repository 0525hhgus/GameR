import math
import openpyxl
import re
import requests
import json
import datetime
import time
from fake_useragent import UserAgent

# web crawling
def steam_crawling(baseUrl):
        time.sleep(30)
        
        newGame = dict()

        ua = UserAgent()
        headers = {'User-Agent':str(ua.random)}

        #url='https://steamcommunity.com/profiles/'+string_ID+'/games/?tab=all&sort=playtime'
        url = baseUrl+'games/?tab=all&sort=playtime'
        print(url)
        
        try:
            html=requests.get(url, headers=headers).text
            
            if 'An error was encountered' in html:
                print('429 Error')
                
            
            
            htmlSearch = re.search(r'var rgGames =(.+?);', html, re.S)

            gameList = htmlSearch.group(1)

            SteamGame = json.loads(gameList)


        except:
            print('error')
            
        
        if (str(SteamGame) != "[]" and 'hours_forever' in gameList):  #Private library Check
            
            for course in SteamGame:
                try:
                    gameName = '{name}'.format(**course)
                    gameName = gameName.replace(',',' ') #if 'comma' inside GameName, replace 'space'
                    gameTime = '{hours_forever}'.format(**course)
                    gameTime = gameTime.replace(',','') #if'comma' inside playtime, replace 'space'
                    print(gameName)
                    print(gameTime)
                    newGame[gameName] = float(gameTime)
                    
                except:
                    print('error')
                    

        else:
            print('비공개 계정입니다. 계정을 공개로 변경해주세요!')
            

        return newGame


def sim_msd(data, name1, name2):
    sum = 0
    count = 0
    for games in data[name1]:
        if games in data[name2]: #같은 게임을 했다면
            sum += pow(data[name1][games]- data[name2][games], 2)
            count += 1
 
    return 1 / ( 1 + (sum / count) )


def sim_cosine(data, name1, name2):
    sum_name1 = 0
    sum_name2 = 0
    sum_name1_name2 = 0
    count = 0
    for games in data[name1]:
        if games in data[name2]: #같은 게임을 했다면
            sum_name1 += pow(data[name1][games], 2)
            sum_name2 += pow(data[name2][games], 2)
            sum_name1_name2 += data[name1][games]*data[name2][games]
    
    return sum_name1_name2 / (math.sqrt(sum_name1)*math.sqrt(sum_name2))

def sim_pearson(data, name1, name2):
    avg_name1 = 0
    avg_name2 = 0
    count = 0
    for games in data[name1]:
        if games in data[name2]: #같은 게임을 했다면
            avg_name1 = data[name1][games]
            avg_name2 = data[name2][games]
            count += 1

    if(count == 0):
        return 0
    
    avg_name1 = avg_name1 / count
    avg_name2 = avg_name2 / count
    
    sum_name1 = 0
    sum_name2 = 0
    sum_name1_name2 = 0
    count = 0

    
    for games in data[name1]:
        if games in data[name2]: #같은 영화를 봤다면
            sum_name1 += pow(data[name1][games] - avg_name1, 2)
            sum_name2 += pow(data[name2][games] - avg_name2, 2)
            sum_name1_name2 += (data[name1][games] - avg_name1) * (data[name2][games] - avg_name2)

   

    if( sum_name1_name2 == 0):
        return 0;
    
    return (sum_name1_name2 / (math.sqrt(sum_name1)*math.sqrt(sum_name2)))

def top_match(data, name, index=3, sim_function=sim_pearson):
    li=[]
    for i in data: #딕셔너리를 돌고
        if name!=i: #자기 자신이 아닐때만
            li.append((sim_function(data,name,i),i)) #sim_function()을 통해 상관계수를 구하고 li[]에 추가
    li.sort() #오름차순
    li.reverse() #내림차순
    return li[:index]

def getRecommendation (data, person, k=3, sim_function=sim_pearson):
    
    result = top_match(data, person, k)
    
    score = 0 # 플레이 시간 합을 위한 변수
    li = list() # 리턴을 위한 리스트
    score_dic = dict() # 유사도 총합을 위한 dic
    sim_dic = dict() # 플레이 시간 총합을 위한 dic
 
    for sim, name in result: # 튜플이므로 한번에
        print(sim, name)
        #simuser = name
        if sim <= 0 : continue #유사도가 양수인 사람만
        for game in data[name]: 
            if game not in data[person]: #name이 플레이 시간을 게임
                score += sim * data[name][game] # 그사람의 플레이 시간 * 유사도
                score_dic.setdefault(game, 0) # 기본값 설정
                score_dic[game] += score # 합계 구함
 
                # 조건에 맞는 사람의 유사도의 누적합을 구한다
                sim_dic.setdefault(game, 0) 
                sim_dic[game] += sim
 
            score = 0  #게임이 바뀌었으니 초기화한다
            
    for key in score_dic:
        score_dic[key] = score_dic[key] / sim_dic[key] # 플레이 시간 총합/ 유사도 총합
        li.append((score_dic[key],key)) # list((tuple))의 리턴을 위해서.
    li.sort() #오름차순
    li.reverse() #내림차순
    #return li
    return name


userdata = { }
playGame = { }

preUser = 1
playGame = { }
 
# 엑셀파일 열기
wb = openpyxl.load_workbook('userdata.xlsx')
 
# 현재 Active Sheet 얻기
ws = wb.active
 
for r in ws.rows:
    userID = r[0].value

    if( preUser != userID ):
        userdata[preUser] = playGame
        playGame = { }
        preUser = userID
    
    game = r[1].value
    playtime = r[2].value
    playGame[game] = playtime 
    
userdata[preUser] = playGame

baseUrl = input('스팀 프로필 주소를 입력해주세요!')

print('탐색 유저')

user = steam_crawling(baseUrl)

userdata[1000] = user

#print(user)
print()
# 한명만 가능
print('결과 유저')
print(userdata[getRecommendation(userdata, 1000, k=1, sim_function=sim_pearson)])

wb.close()

