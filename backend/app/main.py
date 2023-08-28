import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
from models import FixSlides
from templates import (
    FIX_LEAD_IN_TEMPLATE,
    FIX_BODY_TEMPLATE,
    REVIEW_DATA_TEMPLATE,
    REVIEW_HORIZONTAL_FLOW_TEMPLATE,
    REVIEW_VERTICAL_FLOW_TEMPLATE,
    WRITE_EXECSUM_TEMPLATE
    )
import io
import json

app = Flask(__name__)
CORS(app)

load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

@app.route('/fix-slides', methods=['POST'])
def fix_slides():
    print("Received a request at /fix-slides")
    files = request.files
    form = request.form

    if 'wordDoc' in files:
        print("Word doc found")
        from docx import Document
        word_file = files['wordDoc']
        doc = Document(io.BytesIO(word_file.read()))
        slides_string = "\n\n".join([para.text for para in doc.paragraphs if para.text])
    else:
        print("Word doc not found")
        slides_data = json.loads(form['slides'])
        slides = []
        for i, slide in enumerate(slides_data):
            slides.append(f"Slide {i+1}\n")
            slides.append(f"Lead in: < {slide['leadIn']} >\n")
            slides.append(f"Body: < {slide['content']} >\n")
            slides.append(f"Data: < {slide['data']} >\n\n")
        slides_string = "".join(slides)

    use_gpt4 = form['useGPT4'] == "true"
    model_name = "gpt-4" if use_gpt4 else "gpt-3.5-turbo-16k"
    print("Using model: " + model_name)

    # Rewrite slides
    fix_slides_instance = FixSlides(OPENAI_API_KEY, model_name)

    print("Calling model to fix body")
    slides_string_updated_body = fix_slides_instance.call_model(slides_string, FIX_BODY_TEMPLATE)
    print("Calling model to fix lead in")
    slides_string_updated_body_and_lead_ins = fix_slides_instance.call_model(slides_string_updated_body, FIX_LEAD_IN_TEMPLATE)
    print("Calling model to fix data")
    slides_string_updated_body_and_lead_ins_and_review_data = fix_slides_instance.call_model(slides_string_updated_body_and_lead_ins, REVIEW_DATA_TEMPLATE)

    return jsonify(slides_string_updated_body_and_lead_ins_and_review_data)

@app.route('/review-flow', methods=['POST'])
def review_flow():
    print("Received a request at /review-flow")
    form = request.form
    updated_slides = json.loads(form['slides'])
    use_gpt4 = form['useGPT4'] == "true"
    model_name = "gpt-4" if use_gpt4 else "gpt-3.5-turbo-16k"
    print("Using model: " + model_name)

    fix_slides_instance = FixSlides(OPENAI_API_KEY, model_name)

    print("Calling model to review horizontal flow")
    horizontal_flow_review = fix_slides_instance.call_model(updated_slides, REVIEW_HORIZONTAL_FLOW_TEMPLATE)
    print("Calling model to review vertical flow")
    vertical_flow_review = fix_slides_instance.call_model(updated_slides, REVIEW_VERTICAL_FLOW_TEMPLATE)

    return jsonify({
        "horizontalFlowReview": horizontal_flow_review,
        "verticalFlowReview": vertical_flow_review
    })

@app.route('/write-execsum', methods=['POST'])
def write_execsum():
    print("Received a request at /write-execsum")
    form = request.form
    updated_slides = json.loads(form['slides'])
    use_gpt4 = form['useGPT4'] == "true"
    model_name = "gpt-4" if use_gpt4 else "gpt-3.5-turbo-16k"
    print("Using model: " + model_name)

    fix_slides_instance = FixSlides(OPENAI_API_KEY, model_name)
    print("Calling model to write exec sum")
    exec_sum = fix_slides_instance.call_model(updated_slides, WRITE_EXECSUM_TEMPLATE)

    return jsonify(exec_sum)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)))
