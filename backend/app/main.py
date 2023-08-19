import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
from models import FixSlides
from templates import FIX_LEAD_IN_TEMPLATE, FIX_BODY_TEMPLATE, REVIEW_DATA_TEMPLATE, REVIEW_HORIZONTAL_FLOW_TEMPLATE, REVIEW_VERTICAL_FLOW_TEMPLATE, WRITE_EXECSUM_TEMPLATE
from docx import Document
import io
import json

app = Flask(__name__)
CORS(app)

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

@app.route('/fix-slides', methods=['POST'])
def fix_slides():
    if 'wordDoc' in request.files:
        print("Word doc found")
        word_file = request.files['wordDoc']
        doc = Document(io.BytesIO(word_file.read()))
        slides_string = "\n\n".join([para.text for para in doc.paragraphs if para.text])
    else:
        print("Slides found")
        slides = json.loads(request.form['slides'])
        slides_string = ""
        for i, slide in enumerate(slides):
            slides_string += f"Slide {i+1}\n"
            slides_string += f"Lead in: < {slide['leadIn']} >\n"
            slides_string += f"Body: < {slide['content']} >\n"
            slides_string += f"Data: < {slide['data']} >\n\n"
    
    print(slides_string)

    use_gpt4 = request.form['useGPT4'] == "true"
    model_name = "gpt-4" if use_gpt4 else "gpt-3.5-turbo-16k"
    print("Using model: " + model_name)

    # Rewrite slides
    fix_slides_instance = FixSlides(OPENAI_API_KEY, model_name)

    slides_string_updated_body = fix_slides_instance.call_model(slides_string, FIX_BODY_TEMPLATE)
    slides_string_updated_body_and_lead_ins = fix_slides_instance.call_model(slides_string_updated_body, FIX_LEAD_IN_TEMPLATE)
    slides_string_updated_body_and_lead_ins_and_review_data = fix_slides_instance.call_model(slides_string_updated_body_and_lead_ins, REVIEW_DATA_TEMPLATE)

    return jsonify(slides_string_updated_body_and_lead_ins_and_review_data)

@app.route('/review-flow', methods=['POST'])
def review_flow():
    updated_slides = json.loads(request.form['slides'])
    use_gpt4 = request.form['useGPT4'] == "true"

    model_name = "gpt-4" if use_gpt4 else "gpt-3.5-turbo-16k"
    print("Using model: " + model_name)

    fix_slides_instance = FixSlides(OPENAI_API_KEY, model_name)

    horizontal_flow_review = fix_slides_instance.call_model(updated_slides, REVIEW_HORIZONTAL_FLOW_TEMPLATE)
    vertical_flow_review = fix_slides_instance.call_model(updated_slides, REVIEW_VERTICAL_FLOW_TEMPLATE)

    return jsonify({
        "horizontalFlowReview": horizontal_flow_review,
        "verticalFlowReview": vertical_flow_review
    })

@app.route('/write-execsum', methods=['POST'])
def write_execsum():
    updated_slides = json.loads(request.form['slides'])
    use_gpt4 = request.form['useGPT4'] == "true"

    model_name = "gpt-4" if use_gpt4 else "gpt-3.5-turbo-16k"
    print("Using model: " + model_name)

    fix_slides_instance = FixSlides(OPENAI_API_KEY, model_name)
    exec_sum = fix_slides_instance.call_model(updated_slides, WRITE_EXECSUM_TEMPLATE)

    return jsonify(exec_sum)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))