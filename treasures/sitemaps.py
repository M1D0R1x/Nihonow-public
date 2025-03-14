# treasures/sitemaps.py
from django.contrib.sitemaps import Sitemap
from django.urls import reverse

class StaticViewSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.9

    def items(self):
        return [
            'home', 'about', 'resources', 'contact', 'numbers',
            'hiragana', 'katakana', 'n5', 'n4', 'n3', 'n2', 'n1',
            'n5_quiz', 'n4_quiz', 'n3_quiz', 'n2_quiz', 'n1_quiz',
            'n5_kanji', 'n4_kanji', 'n3_kanji', 'n2_kanji', 'n1_kanji',
            'login', 'logout', 'profile', 'dashboard', 'register'
        ]

    def location(self, item):
        return reverse(item)