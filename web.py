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

if not os.path.exists('templates'):
    os.makedirs('templates')

if not os.path.exists('static'):
    os.makedirs('static')

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
        # SocialAnalyzer
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



