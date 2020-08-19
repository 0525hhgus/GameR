import math

def sim_msd(data, name1, name2):
    sum = 0
    count = 0
    for games in data[name1]:
        if games in data[name2]:  # 같은 게임을 했다면
            sum += pow(data[name1][games] - data[name2][games], 2)
            count += 1

    return 1 / (1 + (sum / count))


def sim_cosine(data, name1, name2):
    sum_name1 = 0
    sum_name2 = 0
    sum_name1_name2 = 0
    count = 0
    for games in data[name1]:
        if games in data[name2]:  # 같은 게임을 했다면
            sum_name1 += pow(data[name1][games], 2)
            sum_name2 += pow(data[name2][games], 2)
            sum_name1_name2 += data[name1][games] * data[name2][games]

    return sum_name1_name2 / (math.sqrt(sum_name1) * math.sqrt(sum_name2))


def sim_pearson(data, name1, name2):
    avg_name1 = 0
    avg_name2 = 0
    count = 0
    for games in data[name1]:
        if games in data[name2]:  # 같은 게임을 했다면
            avg_name1 = data[name1][games]
            avg_name2 = data[name2][games]
            count += 1

    if (count == 0):
        return 0

    avg_name1 = avg_name1 / count
    avg_name2 = avg_name2 / count

    sum_name1 = 0
    sum_name2 = 0
    sum_name1_name2 = 0
    count = 0

    for games in data[name1]:
        if games in data[name2]:  # 같은 게임을 플레이했다면
            sum_name1 += pow(data[name1][games] - avg_name1, 2)
            sum_name2 += pow(data[name2][games] - avg_name2, 2)
            sum_name1_name2 += (data[name1][games] - avg_name1) * (data[name2][games] - avg_name2)

    if (sum_name1_name2 == 0):
        return 0

    return (sum_name1_name2 / (math.sqrt(sum_name1) * math.sqrt(sum_name2)))

def top_match(data, name, index=3, sim_function=sim_pearson):
    li=[]
    for i in data: #딕셔너리를 돌고
        if name!=i: #자기 자신이 아닐때만
            li.append((sim_function(data,name,i),i)) #sim_function()을 통해 상관계수를 구하고 li[]에 추가
    li.sort() #오름차순
    li.reverse() #내림차순
    return li[:index]