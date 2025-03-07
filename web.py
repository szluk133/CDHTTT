from flask import Flask, render_template, request, jsonify # type: ignore
from importlib import import_module
import json
import os
import warnings

# Lọc cảnh báo từ BeautifulSoup
try:
    from bs4 import XMLParsedAsHTMLWarning
    warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)
except ImportError:
    pass

app = Flask(__name__)

# Đảm bảo thư mục templates và static tồn tại
if not os.path.exists('templates'):
    os.makedirs('templates')
    
if not os.path.exists('static'):
    os.makedirs('static')

# Tạo một favicon đơn giản bằng Python
try:
    from PIL import Image, ImageDraw
    
    img = Image.new('RGB', (16, 16), color = (73, 109, 137))
    d = ImageDraw.Draw(img)
    d.rectangle([(4, 4), (12, 12)], fill=(255, 255, 255))
    
    img.save('static/favicon.ico')
except ImportError:
    # Nếu không có thư viện PIL, tạo file trống
    with open('static/favicon.ico', 'wb') as f:
        f.write(b'')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    username = data.get('username', '')
    websites = data.get('websites', '')
    metadata = data.get('metadata', False)
    extract = data.get('extract', False)
    
    try:
        # Import và khởi tạo SocialAnalyzer
        SocialAnalyzer = import_module("social-analyzer").SocialAnalyzer(silent=True)
        
        # Chạy phân tích
        if websites:
            results = SocialAnalyzer.run_as_object(
                username=username,
                websites=websites,
                metadata=metadata,
                extract=extract,
                silent=True
            )
        else:
            results = SocialAnalyzer.run_as_object(
                username=username,
                metadata=metadata,
                extract=extract,
                silent=True
            )
        
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('favicon.ico')

if __name__ == '__main__':
    app.run(debug=True)


