#!/usr/bin/env python
"""
Check google.generativeai module structure
"""
import google.generativeai as genai

print("All public attributes and methods in genai:")
print("="*60)
attrs = [a for a in dir(genai) if not a.startswith('_')]
for attr in attrs:
    print(f"  {attr}")
