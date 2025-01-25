from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
import openai

app = Flask(__name__)

# Replace with your OpenAI API key
openai.api_key = "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"

# MongoDB configuration
app.config["MONGO_URI"] = "mongodb+srv://m29annapurna:m29annapurna@cluster0.dnkzs.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
mongo = PyMongo(app)

@app.route('/generate_content', methods=['POST'])
def generate_content():
    data = request.json
    keyword = data.get('keyword')

    if not keyword:
        return jsonify({"error": "Keyword is required"}), 400

    try:
        # Generate content using OpenAI
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=f"Write a detailed paragraph about \"{keyword}\".",
            max_tokens=150,
            temperature=0.7
        )
        content = response['choices'][0]['text'].strip()

        # Save to MongoDB
        content_data = {
            "keyword": keyword,
            "content": content
        }
        mongo.db.GeneratedContent.insert_one(content_data)

        return jsonify({
            "keyword": keyword,
            "content": content
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
