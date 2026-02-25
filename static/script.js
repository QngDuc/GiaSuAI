// hàm để xóa câu trả lời và reset form sau khi người dùng nhấn nút "Đặt câu hỏi khác"
function clearResponse() {
            // Lấy phần từ chứa responseContainer và ẩn nó đi
            document.getElementById('responseContainer').style.display = 'none';
            // Lấy phần tử chứa câu hỏi và hình ảnh, đưa giá trị của chúng về mặc định (rỗng) để người dùng có thể nhập câu hỏi mới và chọn hình ảnh mới nếu muốn
            document.getElementById('question').value = '';
            document.getElementById('imageUpload').value = '';
            // Lấy phần tử chứa câu hỏi dùng để hiển thị lại và focus vào đó để người dùng có thể nhập câu hỏi mới
            document.getElementById('question').focus();
        }
        // Lấy phần tử form câu hỏi và thêm sự kiện lắng nghe khi người dùng submit form
        document.getElementById('questionForm').addEventListener('submit', function(e) {
            // Ngăn chặn hành vi mặc định của form khi submit để chúng ta có thể xử lý bằng JavaScript
            e.preventDefault();
            
            // Gán giá trị userInput là giá trị của trường input có id 'question' (câu hỏi của người dùng)
            const responseDiv = document.getElementById('response');
            // Gán giá trị responseContainer là phần tử có id 'responseContainer' để hiển thị câu trả lời sau khi nhận được từ server
            const responseContainer = document.getElementById('responseContainer');
            
            // Tạo FormData object để gửi cả văn bản và file
            const formData = new FormData();
            // Dùng FormData để lấy giá trị của trường input có id 'question' và gán vào biến userInput
            formData.append('user_input', document.getElementById('question').value);
            const imageFile = document.getElementById('imageUpload').files[0];
            // Nếu người dùng đã chọn một file hình ảnh, thêm nó vào FormData để gửi lên server
            if (imageFile) {
                // Dùng FormData để thêm file hình ảnh vào formData với tên 'image_file' để server có thể nhận và xử lý nó sau này
                formData.append('image_file', imageFile);
            }
            
            // Hiển thị thông báo đang tải
                // Gán giá trị innerHTML của responseDiv thành một phần tử HTML chứa thông báo đang tải và một spinner để người dùng biết rằng câu hỏi đang được xử lý
            responseDiv.innerHTML = '<div class="loading"><div class="spinner"></div><p>Vui lòng đợi 1 phút để gia sư AI trả lời câu hỏi của bạn...</p></div>';
                // Hiển thị phần tử responseContainer để người dùng có thể thấy thông báo đang tải và sau này sẽ hiển thị câu trả lời
            responseContainer.style.display = 'block';
                // Cuộn trang xuống phần tử responseContainer để người dùng có thể thấy thông báo đang tải và sau này sẽ thấy câu trả lời một cách mượt mà
            responseContainer.scrollIntoView({ behavior: 'smooth' });
            
            // Gửi AJAX request
                // Sử dụng fetch API để gửi một POST request đến endpoint '/ask' trên server với dữ liệu formData chứa câu hỏi và hình ảnh (nếu có)
            fetch('/ask', {
                // Chỉ định phương thức là POST để gửi dữ liệu lên server
                method: 'POST',
                // Phần body của request sẽ là formData chứa câu hỏi và hình ảnh (nếu có) để server có thể nhận và xử lý nó
                body: formData
            })
            // Khi nhận được phản hồi từ server, chuyển đổi nó thành text để có thể hiển thị dưới dạng HTML sau này
            .then(response => response.text())
            // Sau khi chuyển đổi thành text, chúng ta sẽ có dữ liệu câu trả lời từ server và có thể hiển thị nó cho người dùng
            .then(data => {
                // Parse Markdown và hiển thị kết quả
                responseDiv.innerHTML = marked.parse(data);
                // Render MathJax cho công thức toán học
                MathJax.typeset();
                // Xóa file đã chọn sau khi gửi thành công
                document.getElementById('imageUpload').value = '';
            })
            // Nếu có lỗi xảy ra trong quá trình gửi request hoặc nhận phản hồi, chúng ta sẽ bắt lỗi và hiển thị thông báo lỗi cho người dùng
            .catch(error => {
                // Gán giá trị innerHTML của responseDiv thành một phần tử HTML chứa thông báo lỗi và biểu tượng cảnh báo để người dùng biết rằng đã có lỗi xảy ra trong quá trình xử lý câu hỏi
                responseDiv.innerHTML = '<div class="error-message"><i class="fas fa-exclamation-circle"></i> Lỗi: ' + error + '</div>';
            });
        });