from flask import Flask, send_from_directory, request, send_file
import replicate
import requests
import io
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Get the API token from environment variables
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")

# Initialize the Replicate client with the API token
client = replicate.Client(api_token=REPLICATE_API_TOKEN)

@app.route('/')
def index():
    # Serve the HTML file from the static folder
    return send_from_directory('static', 'index.html')

@app.route('/generate', methods=['POST'])
def generate_image():
    prompt = request.form['prompt']
    
    # Run the model using replicate.run() with the specific model and version IDs
    try:
        output = replicate.run(
            "aleksa-codes/flux-ghibsky-illustration:a9f94946fa0377091ac0bcfe61b0d62ad9a85224e4b421b677d4747914b908c0",
            input={"prompt": prompt}
        )
    except Exception as e:
        return str(e)  # Return error as a response for debugging

    if not output or not isinstance(output, list) or len(output) == 0:
        return "Failed to generate image or no image URL returned"

    # Download the image
    try:
        img_url = output[0]  # Assuming the first item is the image URL
        img_data = requests.get(img_url).content
        img_file = io.BytesIO(img_data)
    except Exception as e:
        return str(e)  # Return error as a response for debugging

    return send_file(img_file, mimetype='image/png', as_attachment=True, download_name='generated_image.png')

if __name__ == '__main__':
    app.run(debug=True)
