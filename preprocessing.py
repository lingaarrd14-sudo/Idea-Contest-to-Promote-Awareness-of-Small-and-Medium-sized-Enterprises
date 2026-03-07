import pandas as pd

# header=None을 써서 1행부터 읽고, drop_duplicates()로 중복을 제거한 뒤 리스트로 변환
my_sme_list = pd.read_csv("D:\\gitTest\\corpname.csv", header=None).iloc[:, 0]

cleaned_data = my_sme_list.drop_duplicates().tolist()
print(f"이름 중복 기업: {len(my_sme_list) - len(cleaned_data)}개")
print(f"중복 제거 후 기업 수: {len(cleaned_data)}개")

# 2. 새로운 CSV 파일로 저장하기
cleaned_data = pd.DataFrame(cleaned_data, columns=["기업명"])
cleaned_data.to_csv("D:\\gitTest\\cleaned_corpname.csv", index=False, header=False, encoding='utf-8-sig')

print("중복이 제거된 파일이 성공적으로 저장되었습니다!")