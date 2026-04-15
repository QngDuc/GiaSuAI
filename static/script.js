/**
 * AI MentorPro - Logic điều khiển tương tác người dùng (Frontend).
 * Được thiết kế để mang lại trải nghiệm cố vấn mượt mà, chuyên nghiệp.
 */

// Hàm khởi tạo lại trạng thái để tiếp nhận bài toán/dự án mới
function clearResponse() {
    // Ẩn khu vực kết quả cũ để người dùng tập trung vào câu hỏi mới
    document.getElementById('responseContainer').style.display = 'none';
    
    // Reset toàn bộ dữ liệu đầu vào (Văn bản & Hình ảnh) về trạng thái sạch
    document.getElementById('question').value = '';
    document.getElementById('imageUpload').value = '';
    
    // Tự động đưa con trỏ vào ô nhập liệu - Tối ưu UX cho Mentee hành động ngay lập tức
    document.getElementById('question').focus();
}

// Lắng nghe sự kiện gửi yêu cầu cố vấn từ Form
document.getElementById('questionForm').addEventListener('submit', function(e) {
    // Chặn tải lại trang (Single Page Experience) để giữ mạch cảm xúc của người dùng
    e.preventDefault();
    
    const responseDiv = document.getElementById('response');
    const responseContainer = document.getElementById('responseContainer');
    
    // FormData: "Chiếc túi thần kỳ" giúp đóng gói cả văn bản và tệp nhị phân gửi lên Server
    const formData = new FormData();
    formData.append('user_input', document.getElementById('question').value);
    
    const imageFile = document.getElementById('imageUpload').files[0];
    
    // Kiểm soát chất lượng đầu vào - Tránh làm quá tải hệ thống MentorPro
    if (imageFile) {
        const allowedTypes = ['image/jpeg', 'image/png', 'image/gif', 'image/webp', 'application/pdf'];
        if (!allowedTypes.includes(imageFile.type)) {
            alert('MentorPro chỉ tiếp nhận: Hình ảnh (JPEG, PNG, GIF, WebP) hoặc tài liệu PDF!');
            return;
        }
        // Giới hạn 5MB: Đảm bảo tốc độ truyền tải nhanh nhất cho hạ tầng mạng tại BMT
        if (imageFile.size > 5 * 1024 * 1024) {
            alert('Tệp tin quá lớn! Vui lòng giữ dưới 5MB để MentorPro xử lý nhanh nhất.');
            return;
        }
        formData.append('file', imageFile);
    }
    
    // Tạo trạng thái chờ chuyên nghiệp: Giúp Mentee an tâm rằng chuyên gia đang phân tích
    responseDiv.innerHTML = `
        <div class="loading">
            <div class="spinner"></div>
            <p>AI MentorPro đang phân tích dữ liệu và soạn thảo chiến lược cho bạn...</p>
        </div>`;
    
    responseContainer.style.display = 'block';
    // Cuộn mượt mà đến vùng kết quả - Giúp giao diện trông hiện đại và cao cấp hơn
    responseContainer.scrollIntoView({ behavior: 'smooth' });
    
    // AJAX/Fetch: Kết nối không đồng bộ với Backend (app.py)
    fetch('/ask', {
        method: 'POST',
        body: formData
    })
    .then(response => response.text())
    .then(data => {
        // Sử dụng Marked.js để trình bày giải pháp dưới dạng Markdown đẹp mắt
        responseDiv.innerHTML = marked.parse(data);
        
        // Kích hoạt MathJax: Đảm bảo các công thức thuật toán/toán học được hiển thị chuẩn xác
        if (window.MathJax) {
            MathJax.typeset();
        }
    })
    .catch(error => {
        // Xử lý ngoại lệ: Luôn thông báo lỗi một cách minh bạch cho người dùng
        responseDiv.innerHTML = `
            <div class="error-message">
                <i class="fas fa-exclamation-circle"></i> 
                MentorPro gặp gián đoạn: ${error} - Hãy kiểm tra lại kết nối!
            </div>`;
    });
});

/**
 * Các tính năng nâng cao (Enhanced UX): 
 * Giúp việc gửi dữ liệu nhanh chóng như một chuyên gia thực thụ.
 */

const imageUpload = document.getElementById('imageUpload');
const questionForm = document.getElementById('questionForm');

// Drag & Drop: Cho phép kéo thả ảnh trực tiếp vào khu vực MentorPro
questionForm.addEventListener('dragover', (e) => {
    e.preventDefault();
    questionForm.style.borderColor = '#079992'; // Màu xanh Emerald đặc trưng của MentorPro
    questionForm.style.backgroundColor = 'rgba(7, 153, 146, 0.05)';
});

questionForm.addEventListener('dragleave', () => {
    questionForm.style.borderColor = '#ddd';
    questionForm.style.backgroundColor = 'transparent';
});

questionForm.addEventListener('drop', (e) => {
    e.preventDefault();
    questionForm.style.borderColor = '#ddd';
    questionForm.style.backgroundColor = 'transparent';
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        imageUpload.files = files;
        alert('✅ MentorPro đã tiếp nhận file của bạn qua phương thức kéo thả!');
    }
});

// Clipboard Paste: Tính năng "thần thánh" giúp chụp màn hình lỗi và Paste trực tiếp (Ctrl+V)
document.addEventListener('paste', (e) => {
    const items = e.clipboardData?.items;
    if (!items) return;

    for (let item of items) {
        if (item.type.indexOf('image') !== -1) {
            const file = item.getAsFile();
            const dataTransfer = new DataTransfer();
            dataTransfer.items.add(file);
            imageUpload.files = dataTransfer.files;
            
            alert('✅ Đã dán (paste) bằng chứng hình ảnh thành công!');
            break;
        }
    }
});