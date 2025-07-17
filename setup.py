#!/usr/bin/env python3
"""
Setup script for Document Classification API
Handles installation and initial model setup
"""

import os
import sys
import subprocess
import logging

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"📦 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    print("🐍 Checking Python version...")
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} is compatible")
    return True

def create_virtual_environment():
    """Create virtual environment"""
    if os.path.exists('venv'):
        print("📁 Virtual environment already exists")
        return True
    
    return run_command('python -m venv venv', 'Creating virtual environment')

def install_dependencies():
    """Install required dependencies"""
    # Determine the correct pip command based on OS
    if os.name == 'nt':  # Windows
        pip_cmd = 'venv\\Scripts\\pip.exe'
    else:  # Unix/Linux/macOS
        pip_cmd = 'venv/bin/pip'
    
    commands = [
        f'{pip_cmd} install --upgrade pip',
        f'{pip_cmd} install -r requirements.txt'
    ]
    
    for command in commands:
        if not run_command(command, f'Running: {command}'):
            return False
    
    return True

def create_directories():
    """Create necessary directories"""
    directories = ['model', 'temp_uploads', 'tests']
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"📁 Created directory: {directory}")
        else:
            print(f"📁 Directory already exists: {directory}")
    
    return True

def initialize_model():
    """Initialize the stub model"""
    print("🤖 Initializing model...")
    
    # Add app directory to Python path
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))
    
    try:
        from utils import create_stub_model_and_vectorizer, save_model_and_vectorizer
        
        # Create and save stub model
        model, vectorizer = create_stub_model_and_vectorizer()
        save_model_and_vectorizer(model, vectorizer, 'model')
        
        print("✅ Model initialized successfully")
        return True
    except Exception as e:
        print(f"❌ Model initialization failed: {e}")
        return False

def run_tests():
    """Run basic tests"""
    print("🧪 Running tests...")
    
    # Determine the correct python command
    if os.name == 'nt':  # Windows
        python_cmd = 'venv\\Scripts\\python.exe'
    else:  # Unix/Linux/macOS
        python_cmd = 'venv/bin/python'
    
    return run_command(f'{python_cmd} -m pytest tests/ -v', 'Running tests')

def print_next_steps():
    """Print next steps for the user"""
    print("\n" + "="*60)
    print("🎉 SETUP COMPLETED SUCCESSFULLY!")
    print("="*60)
    print("\n📋 Next steps:")
    print("1. Activate the virtual environment:")
    if os.name == 'nt':  # Windows
        print("   venv\\Scripts\\activate")
    else:  # Unix/Linux/macOS
        print("   source venv/bin/activate")
    
    print("\n2. Start the API server:")
    print("   python run.py")
    print("   # or")
    print("   cd app && python classifier_api.py")
    
    print("\n3. Test the API:")
    print("   python test_api_client.py")
    
    print("\n4. Open the chatbot interface:")
    print("   Open chatbot.html in your browser")
    
    print("\n5. For Docker deployment:")
    print("   docker build -t document-classifier .")
    print("   docker run -p 5000:5000 document-classifier")
    
    print("\n📚 API Documentation:")
    print("   http://localhost:5000/status - Health check")
    print("   POST http://localhost:5000/classify - Classify document")
    print("   GET http://localhost:5000/categories - Get categories")
    
    print("\n🔑 Authentication:")
    print("   Use 'Bearer stub_token_12345' in Authorization header")
    
    print("\n📄 Supported formats: PDF, DOCX (max 16MB)")

def main():
    """Main setup function"""
    print("🚀 Document Classification API Setup")
    print("=" * 40)
    
    # Check prerequisites
    if not check_python_version():
        sys.exit(1)
    
    # Setup steps
    steps = [
        ("Create virtual environment", create_virtual_environment),
        ("Install dependencies", install_dependencies),
        ("Create directories", create_directories),
        ("Initialize model", initialize_model),
    ]
    
    for description, func in steps:
        if not func():
            print(f"❌ Setup failed at step: {description}")
            sys.exit(1)
    
    # Optional: Run tests
    print("\n🧪 Would you like to run tests? (y/n): ", end="")
    if input().lower().strip() in ['y', 'yes']:
        run_tests()
    
    # Print next steps
    print_next_steps()

if __name__ == '__main__':
    main()