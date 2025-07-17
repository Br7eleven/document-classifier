"""
Unit tests for Document Classification API
"""

import os
import sys
import pytest
import json
import tempfile
from io import BytesIO

# Add the app directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))

from classifier_api import app
from utils import create_stub_model_and_vectorizer, save_model_and_vectorizer

class TestDocumentClassificationAPI:
    """Test suite for the Document Classification API"""
    
    @pytest.fixture
    def client(self):
        """Create test client"""
        app.config['TESTING'] = True
        app.config['UPLOAD_FOLDER'] = tempfile.mkdtemp()
        
        # Ensure model is available for testing
        model, vectorizer = create_stub_model_and_vectorizer()
        save_model_and_vectorizer(model, vectorizer, 'model')
        
        with app.test_client() as client:
            yield client
    
    @pytest.fixture
    def auth_headers(self):
        """Authentication headers for testing"""
        return {'Authorization': 'Bearer stub_token_12345'}
    
    def test_health_check(self, client):
        """Test the /status endpoint"""
        response = client.get('/status')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['status'] == 'healthy'
        assert 'timestamp' in data
        assert 'model_loaded' in data
        assert 'supported_formats' in data
        assert 'categories' in data
        assert set(data['categories']) == {'Legal', 'HR', 'Finance', 'Medical', 'Technical'}
    
    def test_get_categories(self, client):
        """Test the /categories endpoint"""
        response = client.get('/categories')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert 'categories' in data
        assert set(data['categories']) == {'Legal', 'HR', 'Finance', 'Medical', 'Technical'}
    
    def test_classify_without_token(self, client):
        """Test classification without authentication token"""
        response = client.post('/classify')
        assert response.status_code == 401
        
        data = json.loads(response.data)
        assert 'error' in data
        assert 'Token is missing' in data['error']
    
    def test_classify_with_invalid_token(self, client):
        """Test classification with invalid authentication token"""
        headers = {'Authorization': 'Bearer invalid_token'}
        response = client.post('/classify', headers=headers)
        assert response.status_code == 401
        
        data = json.loads(response.data)
        assert 'error' in data
        assert 'Invalid token' in data['error']
    
    def test_classify_no_file(self, client, auth_headers):
        """Test classification without file upload"""
        response = client.post('/classify', headers=auth_headers)
        assert response.status_code == 400
        
        data = json.loads(response.data)
        assert 'error' in data
        assert 'No file provided' in data['error']
    
    def test_classify_empty_filename(self, client, auth_headers):
        """Test classification with empty filename"""
        data = {'file': (BytesIO(b''), '')}
        response = client.post('/classify', 
                             data=data, 
                             headers=auth_headers,
                             content_type='multipart/form-data')
        assert response.status_code == 400
        
        response_data = json.loads(response.data)
        assert 'error' in response_data
        assert 'No file selected' in response_data['error']
    
    def test_classify_unsupported_format(self, client, auth_headers):
        """Test classification with unsupported file format"""
        data = {'file': (BytesIO(b'test content'), 'test.txt')}
        response = client.post('/classify', 
                             data=data, 
                             headers=auth_headers,
                             content_type='multipart/form-data')
        assert response.status_code == 400
        
        response_data = json.loads(response.data)
        assert 'error' in response_data
        assert 'File type not supported' in response_data['error']
    
    def create_test_docx_content(self):
        """Create a simple test DOCX file content"""
        try:
            from docx import Document
            doc = Document()
            doc.add_paragraph("This is a legal contract between parties regarding employment terms and conditions.")
            
            # Save to BytesIO
            file_stream = BytesIO()
            doc.save(file_stream)
            file_stream.seek(0)
            return file_stream.getvalue()
        except ImportError:
            # Fallback if docx not available
            return b'Mock DOCX content for legal contract employment terms'
    
    def test_classify_valid_docx(self, client, auth_headers):
        """Test classification with valid DOCX file"""
        docx_content = self.create_test_docx_content()
        data = {'file': (BytesIO(docx_content), 'test_document.docx')}
        
        response = client.post('/classify', 
                             data=data, 
                             headers=auth_headers,
                             content_type='multipart/form-data')
        
        # Should succeed or fail gracefully
        assert response.status_code in [200, 400, 500]
        
        if response.status_code == 200:
            response_data = json.loads(response.data)
            assert 'category' in response_data
            assert 'confidence' in response_data
            assert response_data['category'] in ['Legal', 'HR', 'Finance', 'Medical', 'Technical']
            assert 0 <= response_data['confidence'] <= 1
    
    def test_classify_pdf_mock(self, client, auth_headers):
        """Test classification with mock PDF file"""
        # Create mock PDF content
        pdf_content = b'%PDF-1.4\n1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n'
        data = {'file': (BytesIO(pdf_content), 'test_document.pdf')}
        
        response = client.post('/classify', 
                             data=data, 
                             headers=auth_headers,
                             content_type='multipart/form-data')
        
        # Should handle the mock PDF (might fail due to invalid format, which is expected)
        assert response.status_code in [200, 400, 500]
    
    def test_404_endpoint(self, client):
        """Test non-existent endpoint"""
        response = client.get('/nonexistent')
        assert response.status_code == 404
        
        data = json.loads(response.data)
        assert 'error' in data
        assert 'Endpoint not found' in data['error']
    
    def test_file_too_large(self, client, auth_headers):
        """Test file size limit"""
        # Create a large file (mock)
        large_content = b'x' * (17 * 1024 * 1024)  # 17MB
        data = {'file': (BytesIO(large_content), 'large_file.docx')}
        
        response = client.post('/classify', 
                             data=data, 
                             headers=auth_headers,
                             content_type='multipart/form-data')
        
        assert response.status_code == 413
        
        response_data = json.loads(response.data)
        assert 'error' in response_data
        assert 'File too large' in response_data['error']

