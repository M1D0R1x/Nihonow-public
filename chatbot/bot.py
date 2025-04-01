# chatbot/bot.py
import re
import requests
import json
import logging
from urllib.parse import quote_plus
import time

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('nihonow_bot')

# Expanded knowledge base with more Japanese-related content
KNOWLEDGE_BASE = {
    "hiragana": {
        "response": "Here's a basic hiragana chart:\n" +
                    "あ (a), い (i), う (u), え (e), お (o)\n" +
                    "か (ka), き (ki), く (ku), け (ke), こ (ko)\n" +
                    "さ (sa), し (shi), す (su), せ (se), そ (so)\n" +
                    "(and so on... ask for 'full hiragana' for the complete list!)"
    },
    "full hiragana": {
        "response": "Here's the full hiragana chart:\n" +
                    "あ (a), い (i), う (u), え (e), お (o)\n" +
                    "か (ka), き (ki), く (ku), け (ke), こ (ko)\n" +
                    "さ (sa), し (shi), す (su), せ (se), そ (so)\n" +
                    "た (ta), ち (chi), つ (tsu), て (te), と (to)\n" +
                    "な (na), に (ni), ぬ (nu), ね (ne), の (no)\n" +
                    "は (ha), ひ (hi), ふ (fu), へ (he), ほ (ho)\n" +
                    "ま (ma), み (mi), む (mu), め (me), も (mo)\n" +
                    "や (ya), ゆ (yu), よ (yo)\n" +
                    "ら (ra), り (ri), る (ru), れ (re), ろ (ro)\n" +
                    "わ (wa), を (wo), ん (n)"
    },
    "katakana": {
        "response": "Here's a basic katakana chart:\n" +
                    "ア (a), イ (i), ウ (u), エ (e), オ (o)\n" +
                    "カ (ka), キ (ki), ク (ku), ケ (ke), コ (ko)\n" +
                    "(ask for 'full katakana' for the complete list!)"
    },
    "full katakana": {
        "response": "Here's the full katakana chart:\n" +
                    "ア (a), イ (i), ウ (u), エ (e), オ (o)\n" +
                    "カ (ka), キ (ki), ク (ku), ケ (ke), コ (ko)\n" +
                    "サ (sa), シ (shi), ス (su), セ (se), ソ (so)\n" +
                    "タ (ta), チ (chi), ツ (tsu), テ (te), ト (to)\n" +
                    "ナ (na), ニ (ni), ヌ (nu), ネ (ne), ノ (no)\n" +
                    "ハ (ha), ヒ (hi), フ (fu), ヘ (he), ホ (ho)\n" +
                    "マ (ma), ミ (mi), ム (mu), メ (me), モ (mo)\n" +
                    "ヤ (ya), ユ (yu), ヨ (yo)\n" +
                    "ラ (ra), リ (ri), ル (ru), レ (re), ロ (ro)\n" +
                    "ワ (wa), ヲ (wo), ン (n)"
    },
    "hello": {
        "response": "Hello in Japanese is こんにちは (konnichiwa)!"
    },
    "hi": {
        "response": "Hi in Japanese is こんにちは (konnichiwa)!"
    },
    "goodbye": {
        "response": "Goodbye in Japanese can be さようなら (sayounara) for a long farewell, or じゃあね (jaa ne) for a casual 'see you later'."
    },
    "thank you": {
        "response": "Thank you in Japanese is ありがとう (arigatou). For a more polite form, use ありがとうございます (arigatou gozaimasu)."
    },
    "sorry": {
        "response": "Sorry in Japanese is すみません (sumimasen) or ごめんなさい (gomen nasai)."
    },
    "please": {
        "response": "Please in Japanese is お願いします (onegai shimasu)."
    },
    "japan": {
        "response": "Japan, known as 日本 (Nihon) in Japanese, is an island country in East Asia. It consists of four main islands—Honshu, Hokkaido, Kyushu, and Shikoku—and many smaller ones. Japan is famous for its rich culture, advanced technology, and history."
    },
    "japan capital": {
        "response": "The capital of Japan is Tokyo (東京). Tokyo is not only the largest city in Japan but also a major global hub for culture, technology, and economy."
    },
    "capital of japan": {
        "response": "The capital of Japan is Tokyo (東京). Tokyo is not only the largest city in Japan but also a major global hub for culture, technology, and economy."
    },
    "tokyo": {
        "response": "Tokyo (東京) is the capital city of Japan. It's a bustling metropolis known for its blend of modern skyscrapers, historic temples like Senso-ji, and vibrant districts like Shibuya and Akihabara. Tokyo is also a center for Japanese pop culture, including anime and fashion."
    },
    "osaka": {
        "response": "Osaka (大阪) is a major city in the Kansai region of Japan. It’s the capital of Osaka Prefecture and the third-most populous city in Japan, with about 2.7 million people. Known for its vibrant food scene (like takoyaki and okonomiyaki), Osaka is also famous for landmarks like Osaka Castle and the Dotonbori district."
    },
    "saitama": {
        "response": "Saitama (埼玉) is a prefecture north of Tokyo, often considered part of the Greater Tokyo Area. Its capital, Saitama City, is known for the Railway Museum and the Omiya Bonsai Village. Saitama Prefecture has a population of about 7.3 million and is a hub for commuters working in Tokyo."
    },
    "hokkaido": {
        "response": "Hokkaido (北海道) is the northernmost island of Japan and also a prefecture. Its capital, Sapporo, is famous for the annual Snow Festival, featuring massive snow sculptures. Hokkaido is known for its natural beauty, including national parks like Daisetsuzan, and its seafood, especially crab and sea urchin."
    },
    "kyoto": {
        "response": "Kyoto (京都) is a city in Japan’s Kansai region, famous for its historical and cultural significance. It was the imperial capital of Japan for over 1,000 years. Kyoto is known for temples like Kinkaku-ji (Golden Pavilion), Fushimi Inari Shrine with its thousands of red torii gates, and traditional geisha culture in the Gion district."
    },
    "japan currency": {
        "response": "The currency of Japan is the Yen (円, pronounced 'en'). It’s abbreviated with the ¥ symbol. Coins come in denominations of 1, 5, 10, 50, 100, and 500 yen, while banknotes are 1,000, 2,000, 5,000, and 10,000 yen."
    },
    "currency of japan": {
        "response": "The currency of Japan is the Yen (円, pronounced 'en'). It’s abbreviated with the ¥ symbol. Coins come in denominations of 1, 5, 10, 50, 100, and 500 yen, while banknotes are 1,000, 2,000, 5,000, and 10,000 yen."
    },
    "japanese culture": {
        "response": "Japanese culture is rich and diverse, encompassing traditional arts (ikebana, tea ceremony, calligraphy), cuisine (sushi, ramen, tempura), customs (bowing, gift-giving), festivals (matsuri), and modern pop culture (anime, manga, J-pop). What specific aspect would you like to learn about?"
    },
    "anime": {
        "response": "Anime refers to Japanese animation characterized by colorful artwork, fantastical themes, and vibrant characters. Popular anime in Japan include 'My Hero Academia', 'Attack on Titan', 'One Piece', and Studio Ghibli films like 'Spirited Away'. Anime spans various genres from action to romance to sci-fi."
    },
    "popular anime": {
        "response": "Popular anime in Japan include 'My Hero Academia', 'Attack on Titan', 'One Piece', 'Demon Slayer: Kimetsu no Yaiba', and Studio Ghibli films like 'Spirited Away'. Trends change often, but these titles have been widely loved for their storytelling and animation."
    },
    "one punch man": {
        "response": "'One Punch Man' (ワンパンマン) is a popular Japanese anime and manga series created by ONE. It follows Saitama, a superhero who can defeat any opponent with a single punch but struggles with boredom due to his overwhelming strength. The series is known for its humor, action, and satire of superhero tropes."
    },
    "manga": {
        "response": "Manga are Japanese comics or graphic novels with a distinctive style, typically read from right to left. Manga covers diverse genres and age groups, from shonen (boys) to shojo (girls) to seinen (adult men) to josei (adult women). Popular manga include 'One Piece', 'Naruto', and 'Death Note'."
    },
    "food": {
        "response": "Japanese cuisine is known for its emphasis on seasonality, quality ingredients, and presentation. Famous dishes include sushi (vinegared rice with fish), ramen (noodle soup), tempura (battered and fried seafood or vegetables), and washoku (traditional Japanese cuisine recognized by UNESCO)."
    },
    "samurai": {
        "response": "Samurai were the military nobility and warrior class of feudal Japan, active from the 12th century until the Meiji Restoration in 1868. They followed the bushido code, emphasizing honor, loyalty, and discipline. Famous samurai include Miyamoto Musashi and Oda Nobunaga. Their legacy lives on in Japanese culture through stories, films, and festivals."
    },
    "jlpt": {
        "response": "The Japanese Language Proficiency Test (JLPT) has five levels, from N5 (beginner) to N1 (advanced). Each level tests vocabulary, grammar, reading, and listening skills. Ask about a specific level for more details!"
    },
    "n5": {
        "response": "JLPT N5 is the entry-level test. You need to know about 800 basic vocabulary words, hiragana, katakana, and 100 kanji. You should understand basic grammar to form simple sentences and be able to understand basic conversations."
    },
    "n4": {
        "response": "JLPT N4 requires knowledge of about 1,500 vocabulary words and 300 kanji. You should be able to understand basic Japanese used in everyday situations and read and comprehend passages on familiar daily topics."
    },
    "n3": {
        "response": "JLPT N3 is considered intermediate level. You need to know about 3,000 vocabulary words and 650 kanji. You should be able to understand Japanese used in everyday situations to a certain degree and read and comprehend written materials with specific contents."
    },
    "n2": {
        "response": "JLPT N2 is upper-intermediate level. You need to know about 6,000 vocabulary words and 1,000 kanji. You should be able to understand Japanese used in everyday situations and in a variety of circumstances to a certain degree."
    },
    "n1": {
        "response": "JLPT N1 is the most advanced level. You need to know about 10,000 vocabulary words and 2,000 kanji. You should be able to understand Japanese used in a variety of circumstances and read writings with logical complexity and/or abstract writings on a variety of topics."
    },
    "kanji": {
        "response": "Kanji are Chinese characters used in the Japanese writing system. There are over 50,000 kanji characters, but only about 2,000-3,000 are commonly used. Each kanji can have multiple readings (on-yomi and kun-yomi) and meanings. Learning kanji is a gradual process, often starting with the 80 taught in first grade up to the 2,136 jōyō kanji for general use."
    },
    "japanese particles": {
        "response": "Japanese particles are small words that indicate the grammatical relationship between words in a sentence. Common particles include:\n" +
                  "- は (wa): Topic marker (e.g., 私は学生です - I am a student).\n" +
                  "- が (ga): Subject marker (e.g., 犬が好きです - I like dogs).\n" +
                  "- を (o): Direct object marker (e.g., 本を読みます - I read a book).\n" +
                  "- に (ni): Indicates direction, time, or indirect object (e.g., 学校に行きます - I go to school).\n" +
                  "- で (de): Indicates location of action (e.g., 図書館で勉強します - I study at the library).\n" +
                  "Would you like to know about a specific particle?"
    },
    "grammar": {
        "response": "Japanese grammar is quite different from English. It follows a Subject-Object-Verb (SOV) structure, unlike English's Subject-Verb-Object (SVO). For example, 'I eat sushi' in Japanese is 私は寿司を食べます (Watashi wa sushi o tabemasu). Key elements include particles (like は, が, を), verb conjugations, and levels of politeness. Would you like to learn about a specific grammar topic?"
    },
    "japanese learning": {
        "response": "To learn Japanese effectively, focus on these key areas: 1) Writing systems (hiragana, katakana, kanji), 2) Basic vocabulary, 3) Grammar structures, 4) Listening practice, 5) Speaking practice. Would you like resources or tips for any specific area?"
    },
    "nihonbot": {
        "response": "I am NihonBot, your friendly Japanese language learning assistant! I can help with Japanese writing systems, vocabulary, grammar, culture, and more. Just ask me anything about learning Japanese!"
    },
    "nihonow": {
        "response": "Nihonow is a platform to help you learn Japanese! I’m NihonBot, here to assist with Japanese language, culture, and more. What would you like to learn about?"
    },
    "who are you": {
        "response": "I am NihonBot, your friendly Japanese language learning assistant! I can help with Japanese writing systems, vocabulary, grammar, culture, and more. Just ask me anything about learning Japanese!"
    },
    "whats your name": {
        "response": "I am NihonBot, your friendly Japanese language learning assistant! I can help with Japanese writing systems, vocabulary, grammar, culture, and more. Just ask me anything about learning Japanese!"
    },
    "your name": {
        "response": "I am NihonBot, your friendly Japanese language learning assistant! I can help with Japanese writing systems, vocabulary, grammar, culture, and more. Just ask me anything about learning Japanese!"
    }
}

