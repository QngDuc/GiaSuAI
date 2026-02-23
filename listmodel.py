#1.5: Tạo listmodel.py để liệt kê các model có thể sử dụng từ Google Generative AI. Sử dụng Google Generative AI API để lấy danh sách các model có khả năng tạo nội dung (generateContent) và in ra tên chính xác của chúng. 
import google.generativeai as genai

# Thay chuỗi dưới đây bằng API Key của bạn
genai.configure(api_key="AIzaSyCbDCJ7ZsaOZbmkgg0xc4igz_ZrbgSC3bE")

print("--- DANH SÁCH CÁC MODEL BẠN CÓ THỂ DÙNG ---")

# Gọi phương thức list_models để lấy danh sách các model có sẵn từ Google Generative AI và lọc ra những model có khả năng tạo nội dung (generateContent). In ra tên chính xác của các model này.
try:
    #Vòng lặp để duyệt qua tất cả các model được trả về bởi genai.list_models() và kiểm tra xem mỗi model có hỗ trợ phương thức generateContent hay không. Nếu có, in ra tên chính xác của model đó.
    for m in genai.list_models():
        # Chỉ lọc ra những model có khả năng tạo nội dung (generateContent)
        if 'generateContent' in m.supported_generation_methods:
            print(f"Tên chính xác: {m.name}")

# Nếu có lỗi xảy ra trong quá trình gọi danh sách model, in ra thông báo lỗi.
except Exception as e:
    print(f"Đã xảy ra lỗi khi gọi danh sách: {e}")

print("------------------------------------------")