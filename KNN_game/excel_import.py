import openpyxl

userdata = { }
playGame = { }

preUser = 1
playGame = { }
 
# 엑셀파일 열기
wb = openpyxl.load_workbook('userdata_test.xlsx')
 
# 현재 Active Sheet 얻기
ws = wb.active
# ws = wb.get_sheet_by_name("Sheet1")
 
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

    #print(userdata)

    
     
    #print(userID, game, playtime)

print(userdata)
 
wb.close()
