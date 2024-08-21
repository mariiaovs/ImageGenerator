from flask import Flask, send_from_directory, request, jsonify, send_file
import replicate
import requests
import io
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")

client = replicate.Client(api_token=REPLICATE_API_TOKEN)

@app.route('/')
def index():
    # Serve the HTML file from the static folder
    return send_from_directory('static', 'index.html')

@app.route('/generate', methods=['POST'])
def generate_image():
    prompt = request.form['prompt']
    model = client.models.get("stability-ai/stable-diffusion")
    version = model.versions.get("ac732df83cea7fff18b8472768c88ad041fa750ff7682a21affe81863cbe77e4")

   
    output_url = version.predict(prompt=prompt)
    print(f"API Response: {output_url}")

    # Download the image
    img_data = requests.get(output_url).content
    img_file = io.BytesIO(img_data)

    return send_file(img_file, mimetype='image/png', as_attachment=True, download_name='generated_image.png')

if __name__ == '__main__':
    app.run(debug=True)