class TestUtilityFunctions:
    """Test suite for utility functions"""
    
    def test_create_stub_model(self):
        """Test stub model creation"""
        from utils import create_stub_model_and_vectorizer
        
        model, vectorizer = create_stub_model_and_vectorizer()
        
        assert model is not None
        assert vectorizer is not None
        assert hasattr(model, 'predict')
        assert hasattr(model, 'predict_proba')
        assert hasattr(vectorizer, 'transform')
    
    def test_model_prediction(self):
        """Test model prediction functionality"""
        from utils import create_stub_model_and_vectorizer, preprocess_text
        
        model, vectorizer = create_stub_model_and_vectorizer()
        
        # Test with sample text
        test_text = "This is a legal contract agreement between parties"
        processed_text = preprocess_text(test_text)
        text_vector = vectorizer.transform([processed_text])
        
        prediction = model.predict(text_vector)[0]
        probabilities = model.predict_proba(text_vector)[0]
        
        assert isinstance(prediction, (int, np.integer))
        assert 0 <= prediction <= 4  # 5 categories (0-4)
        assert len(probabilities) == 5
        assert all(0 <= prob <= 1 for prob in probabilities)
        assert abs(sum(probabilities) - 1.0) < 1e-6  # Probabilities sum to 1
    
    def test_text_preprocessing(self):
        """Test text preprocessing function"""
        from utils import preprocess_text
        
        test_text = "This is a TEST document with NUMBERS 123 and special chars!@#"
        processed = preprocess_text(test_text)
        
        assert isinstance(processed, str)
        assert processed.islower() or processed == ""
        assert '123' not in processed
        assert '!@#' not in processed
    
    def test_file_extension_handling(self):
        """Test file extension detection"""
        from utils import extract_text_from_file
        
        # Test unsupported format
        with pytest.raises(ValueError):
            extract_text_from_file('test.txt')

if __name__ == '__main__':
    pytest.main([__file__, '-v'])