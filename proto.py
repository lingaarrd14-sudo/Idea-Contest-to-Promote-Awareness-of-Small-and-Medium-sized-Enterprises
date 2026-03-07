from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import pandas as pd

def create_color_text_mosaic(image_path, font_path, text_list, output_path):
    # 1. A3 해상도 세팅 (300 DPI 기준)
    A3_WIDTH, A3_HEIGHT = 3508, 4961

    # 2. 이미지 준비 (원본 컬러 단 한 장!)
    try:
        # RGBA로 불러와서 투명도(Alpha) 채널까지 활용합니다.
        img = Image.open(image_path).convert('RGBA')
        img = ImageEnhance.Color(img).enhance(1)    # 채도 1.5배 상승
        img = ImageEnhance.Contrast(img).enhance(1) # 대비 1.5배 상승
        img = img.resize((A3_WIDTH, A3_HEIGHT))
    except FileNotFoundError:
        print("❌ 이미지를 찾을 수 없어. 경로를 다시 확인해 봐.")
        return

    # 3. 캔버스 생성 (완전 흰색 도화지)
    canvas = Image.new('RGB', (A3_WIDTH, A3_HEIGHT), color=(255, 255, 255))
    draw = ImageDraw.Draw(canvas)

    # 4. 폰트 설정 (모든 글자 크기 절대 동일)
    font_size = 12
    try:
        font = ImageFont.truetype(font_path, font_size)
    except IOError:
        print("❌ 폰트 파일을 찾을 수 없어. 경로를 확인해 줘.")
        return

    # 5. 매핑 변수 초기화
    word_idx = 0
    y = 0
    line_spacing = int(font_size * 1)

    while y < A3_HEIGHT:
        x = 0
        while x < A3_WIDTH:
            # 1. 출력할 단어 하나를 가져옵니다. (예: "정승네트워크")
            current_word = text_list[word_idx % len(text_list)]
        
            # 2. 단어를 한 글자씩 쪼개서 돌립니다.
            for char in current_word:
                if x >= A3_WIDTH: 
                    break # 화면 밖으로 나가면 줄바꿈 준비
                
                # 글자의 실제 가로 폭 계산 (글자마다 미세하게 폭이 다름)
                char_bbox = font.getbbox(char)
                char_w = char_bbox[2] - char_bbox[0]
            
                # 글자 정중앙 좌표의 색상과 투명도 샘플링
                center_x = min(x + (char_w // 2), A3_WIDTH - 1)
                center_y = min(y + (line_spacing // 2), A3_HEIGHT - 1)
                r, g, b, a = img.getpixel((center_x, center_y))

                # 투명하거나 하얀 배경이면 회색, 아니면 원본 색상!
                if a < 128 or (r > 240 and g > 240 and b > 240):
                    text_color = (220, 220, 220)
                else:
                    text_color = (r, g, b)
                
                # 🎨 '한 글자'만 해당 색상으로 캔버스에 찍음
                draw.text((x, y), char, font=font, fill=text_color)
            
                # 찍은 글자의 폭만큼만 x좌표를 미세하게 이동
                x += char_w 
            
            # 단어가 하나 끝나면 띄어쓰기 여백(반 칸) 추가
            x += int(font_size * 0.3)
            word_idx += 1
        
        y += line_spacing

    # 7. 5MB 용량 제한을 위한 JPEG 고화질 저장
    canvas.save(output_path, format="JPEG", quality=80, optimize=True)
    print(f"✅ 저장 완료! 파일 확인해 봐: {output_path}")

# ==========================================
# 🚀 실행 부분
# ==========================================
if __name__ == "__main__":
    # 1. 사용할 마스크 이미지 (구글에서 구한 흑백 실루엣 이미지 경로)
    my_mask_image = "D:\\gitTest\\poster.png" 
    
    # 2. 윈도우 기본 맑은 고딕 폰트 경로 (맥일 경우 "/Library/Fonts/AppleGothic.ttf" 등)
    my_font_path = "C:/Windows/Fonts/malgunbd.ttf" 
    

    # 3. 중소기업 데이터 (실제 데이터로 교체하세요)
    my_sme_list = pd.read_csv("D:\\gitTest\\cleaned_corpname.csv")["기업명"].tolist()  
    
    # 4. 결과물 파일명
    my_output = "a3_text_mosaic_prototype.jpg"

    create_color_text_mosaic(my_mask_image, my_font_path, my_sme_list, my_output)