# Tạo file HTML trong thư mục templates
# with open('templates/index.html', 'w', encoding='utf-8') as f:
#     f.write("""
# <!DOCTYPE html>
# <html lang="vi">
# <head>
#     <meta charset="UTF-8">
#     <meta name="viewport" content="width=device-width, initial-scale=1.0">
#     <title>Social Analyzer</title>
#     <link rel="shortcut icon" href="{{ url_for('static', filename='favicon.ico') }}">
#     <style>
#         body {
#             font-family: Arial, sans-serif;
#             max-width: 1000px;
#             margin: 0 auto;
#             padding: 20px;
#             background-color: #f9f9f9;
#         }
#         h1 {
#             text-align: center;
#             color: #333;
#             margin-bottom: 30px;
#         }
#         .search-container {
#             display: flex;
#             margin-bottom: 20px;
#         }
#         #username {
#             flex: 1;
#             padding: 12px;
#             border: 1px solid #ddd;
#             border-radius: 4px 0 0 4px;
#             font-size: 16px;
#         }
#         #search-btn {
#             padding: 12px 24px;
#             background-color: #4CAF50;
#             color: white;
#             border: none;
#             border-radius: 0 4px 4px 0;
#             cursor: pointer;
#             font-size: 16px;
#         }
#         #search-btn:hover {
#             background-color: #45a049;
#         }
#         .options-card {
#             background-color: white;
#             border-radius: 8px;
#             padding: 20px;
#             box-shadow: 0 2px 4px rgba(0,0,0,0.1);
#             margin-bottom: 20px;
#         }
#         .option {
#             margin-bottom: 15px;
#         }
#         .option:last-child {
#             margin-bottom: 0;
#         }
#         #websites {
#             width: 100%;
#             padding: 10px;
#             border: 1px solid #ddd;
#             border-radius: 4px;
#             font-size: 14px;
#         }
#         #loading {
#             text-align: center;
#             display: none;
#             padding: 20px;
#             font-size: 18px;
#             color: #555;
#         }
#         .spinner {
#             border: 4px solid rgba(0, 0, 0, 0.1);
#             width: 36px;
#             height: 36px;
#             border-radius: 50%;
#             border-left-color: #4CAF50;
#             animation: spin 1s linear infinite;
#             margin: 0 auto 10px;
#         }
#         @keyframes spin {
#             0% { transform: rotate(0deg); }
#             100% { transform: rotate(360deg); }
#         }
#         .checkbox-group {
#             display: flex;
#             gap: 30px;
#         }
#         .checkbox-item {
#             display: flex;
#             align-items: center;
#         }
#         .checkbox-item input[type="checkbox"] {
#             margin-right: 8px;
#             width: 18px;
#             height: 18px;
#         }
#         .download-btn {
#             padding: 10px 20px;
#             background-color: #2196F3;
#             color: white;
#             border: none;
#             border-radius: 4px;
#             cursor: pointer;
#             display: none;
#             font-size: 16px;
#             margin: 20px auto;
#             display: block;
#         }
#         .download-btn:hover {
#             background-color: #0b7dda;
#         }
#         .result-container {
#             display: none;
#             background-color: white;
#             border-radius: 8px;
#             box-shadow: 0 2px 4px rgba(0,0,0,0.1);
#             margin-top: 20px;
#             overflow: hidden;
#         }
#         .result-header {
#             display: flex;
#             justify-content: space-between;
#             align-items: center;
#             padding: 15px 20px;
#             background-color: #f5f5f5;
#             border-bottom: 1px solid #ddd;
#         }
#         .result-title {
#             font-size: 18px;
#             font-weight: bold;
#             margin: 0;
#         }
#         .result-tabs {
#             display: flex;
#             border-bottom: 1px solid #ddd;
#         }
#         .result-tab {
#             padding: 12px 20px;
#             cursor: pointer;
#             background-color: #f9f9f9;
#             border-right: 1px solid #ddd;
#         }
#         .result-tab.active {
#             background-color: white;
#             border-bottom: 2px solid #4CAF50;
#         }
#         .result-content {
#             padding: 0;
#         }
#         .tab-content {
#             display: none;
#         }
#         .tab-content.active {
#             display: block;
#         }
#         #raw-json {
#             white-space: pre-wrap;
#             background-color: #f8f8f8;
#             padding: 15px;
#             border-radius: 4px;
#             overflow-x: auto;
#             font-family: monospace;
#             margin: 0;
#         }
#         .profiles-container {
#             display: grid;
#             grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
#             gap: 20px;
#             padding: 20px;
#         }
#         .profile-card {
#             border: 1px solid #ddd;
#             border-radius: 8px;
#             overflow: hidden;
#             transition: transform 0.2s, box-shadow 0.2s;
#         }
#         .profile-card:hover {
#             transform: translateY(-5px);
#             box-shadow: 0 5px 15px rgba(0,0,0,0.1);
#         }
#         .profile-header {
#             padding: 15px;
#             border-bottom: 1px solid #eee;
#             display: flex;
#             align-items: center;
#         }
#         .profile-icon {
#             width: 30px;
#             height: 30px;
#             margin-right: 10px;
#             display: flex;
#             justify-content: center;
#             align-items: center;
#             border-radius: 50%;
#             background-color: #f0f0f0;
#             font-weight: bold;
#             color: #555;
#         }
#         .profile-site {
#             font-weight: bold;
#             font-size: 16px;
#         }
#         .profile-status {
#             margin-left: auto;
#             padding: 4px 8px;
#             border-radius: 20px;
#             font-size: 12px;
#             font-weight: bold;
#         }
#         .status-found {
#             background-color: #e8f5e9;
#             color: #2e7d32;
#         }
#         .status-not-found {
#             background-color: #ffebee;
#             color: #c62828;
#         }
#         .profile-body {
#             padding: 15px;
#         }
#         .profile-item {
#             margin-bottom: 10px;
#         }
#         .profile-item-label {
#             font-size: 12px;
#             color: #666;
#             margin-bottom: 2px;
#         }
#         .profile-item-value {
#             font-size: 14px;
#             word-break: break-all;
#         }
#         .profile-link {
#             display: block;
#             padding: 10px 15px;
#             text-align: center;
#             background-color: #f5f5f5;
#             text-decoration: none;
#             color: #333;
#             border-top: 1px solid #eee;
#             transition: background-color 0.2s;
#         }
#         .profile-link:hover {
#             background-color: #e9e9e9;
#         }
#         .no-results {
#             padding: 40px;
#             text-align: center;
#             color: #666;
#         }
#     </style>
# </head>
# <body>
#     <h1>Social Analyzer</h1>
    
#     <div class="search-container">
#         <input type="text" id="username" placeholder="Nhập tên người dùng...">
#         <button id="search-btn">Tìm kiếm</button>
#     </div>
    
#     <div class="options-card">
#         <div class="option">
#             <label for="websites">Trang web cụ thể (để trống để tìm tất cả):</label>
#             <input type="text" id="websites" placeholder="youtube pinterest tumblr...">
#         </div>
#         <div class="option">
#             <div class="checkbox-group">
#                 <div class="checkbox-item">
#                     <input type="checkbox" id="metadata" checked>
#                     <label for="metadata">Lấy metadata</label>
#                 </div>
#                 <div class="checkbox-item">
#                     <input type="checkbox" id="extract" checked>
#                     <label for="extract">Trích xuất thông tin</label>
#                 </div>
#             </div>
#         </div>
#     </div>
    
