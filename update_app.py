#!/usr/bin/env python
"""
Update app.py with fixed AI Research Lab functions
"""
import re

# Read the current app.py
with open(r'c:\Users\pooja\OneDrive\Documents\AcademiaPro app\app.py', 'r') as f:
    content = f.read()

# Find and replace the ai_lab_chat function
old_ai_lab_chat = r'''@app.route\('/ai_lab_chat', methods=\['POST'\]\)
def ai_lab_chat\(\):
    data = request\.json
    filename = data\.get\('filename'\)
    query = data\.get\('query'\)
    
    file_path = os\.path\.join\(UPLOAD_FOLDER, 'ai_lab_docs', filename\)
    
    try:
        # 1\. Upload to Gemini
        myfile = genai\.upload_file\(file_path\)
        
        # 2\. Wait for the file to be processed \(Active Learning step\)
        # Some large PDFs take a few seconds to 'index'
        while myfile\.state == \"PROCESSING\":
            time\.sleep\(2\)
            myfile = genai\.get_file\(myfile\.name\)

        # 3\. Use the correct Model ID variable you defined at the top
        model = genai\.GenerativeModel\(AI_MODEL_ID\)
        response = model\.generate_content\(
            \[myfile, f\"\\n\\nPlease analyze this document and answer this question: \{query\}\"\]
        \)
        
        # Delete the file after use
        genai\.delete_file\(myfile\.name\)
        
        return jsonify\(\{\"answer\": response\.text\}\)
        
    except Exception as e:
        print\(f\"Detailed Lab Error: \{str\(e\)\}\"\) # This will show in your terminal
        return jsonify\(\{\"answer\": f\"AI Lab Error: \{str\(e\)\}\"\}\), 500'''

new_ai_lab_chat = '''@app.route('/ai_lab_chat', methods=['POST'])
def ai_lab_chat():
    """
    AI Research Lab - Analyze documents or text with AI
    Accepts text content directly
    """
    try:
        data = request.json
        filename = data.get('filename', 'unknown')
        query = data.get('query', '')
        text_content = data.get('text_content', '')
        
        if not text_content:
            return jsonify({"error": "No text content provided"}), 400
        
        if not query:
            query = "Please analyze this content and provide insights."
        
        # Create a prompt with the document content and query
        prompt = f"""You are an academic research assistant specializing in document analysis.
        
Content to analyze:
---
{text_content[:4000]}
---

User Question/Request:
{query}

Please provide a detailed, professional analysis."""
        
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
        }), 500'''

# Replace the function
content = re.sub(
    r"@app\.route\('/ai_lab_chat', methods=\['POST'\]\)\ndef ai_lab_chat\(\):.*?return jsonify\(\{\"answer\": f\"AI Lab Error: \{str\(e\)\}\"\}\), 500",
    new_ai_lab_chat,
    content,
    flags=re.DOTALL
)

# Also update ai_lab_upload
old_ai_lab_upload = r'''@app\.route\('/ai_lab_upload', methods=\['POST'\]\)
def ai_lab_upload\(\):
    file = request\.files\.get\('file'\)
    if not file: return jsonify\(\{\"error\": \"No file\"\}\), 400
    
    # Using a separate sub-folder to avoid mixing with Vault
    LAB_FOLDER = os\.path\.join\(UPLOAD_FOLDER, 'ai_lab_docs'\)
    os\.makedirs\(LAB_FOLDER, exist_ok=True\)
    
    filename = secure_filename\(file\.filename\)
    save_path = os\.path\.join\(LAB_FOLDER, filename\)
    file\.save\(save_path\)
    
    return jsonify\(\{\"status\": \"success\", \"filename\": filename\}\)'''

new_ai_lab_upload = '''@app.route('/ai_lab_upload', methods=['POST'])
def ai_lab_upload():
    """
    Upload document content for AI analysis
    Accepts text files for content extraction
    """
    try:
        file = request.files.get('file')
        
        if not file:
            return jsonify({"error": "No file selected"}), 400
        
        filename = secure_filename(file.filename)
        
        # Read file content
        try:
            if filename.endswith(('.txt', '.md', '.py', '.json', '.csv')):
                text_content = file.read().decode('utf-8')
                message = f"Text file '{filename}' loaded successfully. Enter your question to analyze it."
            else:
                # For other file types, provide a message
                text_content = f"Please upload a text file (.txt, .md, .json, .csv, etc.) for analysis. Received: {filename}"
                message = "Binary files are not directly supported. Please convert to text format."
        except Exception as e:
            text_content = f"Could not read file: {str(e)}"
            message = "Error reading file content"
        
        return jsonify({
            "status": "success",
            "filename": filename,
            "text_content": text_content[:10000],  # Limit to 10k chars
            "message": message
        })
        
    except Exception as e:
        logger.error(f"Upload Error: {str(e)}")
        return jsonify({"error": str(e)}), 500'''

content = re.sub(
    r"@app\.route\('/ai_lab_upload', methods=\['POST'\]\)\ndef ai_lab_upload\(\):.*?return jsonify\(\{\"status\": \"success\", \"filename\": filename\}\)",
    new_ai_lab_upload,
    content,
    flags=re.DOTALL
)

# Write the updated content back
with open(r'c:\Users\pooja\OneDrive\Documents\AcademiaPro app\app.py', 'w') as f:
    f.write(content)

print("✓ Updated app.py with fixed AI Research Lab functions")
print("✓ ai_lab_chat now accepts text content")
print("✓ ai_lab_upload reads text files directly")
print("✓ Removed dependency on genai file upload API")
