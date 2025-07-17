#!/usr/bin/env python3
"""
Test script to check which packages can be imported
"""

packages_to_test = [
    'flask',
    'flask_cors',
    'numpy',
    'pandas',
    'sklearn',
    'joblib',
    'docx',
    'fitz',
    'nltk',
    'pytest'
]

print("Testing package imports...")
print("=" * 40)

working_packages = []
failed_packages = []

for package in packages_to_test:
    try:
        __import__(package)
        print(f"✅ {package} - OK")
        working_packages.append(package)
    except ImportError as e:
        print(f"❌ {package} - FAILED: {e}")
        failed_packages.append(package)

print("\n" + "=" * 40)
print(f"Working packages: {len(working_packages)}")
print(f"Failed packages: {len(failed_packages)}")

if failed_packages:
    print(f"\nTo install failed packages:")
    for package in failed_packages:
        if package == 'sklearn':
            print(f"pip install scikit-learn")
        elif package == 'docx':
            print(f"pip install python-docx")
        elif package == 'fitz':
            print(f"pip install PyMuPDF")
        else:
            print(f"pip install {package}")