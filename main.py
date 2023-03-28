# import member
import datetime as dt
import random

from member import Member
import requests
import json
import pandas as pd
from pandas import json_normalize
from tkinter import *
import numpy as np

class KoreaHolidays:


    def get_holidays(self):
        today = dt.datetime.today().strftime("%Y%m%d")
        today_year = dt.datetime.today().year

        KEY = "pKHtIPLJIFBsdudPWOIF4TEBHnwirJTRIdp7GFfIpKiRTLfHcWWWaPKMATdA9W%2BNFIUt6fd0aPkuoQl1hkKMUw%3D%3D"
        url = (
                "http://apis.data.go.kr/B090041/openapi/service/SpcdeInfoService/getRestDeInfo?_type=json&numOfRows=50&solYear="
                + str(today_year)
                + "&ServiceKey="
                + str(KEY)
        )
        response = requests.get(url)
        if response.status_code == 200:
            json_ob = json.loads(response.text)
            holidays_data = json_ob["response"]["body"]["items"]["item"]
            dataframe = json_normalize(holidays_data)
        # dateName = dataframe.loc[dataframe["locdate"] == int(today), "dateName"]
        # print(dateName)
        return dataframe["locdate"].to_list()

    def today_is_holiday(self):
        _today = dt.datetime.now().strftime("%Y%m%d")
        holidays = self.get_holidays()
        return holidays




localToday = dt.datetime.now()
# 날짜설정 완료

# print("localToday.weekday : " + str(localToday.weekday()))


# 공휴일 조건 빼주기

# 공휴일 배열 = holidays
KH = KoreaHolidays()
holidays = KH.today_is_holiday()


for i in holidays:  # 공휴일 조건
    if i == localToday:
        localToday = localToday + dt.timedelta(days=1)
        while True:  # 금토일 조건도 빼주기
            if localToday.weekday() <= 3:
                break;
            localToday = localToday + dt.timedelta(days=1)
while True:  # 금토일 조건도 빼주기
    if localToday.weekday() <= 3:
        break;
    localToday = localToday + dt.timedelta(days=1)
##################################### 함수만들기
def holidayCalculateAndPlus(lt) :
    localToday = lt + dt.timedelta(days=1)
    for i in holidays:  # 공휴일 조건
        if i == localToday:
            localToday = localToday + dt.timedelta(days=1)
            while True: # 금토일 조건도 빼주기
                if localToday.weekday() <= 3:
                    break;
                localToday = localToday + dt.timedelta(days=1)
    while True:  # 금토일 조건도 빼주기
        if localToday.weekday() <= 3:
            break;
        localToday = localToday + dt.timedelta(days=1)
    return localToday
#####################################
# 팀목록 가져와서 섞어주기

teamList = []

for value in Member.member:
    if (value["team"] not in teamList):
        teamList.append(value["team"])

random.shuffle(teamList)


oldMemberList = Member.member
newMemberLIst = []
team = list([] for i in range(0,len(teamList)))

# 팀 나눠주기
for i in range(0,len(teamList)):
    for oldMember in oldMemberList:
        if oldMember["team"]==teamList[i]:
            team[i].append(oldMember)
            # arr0.append(oldMember) # team이 MK인 member만 담긴다.
    # print("team" + str(i) + " : " + str(team[i]))

teamArr = []
for i in range(0,len(teamList)):
    teamArr.append(team[i])

##################################################################################
# 팀에서 랜덤으로 하나씩 뽑기
# teamSearchedResult = list(0 for i in range(0, len(teamList)))
total = 0
while True:
    # 섞어주기
    random.shuffle(teamArr)
    teamSearchedResult = list(0 for i in range(0, len(teamArr)))

    # print("teamArr : " + str(teamArr))
    # print("teamSearchedResult : " + str(teamSearchedResult))

    for i in range(0,len(teamArr)):
        if len(teamArr[i]) != 0: # 팀이 멤버가 있다면 뽑아라
            ranMember = random.choice(teamArr[i])
            newMemberLIst.append(ranMember)
            teamArr[i].remove(ranMember)
        elif len(teamArr[i]) == 0:  # 팀에서 다 뽑았으면
            teamSearchedResult[i] = 1
    if 0 not in teamSearchedResult:
        break

