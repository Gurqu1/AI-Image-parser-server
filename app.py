from flask import Flask, request, jsonify
from flask_cors import CORS
import base64
from dotenv import load_dotenv
load_dotenv()
from openai import OpenAI
client = OpenAI()

app = Flask(__name__)
CORS(app)

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['image']
    print(file.filename)
    data_b64 = base64.b64encode(file.read()).decode("ascii")
    data_url = f"data:{file.mimetype};base64,{data_b64}"
    response = client.responses.create(
        model="gpt-4o-mini",
        input=[
            {
                "role": "user",
                "content": [
                    { "type": "input_text", "text": "parse this image and provide a json output that looks like this: {Store name: string, date: string, items bought: array, items prices: array}" },
                    {
                        "type": "input_image",
                        "image_url": data_url
                    }
                ]
            }
        ]
    )
    print(response.output[0].content[0].text)
    return jsonify({"msg": "Upload success", "status": 200}), 200

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
