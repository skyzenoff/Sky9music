from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import os
import json
import uuid

app = Flask(__name__, static_folder='.')
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024
app.config['UPLOAD_FOLDER_MUSIC'] = 'uploads/music'
app.config['UPLOAD_FOLDER_COVERS'] = 'uploads/covers'
app.config['SONGS_DATA_FILE'] = 'songs.json'

ALLOWED_AUDIO_EXTENSIONS = {'mp3', 'mpeg'}
ALLOWED_IMAGE_EXTENSIONS = {'jpg', 'jpeg', 'png'}

def allowed_file(filename, allowed_extensions):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

def load_songs():
    if os.path.exists(app.config['SONGS_DATA_FILE']):
        with open(app.config['SONGS_DATA_FILE'], 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_songs(songs):
    with open(app.config['SONGS_DATA_FILE'], 'w', encoding='utf-8') as f:
        json.dump(songs, f, ensure_ascii=False, indent=2)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_file(path):
    return send_from_directory('.', path)

@app.route('/api/songs', methods=['GET'])
def get_songs():
    songs = load_songs()
    return jsonify(songs)

@app.route('/api/upload', methods=['POST'])
def upload_song():
    if 'musicFile' not in request.files or 'coverFile' not in request.files:
        return jsonify({'error': 'Fichiers manquants'}), 400
    
    music_file = request.files['musicFile']
    cover_file = request.files['coverFile']
    title = request.form.get('title', '')
    artist = request.form.get('artist', '')
    
    if not title or not artist:
        return jsonify({'error': 'Titre et artiste requis'}), 400
    
    if music_file.filename == '' or cover_file.filename == '':
        return jsonify({'error': 'Fichiers non sélectionnés'}), 400
    
    if not allowed_file(music_file.filename, ALLOWED_AUDIO_EXTENSIONS):
        return jsonify({'error': 'Format audio non supporté (MP3 uniquement)'}), 400
    
    if not allowed_file(cover_file.filename, ALLOWED_IMAGE_EXTENSIONS):
        return jsonify({'error': 'Format image non supporté (JPG, PNG uniquement)'}), 400
    
    song_id = str(uuid.uuid4())
    
    music_ext = music_file.filename.rsplit('.', 1)[1].lower()
    cover_ext = cover_file.filename.rsplit('.', 1)[1].lower()
    
    music_filename = f"{song_id}.{music_ext}"
    cover_filename = f"{song_id}.{cover_ext}"
    
    music_path = os.path.join(app.config['UPLOAD_FOLDER_MUSIC'], music_filename)
    cover_path = os.path.join(app.config['UPLOAD_FOLDER_COVERS'], cover_filename)
    
    music_file.save(music_path)
    cover_file.save(cover_path)
    
    songs = load_songs()
    
    new_song = {
        'id': song_id,
        'title': title,
        'artist': artist,
        'src': f'/uploads/music/{music_filename}',
        'img': f'/uploads/covers/{cover_filename}'
    }
    
    songs.append(new_song)
    save_songs(songs)
    
    return jsonify({'message': 'Musique ajoutée avec succès', 'song': new_song}), 201

@app.route('/api/songs/<song_id>', methods=['DELETE'])
def delete_song(song_id):
    songs = load_songs()
    song = next((s for s in songs if s['id'] == song_id), None)
    
    if not song:
        return jsonify({'error': 'Musique introuvable'}), 404
    
    try:
        music_path = song['src'].lstrip('/')
        cover_path = song['img'].lstrip('/')
        
        if os.path.exists(music_path):
            os.remove(music_path)
        if os.path.exists(cover_path):
            os.remove(cover_path)
    except Exception as e:
        print(f"Erreur lors de la suppression des fichiers: {e}")
    
    songs = [s for s in songs if s['id'] != song_id]
    save_songs(songs)
    
    return jsonify({'message': 'Musique supprimée avec succès'}), 200

@app.route('/uploads/<folder>/<filename>')
def serve_upload(folder, filename):
    upload_path = os.path.join('uploads', folder)
    return send_from_directory(upload_path, filename)

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER_MUSIC'], exist_ok=True)
    os.makedirs(app.config['UPLOAD_FOLDER_COVERS'], exist_ok=True)
    
    if not os.path.exists(app.config['SONGS_DATA_FILE']):
        save_songs([])
    
    app.run(host='0.0.0.0', port=5000, debug=False)
