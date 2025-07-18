#!/usr/bin/env python3
"""
Docker startup script for Document Classification API
"""

import os
import sys
import logging

# Ensure the app directory is in the Python path
sys.path.insert(0, '/app')
sys.path.insert(0, '/app/app')

# Change to app directory
os.chdir('/app')

# Import and run the Flask app
from app.classifier_api import app

if __name__ == '__main__':
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    print("🚀 Starting Document Classification API in Docker...")
    print("🔧 Python path:", sys.path)
    print("📁 Working directory:", os.getcwd())
    
    # Run the Flask app
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=False,
        threaded=True
    )