# print("섞은 MemberList : " + str(newMemberLIst))

# newMemberList에서 4명씩 혹은 3명씩 나눠서 일자에 배치해주자
size = len(newMemberLIst) # 18개 그대로 나온다 (-1 안되고 나온다)
calResult = divmod(size, 4)
# print("몫 : " + str(calResult[0]))
# print("나머지 : " + str(calResult[1]))
print("총인원 : " + str(size))

finalOutput = []
output = {"date":[],"person":[]} # key value여야하고
person = [] # 리스트



def saveFinalOutput(localToday, person):
    output["date"].append(localToday.strftime("%Y-%m-%d"))  #### A타입
    output["person"].append(person)
    finalOutput.append(output)


if calResult[1] == 1:
    if calResult[0] == 0:  # 나머지 1, 몫 0 인경우  (총인원: 1)
        for i in range(size): # 예를들면 size=5, i=0,1,2,3, ...
            person.append(newMemberLIst[i])

            saveFinalOutput(localToday, person)
    elif calResult[0] == 1: # 나머지 1, 몫 1 인경우 (총인원: 5)
        for i in range(size): # 예를들면 size=5, i=0,1,2,3, ...
            person.append(newMemberLIst[i])
            if i == size - 3:
                # person.append(newMemberLIst[i])
                saveFinalOutput(localToday, person)
                person = []                                           #### B타입
                output = {"date": [], "person": []}
                # 날짜를 +1 시켜줘야한다.
                localToday = holidayCalculateAndPlus(localToday)
            elif i == size - 1:
                saveFinalOutput(localToday, person)
            elif i > size - 3:
                pass
    elif calResult[0] == 2: # 나머지 1, 몫 2 인경우 (총인원: 9)
        for i in range(size): # 예를들면 17명일때 size=17, i=0,1,2,3, ...
            person.append(newMemberLIst[i])
            if i == size - 4 or i == size - 7:
                # person.append(newMemberLIst[i])
                saveFinalOutput(localToday, person)
                person = []                                           #### B타입
                output = {"date": [], "person": []}
                # 날짜를 +1 시켜줘야한다.
                localToday = holidayCalculateAndPlus(localToday)
            elif i == size - 1:
                saveFinalOutput(localToday, person)
            elif i > size - 4:
                pass
    else: # 나머지가 1인 일반적인 경우 (마지막 그룹을 3명,3명,3명 으로 묶는다)
        for i in range(size): # 예를들면 17명일때 size=17, i=0,1,2,3, ...
            person.append(newMemberLIst[i])
            if i == size - 7:
                # person.append(newMemberLIst[i])
                saveFinalOutput(localToday, person)
                person = []                                           #### B타입
                output = {"date": [], "person": []}
                # 날짜를 +1 시켜줘야한다.
                localToday = holidayCalculateAndPlus(localToday)
            elif i == size - 4:
                # person.append(newMemberLIst[i])
                saveFinalOutput(localToday, person)
                person = []                                           #### B타입
                output = {"date": [], "person": []}
                # 날짜를 +1 시켜줘야한다.
                localToday = holidayCalculateAndPlus(localToday)
            elif i == size - 1:
                saveFinalOutput(localToday, person)
            elif i > size - 7:
                pass
            elif (i + 1) != 1 and ((i + 1) % 4) == 0:
                # person.append(newMemberLIst[i])
                saveFinalOutput(localToday, person)
                person = []                                           #### B타입
                output = {"date": [], "person": []}
                # 날짜를 +1 시켜줘야한다.
                localToday = holidayCalculateAndPlus(localToday)
