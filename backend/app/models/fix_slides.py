from app.services import chat_model_deterministic, chat_prompt_template

class FixSlides:
    def __init__(self, key, model_name):
        self.key = key
        self.model_name = model_name
        self.chat_model = chat_model_deterministic(key, model_name)

    def call_model(self, slides, template_data):
        results = chat_prompt_template(self.chat_model, slides, **template_data)
        return results
