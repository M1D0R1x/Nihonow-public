import re
import requests
import json
import logging
from urllib.parse import quote_plus
import time
from difflib import get_close_matches

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('nihonow_bot')

# Knowledge base (abbreviated; use your full version)
KNOWLEDGE_BASE = {
    "hello": {"response": "Hello in Japanese is こんにちは (konnichiwa)! [Polite, Anytime]\nUse it any time of day to greet someone politely.\nExample: こんにちは、元気ですか？ (Konnichiwa, genki desu ka?) - Hello, how are you?"},
    "hi": {"response": "Hi in Japanese is こんにちは (konnichiwa)! [Polite, Anytime]\nIt’s a friendly, all-purpose greeting.\nExample: こんにちは、お元気ですか？ (Konnichiwa, o-genki desu ka?) - Hi, are you well?"},
    # Add your full KNOWLEDGE_BASE here
}

# Model configurations
MODELS = {
    "local": {"type": "knowledge_base", "active": True},
    "deepseek/deepseek-chat-v3-0324": {  # Updated model name
        "type": "api",
        "endpoint": "https://openrouter.ai/api/v1/chat/completions",
        "api_key": "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",
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
    elif model_name == "deepseek/deepseek-chat-v3-0324":
        if not api_rate_limiter.is_allowed():
            logger.warning("DeepSeek API call blocked due to rate limit")
            return None
        headers = {
            "Authorization": f"Bearer {MODELS[model_name]['api_key']}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:8000",  # Replace with your site URL
            "X-Title": "NihonBot"  # Replace with your site name
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
            logger.info(f"DeepSeek response: {result[:100]}...")
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
        return "こんにちは (Konnichiwa)! I can help you learn about Japanese language, culture, and more! Try asking about hiragana, JLPT levels, or phrases."

    user_input_lower = user_input.lower().strip()
    logger.debug(f"Normalized input: '{user_input_lower}'")

    # Typo tolerance for greetings
    greeting_keys = ["hello", "hi", "goodbye", "thank you", "sorry", "please"]
    close_match = get_close_matches(user_input_lower, greeting_keys, n=1, cutoff=0.8)
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
                return response if model_name == "local" else f"[{model_name}] {response}"
            logger.debug(f"Model {model_name} failed to respond")

    logger.warning("All models failed to respond")
    return "I’m not sure about that! All models might be busy—try again soon."