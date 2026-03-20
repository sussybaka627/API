import streamlit as st
from google import genai
from google.genai import types
from PIL import Image
import os

# --- 1. THIẾT LẬP CẤU HÌNH WEB APP ---
st.set_page_config(page_title="Gemini Vision Analyzer", page_icon="👁️")
st.title("👁️ Gemini Vision Analyzer - Phân tích ảnh thông minh")

# --- 2. QUẢN LÝ API KEY (BẢO MẬT) ---
# Lấy API Key từ cơ chế Secret của Streamlit
api_key = st.secrets["GEMINI_API_KEY"]
client = genai.Client(api_key=api_key)

# --- 3. SYSTEM INSTRUCTION (HỒN CỦA CON BOT) ---
system_instruction = types.SystemInstruction(
    parts=[types.Part(text="""
    Bạn là một chuyên gia phân tích hình ảnh và trí tuệ nhân tạo.
    Khi người dùng gửi một bức ảnh, hãy:
    1. Mô tả tổng quan về bối cảnh của bức ảnh.
    2. Liệt kê chi tiết các vật thể, con người, động vật xuất hiện (có số lượng, vị trí).
    3. Nhận diện hành động hoặc cảm xúc của các nhân vật (nếu có).
    4. Trích xuất bất kỳ văn bản nào (OCR) xuất hiện trong ảnh.
    5. Đưa ra các thẻ tag (keywords) liên quan đến nội dung ảnh.
    """)]
)

# --- 4. GIAO DIỆN TẢI FILE ---
uploaded_file = st.file_uploader("Tải lên ảnh cần phân tích (PNG, JPG, JPEG)...", type=["png", "jpg", "jpeg"])

# --- 5. XỬ LÝ KHI CÓ FILE ---
if uploaded_file is not None:
    # Hiển thị ảnh
    image = Image.open(uploaded_file)
    st.image(image, caption='Ảnh đã tải lên', use_column_width=True)
    
    # Chuyển đổi ảnh sang bytes để gửi qua API
    image_bytes = uploaded_file.getvalue()

    # Bắt đầu phân tích
    with st.spinner('Gemini đang xem ảnh, đợi tí nhé...'):
        try:
            # Gửi yêu cầu phân tích đa phương thức
            response = client.models.generate_content(
                model="gemini-1.5-flash", # Hoặc gemini-3.1-flash
                system_instruction=system_instruction,
                contents=[
                    types.Part(inline_data=types.Blob(mime_type="image/png", data=image_bytes)),
                    types.Part(text="Hãy phân tích nội dung tấm ảnh này giùm mình.")
                ]
            )
            
            # --- 6. HIỂN THỊ KẾT QUẢ ---
            st.subheader("Kết quả phân tích chi tiết:")
            st.markdown(response.text)
            st.success('Phân tích xong!')
            
        except Exception as e:
            st.error(f"Đã xảy ra lỗi: {e}")

# --- 7. FOOTER CHIA SẺ ---
st.write("---")
st.write("Demo xây dựng cho TechAway 2026 bằng Gemini API & Streamlit.")
