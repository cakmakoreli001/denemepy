from flask import Flask, render_template, jsonify, request
import os
from datetime import datetime
import requests as http_requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# xAI Grok API Configuration
XAI_API_KEY = os.environ.get('XAI_API_KEY', '')
XAI_API_URL = "https://api.x.ai/v1/chat/completions"

# Basit in-memory veri deposu
todos = [
    {"id": 1, "title": "Flask öğren", "completed": True, "created_at": "2025-11-23"},
    {"id": 2, "title": "API yaz", "completed": False, "created_at": "2025-11-23"}
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/docs')
def api_docs():
    return render_template('api_docs.html')

@app.route('/health')
def health():
    return {'status': 'healthy'}, 200

# API Endpoints
@app.route('/api/todos', methods=['GET'])
def get_todos():
    """Tüm todo'ları getir"""
    return jsonify({
        'success': True,
        'data': todos,
        'count': len(todos)
    })

@app.route('/api/todos/<int:todo_id>', methods=['GET'])
def get_todo(todo_id):
    """Tek bir todo getir"""
    todo = next((t for t in todos if t['id'] == todo_id), None)
    if todo:
        return jsonify({'success': True, 'data': todo})
    return jsonify({'success': False, 'message': 'Todo bulunamadı'}), 404

@app.route('/api/todos', methods=['POST'])
def create_todo():
    """Yeni todo oluştur"""
    data = request.get_json()
    
    if not data or 'title' not in data:
        return jsonify({'success': False, 'message': 'Title gerekli'}), 400
    
    new_todo = {
        'id': max([t['id'] for t in todos], default=0) + 1,
        'title': data['title'],
        'completed': data.get('completed', False),
        'created_at': datetime.now().strftime('%Y-%m-%d')
    }
    todos.append(new_todo)
    
    return jsonify({'success': True, 'data': new_todo}), 201

@app.route('/api/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    """Todo güncelle"""
    todo = next((t for t in todos if t['id'] == todo_id), None)
    if not todo:
        return jsonify({'success': False, 'message': 'Todo bulunamadı'}), 404
    
    data = request.get_json()
    todo['title'] = data.get('title', todo['title'])
    todo['completed'] = data.get('completed', todo['completed'])
    
    return jsonify({'success': True, 'data': todo})

@app.route('/api/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    """Todo sil"""
    global todos
    todo = next((t for t in todos if t['id'] == todo_id), None)
    if not todo:
        return jsonify({'success': False, 'message': 'Todo bulunamadı'}), 404
    
    todos = [t for t in todos if t['id'] != todo_id]
    return jsonify({'success': True, 'message': 'Todo silindi'})

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """İstatistikler"""
    completed = sum(1 for t in todos if t['completed'])
    return jsonify({
        'success': True,
        'data': {
            'total': len(todos),
            'completed': completed,
            'pending': len(todos) - completed
        }
    })

# Chatbot Routes
@app.route('/chat')
def chat():
    """Chatbot arayüzü"""
    return render_template('chat.html')

@app.route('/api/chat', methods=['POST'])
def chat_api():
    """Grok AI ile sohbet"""
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({'success': False, 'message': 'Mesaj gerekli'}), 400
        
        # Check API key
        if not XAI_API_KEY:
            return jsonify({
                'success': False,
                'message': 'API anahtarı ayarlanmamış. Lütfen XAI_API_KEY environment variable\'ını ekleyin.'
            }), 500
        
        # xAI Grok API isteği
        headers = {
            'Authorization': f'Bearer {XAI_API_KEY}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            'model': 'grok-beta',
            'messages': [
                {
                    'role': 'system',
                    'content': 'Sen Grok, esprili ve bilgili bir AI asistanısın. Kullanıcılara yardımcı ol ve gerektiğinde esprili yanıtlar ver.'
                },
                {
                    'role': 'user',
                    'content': user_message
                }
            ],
            'temperature': 0.7,
            'max_tokens': 1000,
            'stream': False
        }
        
        response = http_requests.post(XAI_API_URL, json=payload, headers=headers, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            ai_message = result['choices'][0]['message']['content']
            
            return jsonify({
                'success': True,
                'message': ai_message,
                'model': 'grok-beta'
            })
        else:
            error_detail = response.text
            try:
                error_json = response.json()
                error_detail = error_json.get('error', {}).get('message', error_detail)
            except:
                pass
            
            return jsonify({
                'success': False,
                'message': f'API Hatası ({response.status_code}): {error_detail}',
                'debug': {
                    'status': response.status_code,
                    'has_key': bool(XAI_API_KEY),
                    'key_preview': XAI_API_KEY[:10] + '...' if XAI_API_KEY else 'None'
                }
            }), response.status_code
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Hata: {str(e)}'
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
