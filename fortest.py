import pandas as pd
import os
import re
import datetime
import findinglist
import making

# 행 열 제한 해제
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

df1, df2, df3 = making.Makedf()

# -----------------------------
# 📌 문자 이력 출력
# -----------------------------
for idx, row in df3.iterrows():
    name = row['이름']
    phone = row['전화번호']

    print(name)

    history = df1[df1['수신번호'] == phone]

    for _, h in history.iterrows():
        if h['날짜차이'] <= 5:
            print('너무 짧아')

        send = h['전송일자']
        print(f"{send.month}/{send.day} {h['날짜차이']} Days")
        print(h['문자내용'])

        if h['결과'] != '성공':
            print("전송실패!!")
        print()
    print()

# -----------------------------
# 📌 이름 리스트 로드
# -----------------------------
with open('namelist.txt', 'r', encoding="utf-8") as f:
    namelist = [word for line in f for word in re.split(r'\s|,|\.', line) if word]

print(namelist)
print(len(namelist))
print()

# -----------------------------
# 📌 최근 문자 수신자 목록
# -----------------------------
recent_df = df1[df1['날짜차이'] >= 0]

recent_number_diff = (
    recent_df[['수신번호', '날짜차이']]
    .drop_duplicates()
    .merge(df3[['이름', '전화번호']], left_on='수신번호', right_on='전화번호', how='left')
    .drop(columns='전화번호')
    .dropna()
    .drop_duplicates(subset='이름')
)

print(recent_number_diff)
print(len(recent_number_diff))

# -----------------------------
# 📌 namelist 이름들의 전화번호 추출
# -----------------------------
namelist_df = df3[df3['이름'].isin(namelist)]
namelist_phones = namelist_df['전화번호'].tolist()

print("\n📋 namelist 전화번호 목록:")
for phone in namelist_phones:
    print(phone)

# -----------------------------
# 📌 namelist 이름들의 최근 문자 날짜차이 출력
# -----------------------------
print("\n📋 namelist 통합 문자 이력 + log 기록:")

log = pd.read_excel("log.xlsx")

for name in namelist:
    matched = df3[df3['이름'] == name]

    if matched.empty:
        print(f"{name} | 정보 없음")
        continue

    phone = matched.iloc[0]['전화번호']

    # --------------------------------
    # 📌 1) 문자 발송 이력(df1)
    # --------------------------------
    history = df1[df1['수신번호'] == phone]

    if history.empty:
        msg_info = "문자 이력 없음"
    else:
        recent = history.sort_values(by='전송일자', ascending=False).iloc[0]
        msg_info = f"문자: {recent['날짜차이']}일 전"

    # --------------------------------
    # 📌 2) log.xlsx 기록 여부
    # --------------------------------
    log_match = log[log['수신번호'].astype(str).str.contains(str(phone), na=False)]

    if log_match.empty:
        log_info = "로그 없음"
    else:
        # 날짜 컬럼이 '날짜' 라는 가정
        if '날짜' in log_match.columns:
            log_date = log_match.iloc[0]['날짜']
            log_info = f"로그: {log_date}"
        else:
            log_info = "로그 기록 있음(날짜 없음)"

        # --------------------------------
        # 📌 최종 통합 출력
        # --------------------------------
    print(f"{name} | {phone} | {msg_info} | {log_info}")
