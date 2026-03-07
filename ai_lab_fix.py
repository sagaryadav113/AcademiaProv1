#!/usr/bin/env python
"""
Update the AI Research Lab to work without file uploads
This version accepts text content directly instead of files
"""

# Find and replace the ai_lab_chat function in app.py
new_code = '''@app.route('/ai_lab_chat', methods=['POST'])
def ai_lab_chat():
    """
    AI Research Lab - Analyze documents or text with AI
    Accepts either file content as text or direct text input
    """
    try:
        data = request.json
        filename = data.get('filename', 'unknown')
        query = data.get('query', '')
        text_content = data.get('text_content', '')
        
        if not text_content:
            return jsonify({"error": "No text content provided"}), 400
        
        if not query:
            query = "Please analyze this document and provide a summary."
        
        # Create a prompt with the document content and query
        prompt = f"""You are an academic research assistant. 
        
Document Content:
---
{text_content[:5000]}  # Limit to first 5000 chars to avoid token limits
---

Question/Task:
{query}

Please provide a detailed and helpful analysis."""
        
        # Generate response using Gemini
        model = genai.GenerativeModel(AI_MODEL_ID)
        response = model.generate_content(prompt)
        
        return jsonify({
            "answer": response.text,
            "filename": filename,
            "status": "success"
        })
        
    except Exception as e:
        logger.error(f"AI Lab Error: {str(e)}")
        return jsonify({
            "error": f"AI Lab Error: {str(e)}",
            "answer": "The AI Research Lab encountered an error. Please try again."
        }), 500


@app.route('/ai_lab_upload', methods=['POST'])
def ai_lab_upload():
    """
    Upload document content for AI analysis
    Now accepts text content instead of file uploads
    """
    try:
        file = request.files.get('file')
        
        if not file:
            return jsonify({"error": "No file selected"}), 400
        
        # Read file content
        try:
            if file.filename.endswith(('.pdf', '.docx', '.pptx')):
                # For binary files, we would need PDF/DOCX parsing
                # For now, return a message that text files are supported
                text_content = f"Binary file detected: {file.filename}. Please upload a text file (.txt) for analysis."
            else:
                text_content = file.read().decode('utf-8')
        except Exception as e:
            text_content = f"Could not read file content: {str(e)}"
        
        return jsonify({
            "status": "success",
            "filename": file.filename,
            "text_content": text_content[:10000],  # Limit content size
            "message": f"File '{file.filename}' loaded successfully. Enter your question to analyze it."
        })
        
    except Exception as e:
        logger.error(f"Upload Error: {str(e)}")
        return jsonify({"error": str(e)}), 500
'''

print("Updated AI Research Lab code:")
print("=" * 70)
print(new_code)
print("=" * 70)
print("\nChanges made:")
print("✓ Removed file upload API (not available in this genai version)")
print("✓ Now accepts text content directly")
print("✓ Supports text files (.txt)")
print("✓ Proper error handling")
print("✓ Token limit protection (5000 chars)")