#     <div id="loading">
#         <div class="spinner"></div>
#         <div>Đang tìm kiếm, vui lòng đợi...</div>
#     </div>
    
#     <div id="result-container" class="result-container">
#         <div class="result-header">
#             <h3 class="result-title">Kết quả tìm kiếm cho: <span id="result-username"></span></h3>
#             <button id="download-btn" class="download-btn">Tải xuống JSON</button>
#         </div>
#         <div class="result-tabs">
#             <div class="result-tab active" data-tab="profiles">Hồ sơ người dùng</div>
#             <div class="result-tab" data-tab="raw">Dữ liệu thô (JSON)</div>
#         </div>
#         <div id="profile-detail-container" style="display: none; padding: 20px; background: white; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-top: 20px;">
#             <h3>Chi tiết người dùng</h3>
#             <div id="profile-details"></div>
#             <button onclick="closeProfileDetails()">Đóng</button>
#         </div>
#         <div class="result-content">
#             <div id="profiles-tab" class="tab-content active">
#                 <div id="profiles-container" class="profiles-container">
#                     <!-- Profile cards will be inserted here -->
#                 </div>
#             </div>
#             <div id="raw-tab" class="tab-content">
#                 <pre id="raw-json"></pre>
#             </div>
#         </div>
#     </div>

#     <script>
#         let resultData = null;
        
#         // Xử lý tabs
#         document.querySelectorAll('.result-tab').forEach(tab => {
#             tab.addEventListener('click', function() {
#                 // Xóa active từ tất cả tabs
#                 document.querySelectorAll('.result-tab').forEach(t => t.classList.remove('active'));
#                 document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
                
#                 // Thêm active cho tab hiện tại
#                 this.classList.add('active');
                
#                 // Hiển thị nội dung tương ứng
#                 const tabId = this.getAttribute('data-tab');
#                 document.getElementById(tabId + '-tab').classList.add('active');
#             });
#         });
        
#         document.getElementById('search-btn').addEventListener('click', function() {
#             const username = document.getElementById('username').value.trim();
#             if (!username) {
#                 alert('Vui lòng nhập tên người dùng');
#                 return;
#             }
            
#             const websites = document.getElementById('websites').value.trim();
#             const metadata = document.getElementById('metadata').checked;
#             const extract = document.getElementById('extract').checked;
            
#             document.getElementById('loading').style.display = 'block';
#             document.getElementById('result-container').style.display = 'none';
            
#             fetch('/analyze', {
#                 method: 'POST',
#                 headers: {
#                     'Content-Type': 'application/json',
#                 },
#                 body: JSON.stringify({
#                     username: username,
#                     websites: websites,
#                     metadata: metadata,
#                     extract: extract
#                 }),
#             })
#             .then(response => response.json())
#             .then(data => {
#                 resultData = data;
#                 document.getElementById('loading').style.display = 'none';
#                 document.getElementById('result-container').style.display = 'block';
#                 document.getElementById('result-username').textContent = username;
                
#                 // Hiển thị dữ liệu JSON
#                 document.getElementById('raw-json').textContent = JSON.stringify(data, null, 2);
                
#                 // Hiển thị dữ liệu dưới dạng các card
#                 renderProfileCards(data);
#             })
#             .catch(error => {
#                 document.getElementById('loading').style.display = 'none';
#                 alert('Đã xảy ra lỗi: ' + error);
#             });
#         });
        
#         document.getElementById('download-btn').addEventListener('click', function() {
#             if (!resultData) return;
            
#             const dataStr = JSON.stringify(resultData, null, 2);
#             const dataUri = 'data:application/json;charset=utf-8,'+ encodeURIComponent(dataStr);
            
#             const exportFileDefaultName = 'social-analyzer-result.json';
            
#             const linkElement = document.createElement('a');
#             linkElement.setAttribute('href', dataUri);
#             linkElement.setAttribute('download', exportFileDefaultName);
#             linkElement.click();
#         });

#         function renderProfileCards(data) {
#             console.log("dữ liệu:",data);
#             const container = document.getElementById('profiles-container');
#             container.innerHTML = '';

#             if (data.detected && Array.isArray(data.detected) && data.detected.length > 0) {
#                 data.detected.forEach((profile, index) => {
#                     const card = document.createElement('div');
#                     card.className = 'profile-card';
#                     card.dataset.index = index;
#                     card.style.paddingLeft = '15px';
                    
