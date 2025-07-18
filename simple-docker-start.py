#!/usr/bin/env python3
"""
Simple Docker startup script - all imports in one file
"""

import os
import sys
import logging

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app'))

def main():
    """Main function to start the application"""
    try:
        # Try to import the Flask app
        from app.classifier_api import app
        
        print("✅ Successfully imported Flask app")
        
        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        print("🚀 Starting Document Classification API...")
        print(f"📁 Working directory: {os.getcwd()}")
        print(f"🐍 Python path: {sys.path}")
        
        # Run the Flask app
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=False,
            threaded=True
        )
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("📁 Current directory contents:")
        for item in os.listdir('.'):
            print(f"  - {item}")
        
        if os.path.exists('app'):
            print("📁 App directory contents:")
            for item in os.listdir('app'):
                print(f"  - app/{item}")
        
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()