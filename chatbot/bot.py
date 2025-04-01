import requests

def get_duckduckgo_response(query):
    """Fetch Instant Answer from DuckDuckGo API."""
    url = "http://api.duckduckgo.com/"
    params = {
        "q": query,
        "format": "json",
        "no_html": 1,
        "t": "Nihonow"
    }
    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        return data.get("AbstractText", None)
    except requests.RequestException:
        return None

def get_chatbot_response(user_input):
    """Process user input and return a response."""
    response = get_duckduckgo_response(user_input)
    if response:
        return response
    return "Sorry, I don’t have an answer for that. Try asking about Japanese culture, language, or kanji!"