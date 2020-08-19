import openpyxl
import steam_crawling as sc
import sim_function as sf
import Recommend as rc


userdata = {}
playGame = {}

preUser = 1
playGame = {}

# 엑셀파일 열기
wb = openpyxl.load_workbook('userdata.xlsx')

# 현재 Active Sheet 얻기
ws = wb.active

for r in ws.rows:
    userID = r[0].value

    if (preUser != userID):
        userdata[preUser] = playGame
        playGame = {}
        preUser = userID

    game = r[1].value
    playtime = r[2].value
    playGame[game] = playtime

userdata[preUser] = playGame

baseUrl = input('스팀 프로필 주소를 입력해주세요!')

print('탐색 유저')

user = sc.steam_crawling(baseUrl)

userdata[1000] = user

# print(user)
print()
# 한명만 가능
print('결과 유저')
print(userdata[rc.getRecommendation(userdata, 1000, k=1, sim_function=sf.sim_pearson)])

wb.close()