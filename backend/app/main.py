import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
from models import FixSlides
from templates import FIX_LEAD_IN_TEMPLATE, FIX_BODY_TEMPLATE

app = Flask(__name__)
CORS(app)

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

@app.route('/fix-slides', methods=['POST'])
def fix_slides():
    # Retrieve data
    data = request.get_json()
    print(data)
    slides = data['slides']
    use_gpt4 = data['useGPT4']

    # Create string of slides
    slides_string = ""
    for i, slide in enumerate(slides):
        slides_string += f"Slide {i+1}\n"
        slides_string += f"Lead in: < {slide['leadIn']} >\n"
        slides_string += f"Body: < {slide['content']} >\n\n\n"
    print("Slides string: " + slides_string)    
    
    # Select model to use
    if use_gpt4 == "true":
        model_name = "gpt-4"
    else:
        model_name = "gpt-3.5-turbo-16k"
    print("Using model: " + model_name)

    # Rewrite slides
    fix_slides_instance = FixSlides(OPENAI_API_KEY, model_name)

    slides_string_updated_body = fix_slides_instance.call_model(slides_string, FIX_BODY_TEMPLATE)
    slides_string_updated_body_and_lead_ins = fix_slides_instance.call_model(slides_string_updated_body, FIX_LEAD_IN_TEMPLATE)

    return jsonify(slides_string_updated_body_and_lead_ins)

if __name__ == "__main__":
    app.run(debug=True)
