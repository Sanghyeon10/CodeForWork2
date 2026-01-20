import pandas as pd
import os
import re
import datetime


def Makedf():
    # 문자 발송 이력 데이터 불러오기 및 병합
    df1 = pd.read_excel(r'C:\Users\WD\Downloads\data1.xlsx')
    filepaths = [
        r'C:\Users\WD\Downloads\data2.xlsx',
        r'C:\Users\WD\Downloads\data3.xlsx',
        r'C:\Users\WD\Downloads\data4.xlsx',
        r'C:\Users\WD\Downloads\data5.xlsx'
    ]

    for path in filepaths:
        if os.path.exists(path):
            df2 = pd.read_excel(path)
            if "예약일자" in df2.columns:
                df2.rename(columns={'예약일자': '전송일자'}, inplace=True)
            df1 = pd.concat([df1, df2], axis=0, ignore_index=True)

    df1 = df1.sort_values(by='전송일자', ascending=False)
    df1 = df1[['수신번호', '전송일자', '문자내용', '결과']]
    df1['전송일자'] = pd.to_datetime(df1['전송일자'])
    df1['날짜차이'] = (datetime.datetime.now() - df1['전송일자']).dt.days
    df1['문자내용'] = df1['문자내용'].str.replace('\n', '', regex=True)

    # 대상자 리스트 불러오기 및 전화번호 포맷 정리
    df3 = pd.read_excel(r'C:\Users\WD\Downloads\겨울옷재촉리스트.xlsx')
    df3 = df3.dropna()
    df3 = df3.drop_duplicates(subset='전화번호')
    df3['전화번호'] = df3['전화번호'].apply(format_phone_number)

    return df1, df3


def format_phone_number(phone_number) -> str:
    phone_number = str(phone_number)
    if re.match(r"^\d{3}-\d{4}-\d{4}$", phone_number):
        return phone_number
    elif len(phone_number) == 11 and phone_number.isdigit():
        return f"{phone_number[:3]}-{phone_number[3:7]}-{phone_number[7:]}"
    else:
        print("올바른 11자리 전화번호를 입력하세요.")
        return phone_number




with open('namelist.txt', 'r', encoding="utf-8") as f:
    namelist = [word for line in f for word in re.split(r'\s|,|\.', line) if word]
