import pandas as pd

def remove_duplicates():
    # header=None을 써서 1행부터 읽고, drop_duplicates()로 중복을 제거한 뒤 리스트로 변환
    my_sme_list = pd.read_csv("D:\\gitTest\\duplicated_rows.csv", header=None).iloc[:, 0]

    cleaned_data = my_sme_list.drop_duplicates().tolist()
    print(f"이름 중복 기업: {len(my_sme_list) - len(cleaned_data)}개")
    print(f"중복 제거 후 기업 수: {len(cleaned_data)}개")

    # 2. 새로운 CSV 파일로 저장하기
    cleaned_data = pd.DataFrame(cleaned_data, columns=["기업명"])
    cleaned_data.to_csv("D:\\gitTest\\cleaned_corpname.csv", header=False, encoding='utf-8-sig')

    print("중복이 제거된 파일이 성공적으로 저장되었습니다!")

def only_duplicates():
    # 1. iloc[:, 0]을 붙여서 'Series' 형태로 가져오는 것이 핵심입니다.
    my_sme_list = pd.read_csv("D:\\gitTest\\corpname.csv", header=None).iloc[:, 0]

    # 2. 중복된 모든 행을 추출 (keep=False)
    # 예: 'A', 'A', 'B' 가 있다면 'A', 'A'만 남깁니다.
    all_duplicates = my_sme_list[my_sme_list.duplicated(keep=False)]

    # 3. 중복된 이름들을 '한 번씩만' 보고 싶다면 drop_duplicates() 사용
    # 예: 위에서 남은 'A', 'A'를 'A' 하나로 만듭니다.
    unique_duplicates = all_duplicates.drop_duplicates()

    print(f"중복 발견된 기업 종류: {len(unique_duplicates)}개")

    # 4. 저장 (Series에서 바로 to_csv가 가능하므로 DataFrame 변환 단계 생략 가능)
    unique_duplicates.to_csv("D:\\gitTest\\duplicated_rows.csv", 
                             index=False, 
                             header=False, 
                             encoding='utf-8-sig')

    print("중복된 기업 명단이 성공적으로 저장되었습니다!")

if __name__ == "__main__" :
    #only_duplicates()
    remove_duplicates()