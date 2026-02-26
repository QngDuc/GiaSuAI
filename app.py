#1: Tạo app.py để định nghĩa ban đầu cho trang web và gia sư AI. sử dụng Flask để tạo một ứng dụng web đơn giản, và Google Generative AI để tạo nội dung dựa trên câu hỏi của người dùng.

#Thêm framework Flask và Google Generative AI API vào ứng dụng của trang web
#Import os để làm việc với các biến môi trường và cấu hình cổng cho ứng dụng Flask.
import os
from flask import Flask, render_template, request
import google.generativeai as genai
#Import secure_filename từ werkzeug.utils để xử lý tên tệp an toàn khi người dùng tải lên tệp (nếu có).
from werkzeug.utils import secure_filename
app = Flask(__name__, 
    static_folder='static',
    static_url_path='/static',
    template_folder='templates'
)
api_key = os.environ.get("GEMINI_API_KEY") #Lấy API key từ biến môi trường GEMINI_API_KEY trên Render để sử dụng Google Generative AI
genai.configure(api_key=api_key) #Cấu hình API key để sử dụng Google Generative AI cho phép truy cập vào Google Generative AI để tạo nội dung dựa trên câu hỏi của người dùng.
model = genai.GenerativeModel("models/gemini-2.5-flash") #Khởi tạo mô hình GenerativeModel từ Google Generative AI với tên "models/gemini-2.5-flash". Đây là mô hình được sử dụng để tạo nội dung dựa trên câu hỏi của người dùng.
UPLOAD_FOLDER = 'uploads' #Định nghĩa thư mục để lưu trữ các tệp tải lên từ người dùng (nếu có).
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# Tạo thư mục UPLOAD_FOLDER nếu nó chưa tồn tại
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
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
    # Khởi tạo một danh sách để chứa các phần nội dung sẽ gửi đến mô hình Gemini
    contents = [f"Bạn là một gia sư tận tâm hãy trả lời câu hỏi sau: {user_input}",image_parts]
    #Lấy tệp hình ảnh từ form nếu có và lưu vào biến
    file = request.files.get('file')
    # Kiểm tra xem có file hình ảnh nào được tải lên không
    try:
        if file and file.filename != '':
            img_data = file.read()  # Đọc dữ liệu hình ảnh từ tệp
            image_parts = [
                {
                    "mime_type": file.mimetype,  # Loại MIME của hình ảnh
                    "data": img_data  # Dữ liệu hình ảnh đã đọc
                }
            ]
            response = model.generate_content(contents + image_parts)  # Gửi cả câu hỏi và hình ảnh đến mô hình Gemini để tạo nội dung
            
        else:
            response = model.generate_content(contents)  # Nếu không có hình ảnh, chỉ gửi câu hỏi đến mô hình Gemini để tạo nội dung
        return response.text  # Trả về nội dung của phản hồi từ mô hình Gemini để hiển thị câu trả lời từ gia sư AI trên trang web
    #Thêm khối ngoại lệ để xử lý bất kỳ lỗi nào có thể xảy ra trong quá trình xử lý yêu cầu, chẳng hạn như lỗi khi đọc tệp hình ảnh hoặc lỗi khi gọi mô hình Gemini để tạo nội dung. Nếu có lỗi, nó sẽ được in ra console để dễ dàng phát hiện và khắc phục.
    except Exception as e:
        print(f"Error processing request: {e}")
        return "Đã xảy ra lỗi khi xử lý yêu cầu của bạn. Vui lòng thử lại sau."  # Trả về thông báo lỗi cho người dùng nếu có lỗi xảy ra

    #Gán biến response bằng cách gọi generate_content của mô hình GenerativeModel với câu hỏi của người dùng được truyền vào. Câu hỏi được định dạng để yêu cầu gia sư AI trả lời một cách tận tâm. 
    response = model.generate_content(contents)
    #Trả về nội dung của phản hồi bằng response.text để hiển thị câu trả lời từ gia sư AI trên trang web.
    return response.text

#Chạy ứng dụng Flask với chế độ debug để dễ dàng phát hiện lỗi và tự động tải lại khi có thay đổi trong mã nguồn.
if __name__ == "__main__":
    #Lấy cổng từ biến môi trường PORT nếu có, nếu không thì sử dụng cổng mặc định 5000. Điều này cho phép ứng dụng chạy trên các nền tảng đám mây như Heroku, nơi cổng được chỉ định thông qua biến môi trường.
    port = int(os.environ.get("PORT", 5000))
    # Host '0.0.0.0' để thế giới bên ngoài có thể kết nối vào
    app.run(host='0.0.0.0', port=port)