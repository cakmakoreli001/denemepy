from flask import Flask, render_template_string, request, jsonify, send_file
import os
import yt_dlp
import tempfile
from pathlib import Path

app = Flask(__name__)

# HTML Template
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Video İndirici</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 800px;
            margin: 0 auto;
            padding: 40px 0;
        }
        
        .header {
            text-align: center;
            color: white;
            margin-bottom: 40px;
        }
        
        .header h1 {
            font-size: 2.5rem;
            margin-bottom: 10px;
            font-weight: 700;
        }
        
        .header p {
            font-size: 1.1rem;
            opacity: 0.9;
        }
        
        .card {
            background: white;
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            margin-bottom: 30px;
        }
        
        .platforms {
            display: flex;
            gap: 15px;
            justify-content: center;
            flex-wrap: wrap;
            margin-bottom: 30px;
        }
        
        .platform {
            padding: 10px 20px;
            background: #f0f0f0;
            border-radius: 25px;
            font-size: 0.9rem;
            font-weight: 500;
            color: #666;
        }
        
        .input-group {
            margin-bottom: 25px;
        }
        
        .input-group label {
            display: block;
            margin-bottom: 10px;
            font-weight: 600;
            color: #333;
        }
        
        .input-wrapper {
            position: relative;
        }
        
        input[type="text"] {
            width: 100%;
            padding: 15px 20px;
            border: 2px solid #e0e0e0;
            border-radius: 12px;
            font-size: 1rem;
            transition: border-color 0.3s;
        }
        
        input[type="text"]:focus {
            outline: none;
            border-color: #667eea;
        }
        
        .options {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 25px;
        }
        
        .option-card {
            padding: 20px;
            border: 2px solid #e0e0e0;
            border-radius: 12px;
            cursor: pointer;
            transition: all 0.3s;
            text-align: center;
        }
        
        .option-card:hover {
            border-color: #667eea;
            background: #f8f9ff;
        }
        
        .option-card.selected {
            border-color: #667eea;
            background: #667eea;
            color: white;
        }
        
        .option-card .icon {
            font-size: 2rem;
            margin-bottom: 10px;
        }
        
        .option-card .title {
            font-weight: 600;
            margin-bottom: 5px;
        }
        
        .option-card .desc {
            font-size: 0.85rem;
            opacity: 0.8;
        }
        
        .quality-options {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }
        
        .quality-btn {
            padding: 10px 20px;
            border: 2px solid #e0e0e0;
            background: white;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s;
            font-weight: 500;
        }
        
        .quality-btn:hover {
            border-color: #667eea;
        }
        
        .quality-btn.selected {
            border-color: #667eea;
            background: #667eea;
            color: white;
        }
        
        .download-btn {
            width: 100%;
            padding: 18px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 12px;
            font-size: 1.1rem;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        
        .download-btn:hover:not(:disabled) {
            transform: translateY(-2px);
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
        }
        
        .download-btn:disabled {
            opacity: 0.6;
            cursor: not-allowed;
        }
        
        .result {
            margin-top: 30px;
            padding: 20px;
            border-radius: 12px;
            display: none;
        }
        
        .result.success {
            background: #d4edda;
            border: 2px solid #28a745;
            color: #155724;
        }
        
        .result.error {
            background: #f8d7da;
            border: 2px solid #dc3545;
            color: #721c24;
        }
        
        .result.info {
            background: #d1ecf1;
            border: 2px solid #17a2b8;
            color: #0c5460;
        }
        
        .loading {
            display: none;
            text-align: center;
            margin-top: 20px;
        }
        
        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto 10px;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .video-info {
            display: none;
            margin-top: 20px;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 12px;
        }
        
        .video-info img {
            width: 100%;
            max-width: 300px;
            border-radius: 8px;
            margin-bottom: 15px;
        }
        
        .video-info h3 {
            margin-bottom: 10px;
            color: #333;
        }
        
        .video-info p {
            color: #666;
            margin-bottom: 5px;
        }
        
        @media (max-width: 768px) {
            .header h1 {
                font-size: 2rem;
            }
            
            .card {
                padding: 25px;
            }
            
            .options {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📥 Video İndirici</h1>
            <p>YouTube, Instagram, Facebook ve daha fazlasından video indirin</p>
        </div>
        
        <div class="card">
            <div class="platforms">
                <span class="platform">YouTube</span>
                <span class="platform">Instagram</span>
                <span class="platform">Facebook</span>
                <span class="platform">Twitter</span>
                <span class="platform">TikTok</span>
                <span class="platform">Vimeo</span>
            </div>
            
            <div class="input-group">
                <label>Video URL'si</label>
                <div class="input-wrapper">
                    <input type="text" id="videoUrl" placeholder="https://www.youtube.com/watch?v=..." />
                </div>
            </div>
            
            <div class="input-group">
                <label>İndirme Türü</label>
                <div class="options">
                    <div class="option-card selected" data-type="video">
                        <div class="icon">🎬</div>
                        <div class="title">Video</div>
                        <div class="desc">Video + Ses</div>
                    </div>
                    <div class="option-card" data-type="audio">
                        <div class="icon">🎵</div>
                        <div class="title">Sadece Ses</div>
                        <div class="desc">MP3 Format</div>
                    </div>
                </div>
            </div>
            
            <div class="input-group">
                <label>Kalite Seçimi</label>
                <div class="quality-options">
                    <button class="quality-btn selected" data-quality="best">En İyi</button>
                    <button class="quality-btn" data-quality="1080">1080p</button>
                    <button class="quality-btn" data-quality="720">720p</button>
                    <button class="quality-btn" data-quality="480">480p</button>
                    <button class="quality-btn" data-quality="360">360p</button>
                </div>
            </div>
            
            <button class="download-btn" onclick="downloadVideo()">İndir</button>
            
            <div class="loading" id="loading">
                <div class="spinner"></div>
                <p>Video bilgileri alınıyor...</p>
            </div>
            
            <div class="video-info" id="videoInfo"></div>
            <div class="result" id="result"></div>
        </div>
    </div>
    
    <script>
        let selectedType = 'video';
        let selectedQuality = 'best';
        
        // Tip seçimi
        document.querySelectorAll('.option-card').forEach(card => {
            card.addEventListener('click', function() {
                document.querySelectorAll('.option-card').forEach(c => c.classList.remove('selected'));
                this.classList.add('selected');
                selectedType = this.dataset.type;
            });
        });
        
        // Kalite seçimi
        document.querySelectorAll('.quality-btn').forEach(btn => {
            btn.addEventListener('click', function() {
                document.querySelectorAll('.quality-btn').forEach(b => b.classList.remove('selected'));
                this.classList.add('selected');
                selectedQuality = this.dataset.quality;
            });
        });
        
        async function downloadVideo() {
            const url = document.getElementById('videoUrl').value.trim();
            const loading = document.getElementById('loading');
            const result = document.getElementById('result');
            const videoInfo = document.getElementById('videoInfo');
            const downloadBtn = document.querySelector('.download-btn');
            
            if (!url) {
                showResult('Lütfen bir video URL\'si girin', 'error');
                return;
            }
            
            // Reset
            result.style.display = 'none';
            videoInfo.style.display = 'none';
            loading.style.display = 'block';
            downloadBtn.disabled = true;
            
            try {
                const response = await fetch('/api/download', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        url: url,
                        type: selectedType,
                        quality: selectedQuality
                    })
                });
                
                const data = await response.json();
                loading.style.display = 'none';
                downloadBtn.disabled = false;
                
                if (data.success) {
                    // Video bilgilerini göster
                    if (data.info) {
                        showVideoInfo(data.info);
                    }
                    showResult('✅ ' + data.message, 'success');
                    
                    // İndirme linki varsa
                    if (data.download_url) {
                        window.open(data.download_url, '_blank');
                    }
                } else {
                    showResult('❌ ' + data.message, 'error');
                }
            } catch (error) {
                loading.style.display = 'none';
                downloadBtn.disabled = false;
                showResult('❌ Bir hata oluştu: ' + error.message, 'error');
            }
        }
        
        function showResult(message, type) {
            const result = document.getElementById('result');
            result.textContent = message;
            result.className = 'result ' + type;
            result.style.display = 'block';
        }
        
        function showVideoInfo(info) {
            const videoInfo = document.getElementById('videoInfo');
            videoInfo.innerHTML = `
                ${info.thumbnail ? '<img src="' + info.thumbnail + '" alt="Thumbnail" />' : ''}
                <h3>${info.title || 'Video'}</h3>
                ${info.duration ? '<p>Süre: ' + info.duration + '</p>' : ''}
                ${info.uploader ? '<p>Yükleyen: ' + info.uploader + '</p>' : ''}
            `;
            videoInfo.style.display = 'block';
        }
        
        // Enter tuşu ile indir
        document.getElementById('videoUrl').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                downloadVideo();
            }
        });
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/download', methods=['POST'])
def download_video():
    try:
        data = request.get_json()
        url = data.get('url', '').strip()
        download_type = data.get('type', 'video')
        quality = data.get('quality', 'best')
        
        if not url:
            return jsonify({'success': False, 'message': 'URL gerekli'})
        
        # yt-dlp seçenekleri
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
        }
        
        # Video bilgilerini al
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            video_info = {
                'title': info.get('title', 'Video'),
                'duration': str(info.get('duration', 0)) + ' saniye' if info.get('duration') else None,
                'uploader': info.get('uploader', None),
                'thumbnail': info.get('thumbnail', None)
            }
        
        # İndirme formatını ayarla
        if download_type == 'audio':
            format_str = 'bestaudio/best'
        else:
            if quality == 'best':
                format_str = 'bestvideo+bestaudio/best'
            else:
                format_str = f'bestvideo[height<={quality}]+bestaudio/best[height<={quality}]'
        
        return jsonify({
            'success': True,
            'message': 'Video bilgileri alındı! Not: İndirme özelliği sunucu tarafında devre dışı (demo amaçlı)',
            'info': video_info,
            'download_url': url
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Hata: {str(e)}'
        })

@app.route('/health')
def health():
    return {'status': 'healthy'}, 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
