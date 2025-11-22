from flask import Flask, render_template, jsonify, request
import os
from datetime import datetime

app = Flask(__name__)

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

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
