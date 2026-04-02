import streamlit as st
import json
from PIL import Image, ImageDraw

# 페이지 기본 설정
st.set_page_config(page_title="거북선 사명 찾기", layout="wide")

@st.cache_data
def load_data():
    with open('word_coordinates.json', 'r', encoding='utf-8') as f:
        return json.load(f)

@st.cache_resource
def load_image():
    return Image.open("a3_text_mosaic_prototype.png").convert("RGBA")

st.title("🐢 거북선 텍스트 모자이크 - 우리 기업 찾기")
st.markdown("포스터를 구성하는 약 34,000개 이상의 사명 중, 찾고 싶은 기업명을 입력하세요.")

# 파일 존재 여부 체크
try:
    data = load_data()
    base_img = load_image()
except FileNotFoundError:
    st.error("❌ 'word_coordinates.json' 또는 'a3_text_mosaic_prototype.png' 파일을 찾을 수 없습니다. 실행 위치를 확인해주세요.")
    st.stop()

# 검색 UI
search_query = st.text_input("🔍 부분 일치 검색 지원, 띄워쓰기❌  \n중복 결과가 많을 경우 사명을 더 구체적으로 입력해주세요. ", placeholder="예: 대진엔지니어링 ")

if search_query:
    # 부분 일치하는 모든 기업 검색
    results = [item for item in data if search_query in item['company']]

    if not results:
        st.warning("일치하는 기업명이 없습니다. 오타를 확인해 주세요.")
    else:
        st.success(f"총 {len(results)}개의 결과를 찾았습니다.")

        for i, match in enumerate(results):
            st.markdown(f"### {i+1}. {match['company']}")
            
            x, y = match['x'], match['y']
            w, h = match['width'], match['height']

            # 이미지 시각화 처리
            img_copy = base_img.copy()
            draw = ImageDraw.Draw(img_copy)

            # 포스터 전체 뷰에서 멀리서도 보이게 큰 빨간색 가이드 박스 생성
            highlight_padding = 80
            draw.rectangle(
                [x - highlight_padding, y - highlight_padding, x + w + highlight_padding, y + h + highlight_padding],
                outline="red",
                width=15
            )
            
            # 정확한 단어 위치에 노란색 타이트한 박스 생성
            draw.rectangle([x, y, x + w, y + h], outline="yellow", width=4)

            # 확대 보기용 이미지 크롭 (단어 기준 상하좌우 400px)
            crop_size = 400
            left = max(0, x - crop_size)
            top = max(0, y - crop_size)
            right = min(img_copy.width, x + w + crop_size)
            bottom = min(img_copy.height, y + h + crop_size)
            
            zoomed_img = img_copy.crop((left, top, right, bottom))

            # 4. 화면 레이아웃 (좌측: 확대 뷰 / 우측: 전체 뷰)
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.write("**🔍 확대 보기**")
                st.image(zoomed_img, use_container_width=True)
            
            with col2:
                st.write("**🗺️ 전체 포스터 위치**")
                st.image(img_copy, use_container_width=True)
            
            st.divider()