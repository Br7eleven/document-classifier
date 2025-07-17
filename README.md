# Document Classification API

An AI-powered document classification service that automatically categorizes uploaded documents into one of five categories: **Legal**, **HR**, **Finance**, **Medical**, and **Technical**.

## 🚀 Features

- **Document Processing**: Supports PDF (.pdf) and Word (.docx) file formats
- **AI Classification**: Uses scikit-learn with TF-IDF vectorization and Random Forest classifier
- **RESTful API**: Clean REST endpoints with JSON responses
- **Authentication**: Token-based authentication (stub implementation)
- **Performance**: Optimized for <500ms latency and 100 docs/sec throughput
- **Containerized**: Docker support for easy deployment
- **Comprehensive Testing**: Full test suite with pytest

## 📋 Requirements

- Python 3.9+
- Flask 2.3.3
- scikit-learn 1.3.0
- PyMuPDF (for PDF processing)
- python-docx (for Word document processing)
- See `requirements.txt` for complete dependencies

## 🛠️ Installation

### Local Development

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd document-classifier
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   cd app
   python classifier_api.py
   ```

   The API will be available at `http://localhost:5000`

### Docker Deployment

1. **Build the Docker image**
   ```bash
   docker build -t document-classifier .
   ```

2. **Run the container**
   ```bash
   docker run -p 5000:5000 document-classifier
   ```

3. **Using Docker Compose (optional)**
   ```yaml
   version: '3.8'
   services:
     classifier:
       build: .
       ports:
         - "5000:5000"
       environment:
         - FLASK_ENV=production
   ```

## 📚 API Documentation

### Base URL
```
http://localhost:5000
```

### Authentication
All classification endpoints require authentication via Bearer token in the Authorization header:
```
Authorization: Bearer stub_token_12345
```

### Endpoints

#### 1. Health Check
```http
GET /status
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": 1703123456.789,
  "model_loaded": true,
  "supported_formats": ["pdf", "docx"],
  "categories": ["Legal", "HR", "Finance", "Medical", "Technical"]
}
```

#### 2. Document Classification
```http
POST /classify
Content-Type: multipart/form-data
Authorization: Bearer stub_token_12345
```

**Request:**
- `file`: Document file (PDF or DOCX, max 16MB)

**Response:**
```json
{
  "category": "Legal",
  "confidence": 0.932,
  "processing_time": 0.245,
  "filename": "contract.pdf",
  "all_probabilities": {
    "Legal": 0.932,
    "HR": 0.045,
    "Finance": 0.012,
    "Medical": 0.008,
    "Technical": 0.003
  }
}
```

#### 3. Get Categories
```http
GET /categories
```

**Response:**
```json
{
  "categories": ["Legal", "HR", "Finance", "Medical", "Technical"]
}
```

### Error Responses

**400 Bad Request**
```json
{
  "error": "No file provided"
}
```

**401 Unauthorized**
```json
{
  "error": "Token is missing"
}
```

**413 Payload Too Large**
```json
{
  "error": "File too large. Maximum size: 16MB"
}
```

**500 Internal Server Error**
```json
{
  "error": "Classification failed: <error_message>"
}
```

## 🧪 Testing

Run the test suite:
```bash
pytest tests/ -v
```

Run tests with coverage:
```bash
pytest tests/ --cov=app --cov-report=html
```

## 📁 Project Structure

```
document-classifier/
├── app/
│   ├── classifier_api.py      # Main Flask application
│   └── utils.py              # Utility functions
├── model/
│   ├── classifier_model.joblib   # Trained model (generated)
│   └── vectorizer.joblib         # TF-IDF vectorizer (generated)
├── tests/
│   └── test_api.py           # Unit tests
├── Dockerfile                # Container configuration
├── requirements.txt          # Python dependencies
└── README.md                # This file
```

## 🔧 Configuration

### Environment Variables

- `FLASK_ENV`: Set to `production` for production deployment
- `FLASK_APP`: Path to the Flask application
- `PYTHONPATH`: Python path configuration

### Model Configuration

The application uses a stub model by default. For production use:

1. **Train a custom model** with your dataset
2. **Replace the stub model** in `utils.py`
3. **Save the trained model** using `save_model_and_vectorizer()`

## 📊 Performance Metrics

- **Latency**: <500ms per document (target)
- **Throughput**: 100 documents/second (target)
- **Accuracy**: ≥90% (target with proper training data)
- **File Size Limit**: 16MB maximum
- **Supported Formats**: PDF, DOCX

## 🔐 Security

- **Authentication**: Token-based authentication (stub implementation)
- **File Validation**: Strict file type and size validation
- **Secure Headers**: CORS configuration
- **Container Security**: Non-root user in Docker container

## 🚀 Usage Examples

