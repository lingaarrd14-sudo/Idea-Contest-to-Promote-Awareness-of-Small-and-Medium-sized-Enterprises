import json
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import pandas as pd

def create_color_text_mosaic_with_coords(image_path, font_path, text_list, output_img_path, output_json_path):
    # 1. A3 해상도 세팅 (300 DPI 기준)
    A3_WIDTH, A3_HEIGHT = 3508, 4961

    # 2. 이미지 준비
    try:
        img = Image.open(image_path).convert('RGBA')
        img = ImageEnhance.Color(img).enhance(1.1)
        img = ImageEnhance.Contrast(img).enhance(1)
        img = img.resize((A3_WIDTH, A3_HEIGHT))
    except FileNotFoundError:
        print("❌ 이미지를 찾을 수 없어. 경로를 다시 확인해 봐.")
        return

    # 3. 캔버스 생성 (완전 흰색 도화지)
    canvas = Image.new('RGB', (A3_WIDTH, A3_HEIGHT), color=(255, 255, 255)) #253, 251, 247
    draw = ImageDraw.Draw(canvas)

    # 4. 폰트 설정
    font_size = 13
    try:
        font = ImageFont.truetype(font_path, font_size)
    except IOError:
        print("❌ 폰트 파일을 찾을 수 없어. 경로를 확인해 줘.")
        return

    # 5. 매핑 변수 및 좌표 저장 리스트 초기화
    word_coordinates = [] # 💡 좌표를 담을 빈 리스트 생성
    word_idx = 0
    y = 0
    line_spacing = int(font_size)*0.98

    print("⏳ 텍스트 모자이크 생성 및 좌표 추출 중... (시간이 조금 걸릴 수 있습니다)")

    while y < A3_HEIGHT:
        x = 0
        while x < A3_WIDTH:
            # 출력할 단어 하나를 가져옵니다.
            current_word = text_list[word_idx % len(text_list)]
            
            # 💡 단어가 시작되는 최초의 x, y 좌표를 기록해 둡니다.
            start_x = x
            start_y = y
            
            # 단어를 한 글자씩 쪼개서 돌립니다.
            for char in current_word:
                if x >= A3_WIDTH: 
                    break # 화면 밖으로 나가면 줄바꿈 준비
                
                char_w = font.getlength(char)
            
                center_x = min(x + (char_w // 2), A3_WIDTH - 1)
                center_y = min(y + (line_spacing // 2), A3_HEIGHT - 1)
                r, g, b, a = img.getpixel((center_x, center_y))

                # 색상 결정 로직
                if y < A3_HEIGHT // 2 and (r > 250 and g > 250 and b > 250):
                    text_color = (r-(255-180), g-(255-170), b-(255-160))
                elif a < 128 or (r > 90 and g > 90 and b > 90):
                    text_color = (r-(255-180), g-(255-170), b-(255-160))
                else:
                    if r < 50 and g < 50 and b < 50:
                        text_color = (0, 0, 0) # 순도 100% 검정
                    else:
                        text_color = (int(r), int(g), int(b))
                
                # 결정된 색상으로 도화지에 글자 찍기
                draw.text((x, y), char, font=font, fill=text_color)
                
                # 찍은 글자의 폭만큼만 x좌표를 미세하게 이동
                x += char_w*0.85
            
  
            word_width = x - start_x # 최종 x에서 시작 x를 빼서 단어의 총 가로 길이를 구함
            
            word_coordinates.append({
                "company": current_word,
                "x": start_x,
                "y": start_y,
                "width": word_width,
                "height": line_spacing
            })
            
            # 단어가 하나 끝나면 띄어쓰기 여백(반 칸) 추가
            x += font_size * 0.16
            word_idx += 1
        
        y += line_spacing

    # 6. 이미지 저장
    canvas.save(output_img_path, format="PNG", quality=100, optimize=True)
    print(f"✅ 이미지 저장 완료: {output_img_path}")

    # 7. 💡 추출된 좌표 데이터를 JSON 파일로 저장
    with open(output_json_path, 'w', encoding='utf-8') as f:
        json.dump(word_coordinates, f, ensure_ascii=False, indent=2)
    print(f"✅ 좌표 데이터 JSON 저장 완료: {output_json_path}")

# ==========================================
# 🚀 실행 부분
# ==========================================
if __name__ == "__main__":
    # 1. 사용할 마스크 이미지 경로
    my_mask_image = "poster.png" 
    
    # 2. 폰트 경로
    my_font_path = "malgunbd.ttf" 
    
    # 3. 중소기업 데이터 로드
    my_sme_list = pd.read_csv("통합_기업명단_상세추적.csv")["기업명"].tolist()  
    
    # 4. 결과물 저장 경로 설정
    my_output_image = "a3_text_mosaic_prototype.png"
    my_output_json = "word_coordinates.json" # 💡 생성될 JSON 파일명

    # 함수 실행
    create_color_text_mosaic_with_coords(
        my_mask_image, 
        my_font_path, 
        my_sme_list, 
        my_output_image, 
        my_output_json
    )