#                     const header = document.createElement('div');
#                     header.className = 'profile-header';
                    
#                     const icon = document.createElement('div');
#                     icon.className = 'profile-icon';
#                     icon.textContent = profile.title ? profile.title.charAt(0).toUpperCase() : '?';
                    
#                     const siteName = document.createElement('div');
#                     siteName.className = 'profile-site';
#                     siteName.textContent = profile.title || 'Unknown';
                    
#                     const status = document.createElement('div');
#                     status.className = 'profile-status';
#                     status.textContent = profile.status || 'Unknown';
                    
#                     header.appendChild(icon);
#                     header.appendChild(siteName);
#                     header.appendChild(status);
                    
#                     card.appendChild(header);
                    
#                     const infoContainer = document.createElement('div');
#                     infoContainer.className = 'profile-info';
                    
#                     const infoFields = [
#                         { label: 'country', value: profile.country },
#                         { label: 'extracted', value: profile.extracted },
#                         { label: 'found', value: profile.found },
#                         { label: 'language', value: profile.language },
#                         { label: 'Link', value: profile.link }
#                     ];

#                     infoFields.forEach(field => {
#                         if (field.value) {
#                             const paragraph = document.createElement('p');
#                             paragraph.style.marginLeft = '15px';
#                             paragraph.textContent = `${field.label}: ${field.value}`;
#                             infoContainer.appendChild(paragraph);
#                         }
#                     });
                    
#                     card.appendChild(infoContainer);
                    
#                     card.addEventListener('click', () => showProfileDetails(profile));
#                     container.appendChild(card);
#                 });
#             } else {
#                 container.innerHTML = '<div class="no-results">Không có kết quả nào được tìm thấy.</div>';
#             }
#         }


#         function showProfileDetails(profile) {
#             const detailsContainer = document.getElementById('profile-details');
#             detailsContainer.innerHTML = '';
            
#             const title = document.createElement('h3');
#             title.textContent = profile.title || 'Chi tiết người dùng';
#             detailsContainer.appendChild(title);
            
#             if (profile.link) {
#                 const link = document.createElement('a');
#                 link.href = profile.link;
#                 link.textContent = profile.link;
#                 link.target = '_blank';
#                 detailsContainer.appendChild(link);
#             }
            
#             const infoFields = [
#                 { label: 'country', value: profile.country },
#                 { label: 'language', value: profile.language },
#                 { label: 'found', value: profile.rank },
#                 { label: 'rate', value: profile.rate },
#                 { label: 'content', value: profile.text },
#                 { label: 'type', value: profile.type }
#             ];

#             infoFields.forEach(field => {
#                 if (field.value) {
#                     const paragraph = document.createElement('p');
#                     paragraph.textContent = `${field.label}: ${field.value}`;
#                     detailsContainer.appendChild(paragraph);
#                 }
#             });
            
#             if (profile.metadata && profile.metadata.length > 0) {
#                 const metadataSection = document.createElement('div');
#                 metadataSection.innerHTML = '<h4>Metadata</h4>';
#                 const metadataList = document.createElement('ul');

#                 profile.metadata.forEach(meta => {
#                     const metaItem = document.createElement('li');
#                     metaItem.textContent = `${meta.name}: ${meta.content}`;
#                     metadataList.appendChild(metaItem);
#                 });

#                 metadataSection.appendChild(metadataList);
#                 detailsContainer.appendChild(metadataSection);
#             }
            
#             const imageMeta = profile.metadata?.find(meta => meta.property === 'og:image');
#             if (imageMeta) {
#                 const image = document.createElement('img');
#                 image.src = imageMeta.content;
#                 image.alt = 'Profile Image';
#                 image.style.maxWidth = '100%';
#                 detailsContainer.appendChild(image);
#             }
            
#             document.getElementById('profile-detail-container').style.display = 'block';
#         }

#         function closeProfileDetails() {
#             document.getElementById('profile-detail-container').style.display = 'none';
#         }

#         function createProfileItem(label, value) {
#             const item = document.createElement('div');
#             item.className = 'profile-item';
            
#             const itemLabel = document.createElement('div');
#             itemLabel.className = 'profile-item-label';
#             itemLabel.textContent = label;
            
#             const itemValue = document.createElement('div');
#             itemValue.className = 'profile-item-value';
#             itemValue.textContent = value;
            
#             item.appendChild(itemLabel);
#             item.appendChild(itemValue);
            
#             return item;
#         }
#     </script>
# </body>
# </html>
#     """)