# Updated category mapping with more keywords
CATEGORIES = {
    "greetings": ["hello", "hi", "goodbye", "bye", "thank you", "thanks", "sorry", "please", "konnichiwa", "sayonara", "arigatou"],
    "writing": ["hiragana", "katakana", "kanji", "alphabet", "characters", "writing system", "japanese writing", "stroke order"],
    "jlpt": ["jlpt", "n5", "n4", "n3", "n2", "n1", "test", "exam", "certification", "level", "japanese proficiency"],
    "culture": ["japanese culture", "tradition", "festival", "matsuri", "anime", "manga", "food", "cuisine", "sushi", "ramen", "kimono", "tea ceremony", "sakura", "cherry blossom", "samurai", "popular anime", "one punch man"],
    "grammar": ["grammar", "particle", "verb", "adjective", "conjugation", "tense", "form", "sentence structure", "japanese grammar", "japanese particles"],
    "japan": ["japan", "japan capital", "capital of japan", "tokyo", "kyoto", "osaka", "hokkaido", "saitama", "okinawa", "japanese city", "prefecture", "japan currency", "currency of japan", "currency"],
    "learning": ["learn japanese", "study japanese", "japanese course", "japanese class", "japanese learning", "beginner japanese", "japanese resources", "japanese practice"],
    "bot": ["nihonbot", "nihonow", "who are you", "whats your name", "your name"]
}

