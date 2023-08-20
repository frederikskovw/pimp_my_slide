import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
from models import FixSlides
from templates import FIX_LEAD_IN_TEMPLATE, FIX_BODY_TEMPLATE, REVIEW_DATA_TEMPLATE, REVIEW_HORIZONTAL_FLOW_TEMPLATE, REVIEW_VERTICAL_FLOW_TEMPLATE, WRITE_EXECSUM_TEMPLATE
from docx import Document
import logging
import io
import json
from celery import Celery
from celery_config import CELERY_BROKER_URL, CELERY_RESULT_BACKEND

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "https://main--teal-conkies-5d8062.netlify.app"}})
logging.basicConfig(level=logging.DEBUG)

app.config['CELERY_BROKER_URL'] = CELERY_BROKER_URL
app.config['CELERY_RESULT_BACKEND'] = CELERY_RESULT_BACKEND

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Function to initiate the celery task for fixing slides
@celery.task(bind=True)
def fix_slides_task(self, files, form):
    logging.info("Received a request at /fix-slides")
    if 'wordDoc' in files:
        logging.info("Word doc found")
        word_file = files['wordDoc']
        doc = Document(io.BytesIO(word_file.read()))
        slides_string = "\n\n".join([para.text for para in doc.paragraphs if para.text])
    else:
        logging.info("Word doc not found")
        slides = json.loads(form['slides'])
        slides_string = ""
        for i, slide in enumerate(slides):
            slides_string += f"Slide {i+1}\n"
            slides_string += f"Lead in: < {slide['leadIn']} >\n"
            slides_string += f"Body: < {slide['content']} >\n"
            slides_string += f"Data: < {slide['data']} >\n\n"

    use_gpt4 = form['useGPT4'] == "true"
    model_name = "gpt-4" if use_gpt4 else "gpt-3.5-turbo-16k"
    logging.info("Using model: " + model_name)

    # Rewrite slides
    fix_slides_instance = FixSlides(OPENAI_API_KEY, model_name)

    logging.info("Calling model to fix body")
    slides_string_updated_body = fix_slides_instance.call_model(slides_string, FIX_BODY_TEMPLATE)
    logging.info("Calling model to fix lead in")
    slides_string_updated_body_and_lead_ins = fix_slides_instance.call_model(slides_string_updated_body, FIX_LEAD_IN_TEMPLATE)
    logging.info("Calling model to fix data")
    slides_string_updated_body_and_lead_ins_and_review_data = fix_slides_instance.call_model(slides_string_updated_body_and_lead_ins, REVIEW_DATA_TEMPLATE)

    return slides_string_updated_body_and_lead_ins_and_review_data

@app.route('/fix-slides', methods=['POST'])
def fix_slides():
    task = fix_slides_task.apply_async(args=[request.files, request.form])
    logging.debug(f"Task {task.id} initiated for /fix-slides endpoint.")
    return jsonify({"message": "Processing request", "task_id": task.id}), 202

# Function to initiate the celery task for review flow
@celery.task(bind=True)
def review_flow_task(self, form):
    logging.info("Received a request at /review-flow")
    updated_slides = json.loads(form['slides'])
    use_gpt4 = form['useGPT4'] == "true"

    model_name = "gpt-4" if use_gpt4 else "gpt-3.5-turbo-16k"
    logging.info("Using model: " + model_name)

    fix_slides_instance = FixSlides(OPENAI_API_KEY, model_name)

    logging.info("Calling model to review horizontal flow")
    horizontal_flow_review = fix_slides_instance.call_model(updated_slides, REVIEW_HORIZONTAL_FLOW_TEMPLATE)
    logging.info("Calling model to review vertical flow")
    vertical_flow_review = fix_slides_instance.call_model(updated_slides, REVIEW_VERTICAL_FLOW_TEMPLATE)

    return {
        "horizontalFlowReview": horizontal_flow_review,
        "verticalFlowReview": vertical_flow_review
    }

@app.route('/review-flow', methods=['POST'])
def review_flow():
    task = review_flow_task.apply_async(args=[request.form])
    logging.debug(f"Task {task.id} initiated for /review-flow endpoint.")
    return jsonify({"message": "Processing request", "task_id": task.id}), 202

# Function to initiate the celery task for writing exec sum
@celery.task(bind=True)
def write_execsum_task(self, form):
    logging.info("Received a request at /write-execsum")
    updated_slides = json.loads(form['slides'])
    use_gpt4 = form['useGPT4'] == "true"

    model_name = "gpt-4" if use_gpt4 else "gpt-3.5-turbo-16k"
    logging.info("Using model: " + model_name)

    fix_slides_instance = FixSlides(OPENAI_API_KEY, model_name)

    logging.info("Calling model to write exec sum")
    exec_sum = fix_slides_instance.call_model(updated_slides, WRITE_EXECSUM_TEMPLATE)

    return exec_sum

@app.route('/write-execsum', methods=['POST'])
def write_execsum():
    task = write_execsum_task.apply_async(args=[request.form])
    logging.debug(f"Task {task.id} initiated for /write-execsum endpoint.")
    return jsonify({"message": "Processing request", "task_id": task.id}), 202

# Polling endpoint that allows the client to poll for task status/results
@app.route('/task-status/<task_id>')
def task_status(task_id):
    task = fix_slides_task.AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {
            'state': task.state,
            'current': 0,
            'total': 1,
            'status': 'Pending...'
        }
    elif task.state != 'FAILURE':
        response = {
            'state': task.state,
            'current': task.info.get('current', 0),
            'total': task.info.get('total', 1),
            'status': str(task.info)
        }
    else:
        response = {
            'state': task.state,
            'status': str(task.info)
        }
    return jsonify(response)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))