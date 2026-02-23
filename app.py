#1: Tạo app.py để định nghĩa ban đầu cho trang web và gia sư AI. sử dụng Flask để tạo một ứng dụng web đơn giản, và Google Generative AI để tạo nội dung dựa trên câu hỏi của người dùng.

#Thêm framework Flask và Google Generative AI API vào ứng dụng của trang web
from flask import Flask, render_template, request
import google.generativeai as genai
app = Flask(__name__) #Tạo một ứng dụng Flask mới
genai.configure(api_key="AIzaSyCbDCJ7ZsaOZbmkgg0xc4igz_ZrbgSC3bE") #Cấu hình API key để sử dụng Google Generative AI cho phép truy cập vào Google Generative AI để tạo nội dung dựa trên câu hỏi của người dùng.
model = genai.GenerativeModel("models/gemini-2.5-flash") #Khởi tạo mô hình GenerativeModel từ Google Generative AI với tên "models/gemini-2.0-pro" 

#Hàm định nghĩa hiển thị trang chủ
@app.route("/")
def index():
    return render_template("index.html") #Return trả về trang index.html để hiển thị giao diện trang chủ

#Hàm định nghĩa xử lý yêu cầu từ người dùng khi họ gửi câu hỏi qua form sử dụng phương thức POST.
#POST được sử dụng để gửi dữ liệu từ form câu hỏi đến server
@app.route("/ask", methods=["POST"])
def ask():
    #Lấy dữ liệu từ form câu hỏi của người dùng thông qua request.form và lưu vào biến user_input
    user_input = request.form["user_input"]
    #Gán biến response bằng cách gọi generate_content của mô hình GenerativeModel với câu hỏi của người dùng được truyền vào. Câu hỏi được định dạng để yêu cầu gia sư AI trả lời một cách tận tâm. 
    response = model.generate_content(f"Bạn là một gia sư tận tâm hãy trả lời câu hỏi sau: {user_input}")
    #Trả về nội dung của phản hồi bằng response.text để hiển thị câu trả lời từ gia sư AI trên trang web.
    return response.text

#Chạy ứng dụng Flask với chế độ debug để dễ dàng phát hiện lỗi và tự động tải lại khi có thay đổi trong mã nguồn.
if __name__ == "__main__":
    app.run(debug=True)