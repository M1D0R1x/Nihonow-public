import json
import logging
import time
from difflib import get_close_matches

import requests

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('nihonow_bot')

# Static Knowledge Base for Greetings, Identity, and Purpose Questions
KNOWLEDGE_BASE = {
    # Greetings with consistent responses
    "hello": {"response": "こんにちは (Konnichiwa)! How can I assist you today?"},
    "hi": {"response": "こんにちは (Konnichiwa)! How can I assist you today?"},
    "hii": {"response": "こんにちは (Konnichiwa)! How can I assist you today?"},
    "good morning": {"response": "おはようございます (Ohayou gozaimasu)! How can I assist you today?"},
    "good afternoon": {"response": "こんにちは (Konnichiwa)! How can I assist you today?"},
    "good evening": {"response": "こんばんは (Konbanwa)! How can I assist you today?"},
    "hey": {"response": "こんにちは (Konnichiwa)! How can I assist you today?"},

    # Identity and name-related questions
    "what are you": {"response": "I am NihonBot. I’m here to help you with almost anything—ask me a question!"},
    "who are you": {"response": "I am NihonBot. I’m here to help you with almost anything—ask me a question!"},
    "what is your name": {"response": "I am NihonBot."},
    "your name": {"response": "I am NihonBot."},
    "name": {"response": "I am NihonBot."},
    "what's your name": {"response": "I am NihonBot."},
    "whats your name": {"response": "I am NihonBot."},
    "why are you": {"response": "I exist to assist and provide helpful answers, created by xAI to advance our understanding of the universe!"},
    "how are you": {"response": "I’m doing great, thanks for asking! How can I help you today?"},
    "how you doing": {"response": "I’m doing great, thanks for asking! How can I help you today?"},

    # Purpose-related questions
    "what do you do": {"response": "I help you learn about Japanese language, culture, and more!"},
    "what is your purpose": {"response": "I help you learn about Japanese language, culture, and more!"},
    "what can you do": {"response": "I help you learn about Japanese language, culture, and more!"},
    "what's your purpose": {"response": "I help you learn about Japanese language, culture, and more!"},
    "whats your purpose": {"response": "I help you learn about Japanese language, culture, and more!"},
    "what are you for": {"response": "I help you learn about Japanese language, culture, and more!"}
}

# Model configurations with updated API keys
MODELS = {
    "local": {"type": "knowledge_base", "active": True},
    "YOUR_MODEL": {
        "type": "api",
        "endpoint": "YOUR_END_POINT",
        "api_key": "Your_API_KEY",
        "context": 131072,
        "active": True
    },
    "YOUR_MODEL": {
        "type": "api",
        "endpoint": "YOUR_END_POINT",
        "api_key": "YOUR_API_KEY",
        "context": 131072,
        "active": True
    },
    "YOUR_MODEL": {
        "type": "api",
        "endpoint": "YOUR_END_POINT",
        "api_key": "YOUR_API_KEY",
        "context": 131072,
        "active": True
    }
}

# Rate limiter class
class RateLimiter:
    def __init__(self, max_calls, time_frame):
        self.max_calls = max_calls
        self.time_frame = time_frame
        self.calls = []

    def is_allowed(self):
        current_time = time.time()
        self.calls = [call_time for call_time in self.calls if current_time - call_time < self.time_frame]
        logger.debug(f"Rate limiter check: {len(self.calls)} calls in last {self.time_frame}s, max {self.max_calls}")
        if len(self.calls) < self.max_calls:
            self.calls.append(current_time)
            logger.info(f"Rate limit allowed: {len(self.calls)}/{self.max_calls}")
            return True
        logger.warning(f"Rate limit exceeded: {len(self.calls)}/{self.max_calls}")
        return False

api_rate_limiter = RateLimiter(max_calls=20, time_frame=60)  # 20 calls/minute

def generate_response(model_name, prompt):
    logger.info(f"Generating response for model: {model_name}, Prompt: '{prompt}'")
    if model_name == "local":
        response = KNOWLEDGE_BASE.get(prompt.lower(), {}).get("response")
        logger.debug(f"Local response: {response}")
        return response
    elif model_name in MODELS and MODELS[model_name]["type"] == "api":
        if not api_rate_limiter.is_allowed():
            logger.warning(f"{model_name} API call blocked due to rate limit")
            return None
        headers = {
            "Authorization": f"Bearer {MODELS[model_name]['api_key']}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://nihonow.vercel.app/",  # Replace with your site URL
            "X-Title": "NihonBot"
        }
        data = {
            "model": model_name,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 500
        }
        logger.debug(f"API request headers: {headers}")
        logger.debug(f"API request data: {json.dumps(data)}")
        try:
            logger.info(f"Sending API request to {MODELS[model_name]['endpoint']}")
            response = requests.post(MODELS[model_name]["endpoint"], headers=headers, data=json.dumps(data), timeout=10)
            response.raise_for_status()
            result = response.json()["choices"][0]["message"]["content"]
            logger.info(f"{model_name} response: {result[:100]}...")
            return result
        except requests.RequestException as e:
            logger.error(f"Error with {model_name}: {str(e)}")
            MODELS[model_name]["active"] = False
            return None
    logger.warning(f"Model {model_name} not recognized or not active")
    return None

def get_chatbot_response(user_input, selected_model=None):
    logger.info(f"Received user input: '{user_input}', Selected model: {selected_model}")
    if not user_input or user_input.strip() == "":
        logger.debug("Empty input, returning welcome message")
        return "こんにちは (Konnichiwa)! I am NihonBot. I can help you learn about Japanese language, culture, and more! Try asking about hiragana, JLPT levels, or phrases."

    user_input_lower = user_input.lower().strip()
    logger.debug(f"Normalized input: '{user_input_lower}'")

    # Typo tolerance for greetings, identity, and purpose questions
    kb_keys = list(KNOWLEDGE_BASE.keys())
    close_match = get_close_matches(user_input_lower, kb_keys, n=1, cutoff=0.8)
    if close_match:
        logger.info(f"Found close match: {close_match[0]}")
        return KNOWLEDGE_BASE[close_match[0]]["response"]

    # Direct knowledge base match
    if user_input_lower in KNOWLEDGE_BASE:
        logger.info(f"Knowledge base match for: '{user_input_lower}'")
        return KNOWLEDGE_BASE[user_input_lower]["response"]

    # Model selection and exhaustion
    available_models = [m for m, config in MODELS.items() if config["active"]]
    logger.info(f"Available models: {available_models}")

    if selected_model and selected_model in available_models:
        logger.debug(f"Using selected model: {selected_model}")
        response = generate_response(selected_model, user_input)
        if response:
            logger.info(f"Response from {selected_model}: {response[:100]}...")
            return response
        logger.warning(f"No response from selected model: {selected_model}")
    else:
        logger.debug("No model selected, trying available models in order")
        for model_name in available_models:
            response = generate_response(model_name, user_input)
            if response:
                logger.info(f"Response from {model_name}: {response[:100]}...")
                return response
            logger.debug(f"Model {model_name} failed to respond")

    logger.warning("All models failed to respond")
    return "I’m not sure about that! All models might be busy—try again soon."