import pandas as pd
import re
import datetime
import making

# 행 열 제한 해제
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

df1, df3 = making.Makedf()

# -----------------------------
# 📌 문자 이력 출력 (iterrows → itertuples)
# -----------------------------
for row in df3.itertuples():
    name = row.이름
    phone = row.전화번호

    print(name)

    history = df1[df1['수신번호'] == phone]

    for h in history.itertuples():
        if h.날짜차이 <= 5:
            print("너무 짧아")

        send = h.전송일자
        print(f"{send.month}/{send.day} {h.날짜차이} Days")
        print(h.문자내용)

        if h.결과 != '성공':
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
# 📌 최근 문자 수신자 목록 (벡터 기반)
# -----------------------------
recent_df = df1[df1['날짜차이'] >= 0]

recent_number_diff = (
    recent_df[['수신번호', '날짜차이']]
    .drop_duplicates()
    .merge(df3[['이름', '전화번호']], left_on='수신번호', right_on='전화번호')
    .drop(columns=['전화번호'])
    .dropna()
)

print(recent_number_diff)
print(len(recent_number_diff))

# -----------------------------
# 📌 namelist → 전화번호 매핑 (merge 기반)
# -----------------------------
namelist_df = pd.DataFrame({'이름': namelist})
namelist_df = namelist_df.merge(df3[['이름', '전화번호']], how='left')
namelist_df['전화번호'] = namelist_df['전화번호'].fillna("정보 없음")

namelist_phones = namelist_df['전화번호'].tolist()

print("\n📋 namelist 전화번호 목록:")
for phone in namelist_phones:
    print(phone)

# -----------------------------
# 📌 namelist 문자 이력 + log 통합 출력
# -----------------------------
print("\n📋 namelist 통합 문자 이력 + log 기록:")

log = pd.read_excel("log.xlsx")

for row in namelist_df.itertuples():
    name = row.이름
    phone = row.전화번호

    if phone == "정보 없음":
        print(f"{name} | 정보 없음")
        continue

    # 문자 이력(df1)
    history = df1[df1['수신번호'] == phone]

    if history.empty:
        msg_info = "문자 이력 없음"
    else:
        recent = history.sort_values(by='전송일자', ascending=False).iloc[0]
        msg_info = f"문자: {recent['날짜차이']}일 전"

    # 로그 파일
    log_match = log[log['수신번호'].astype(str) == str(phone)]
    # print(log_match)
    if log_match.empty:
        log_info = "로그 없음"
    else:
        if '날짜' in log_match.columns:
            log_date = log_match.iloc[0]['날짜']
            log_info = f"로그: {log_date}"
        else:
            log_info = "로그 기록 있음(날짜 없음)"

    print(f"{name} | {phone} | {msg_info} | {log_info}")