# API handlers
def get_wikipedia_response(query):
    """Get information from Wikipedia API"""
    base_url = "https://en.wikipedia.org/api/rest_v1/page/summary/"
    search_url = "https://en.wikipedia.org/w/api.php"

    # First search for the term
    search_params = {
        "action": "query",
        "format": "json",
        "list": "search",
        "srsearch": query,  # Removed "japanese language" suffix to broaden search
        "utf8": 1
    }

    try:
        search_response = requests.get(search_url, params=search_params, timeout=5)
        search_response.raise_for_status()
        search_data = search_response.json()

        if search_data.get("query", {}).get("search"):
            # Get the first result title
            title = search_data["query"]["search"][0]["title"]
            encoded_title = quote_plus(title)

            # Get the summary for that page
            summary_response = requests.get(f"{base_url}{encoded_title}", timeout=5)
            summary_response.raise_for_status()
            summary_data = summary_response.json()

            if summary_data.get("extract"):
                return summary_data["extract"]

        return None
    except requests.RequestException as e:
        logger.error(f"Wikipedia API error: {e}")
        return None

def get_duckduckgo_response(query):
    """Get information from DuckDuckGo API"""
    url = "https://api.duckduckgo.com/"
    params = {
        "q": query,  # Removed "japanese language" suffix to broaden search
        "format": "json",
        "no_html": 1,
        "skip_disambig": 1,
        "t": "nihonow"
    }

    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()

        # Log the response for debugging
        logger.info(f"DuckDuckGo response: {json.dumps(data, indent=2)}")

        if data.get("AbstractText"):
            return data["AbstractText"]
        elif data.get("RelatedTopics") and len(data["RelatedTopics"]) > 0:
            for topic in data["RelatedTopics"]:
                if isinstance(topic, dict) and topic.get("Text"):
                    return topic["Text"]

        return None
    except requests.RequestException as e:
        logger.error(f"DuckDuckGo API error: {e}")
        return None
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error: {e}")
        return None

