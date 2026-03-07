#!/usr/bin/env python
"""
Check the correct Google Generative AI File API
"""
import google.generativeai as genai

# Check available attributes
print("Available file-related attributes in genai:")
print("="*50)
for attr in dir(genai):
    if 'file' in attr.lower() or 'upload' in attr.lower():
        print(f"  - {attr}")

print("\n" + "="*50)
print("Checking genai.files:")
try:
    print(dir(genai.files))
except Exception as e:
    print(f"Error accessing genai.files: {e}")
