#!/usr/bin/env python
"""
Check google.generativeai.generative_models
"""
import google.generativeai as genai

print("Checking generative_models module:")
print("="*60)
try:
    from google.generativeai import generative_models
    attrs = [a for a in dir(generative_models) if not a.startswith('_')]
    for attr in attrs:
        if 'file' in attr.lower() or 'upload' in attr.lower():
            print(f"  ✓ {attr}")
    
    print("\nAll attributes:")
    for attr in sorted(attrs)[:30]:  # First 30
        print(f"  {attr}")
except Exception as e:
    print(f"Error: {e}")

print("\n" + "="*60)
print("Checking for Files class or similar:")
try:
    # Check if there's a Files API
    if hasattr(genai.generative_models, 'File'):
        print("  ✓ Found File class")
    if hasattr(genai.generative_models, 'upload_file'):
        print("  ✓ Found upload_file method")
    if hasattr(genai.generative_models, 'Files'):
        print("  ✓ Found Files class")
except:
    pass