def get_jisho_response(query):
    """Get Japanese word information from Jisho API"""
    url = f"https://jisho.org/api/v1/search/words?keyword={quote_plus(query)}"

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()

        if data.get("data") and len(data["data"]) > 0:
            result = data["data"][0]
            output = []

            # Get Japanese word
            if result.get("japanese") and len(result["japanese"]) > 0:
                word = result["japanese"][0]
                if word.get("word"):
                    output.append(f"Word: {word.get('word')}")
                if word.get("reading"):
                    output.append(f"Reading: {word.get('reading')}")

            # Get English definitions
            if result.get("senses") and len(result["senses"]) > 0:
                definitions = result["senses"][0].get("english_definitions", [])
                if definitions:
                    output.append(f"Meaning: {', '.join(definitions)}")

            if output:
                return "\n".join(output)

        return None
    except requests.RequestException as e:
        logger.error(f"Jisho API error: {e}")
        return None

def detect_japanese_query(text):
    """Detect if the query contains Japanese characters and might be a translation request"""
    japanese_pattern = re.compile(r'[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FAF]')
    return bool(japanese_pattern.search(text))

def get_chatbot_response(user_input):
    """Main function to get a response for user input"""
    if not user_input or user_input.isspace():
        return "Please ask me something about Japanese language or culture!"

    user_input_lower = user_input.lower().strip()

    # Direct match from knowledge base (exact match)
    for key, value in KNOWLEDGE_BASE.items():
        if key == user_input_lower:
            return value["response"]

    # Category-based matching (partial match)
    for category, keywords in CATEGORIES.items():
        for keyword in keywords:
            # Check if the keyword is a substring of the input
            if keyword in user_input_lower:
                # Find the most relevant knowledge base entry
                for key in KNOWLEDGE_BASE:
                    if key in user_input_lower or keyword in key:
                        return KNOWLEDGE_BASE[key]["response"]

    # Check if it's a Japanese word/phrase (potential translation request)
    if detect_japanese_query(user_input):
        jisho_response = get_jisho_response(user_input)
        if jisho_response:
            return jisho_response
        return f"I see you're asking about '{user_input}'. This contains Japanese characters. If you're asking for a translation or meaning, please specify what you'd like to know about these characters."

    # Try Wikipedia API
    wiki_response = get_wikipedia_response(user_input)
    if wiki_response:
        return wiki_response

    # Try DuckDuckGo API as a fallback
    ddg_response = get_duckduckgo_response(user_input)
    if ddg_response:
        return ddg_response

    # Final fallback response
    return "I'm not sure about that, but I can help with Japanese language (hiragana, katakana, kanji), JLPT levels (N1-N5), basic phrases, or cultural topics like anime, manga, and food. What would you like to know?"

# Rate limiting functionality
class RateLimiter:
    def __init__(self, max_calls, time_frame):
        self.max_calls = max_calls
        self.time_frame = time_frame  # in seconds
        self.calls = []

    def is_allowed(self):
        current_time = time.time()
        # Remove old calls
        self.calls = [call_time for call_time in self.calls if current_time - call_time < self.time_frame]

        # Check if we're under the limit
        if len(self.calls) < self.max_calls:
            self.calls.append(current_time)
            return True
        return False

# Create a rate limiter instance (10 calls per minute)
api_rate_limiter = RateLimiter(max_calls=10, time_frame=60)