### Python Example
```python
import requests

# Health check
response = requests.get('http://localhost:5000/status')
print(response.json())

# Classify document
headers = {'Authorization': 'Bearer stub_token_12345'}
files = {'file': open('contract.pdf', 'rb')}

response = requests.post(
    'http://localhost:5000/classify',
    headers=headers,
    files=files
)
print(response.json())
```

### cURL Example
```bash
# Health check
curl -X GET http://localhost:5000/status

# Classify document
curl -X POST \
  -H "Authorization: Bearer stub_token_12345" \
  -F "file=@contract.pdf" \
  http://localhost:5000/classify
```

### JavaScript Example
```javascript
// Health check
fetch('http://localhost:5000/status')
  .then(response => response.json())
  .then(data => console.log(data));

// Classify document
const formData = new FormData();
formData.append('file', fileInput.files[0]);

fetch('http://localhost:5000/classify', {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer stub_token_12345'
  },
  body: formData
})
.then(response => response.json())
.then(data => console.log(data));
```

## 🤖 Chatbot Integration (Bonus)

### Basic HTML/JS Chatbot

Create a simple chatbot interface:

```html
<!DOCTYPE html>
<html>
<head>
    <title>Document Classifier Chatbot</title>
    <style>
        .chat-container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .message { margin: 10px 0; padding: 10px; border-radius: 5px; }
        .bot-message { background-color: #f0f0f0; }
        .user-message { background-color: #007bff; color: white; text-align: right; }
        .file-input { margin: 10px 0; }
    </style>
</head>
<body>
    <div class="chat-container">
        <div id="messages"></div>
        <input type="file" id="fileInput" accept=".pdf,.docx" class="file-input">
        <button onclick="classifyDocument()">Classify Document</button>
    </div>

    <script>
        function addMessage(message, isBot = true) {
            const messagesDiv = document.getElementById('messages');
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${isBot ? 'bot-message' : 'user-message'}`;
            messageDiv.textContent = message;
            messagesDiv.appendChild(messageDiv);
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
        }

        function classifyDocument() {
            const fileInput = document.getElementById('fileInput');
            const file = fileInput.files[0];
            
            if (!file) {
                addMessage('Please select a file first.');
                return;
            }

            addMessage(`Analyzing ${file.name}...`);
            
            const formData = new FormData();
            formData.append('file', file);

            fetch('http://localhost:5000/classify', {
                method: 'POST',
                headers: {
                    'Authorization': 'Bearer stub_token_12345'
                },
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    addMessage(`Error: ${data.error}`);
                } else {
                    addMessage(`Document classified as: ${data.category} (${(data.confidence * 100).toFixed(1)}% confidence)`);
                }
            })
            .catch(error => {
                addMessage(`Error: ${error.message}`);
            });
        }

        // Welcome message
        addMessage('Welcome! Please upload a document (.pdf or .docx) to classify it.');
    </script>
</body>
</html>
```

### Botpress Integration

For Botpress integration:

1. **Create a new Botpress bot**
2. **Add a file upload action** in the flow
3. **Configure API call** to the classification endpoint
4. **Display results** in the chat interface

Example Botpress action:
```javascript
// In Botpress action
const formData = new FormData();
formData.append('file', event.payload.file);

const response = await axios.post('http://localhost:5000/classify', formData, {
  headers: {
    'Authorization': 'Bearer stub_token_12345',
    'Content-Type': 'multipart/form-data'
  }
});

await bp.dialogs.processMessage(event.botId, {
  type: 'text',
  text: `Document classified as: ${response.data.category} (${(response.data.confidence * 100).toFixed(1)}% confidence)`
});
```

## 📈 Monitoring and Logging

The application includes comprehensive logging:

- **Request logging**: All API requests are logged
- **Performance metrics**: Processing time tracking
- **Error logging**: Detailed error information
- **Health monitoring**: Built-in health check endpoint

## 🔄 Deployment

### Production Deployment

1. **Environment setup**
   ```bash
   export FLASK_ENV=production
   export FLASK_APP=app/classifier_api.py
   ```

2. **Use production WSGI server**
   ```bash
   gunicorn --bind 0.0.0.0:5000 --workers 4 app.classifier_api:app
   ```

3. **Reverse proxy** (nginx example)
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
       
       location / {
           proxy_pass http://localhost:5000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

### Scaling

- **Horizontal scaling**: Deploy multiple instances behind a load balancer
- **Vertical scaling**: Increase CPU/memory resources
- **Model optimization**: Use more efficient models for production

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For issues and questions:
- Check the API documentation above
- Run the test suite to verify functionality
- Review logs for error details
- Open an issue in the repository

---

**Note**: This is a demonstration implementation with a stub model. For production use, train the model with real data and implement proper authentication and security measures.