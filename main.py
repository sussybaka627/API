import streamlit as st
import random
from google import genai
from google.genai import types
from PIL import Image

st.set_page_config(page_title="Gemini Vision Analyzer", page_icon="👁️", layout="centered")
st.title("👁️ Gemini Vision Analyzer")
st.markdown("**Demo Phân tích ảnh thông minh bằng Gemini API**")

try:
    # Lấy ra nguyên một danh sách (list) các key
    api_keys = st.secrets["GEMINI_API_KEYS"]
except KeyError:
    st.error("⚠️ Chưa tìm thấy GEMINI_API_KEYS trong cài đặt Secrets.")
    st.stop()

uploaded_file = st.file_uploader("Tải lên ảnh cần phân tích (PNG, JPG, JPEG)...", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    # Mở và thu nhỏ ảnh để tối ưu tốc độ, tránh lỗi 503
    image = Image.open(uploaded_file)
    image.thumbnail((1024, 1024)) 
    st.image(image, caption='Ảnh đã tải lên', use_container_width=True)
    
    if st.button("🚀 Phân tích ảnh ngay"):
        with st.spinner('Gemini đang phân tích ảnh...'):
            success = False

            random.shuffle(api_keys)
            for key in api_keys:
                try:
                    client = genai.Client(api_key=key)
                    config = types.GenerateContentConfig(
                        system_instruction="""
                        Bạn là một chuyên gia phân tích hình ảnh. Hãy mô tả hình ảnh cụ thể nhưng ko cần quá chi tiết đâu.
                        """
                    )

                    response = client.models.generate_content(
                        model="gemini-2.5-flash", 
                        contents=[image, "Hãy phân tích nội dung tấm ảnh này một cách chi tiết nhất."],
                        config=config
                    )
                    st.subheader("📋 Kết quả phân tích chi tiết:")
                    st.markdown(response.text)
                    success = True
                    break 
                    
                except Exception as e:
                    st.toast(f"Một API Key đang bận, tự động chuyển sang key dự phòng...", icon="🔄")
                    continue
            if not success:
                st.error("Rất tiếc, tất cả các API Key dự phòng đều đang quá tải. Vui lòng thử lại sau ít phút!")

st.write("---")
st.caption("Demo xây dựng cho TechAway 2026.")