elif calResult[1] == 2: # 나머지=2
    if calResult[0] == 0: # 나머지 2, 몫 0 인경우  (총인원: 2)
        for i in range(size):
            person.append(newMemberLIst[i])
            if i == size - 1:
                saveFinalOutput(localToday, person)
    elif calResult[0] == 1: # 나머지 2, 몫 1 인경우 (총인원: 6)
        for i in range(size):
            person.append(newMemberLIst[i])
            if i == size - 4:
                # person.append(newMemberLIst[i])
                saveFinalOutput(localToday, person)
                person = []                                           #### B타입
                output = {"date": [], "person": []}
                # 날짜를 +1 시켜줘야한다.
                localToday = holidayCalculateAndPlus(localToday)

            elif i == size - 1:
                saveFinalOutput(localToday, person)
            elif i > size - 4:
                pass

    else: # 나머지가 2인 일반적인 경우 -> 마지막 그룹을 3명, 3명으로 묶는다.
        for i in range(size):
            person.append(newMemberLIst[i])
            if i == size - 4:
                # person.append(newMemberLIst[i])
                saveFinalOutput(localToday, person)
                person = []                                           #### B타입
                output = {"date": [], "person": []}
                # 날짜를 +1 시켜줘야한다.
                localToday = holidayCalculateAndPlus(localToday)

            elif i == size - 1:
                saveFinalOutput(localToday, person)
            elif i > size - 4:
                pass
            elif (i + 1) != 1 and ((i + 1) % 4) == 0:
                # person.append(newMemberLIst[i])
                saveFinalOutput(localToday, person)
                person = []                                           #### B타입
                output = {"date": [], "person": []}
                # 날짜를 +1 시켜줘야한다.
                localToday = holidayCalculateAndPlus(localToday)
elif calResult[1] == 3: # 나머지=3
    if calResult[0] == 0: # 나머지 3, 몫 0 인경우  (총인원: 3)
        for i in range(size):
            person.append(newMemberLIst[i])
            if i == size - 1:
                saveFinalOutput(localToday, person)
    else: # 나머지가 3인 일반적인 경우
        for i in range(size): # size : 11 , i=0,1,2,3,4,5,6,7,8,9,10
            person.append(newMemberLIst[i])
            if i == size - 4:
                # person.append(newMemberLIst[i])
                saveFinalOutput(localToday, person)
                person = []                                           #### B타입
                output = {"date": [], "person": []}
                # 날짜를 +1 시켜줘야한다.
                localToday = holidayCalculateAndPlus(localToday)

            elif i == size - 1:
                saveFinalOutput(localToday, person)
            elif i > size - 4:
                pass
            elif (i + 1) != 1 and ((i + 1) % 4) == 0:
                # person.append(newMemberLIst[i])
                saveFinalOutput(localToday, person)
                person = []                                           #### B타입
                output = {"date": [], "person": []}
                # 날짜를 +1 시켜줘야한다.
                localToday = holidayCalculateAndPlus(localToday)
elif calResult[1] == 0:
    for i in range(size):  # size : 11 , i=0,1,2,3,4,5,6,7,8,9,10
        person.append(newMemberLIst[i])
        if (i + 1) != 1 and ((i + 1) % 4) == 0:
            # person.append(newMemberLIst[i])
            saveFinalOutput(localToday, person)
            person = []                                           #### B타입
            output = {"date": [], "person": []}
            # 날짜를 +1 시켜줘야한다.
            localToday = holidayCalculateAndPlus(localToday)











print("[결과 - 중복 제거작업 전]")
for finalOutputDetail in finalOutput:
    print(finalOutputDetail)





