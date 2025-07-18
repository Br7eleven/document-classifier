"""
Flask API for Document Classification Service
Automatically categorizes uploaded documents into: Legal, HR, Finance, Medical, Technical
"""

import os
import time
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import joblib
import logging
from functools import wraps

try:
    from .utils import extract_text_from_file, preprocess_text, load_model_and_vectorizer
except ImportError:
    from utils import extract_text_from_file, preprocess_text, load_model_and_vectorizer

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configuration
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'temp_uploads'
ALLOWED_EXTENSIONS = {'pdf', 'docx'}

# Create upload folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Load model and vectorizer at startup
try:
    model, vectorizer = load_model_and_vectorizer()
    logger.info("Model and vectorizer loaded successfully")
except Exception as e:
    logger.error(f"Failed to load model: {e}")
    model, vectorizer = None, None

# Categories
CATEGORIES = ['Legal', 'HR', 'Finance', 'Medical', 'Technical']

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def token_required(f):
    """Authentication decorator - stub implementation"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        # Stub token validation - in production, validate against proper auth system
        if token != 'Bearer stub_token_12345':
            return jsonify({'error': 'Invalid token'}), 401
        
        return f(*args, **kwargs)
    return decorated

@app.route('/status', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        status = {
            'status': 'healthy',
            'timestamp': time.time(),
            'model_loaded': model is not None and vectorizer is not None,
            'supported_formats': list(ALLOWED_EXTENSIONS),
            'categories': CATEGORIES
        }
        return jsonify(status), 200
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify({'status': 'unhealthy', 'error': str(e)}), 500

@app.route('/classify', methods=['POST'])
@token_required
def classify_document():
    """
    Classify uploaded document
    Returns: JSON with category and confidence score
    """
    start_time = time.time()
    
    try:
        # Check if file is present
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Validate file type
        if not allowed_file(file.filename):
            return jsonify({
                'error': f'File type not supported. Allowed: {", ".join(ALLOWED_EXTENSIONS)}'
            }), 400
        
        # Check if model is loaded
        if model is None or vectorizer is None:
            return jsonify({'error': 'Classification model not available'}), 503
        
        # Save uploaded file temporarily
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            # Extract text from document
            text = extract_text_from_file(filepath)
            if not text or len(text.strip()) < 10:
                return jsonify({'error': 'Could not extract sufficient text from document'}), 400
            
            # Preprocess text
            processed_text = preprocess_text(text)
            
            # Vectorize text
            text_vector = vectorizer.transform([processed_text])
            
            # Make prediction
            prediction = model.predict(text_vector)[0]
            probabilities = model.predict_proba(text_vector)[0]
            
            # Get confidence score
            confidence = float(max(probabilities))
            predicted_category = CATEGORIES[prediction]
            
            # Calculate processing time
            processing_time = time.time() - start_time
            
            # Log the classification
            logger.info(f"Classified '{filename}' as '{predicted_category}' with confidence {confidence:.3f} in {processing_time:.3f}s")
            
            # Clean up temporary file
            os.remove(filepath)
            
            response = {
                'category': predicted_category,
                'confidence': round(confidence, 3),
                'processing_time': round(processing_time, 3),
                'filename': filename,
                'all_probabilities': {
                    category: round(float(prob), 3) 
                    for category, prob in zip(CATEGORIES, probabilities)
                }
            }
            
            return jsonify(response), 200
            
        except Exception as e:
            # Clean up temporary file on error
            if os.path.exists(filepath):
                os.remove(filepath)
            raise e
            
    except Exception as e:
        logger.error(f"Classification error: {e}")
        return jsonify({'error': f'Classification failed: {str(e)}'}), 500

@app.route('/categories', methods=['GET'])
def get_categories():
    """Get list of available categories"""
    return jsonify({'categories': CATEGORIES}), 200

@app.errorhandler(413)
def too_large(e):
    """Handle file too large error"""
    return jsonify({'error': 'File too large. Maximum size: 16MB'}), 413

@app.errorhandler(404)
def not_found(e):
    """Handle not found error"""
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(e):
    """Handle internal server error"""
    logger.error(f"Internal server error: {e}")
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # For development only
    app.run(debug=True, host='0.0.0.0', port=5000)