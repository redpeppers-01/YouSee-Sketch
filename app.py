from flask import Flask, render_template, send_from_directory, jsonify, request
import os
import logging
from werkzeug.utils import secure_filename
from datetime import datetime, UTC

app = Flask(__name__)

# Configuration
class Config:
    IMAGE_FOLDER = os.path.join(app.root_path, 'static', 'images')
    SAVED_FOLDER = os.path.join(app.root_path, 'static', 'saved')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

app.config.from_object(Config)

# Ensure that IMAGE_FOLDER and SAVED_FOLDER exist
os.makedirs(Config.IMAGE_FOLDER, exist_ok=True)
os.makedirs(Config.SAVED_FOLDER, exist_ok=True)

# Logging Configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def allowed_file(filename):
    """Check if the uploaded file has an allowed extension."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def allowed_file_size(file):
    """Check if file size is within limits"""
    file.seek(0, 2)  # Seek to end
    size = file.tell()
    file.seek(0)  # Reset file position
    return size <= app.config['MAX_CONTENT_LENGTH']

@app.route('/')
def index():
    """Render the main page with sorted coloring book previews."""
    try:
        # Retrieve and sort images alphabetically (case-insensitive)
        images = sorted([
            os.path.relpath(os.path.join(root, file), Config.IMAGE_FOLDER)
            for root, _, files in os.walk(Config.IMAGE_FOLDER)
            for file in files if file.lower().endswith(tuple(app.config['ALLOWED_EXTENSIONS']))
        ], key=lambda x: x.lower())
        
        # Pagination parameters
        page = int(request.args.get('page', 1))
        per_page = 10  # Number of images per page
        start = (page - 1) * per_page
        end = start + per_page

        # Retrieve saved images (sorted in reverse order)
        saved_images = sorted([
            os.path.relpath(os.path.join(root, file), Config.SAVED_FOLDER)
            for root, _, files in os.walk(Config.SAVED_FOLDER)
            for file in files if file.lower().endswith(tuple(app.config['ALLOWED_EXTENSIONS']))
        ], key=lambda x: x.lower(), reverse=True)

        # Paginate saved images
        paginated_saved_images = saved_images[start:end]
        total_pages = (len(saved_images) + per_page - 1) // per_page

        return render_template('index.html', 
                             images=images, 
                             saved_images=paginated_saved_images, 
                             page=page, 
                             total_pages=total_pages)
    except Exception as e:
        logger.error(f"Error in index route: {str(e)}")
        return jsonify({'status': 'fail', 'message': 'Internal server error'}), 500

@app.route('/images/<path:filename>')
def serve_image(filename):
    """Serve image files from IMAGE_FOLDER."""
    try:
        return send_from_directory(app.config['IMAGE_FOLDER'], filename)
    except FileNotFoundError:
        logger.error(f"Image not found: {filename}")
        return jsonify({'status': 'fail', 'message': 'Image not found.'}), 404

@app.route('/saved/<path:filename>')
def serve_saved_image(filename):
    """Serve image files from SAVED_FOLDER."""
    try:
        return send_from_directory(app.config['SAVED_FOLDER'], filename)
    except FileNotFoundError:
        logger.error(f"Saved image not found: {filename}")
        return jsonify({'status': 'fail', 'message': 'Saved image not found.'}), 404

@app.route('/upload-image', methods=['POST'])
def upload_image():
    """Handle image uploads from the client-side."""
    if 'image' not in request.files:
        logger.warning("No image part in the request.")
        return jsonify({'status': 'fail', 'message': 'No image part in the request.'}), 400

    file = request.files['image']

    if file.filename == '':
        logger.warning("No selected file.")
        return jsonify({'status': 'fail', 'message': 'No selected file.'}), 400

    if not allowed_file(file.filename):
        logger.warning("Unsupported file type.")
        return jsonify({'status': 'fail', 'message': 'Unsupported file type.'}), 400

    if not allowed_file_size(file):
        logger.warning("File too large.")
        return jsonify({'status': 'fail', 'message': 'File too large'}), 413

    try:
        # Secure the filename to prevent directory traversal attacks
        filename = secure_filename(file.filename)
        timestamp = datetime.now(UTC).strftime('%Y%m%d%H%M%S%f')
        filename = f"{timestamp}_{filename}"
        
        # Save the file
        file_path = os.path.join(app.config['SAVED_FOLDER'], filename)
        file.save(file_path)
        logger.info(f"Image saved: {filename}")
        return jsonify({'status': 'success', 
                       'message': 'Image saved successfully.', 
                       'filename': filename}), 200
    except Exception as e:
        logger.error(f"Error saving image: {str(e)}")
        return jsonify({'status': 'fail', 
                       'message': 'Failed to save image.'}), 500

@app.route('/saved-images')
def saved_images():
    """Serve paginated saved images for AJAX requests."""
    try:
        page = int(request.args.get('page', 1))
        per_page = 10
        start = (page - 1) * per_page
        end = start + per_page

        saved_images = sorted([
            os.path.relpath(os.path.join(root, file), Config.SAVED_FOLDER)
            for root, _, files in os.walk(Config.SAVED_FOLDER)
            for file in files if file.lower().endswith(tuple(app.config['ALLOWED_EXTENSIONS']))
        ], key=lambda x: x.lower(), reverse=True)

        paginated_saved_images = saved_images[start:end]
        total_pages = (len(saved_images) + per_page - 1) // per_page

        return jsonify({
            'saved_images': paginated_saved_images,
            'page': page,
            'total_pages': total_pages
        })
    except Exception as e:
        logger.error(f"Error in saved_images route: {str(e)}")
        return jsonify({'status': 'fail', 'message': 'Internal server error'}), 500

@app.errorhandler(404)
def not_found_error(error):
    """Handle 404 errors with a JSON response."""
    logger.error(f"404 Not Found: {str(error)}")
    return jsonify({'status': 'fail', 'message': 'Resource not found.'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors with a JSON response."""
    logger.error(f"500 Internal Server Error: {str(error)}")
    return jsonify({'status': 'fail', 'message': 'Internal server error.'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

