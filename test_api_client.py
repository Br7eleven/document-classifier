#!/usr/bin/env python3
"""
Test client for Document Classification API
Demonstrates how to use the API endpoints
"""

import requests
import json
import os
import sys
from io import BytesIO
from docx import Document

# API Configuration
API_BASE_URL = 'http://localhost:5000'
AUTH_TOKEN = 'Bearer stub_token_12345'
HEADERS = {'Authorization': AUTH_TOKEN}

def test_health_check():
    """Test the health check endpoint"""
    print("🔍 Testing health check endpoint...")
    try:
        response = requests.get(f'{API_BASE_URL}/status')
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_get_categories():
    """Test the categories endpoint"""
    print("\n📋 Testing categories endpoint...")
    try:
        response = requests.get(f'{API_BASE_URL}/categories')
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def create_sample_docx(content, filename):
    """Create a sample DOCX file for testing"""
    doc = Document()
    doc.add_paragraph(content)
    
    # Save to BytesIO
    file_stream = BytesIO()
    doc.save(file_stream)
    file_stream.seek(0)
    
    # Save to file for testing
    with open(filename, 'wb') as f:
        f.write(file_stream.getvalue())
    
    return filename

def test_document_classification():
    """Test document classification with sample documents"""
    print("\n📄 Testing document classification...")
    
    # Sample documents for each category
    test_documents = [
        {
            'content': 'This employment contract establishes the terms and conditions of employment between the employer and employee. The contract includes provisions for salary, benefits, termination clauses, and legal obligations of both parties.',
            'filename': 'legal_contract.docx',
            'expected_category': 'Legal'
        },
        {
            'content': 'Employee performance evaluation for Q4 2023. This review covers job performance, goal achievement, professional development, and recommendations for salary adjustment and promotion opportunities.',
            'filename': 'hr_evaluation.docx',
            'expected_category': 'HR'
        },
        {
            'content': 'Quarterly financial report showing revenue growth of 15% year-over-year. The report includes profit and loss statements, cash flow analysis, and budget forecasts for the next fiscal quarter.',
            'filename': 'finance_report.docx',
            'expected_category': 'Finance'
        },
        {
            'content': 'Patient medical record including diagnosis, treatment plan, medication prescriptions, and follow-up care instructions. The patient presents with symptoms requiring immediate medical attention.',
            'filename': 'medical_record.docx',
            'expected_category': 'Medical'
        },
        {
            'content': 'Technical documentation for software API including endpoint specifications, authentication methods, request/response formats, and code examples for integration with third-party systems.',
            'filename': 'technical_docs.docx',
            'expected_category': 'Technical'
        }
    ]
    
    results = []
    
    for doc in test_documents:
        print(f"\n🔬 Testing: {doc['filename']} (Expected: {doc['expected_category']})")
        
        try:
            # Create sample document
            filename = create_sample_docx(doc['content'], doc['filename'])
            
            # Upload and classify
            with open(filename, 'rb') as f:
                files = {'file': f}
                response = requests.post(
                    f'{API_BASE_URL}/classify',
                    headers=HEADERS,
                    files=files
                )
            
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Classified as: {result['category']}")
                print(f"Confidence: {result['confidence']:.3f}")
                print(f"Processing time: {result['processing_time']:.3f}s")
                
                # Check if prediction matches expected
                correct = result['category'] == doc['expected_category']
                print(f"Prediction correct: {'✅' if correct else '❌'}")
                
                results.append({
                    'filename': doc['filename'],
                    'expected': doc['expected_category'],
                    'predicted': result['category'],
                    'confidence': result['confidence'],
                    'correct': correct
                })
            else:
                print(f"❌ Error: {response.json()}")
                results.append({
                    'filename': doc['filename'],
                    'expected': doc['expected_category'],
                    'predicted': 'ERROR',
                    'confidence': 0,
                    'correct': False
                })
            
            # Clean up
            if os.path.exists(filename):
                os.remove(filename)
                
        except Exception as e:
            print(f"❌ Error processing {doc['filename']}: {e}")
            results.append({
                'filename': doc['filename'],
                'expected': doc['expected_category'],
                'predicted': 'ERROR',
                'confidence': 0,
                'correct': False
            })
    
    return results

def test_authentication():
    """Test authentication requirements"""
    print("\n🔐 Testing authentication...")
    
    # Test without token
    print("Testing without token...")
    response = requests.post(f'{API_BASE_URL}/classify')
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # Test with invalid token
    print("\nTesting with invalid token...")
    invalid_headers = {'Authorization': 'Bearer invalid_token'}
    response = requests.post(f'{API_BASE_URL}/classify', headers=invalid_headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")

def test_error_handling():
    """Test error handling"""
    print("\n⚠️  Testing error handling...")
    
    # Test with no file
    print("Testing with no file...")
    response = requests.post(f'{API_BASE_URL}/classify', headers=HEADERS)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # Test with unsupported file type
    print("\nTesting with unsupported file type...")
    files = {'file': ('test.txt', BytesIO(b'test content'), 'text/plain')}
    response = requests.post(f'{API_BASE_URL}/classify', headers=HEADERS, files=files)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")

def print_summary(results):
    """Print test summary"""
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    
    total_tests = len(results)
    correct_predictions = sum(1 for r in results if r['correct'])
    accuracy = correct_predictions / total_tests if total_tests > 0 else 0
    
    print(f"Total tests: {total_tests}")
    print(f"Correct predictions: {correct_predictions}")
    print(f"Accuracy: {accuracy:.1%}")
    print()
    
    print("Detailed results:")
    for result in results:
        status = "✅" if result['correct'] else "❌"
        print(f"{status} {result['filename']}: {result['expected']} → {result['predicted']} ({result['confidence']:.3f})")

def main():
    """Main test function"""
    print("🚀 Document Classification API Test Client")
    print("=" * 50)
    
    # Test API availability
    if not test_health_check():
        print("❌ API is not available. Please start the server first.")
        sys.exit(1)
    
    # Run tests
    test_get_categories()
    test_authentication()
    test_error_handling()
    
    # Test classification
    results = test_document_classification()
    
    # Print summary
    print_summary(results)
    
    print("\n✅ All tests completed!")

if __name__ == '__main__':
    main()