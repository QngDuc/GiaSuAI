"""
AI MentorPro - Hệ thống cố vấn chiến lược và công nghệ.
Dự án được phát triển bởi một CS Student đầy tâm huyết tại Buôn Ma Thuột.
"""

import os
import io
from flask import Flask, render_template, request
import google.generativeai as genai

# Khởi tạo Flask: "Xương sống" cho ứng dụng web của MentorPro
app = Flask(__name__, 
    static_folder='static',
    static_url_path='/static',
    template_folder='templates'
)

# Cấu hình API: Kết nối với "bộ não" Gemini 1.5 Flash của Google
# Sử dụng biến môi trường để bảo mật khóa bí mật khi đẩy lên Render
api_key = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# Lựa chọn model: Gemini 1.5 Flash mang lại sự cân bằng hoàn hảo giữa tốc độ và trí tuệ
model = genai.GenerativeModel("gemini-1.5-flash")

@app.route("/")
def index():
    """Hiển thị giao diện chính - Nơi bắt đầu mọi cuộc hội thoại chiến lược."""
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    """
    Điểm tiếp nhận yêu cầu từ Mentee.
    Xử lý đa phương thức: Kết hợp cả văn bản và dữ liệu hình ảnh (Raw Bytes).
    """
    user_input = request.form.get("user_input")
    file = request.files.get('file')
    
    # Thiết lập 'Mindset' cho MentorPro: Định hướng chuyên gia, thẳng thắn và hiện đại
    system_instruction = (
        "Bạn là AI MentorPro - Chuyên gia cố vấn chiến lược và công nghệ. "
        "Phong cách: Thẳng thắn, thực tế, tập trung vào giải pháp tối ưu. "
        "Nhiệm vụ: Tư vấn lộ trình phát triển, review code/thiết kế từ ảnh chụp, "
        "và đưa ra lời khuyên dựa trên xu hướng thị trường năm 2026. "
        "Hãy luôn lồng ghép tư duy phát triển bền vững (Green Tech) vào lời khuyên."
    )
    
    full_prompt = f"{system_instruction}\n\nYêu cầu từ Mentee: {user_input}"

    try:
        # Xử lý khi người dùng gửi kèm bằng chứng hình ảnh (code, sơ đồ, ảnh chụp lỗi)
        if file and file.filename != '':
            # Đọc dữ liệu thô (Bytes): Giải pháp linh hoạt, không cần thư viện trung gian (Pillow)
            # Giúp hệ thống ổn định trên mọi phiên bản Python (kể cả 3.14)
            img_data = file.read()
            
            response = model.generate_content([
                full_prompt,
                {
                    "mime_type": file.mimetype,
                    "data": img_data
                }
            ])
        else:
            # Chỉ xử lý văn bản nếu không có dữ liệu hình ảnh đi kèm
            response = model.generate_content(full_prompt)
            
        return response.text 
        
    except Exception as e:
        # Ghi nhật ký lỗi để Debug nhưng chỉ hiển thị thông báo lịch sự cho người dùng
        print(f"MentorPro Log Error: {e}")
        return "MentorPro đang gặp sự cố kết nối. Vui lòng thử lại sau hoặc liên hệ Admin tại BMT!"

if __name__ == "__main__":
    # Tự động thích ứng với cổng của Render hoặc mặc định là 5000 khi chạy local bằng lệnh 'py'
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)