# 프로그램 소개
- **우정의 밥 프로그램** - 다른팀 직원들과 식사를 할 수 있게 인원배치를 도와주는 프로그램을 파이썬언어를 이용해 script 작성<br>
### 1. 전체적인 로직

1. 먼저, 각 팀에서 한 명씩 랜덤으로 뽑아서 다시 newMemberList에 append
→ 모든 팀에서 한명씩 뽑고 나서, 팀 순서를 다시 랜덤으로 섞기
(인접한 팀끼리만 먹는 경우 방지)
2. 총인원이 몇명인지에 따라서 묶어주는 인원을 각각 선언

![image](https://user-images.githubusercontent.com/70586428/229981294-7da302ad-ef79-476f-ae77-8a5163e9a6d8.png)

이렇게 각 날짜로 배치가 됐다면, 팀이 중복이 되는 부분이 있다면
최대한 중복을 없애주어야 한다.

1. 자바로 개발했던 방식 (버블 정렬처럼 첫 member부터 마지막 member까지 바꿔주는 방식)은 팀이 2팀만 있을때 문제가 된다.

![image](https://user-images.githubusercontent.com/70586428/229981332-78d317c4-0be7-49cc-a06e-17cee0ad4ee8.png)

→ 그래서 팀이 2팀만 있을 때에는 그 케이스를 따로 나누어주면 해결이 된다.
→ 무한루프에 걸리진 않을까? 하는 부분은 중복된 인원이 나오던 안 나오던 끝까지 바꿔주는 부분이었기 때문에 무한루프에는 걸리지 않는다는 사실을 도출해냈음.
→ 하지만 다른 방식으로 한번 개발해보고 싶었음
그래서 생각해낸 방안은…

- 한 날짜에서 팀원이 중복되는 상황이 있다면, 다음 날짜의 겹치는 팀원(혹은 안겹치는팀원)과 회원을 서로 바꿔주면 어떨까? 하는 아이디어 도출

![image](https://user-images.githubusercontent.com/70586428/229981354-1ef11d35-f954-4d8b-845f-059a230d62f1.png)

- 그래서, 첫 날짜에 중복되는 팀원들이 존재하면
다음팀 중복되는 인원(혹은 중복이 없다면 아무나)과 바꾸고,
→ 그다음 날짜도 체크해주고, 그 다다음 날짜로 체크해주고,,,
→ 결국은 마지막까지 비교하게 된다.

### 2. 특이사항

- 밥 투표 배치 날짜 중, 공휴일을 제외하는 부분 : 변경 위험성, 수정횟수 압축
    - **공공데이터포털 - Open API**를 불러와서 비교하는 방식으로 진행
- team의 len 만큼 리스트를 만들어주고싶은 상황 ( ex - team[0] : …. , team[1] : …. ,
…)
    
    → global 변수를 사용하려고 시도 : team0, team1 이런식으로 변수를 만들어주었으나
    for문을 돌려서 만들었으므로, 끝번호가 몇 번인지 파악이 안되는 문제
    → team = list([] for i in range(0,len(teamList))) 이런식으로 list 제작
    그러면 끝번호가 len(teamList)로 명확하게 나오게 되어 나중에 사용이 용이
    
- if문 안에 조건으로 for문을 작성할 수있는 방법이 파이썬에서는 없는 문제
    - 처음에 고안한 방법: boolean값인 teamSearchedResult를 len(team)만큼 만들
    어놓고,
    조건을 충족 할 때마다 teamSearchedResult[i] 값에 1을 넣는다. 그리고
    if 0 not in teamSearchedResult:
    위의 조건을 달아주어, while문을 탈출할 수 있게 만들어주었다.
    (처음에는 랜덤으로 두 배열을 섞어주려고 하였으나, 그러면 numpy의 shape개념
    까지
    공부하게되어 시간이 너무 오래걸릴 것 같아서 pass)


# Member
|Back-end|
|:---:|
|<img src="https://user-images.githubusercontent.com/70586428/197694674-88686917-38b4-4d9c-8a6e-93367fb56055.jpg" width="100"/>|
|[안인택](https://github.com/intacka)|

# Wiki
[Wiki 보러가기](https://shrouded-marigold-0d2.notion.site/WORK-COMMUTE-07c6a68d058749c0a7fe5e76b46f5668)
