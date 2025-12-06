import pandas as pd
import os
import re
import datetime
import findinglist
import making



# 행과 열 제한 해제
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)


df1, df2, df3 = making.Makedf()


# 문자 이력 확인
for i in range(len(df3.index)):
    print(df3.loc[df3.index[i], '이름'])
    for j in range(len(df1)):
        if df1.loc[df1.index[j], '수신번호'] == df3.loc[df3.index[i], '전화번호']:
            if df1.loc[df1.index[j], '날짜차이'] <= 5:
                print('너무 짧아')
            print(f"{df1.loc[df1.index[j], '전송일자'].month}/{df1.loc[df1.index[j], '전송일자'].day} "
                  f"{df1.loc[df1.index[j], '날짜차이']} Days")
            print(df1.loc[df1.index[j], '문자내용'])
            if df1.loc[df1.index[j], '결과'] != '성공':
                print('전송실패!!')
            print()
    print()

# 이름 리스트 로드
namelist = []
with open('namelist.txt', 'r', encoding="utf-8") as f:
    for line in f:
        namelist += [word for word in re.split(r'\s|,|\.', line) if word]

print(namelist)
print(len(namelist))
print()

# 최근 5일 이내 문자 수신자 목록 출력
recent_df = df1[df1['날짜차이'] >=0 ]
recent_numbers = recent_df['수신번호'].unique()


print("\n✅ 최근  문자 수신자 전화번호 + 날짜차이 목록:")
recent_number_diff = recent_df[['수신번호', '날짜차이']].drop_duplicates()
# print(recent_number_diff)
# 전화번호 기준으로 df3와 조인 (df3['전화번호']와 recent_number_diff['수신번호'])
recent_number_diff = recent_number_diff.merge(
    df3[['이름', '전화번호']],
    left_on='수신번호',
    right_on='전화번호',
    how='left'
)

# '전화번호' 컬럼은 중복이므로 제거
recent_number_diff.drop(columns='전화번호', inplace=True)
recent_number_diff = recent_number_diff.dropna()
# 결과 출력
# print(recent_number_diff)

recent_number_diff = recent_number_diff.drop_duplicates(subset='이름')
print(recent_number_diff)
print(len(recent_number_diff))




# namelist에 포함된 이름의 전화번호와 문자 발송 이력 출력
print("\n📋 namelist에 있는 이름들의 전화번호:")
namelist_phones = []

for name in namelist:
    for i in range(len(df3)):
        if df3.loc[df3.index[i], '이름'] == name:
            phone = df3.loc[df3.index[i], '전화번호']
            namelist_phones.append(phone)
            print(phone)

print("\n📋 namelist에 있는 이름들의 전화번호 + 날짜차이:")

for name in namelist:
    # df3에서 이름으로 검색
    matched = df3[df3['이름'] == name]

    if not matched.empty:
        phone = matched.iloc[0]['전화번호']
        # 문자 이력에서 해당 전화번호에 대한 이력 필터
        history = df1[df1['수신번호'] == phone]

        if not history.empty:
            recent = history.sort_values(by='전송일자', ascending=False).iloc[0]
            days_diff = recent['날짜차이']
            print(f" {name},  {phone},  {days_diff}")
        else:
            print(f"이름: {name}, 전화번호: {phone}, 날짜차이: 문자 발송 이력 없음")
    else:
        print(f"이름: {name}, 전화번호: 없음, 날짜차이: 정보 없음")


findinglist
log = pd.read_excel("log.xlsx")

for i in namelist_phones:
    mask = log['수신번호'].str.contains(i, na=False)

    if mask.any():
        print()
        # print(log[mask].iloc[0])    # ← 일치하는 행 출력
    else:
        print()