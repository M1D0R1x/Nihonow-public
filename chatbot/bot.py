import requests
import json
import os
import re

# Expanded knowledge base with more Japanese learning content
KNOWLEDGE_BASE = {
    # Hiragana and Katakana sections (keeping your existing content)
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

    # Basic greetings and phrases
    "hello": {
        "response": "Hello in Japanese is こんにちは (konnichiwa)!"
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

    # JLPT levels information
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
        "response": "JLPT N3 is the intermediate level. You need to know about 3,000 vocabulary words and 650 kanji. You should be able to understand Japanese used in everyday situations to a certain degree and read and comprehend written materials with specific contents."
    },
    "n2": {
        "response": "JLPT N2 requires knowledge of about 6,000 vocabulary words and 1,000 kanji. You should be able to understand Japanese used in everyday situations and in a variety of circumstances and read and comprehend written materials with clearly expressed, specific contents."
    },
    "n1": {
        "response": "JLPT N1 is the most advanced level. You need to know about 10,000 vocabulary words and 2,000 kanji. You should be able to understand Japanese used in a variety of circumstances and read and comprehend logical texts, articles, and discussions on a wide range of topics."
    },

    # Japanese culture
    "japanese culture": {
        "response": "Japanese culture is rich and diverse, encompassing traditional arts (ikebana, tea ceremony, calligraphy), cuisine (sushi, ramen, tempura), customs (bowing, gift-giving), festivals (matsuri), and modern pop culture (anime, manga, J-pop). What specific aspect would you like to learn about?"
    },
    "anime": {
        "response": "Anime refers to Japanese animation characterized by colorful artwork, fantastical themes, and vibrant characters. Popular anime include 'My Hero Academia', 'Attack on Titan', 'One Piece', and Studio Ghibli films like 'Spirited Away'. Anime spans various genres from action to romance to sci-fi."
    },
    "manga": {
        "response": "Manga are Japanese comics or graphic novels with a distinctive style, typically read from right to left. Manga covers diverse genres and age groups, from shonen (boys) to shojo (girls) to seinen (adult men) to josei (adult women). Popular manga include 'One Piece', 'Naruto', and 'Death Note'."
    },
    "food": {
        "response": "Japanese cuisine is known for its emphasis on seasonality, quality ingredients, and presentation. Famous dishes include sushi (vinegared rice with fish), ramen (noodle soup), tempura (battered and fried seafood or vegetables), and washoku (traditional Japanese cuisine recognized by UNESCO)."
    },

    # Grammar concepts
    "particles": {
        "response": "Japanese particles are small words that indicate the grammatical function of words in a sentence. Common particles include:\n- は (wa): topic marker\n- が (ga): subject marker\n- を (wo): direct object marker\n- に (ni): indicates direction, time, or location\n- で (de): indicates place of action or means"
    },
    "verbs": {
        "response": "Japanese verbs have different forms based on tense, politeness, and function. The dictionary form (辞書形) ends in -u. Common verb groups are:\n- Group 1: -u verbs (like 話す, hanasu)\n- Group 2: -ru verbs (like 食べる, taberu)\n- Group 3: irregular verbs (する, suru and 来る, kuru)"
    },
    "adjectives": {
        "response": "Japanese has two main types of adjectives:\n- い-adjectives (like 高い, takai) which conjugate directly\n- な-adjectives (like 静かな, shizuka na) which need な when modifying nouns"
    },

    # General information
    "what is japanese": {
        "response": "Japanese (日本語, Nihongo) is the national language of Japan, spoken by about 128 million people. It uses three writing systems: hiragana, katakana, and kanji (Chinese characters). Japanese is an agglutinative language with a subject-object-verb word order and a complex system of honorifics reflecting the hierarchical nature of Japanese society."
    },
    "kanji": {
        "response": "Kanji are Chinese characters used in the Japanese writing system alongside hiragana and katakana. There are over 50,000 kanji, but daily use requires knowledge of about 2,000-3,000 characters. The Japanese government has designated 2,136 characters as Jōyō kanji for everyday use."
    }
}

# Category mapping for better query matching
CATEGORIES = {
    "greetings": ["hello", "hi", "goodbye", "bye", "thank you", "thanks", "sorry", "please"],
    "writing": ["hiragana", "katakana", "kanji", "alphabet", "characters", "writing system"],
    "jlpt": ["jlpt", "n5", "n4", "n3", "n2", "n1", "test", "exam", "certification", "level"],
    "culture": ["culture", "tradition", "festival", "matsuri", "anime", "manga", "food", "cuisine", "sushi", "ramen"],
    "grammar": ["grammar", "particle", "verb", "adjective", "conjugation", "tense", "form"]
}


def get_duckduckgo_response(query):
    url = "http://api.duckduckgo.com/"
    params = {"q": query + " japanese", "format": "json", "no_html": 1, "t": "nihonow"}
    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        return data.get("AbstractText", None)
    except requests.RequestException:
        return None


def get_chatbot_response(user_input):
    user_input_lower = user_input.lower().strip()

    # Direct match from knowledge base
    for key, value in KNOWLEDGE_BASE.items():
        if key in user_input_lower:
            return value["response"]

    # Category-based matching
    for category, keywords in CATEGORIES.items():
        for keyword in keywords:
            if keyword in user_input_lower:
                # Find the most relevant entry in the knowledge base for this category
                for key in KNOWLEDGE_BASE:
                    if keyword in key or key in keyword:
                        return KNOWLEDGE_BASE[key]["response"]

    # Check for Japanese words or phrases in the query
    japanese_pattern = re.compile(r'[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FAF]')
    if japanese_pattern.search(user_input):
        # If Japanese characters are detected, try to provide information about them
        return f"I see you're asking about '{user_input}'. This contains Japanese characters. If you're asking for a translation or meaning, please specify what you'd like to know about these characters."

    # Enhanced DuckDuckGo search with Japanese context
    response = get_duckduckgo_response(user_input)
    if response:
        return response

    # Fallback response with suggestions
    return "I don't have specific information about that yet. Try asking about Japanese hiragana, katakana, kanji, JLPT levels (N1-N5), basic phrases, or cultural aspects like anime, manga, and food. You can also ask specific questions about Japanese grammar!"

