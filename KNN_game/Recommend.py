import sim_function as sf

def getRecommendation(data, person, k=3, sim_function=sf.sim_pearson):
    result = sf.top_match(data, person, k)

    score = 0  # 플레이 시간 합을 위한 변수
    li = list()  # 리턴을 위한 리스트
    score_dic = dict()  # 유사도 총합을 위한 dic
    sim_dic = dict()  # 플레이 시간 총합을 위한 dic

    for sim, name in result:  # 튜플이므로 한번에
        print(sim, name)
        # simuser = name
        if sim <= 0: continue  # 유사도가 양수인 사람만
        for game in data[name]:
            if game not in data[person]:  # name이 플레이 시간을 게임
                score += sim * data[name][game]  # 그사람의 플레이 시간 * 유사도
                score_dic.setdefault(game, 0)  # 기본값 설정
                score_dic[game] += score  # 합계 구함

                # 조건에 맞는 사람의 유사도의 누적합을 구한다
                sim_dic.setdefault(game, 0)
                sim_dic[game] += sim

            score = 0  # 게임이 바뀌었으니 초기화한다

    for key in score_dic:
        score_dic[key] = score_dic[key] / sim_dic[key]  # 플레이 시간 총합/ 유사도 총합
        li.append((score_dic[key], key))  # list((tuple))의 리턴을 위해서.
    li.sort()  # 오름차순
    li.reverse()  # 내림차순
    # return li
    return name