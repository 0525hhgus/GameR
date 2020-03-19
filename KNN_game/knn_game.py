import math
import openpyxl


def sim_msd(data, name1, name2):
    sum = 0
    count = 0
    for movies in data[name1]:
        if movies in data[name2]: #같은 영화를 봤다면
            sum += pow(data[name1][movies]- data[name2][movies], 2)
            count += 1
 
    return 1 / ( 1 + (sum / count) )


def sim_cosine(data, name1, name2):
    sum_name1 = 0
    sum_name2 = 0
    sum_name1_name2 = 0
    count = 0
    for movies in data[name1]:
        if movies in data[name2]: #같은 영화를 봤다면
            sum_name1 += pow(data[name1][movies], 2)
            sum_name2 += pow(data[name2][movies], 2)
            sum_name1_name2 += data[name1][movies]*data[name2][movies]
    
    return sum_name1_name2 / (math.sqrt(sum_name1)*math.sqrt(sum_name2))

def sim_pearson(data, name1, name2):
    avg_name1 = 0
    avg_name2 = 0
    count = 0
    for movies in data[name1]:
        if movies in data[name2]: #같은 영화를 봤다면
            avg_name1 = data[name1][movies]
            avg_name2 = data[name2][movies]
            count += 1

    if(count == 0):
        return 0
    
    avg_name1 = avg_name1 / count
    avg_name2 = avg_name2 / count
    
    sum_name1 = 0
    sum_name2 = 0
    sum_name1_name2 = 0
    count = 0

    
    for movies in data[name1]:
        if movies in data[name2]: #같은 영화를 봤다면
            sum_name1 += pow(data[name1][movies] - avg_name1, 2)
            sum_name2 += pow(data[name2][movies] - avg_name2, 2)
            sum_name1_name2 += (data[name1][movies] - avg_name1) * (data[name2][movies] - avg_name2)

   

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
    
    score = 0 # 평점 합을 위한 변수
    li = list() # 리턴을 위한 리스트
    score_dic = dict() # 유사도 총합을 위한 dic
    sim_dic = dict() # 평점 총합을 위한 dic
 
    for sim, name in result: # 튜플이므로 한번에
        print(sim, name)
        #simuser = name
        if sim <= 0 : continue #유사도가 양수인 사람만
        for movie in data[name]: 
            if movie not in data[person]: #name이 평가를 내리지 않은 영화
                score += sim * data[name][movie] # 그사람의 영화평점 * 유사도
                score_dic.setdefault(movie, 0) # 기본값 설정
                score_dic[movie] += score # 합계 구함
 
                # 조건에 맞는 사람의 유사도의 누적합을 구한다
                sim_dic.setdefault(movie, 0) 
                sim_dic[movie] += sim
 
            score = 0  #영화가 바뀌었으니 초기화한다
            
    for key in score_dic:
        score_dic[key] = score_dic[key] / sim_dic[key] # 평점 총합/ 유사도 총합
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


print('탐색 유저')
print(userdata[10])
print()
# 한명만 가능
print('결과 유저')
print(userdata[getRecommendation(userdata, 10, k=1, sim_function=sim_pearson)])

wb.close()
