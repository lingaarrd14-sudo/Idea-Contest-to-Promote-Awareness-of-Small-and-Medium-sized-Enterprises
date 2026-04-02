import pandas as pd

# 1. 파일 경로 설정
f1 = "2024년도 고용노동부 선정 강소기업 명단(게시용).csv"
f2 = "공공데이터 경영혁신형 중소기업.csv"
f3 = "공공데이터 기술혁신형 중소기업.csv"

def load_csv(path):
    try:
        return pd.read_csv(path)
    except UnicodeDecodeError:
        return pd.read_csv(path, encoding='cp949')

# 데이터 불러오기
df1 = load_csv(f1)
df2 = load_csv(f2)
df3 = load_csv(f3)

# 2. 기업명 통일 및 공백 제거 처리
def clean_name(df):
    col = '사업자명' if '사업자명' in df.columns else '회사명'
    if col not in df.columns: 
        col = df.columns[1] # 혹시 컬럼명이 다를 경우를 대비한 대체 코드
    df['기업명'] = df[col].astype(str).str.strip()
    return df

df1 = clean_name(df1)
df2 = clean_name(df2)
df3 = clean_name(df3)

# 3. 핵심! 각 CSV 파일별로 기업명이 몇 번(N번) 등장했는지 횟수 계산
count1 = df1.groupby('기업명').size().reset_index(name='강소_등장횟수')
count2 = df2.groupby('기업명').size().reset_index(name='경영_등장횟수')
count3 = df3.groupby('기업명').size().reset_index(name='기술_등장횟수')

# 4. 전체 데이터를 하나로 병합 (아직 중복 제거 안 함)
all_df = pd.concat([df1, df2, df3], ignore_index=True)

# 전체 파일 통합 기준 총 등장 횟수 계산
total_counts = all_df.groupby('기업명').size().reset_index(name='총_등장횟수')

# 5. 이제 전체 데이터에서 기업명을 기준으로 중복을 제거하여 1행만 남김 (가장 위 정보 유지)
dedup_df = all_df.drop_duplicates(subset=['기업명'], keep='first').copy()

# 6. 중복 제거된 1개의 행 옆에 앞서 계산한 N번 등장 횟수(추적 데이터)를 가져다 붙임
dedup_df = dedup_df.merge(count1, on='기업명', how='left')
dedup_df = dedup_df.merge(count2, on='기업명', how='left')
dedup_df = dedup_df.merge(count3, on='기업명', how='left')
dedup_df = dedup_df.merge(total_counts, on='기업명', how='left')

# 빈 값(해당 명단에 없는 경우)은 0으로 채우기
for col in ['강소_등장횟수', '경영_등장횟수', '기술_등장횟수']:
    dedup_df[col] = dedup_df[col].fillna(0).astype(int)

# 7. 몇 개의 명단(CSV)에 걸쳐 포함되어 있는지 계산 (최대 3)
dedup_df['포함된_명단_수'] = (dedup_df['강소_등장횟수'] > 0).astype(int) + \
                           (dedup_df['경영_등장횟수'] > 0).astype(int) + \
                           (dedup_df['기술_등장횟수'] > 0).astype(int)

# 8. 가장 많은 파일에 등장하고(교집합), 총 중복 횟수가 많은 순으로 상단 정렬
dedup_df = dedup_df.sort_values(by=['포함된_명단_수', '총_등장횟수', '기업명'], ascending=[False, False, True])

# 9. 최종 엑셀 파일 저장
output_file = "통합_기업명단_상세추적.csv"
dedup_df.to_csv(output_file, index=False, encoding='utf-8-sig')

print(f"추적 완료! 결과가 '{output_file}'에 저장되었습니다.")