# 한 날짜에 중복된 팀이 있다면, 다음 날짜의 팀원들과 바꿔주기
for i in range(len(finalOutput)):

    # print(str(i) + "째날")
    list = []
    list2 = []
    for j in range(len(finalOutput[i]["person"][0])): # i번째날 우정의밥멤버수만큼 반복 -> j번째
        # print("dddd" + str(j))
        # print(finalOutput[i]["person"][0][j]["team"]) # MK
        # print(finalOutput[i]["person"][0]) # [{'name': '바바바', 'team': 'MK'}, {'name': '최상수', 'team': 'MK'}, {'name': '유단비', 'team': 'MK'}]
        # print(finalOutput[i]["person"][0][j]) # {'name': '최상수', 'team': 'MK'}
        list.append(finalOutput[i]["person"][0][j]["team"])

    if ((i+1) != len(finalOutput)):  # 마지막 i번째가 아닐때
        for z in range(len(finalOutput[i+1]["person"][0])):  # i번째날 우정의밥멤버수만큼 반복 -> j번째
            list2.append(finalOutput[i+1]["person"][0][z]["team"])
    else:
        pass

    duplicatedMember = {}
    q = 0
    resultbol = False
    while q < len(finalOutput[i]["person"][0]):
        # 한날짜에 같은팀이 존재하는지? -> duplicated에 저장
        dup = [x for i, x in enumerate(list) if i != list.index(x)] # duplicated에 해당하는 멤버를 아무나 뽑아서, i+1 번째 duplicated에 해당하지 않는 멤버와 바꾼다. (duplicated = 중복된 팀 멤버의 팀이름)

        # 다음날짜
        dup2 = [x for i, x in enumerate(list2) if i != list2.index(x)] # print("finalOutput[i][person][0][j][team] : " + str(finalOutput[i]["person"][0][j]["team"])) # MK
        if dup!=[]:
            if finalOutput[i]["person"][0][q]["team"]==dup[0]: # 중복된게 있다면
                duplicatedMember = finalOutput[i]["person"][0][q] # duplicated = 팀중복의 멤버에 담고

                if dup2 != []: # 다음날짜에도 중복된 인원이 있다면? -> 그 인원을 뽑아서 현재날짜의 중복된 인원과 바꿔준다.
                    if (i+1) != len(finalOutput):
                        w = 0
                        while w < len(finalOutput[i+1]["person"][0]):
                            # for a in range(len(finalOutput[i+1]["person"][0])): # 그 멤버로 뽑는다.
                            if finalOutput[i+1]["person"][0][w]["team"] == dup2[0]:
                                duplicatedMember2 = finalOutput[i+1]["person"][0][w]  # duplicated = 팀중복의 멤버
                                finalOutput[i]["person"][0][q] = duplicatedMember2
                                finalOutput[i+1]["person"][0][w] = duplicatedMember
                                resultbol = True
                                break
                            w += 1
                    else: # 다음날짜에도 중복된 인원이 없다면?? -> 그래도 바꿔준다.
                        w = random.randint(0,len(finalOutput[i + 1]["person"][0]))
                        duplicatedMember2 = finalOutput[i + 1]["person"][0][w]  # duplicated = 팀중복의 멤버  ####### w는 랜덤으로 뽑은 숫자 (finalOutput[i + 1]["person"][0]의 len)
                        finalOutput[i]["person"][0][q] = duplicatedMember2
                        finalOutput[i + 1]["person"][0][w] = duplicatedMember
        q += 1
        if resultbol:
            break
    if resultbol:
        break

print("[최종결과]")
for finalOutputDetail in finalOutput:
    print(finalOutputDetail)


# # 예제2) 버튼만들기
# tk = Tk()
# # 함수 정의 (버튼을 누르면 텍스트 내용이 바뀜)
# def event():
#     button['text'] = '버튼 누름!'
#
# button = Button(tk,text='버튼입니다. 누르면 함수가 실행됩니다.',command=event)
# button2 = Button(tk,text='버튼2 입니다.')
# button.pack(side=LEFT,padx=10,pady=10) #side로 배치설정, padx로 좌우 여백설정, pady로 상하 여백설정
# button2.pack(side=LEFT, padx=10, pady= 10)
# tk.mainloop()



#
# localToday = localToday.strftime("%Y-%m-%d")
# print(localToday)






# 오늘 날짜부터 가져와야함


