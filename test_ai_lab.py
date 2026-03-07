#!/usr/bin/env python
"""
Test script to verify the AI Lab functionality
"""
import os
import sys
sys.path.insert(0, r'c:\Users\pooja\OneDrive\Documents\AcademiaPro app')

from dotenv import load_dotenv
import google.generativeai as genai

# Load env
load_dotenv()
api_key = os.getenv('GOOGLE_API_KEY')

if not api_key:
    print("ERROR: GOOGLE_API_KEY not set")
    sys.exit(1)

genai.configure(api_key=api_key)

# Test the File API
print("Testing Gemini File API...")
print("="*50)

# List available models
try:
    print("\n✓ Available models:")
    for model in genai.list_models():
        if 'vision' in model.name or 'gemini' in model.name.lower():
            print(f"  - {model.name}")
except Exception as e:
    print(f"✗ Error listing models: {e}")

# Test file upload (with a small text file)
try:
    print("\n✓ Testing file upload API...")
    test_file = r'c:\Users\pooja\OneDrive\Documents\AcademiaPro app\check.py'
    
    if os.path.exists(test_file):
        uploaded_file = genai.upload_file(test_file)
        print(f"  - File uploaded: {uploaded_file.name}")
        print(f"  - File state: {uploaded_file.state}")
        print(f"  - File URI: {uploaded_file.uri}")
        
        # Try to get the file
        retrieved_file = genai.get_file(uploaded_file.name)
        print(f"  - Retrieved file state: {retrieved_file.state}")
        
        # Clean up
        genai.delete_file(uploaded_file.name)
        print(f"  - File deleted successfully")
    else:
        print(f"  - Test file not found: {test_file}")
        
except Exception as e:
    print(f"✗ Error during file operations: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*50)
print("Test complete!")
