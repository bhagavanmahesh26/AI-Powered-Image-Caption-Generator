import os
from flask import Flask, request, render_template, jsonify
from PIL import Image
import torch
from transformers import BlipProcessor, BlipForConditionalGeneration

app = Flask(__name__)

# Load model and processor
device = "cuda" if torch.cuda.is_available() else "cpu"
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base").to(device)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/caption", methods=["POST"])
def caption():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400
    image_file = request.files["image"]
    image = Image.open(image_file).convert("RGB")

    inputs = processor(image, return_tensors="pt").to(device)
    out = model.generate(**inputs)
    caption = processor.decode(out[0], skip_special_tokens=True)

    return jsonify({"caption": caption})

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
