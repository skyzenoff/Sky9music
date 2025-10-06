# Sky9Music

## Overview
Sky9Music is a web-based music player application with a Spotify-inspired interface. It includes an admin panel for managing music uploads and a complete file management system.

## Project Structure
- `index.html` - Main application page with the music player interface
- `admin.html` - Administration page for uploading and managing music
- `news.html` - News and updates page
- `paramètres.html` - Settings page with multi-language support
- `app.py` - Flask backend server for handling uploads and API
- `uploads/` - Directory for storing uploaded music and cover files
  - `uploads/music/` - MP3 audio files
  - `uploads/covers/` - Cover images (JPG, PNG)
- `songs.json` - Database file storing music metadata
- `replay-icon.svg` - Replay button icon

## Features

### Main Application
- Music player with play/pause, next/previous controls
- Progress bar with time tracking
- Volume control
- Search functionality across titles and artists
- Shuffle and repeat modes
- Multi-language support (28+ languages)
- Enhanced responsive design for mobile and desktop
- Animated starfield background
- Dynamic music loading from backend API

### Admin Panel
- Upload music files (MP3 format)
- Upload cover images (JPG, PNG formats)
- Add title and artist information
- View all uploaded music
- Delete music from the library
- Real-time preview of cover images
- File validation and error handling

## Technology Stack
- **Frontend**: Pure HTML5, CSS3, and JavaScript
- **Backend**: Flask (Python 3.11)
- **Storage**: File-based system with JSON metadata
- **APIs**: RESTful API endpoints for music management
- HTML5 Audio API for playback
- Canvas API for animated backgrounds
- LocalStorage for settings persistence

## API Endpoints
- `GET /api/songs` - Retrieve all songs
- `POST /api/upload` - Upload a new song with metadata
- `DELETE /api/songs/:id` - Delete a song
- `GET /uploads/music/:filename` - Serve music files
- `GET /uploads/covers/:filename` - Serve cover images

## Running the Project
The project uses a Flask server running on port 5000.

## Recent Changes
- 2025-10-06: Project imported and configured for Replit environment
- 2025-10-06: Removed all hardcoded music data
- 2025-10-06: Enhanced mobile interface with improved touch controls
- 2025-10-06: Created admin panel with file upload system
- 2025-10-06: Implemented Flask backend with REST API
- 2025-10-06: Added file-based storage system for music and covers
- 2025-10-06: Connected frontend to backend API
