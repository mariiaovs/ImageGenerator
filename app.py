from flask import Flask, request, jsonify, send_file
import replicate
import requests
import io

app = Flask(__name__)

# Initialize the Replicate client
client = replicate.Client(api_token="your_api_token_here")

# Endpoint for generating images
@app.route('/generate', methods=['POST'])
def generate_image():
    prompt = request.form['prompt']
    model = client.models.get("stability-ai/stable-diffusion")
    version = model.versions.get("your_version_id_here")
    
    output_url = version.predict(prompt=prompt)

    # Download the image
    img_data = requests.get(output_url).content
    img_file = io.BytesIO(img_data)
    
    return send_file(img_file, mimetype='image/png', as_attachment=True, download_name='generated_image.png')

if __name__ == '__main__':
    app.run(debug=True)
