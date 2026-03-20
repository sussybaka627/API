import streamlit as st
from google import genai
from google.genai import types
from PIL import Image

# --- 1. THIẾT LẬP CẤU HÌNH WEB APP ---
st.set_page_config(page_title="Gemini Vision Analyzer", page_icon="👁️", layout="centered")
st.title("👁️ Gemini Vision Analyzer")
st.markdown("**Demo Phân tích ảnh thông minh bằng Gemini API**")

# --- 2. KHỞI TẠO CLIENT BẢO MẬT ---
# Lấy API Key từ cơ chế Secret của Streamlit (bạn đã cấu hình trên web)
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)
except KeyError:
    st.error("⚠️ Chưa tìm thấy GEMINI_API_KEY trong Streamlit Secrets. Vui lòng kiểm tra lại phần cài đặt trên Streamlit Cloud.")
    st.stop()

# --- 3. GIAO DIỆN TẢI FILE ---
uploaded_file = st.file_uploader("Tải lên ảnh cần phân tích (PNG, JPG, JPEG)...", type=["png", "jpg", "jpeg"])

# --- 4. XỬ LÝ KHI CÓ FILE ---
if uploaded_file is not None:
    # Mở và hiển thị ảnh bằng PIL
    image = Image.open(uploaded_file)
    st.image(image, caption='Ảnh đã tải lên', use_container_width=True)
    
    # Nút bấm để bắt đầu phân tích
    if st.button("🚀 Phân tích ảnh ngay"):
        with st.spinner('Gemini đang xem ảnh, đợi tí nhé...'):
            try:
                # --- CẤU HÌNH SYSTEM INSTRUCTION ---
                config = types.GenerateContentConfig(
                    system_instruction="""
                    Bạn là một chuyên gia phân tích hình ảnh và trí tuệ nhân tạo.
                    Khi người dùng gửi một bức ảnh, hãy:
                    1. Mô tả tổng quan về bối cảnh của bức ảnh.
                    2. Liệt kê chi tiết các vật thể, con người, động vật xuất hiện (có số lượng, vị trí).
                    3. Nhận diện hành động hoặc cảm xúc của các nhân vật (nếu có).
                    4. Trích xuất bất kỳ văn bản nào (OCR) xuất hiện trong ảnh.
                    5. Đưa ra các thẻ tag (keywords) liên quan đến nội dung ảnh.
                    Trình bày bằng tiếng Việt, rõ ràng, chia bullet point dễ đọc.
                    """
                )

                # --- GỬI YÊU CẦU LÊN GEMINI ---
                # Truyền trực tiếp biến `image` và câu lệnh prompt
                response = client.models.generate_content(
                    model="gemini-3.1-flash", 
                    contents=[image, "Hãy phân tích nội dung tấm ảnh này một cách chi tiết nhất."],
                    config=config
                )
                
                # --- HIỂN THỊ KẾT QUẢ ---
                st.subheader("📋 Kết quả phân tích chi tiết:")
                st.markdown(response.text)
                st.success('Phân tích hoàn tất!')
                
            except Exception as e:
                st.error(f"Đã xảy ra lỗi trong quá trình phân tích: {e}")

# --- 5. FOOTER ---
st.write("---")
st.caption("Demo xây dựng cho TechAway 2026.")
