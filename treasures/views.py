# treasures/views.py
import csv
import logging
import random
import re

from Nihonow import settings

logger = logging.getLogger(__name__)

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse_lazy
from datetime import timedelta, datetime
from .models import UserProgress, DailyWord, Kanji, QuizQuestion, DailyKanji
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from .models import UserProfile

def home(request):
    today = timezone.now().date()
    daily_word = DailyWord.objects.filter(date=today).first()

    # Fallback: If no word for today, get the earliest word and reuse it
    if not daily_word:
        daily_word = DailyWord.objects.order_by('date').first()

    context = {
        'daily_word': daily_word,
    }
    return render(request, 'home.html', context)

def profile(request):
    if not request.user.is_authenticated:
        return redirect('login')
    context = {
        'user': request.user,
    }
    return render(request, 'profile.html', context)

def numbers(request):
    return render(request, 'numbers.html')

def hiragana(request):
    return render(request, 'hiragana.html')

def katakana(request):
    return render(request, 'katakana.html')

def n5(request):
    return render(request, 'level_detail.html', {'level': 'N5'})

def n5_quiz(request):
    return render(request, 'quiz.html', {'level': 'N5'})

def n5_kanji(request):
    # Full list of 103 N5 kanji from your provided data
    kanji_data = [
        {'character': '安', 'onyomi': 'AN', 'kunyomi': 'yasu(i)', 'meaning': 'peace, cheap, safety'},
        {'character': '一', 'onyomi': 'ICHI, ITSU', 'kunyomi': 'hito(tsu), hito-', 'meaning': 'one'},
        {'character': '飲', 'onyomi': 'IN', 'kunyomi': 'no(mu)', 'meaning': 'to drink'},
        {'character': '右', 'onyomi': 'U, YUU', 'kunyomi': 'migi', 'meaning': 'right'},
        {'character': '雨', 'onyomi': 'U', 'kunyomi': 'ame', 'meaning': 'rain'},
        {'character': '駅', 'onyomi': 'EKI', 'kunyomi': '–', 'meaning': 'station'},
        {'character': '円', 'onyomi': 'EN', 'kunyomi': 'maru(i)', 'meaning': 'circle, Yen, round'},
        {'character': '火', 'onyomi': 'KA', 'kunyomi': 'hi', 'meaning': 'fire'},
        {'character': '花', 'onyomi': 'KA', 'kunyomi': 'hana', 'meaning': 'flower, blossom'},
        {'character': '下', 'onyomi': 'KA, GE', 'kunyomi': 'shimo, sa(geru), o(rosu), ku(daru)', 'meaning': 'below, down'},
        {'character': '何', 'onyomi': 'KA', 'kunyomi': 'nani', 'meaning': 'what, how many, which'},
        {'character': '会', 'onyomi': 'KAI, E', 'kunyomi': 'a(u)', 'meaning': 'to meet, to come together, society'},
        {'character': '外', 'onyomi': 'GAI, GE', 'kunyomi': 'soto, hoka, hazu(reru), hazu(su)', 'meaning': 'outside, other, disconnect'},
        {'character': '学', 'onyomi': 'GAKU', 'kunyomi': 'mana(bu)', 'meaning': 'school, science, learning'},
        {'character': '間', 'onyomi': 'KAN, KEN', 'kunyomi': 'aida', 'meaning': 'time, time span'},
        {'character': '気', 'onyomi': 'KI, KE', 'kunyomi': '–', 'meaning': 'soul, spirit'},
        {'character': '九', 'onyomi': 'KYUU, KU', 'kunyomi': 'kokono(tsu), kokono-', 'meaning': 'nine'},
        {'character': '休', 'onyomi': 'KYUU', 'kunyomi': 'yasu(mu)', 'meaning': 'to rest'},
        {'character': '魚', 'onyomi': 'GYO', 'kunyomi': 'sakana, uo', 'meaning': 'fish'},
        {'character': '金', 'onyomi': 'KIN, KON', 'kunyomi': 'kane', 'meaning': 'gold, metal, money'},
        {'character': '空', 'onyomi': 'KUU', 'kunyomi': 'sora, a(keru), kara', 'meaning': 'sky, to become free, empty'},
        {'character': '月', 'onyomi': 'GETSU, GATSU', 'kunyomi': 'tsuki', 'meaning': 'month, moon'},
        {'character': '見', 'onyomi': 'KEN', 'kunyomi': 'mi(ru), mi(eru), mi(seru)', 'meaning': 'to see, to be visible, to show'},
        {'character': '言', 'onyomi': 'GEN, GON', 'kunyomi': 'i(u)', 'meaning': 'word, to talk'},
        {'character': '古', 'onyomi': 'KO', 'kunyomi': 'furu(i)', 'meaning': 'old, used'},
        {'character': '五', 'onyomi': 'GO', 'kunyomi': 'itsu(tsu), itsu-', 'meaning': 'five'},
        {'character': '後', 'onyomi': 'GO, KOU', 'kunyomi': 'ato, oku(reru), nochi', 'meaning': 'after, later, back, to stay behind'},
        {'character': '午', 'onyomi': 'GO', 'kunyomi': '–', 'meaning': 'noon'},
        {'character': '語', 'onyomi': 'GO', 'kunyomi': 'kata(ru), kata(rau)', 'meaning': 'word, to talk'},
        {'character': '校', 'onyomi': 'KOU', 'kunyomi': '–', 'meaning': 'school'},
        {'character': '口', 'onyomi': 'KOU, KU', 'kunyomi': 'kuchi', 'meaning': 'mouth'},
        {'character': '行', 'onyomi': 'KOU', 'kunyomi': 'i(ku), yu(ku), okona(u)', 'meaning': 'to walk, to go, to do, to carry out'},
        {'character': '高', 'onyomi': 'KOU', 'kunyomi': 'taka(i), taka(maru), taka(meru)', 'meaning': 'high, expensive, increase, quantity'},
        {'character': '国', 'onyomi': 'KOKU', 'kunyomi': 'kuni', 'meaning': 'country'},
        {'character': '今', 'onyomi': 'KON, KIN', 'kunyomi': 'ima', 'meaning': 'now'},
        {'character': '左', 'onyomi': 'SA', 'kunyomi': 'hidari', 'meaning': 'left'},
        {'character': '三', 'onyomi': 'SAN', 'kunyomi': 'mit(tsu), mi-', 'meaning': 'three'},
        {'character': '山', 'onyomi': 'SAN', 'kunyomi': 'yama', 'meaning': 'mountain'},
        {'character': '四', 'onyomi': 'SHI', 'kunyomi': 'yo(ttsu), yu(tsu), yo-, yon-', 'meaning': 'four'},
        {'character': '子', 'onyomi': 'SHI, SU', 'kunyomi': 'ko', 'meaning': 'child'},
        {'character': '耳', 'onyomi': 'JI', 'kunyomi': 'mimi', 'meaning': 'ear'},
        {'character': '時', 'onyomi': 'JI', 'kunyomi': 'toki', 'meaning': 'time, hour'},
        {'character': '七', 'onyomi': 'SHICHI', 'kunyomi': 'nana(tsu), nana-, nano-', 'meaning': 'seven'},
        {'character': '車', 'onyomi': 'SHA', 'kunyomi': 'kuruma', 'meaning': 'car, wheel'},
        {'character': '社', 'onyomi': 'SHA', 'kunyomi': 'yashiro', 'meaning': 'shinto shrine, society'},
        {'character': '手', 'onyomi': 'SHU', 'kunyomi': 'te', 'meaning': 'hand'},
        {'character': '週', 'onyomi': 'SHUU', 'kunyomi': '–', 'meaning': 'week'},
        {'character': '十', 'onyomi': 'JUU, JI', 'kunyomi': 'too, to-', 'meaning': 'ten, cross'},
        {'character': '出', 'onyomi': 'SHUTSU', 'kunyomi': 'da(su), de(ru)', 'meaning': 'to leave, to get out, to take out'},
        {'character': '書', 'onyomi': 'SHO', 'kunyomi': 'ka(ku)', 'meaning': 'to write'},
        {'character': '女', 'onyomi': 'JO, NYO', 'kunyomi': 'onna, me', 'meaning': 'woman, female'},
        {'character': '小', 'onyomi': 'SHOU', 'kunyomi': 'chii(sai), ko-, o-', 'meaning': 'small'},
        {'character': '少', 'onyomi': 'SHOU', 'kunyomi': 'suko(shi), suku(nai)', 'meaning': 'a little'},
        {'character': '上', 'onyomi': 'SHOU, JOU', 'kunyomi': 'ue, kami, a(geru), a(garu)', 'meaning': 'above, upper'},
        {'character': '食', 'onyomi': 'SHOKU', 'kunyomi': 'ta(beru), ku(ru), ku(rau)', 'meaning': 'to eat'},
        {'character': '新', 'onyomi': 'SHIN', 'kunyomi': 'atara(shii), ara(ta), nii-', 'meaning': 'new'},
        {'character': '人', 'onyomi': 'JIN, NIN', 'kunyomi': 'hito', 'meaning': 'person'},
        {'character': '水', 'onyomi': 'SUI', 'kunyomi': 'mizu', 'meaning': 'water'},
        {'character': '生', 'onyomi': 'SEI, SHOU', 'kunyomi': 'i(kiru), u(mu), ha(yasu), nama, ki', 'meaning': 'to live, to grow, to be born, raw'},
        {'character': '西', 'onyomi': 'SEI, SAI', 'kunyomi': 'nishi', 'meaning': 'west'},
        {'character': '川', 'onyomi': 'SEN', 'kunyomi': 'kawa', 'meaning': 'river'},
        {'character': '千', 'onyomi': 'SEN', 'kunyomi': 'chi', 'meaning': 'thousand'},
        {'character': '先', 'onyomi': 'SEN', 'kunyomi': 'saki', 'meaning': 'before, in future'},
        {'character': '前', 'onyomi': 'ZEN', 'kunyomi': 'mae', 'meaning': 'before'},
        {'character': '足', 'onyomi': 'SOKU', 'kunyomi': 'ashi, ta(riru), ta(su)', 'meaning': 'foot, to be sufficient, to add'},
        {'character': '多', 'onyomi': 'TA', 'kunyomi': 'oo(i)', 'meaning': 'many'},
        {'character': '大', 'onyomi': 'DAI, TAI', 'kunyomi': 'ou(kii), oo(i)', 'meaning': 'big, a lot'},
        {'character': '男', 'onyomi': 'DAN, NAN', 'kunyomi': 'otoko', 'meaning': 'man, male'},
        {'character': '中', 'onyomi': 'CHUU', 'kunyomi': 'naka', 'meaning': 'inner, center, between'},
        {'character': '長', 'onyomi': 'CHOU', 'kunyomi': 'naga(i)', 'meaning': 'long, leader'},
        {'character': '天', 'onyomi': 'TEN', 'kunyomi': 'ame, ama', 'meaning': 'sky'},
        {'character': '店', 'onyomi': 'TEN', 'kunyomi': 'mise', 'meaning': 'shop'},
        {'character': '電', 'onyomi': 'DEN', 'kunyomi': '–', 'meaning': 'electricity'},
        {'character': '土', 'onyomi': 'DO, TO', 'kunyomi': 'tsuchi', 'meaning': 'earth, ground'},
        {'character': '東', 'onyomi': 'TOU', 'kunyomi': 'higashi', 'meaning': 'east'},
        {'character': '道', 'onyomi': 'DOU', 'kunyomi': 'michi', 'meaning': 'street, path'},
        {'character': '読', 'onyomi': 'DOKU', 'kunyomi': 'yo(mu)', 'meaning': 'to read'},
        {'character': '南', 'onyomi': 'NAN', 'kunyomi': 'minami', 'meaning': 'south'},
        {'character': 'ニ', 'onyomi': 'NI', 'kunyomi': 'futa(tsu), futa-', 'meaning': 'two'},
        {'character': '日', 'onyomi': 'NICHI, JITSU', 'kunyomi': 'hi, -ka', 'meaning': 'day, sun'},
        {'character': '入', 'onyomi': 'NYUU', 'kunyomi': 'hai(ru), i(ru), i(reru)', 'meaning': 'to enter, to insert'},
        {'character': '年', 'onyomi': 'NEN', 'kunyomi': 'toshi', 'meaning': 'year'},
        {'character': '買', 'onyomi': 'BAI', 'kunyomi': 'ka(u)', 'meaning': 'to buy'},
        {'character': '白', 'onyomi': 'HAKU, BYAKU', 'kunyomi': 'shiro(i), shiro', 'meaning': 'white'},
        {'character': '八', 'onyomi': 'HACHI', 'kunyomi': 'yat(tsu), ya(tsu), ya-, you-', 'meaning': 'eight'},
        {'character': '半', 'onyomi': 'HAN', 'kunyomi': 'naka(ba)', 'meaning': 'half, middle, semi-'},
        {'character': '百', 'onyomi': 'HYAKU', 'kunyomi': '–', 'meaning': 'hundred'},
        {'character': '父', 'onyomi': 'FU', 'kunyomi': 'chichi', 'meaning': 'father'},
        {'character': '分', 'onyomi': 'BUN, BU, FUN', 'kunyomi': 'wa(keru), wa(kareru), wa(karu)', 'meaning': 'part, minute, to divide, to understand'},
        {'character': '聞', 'onyomi': 'BUN, MON', 'kunyomi': 'ki(ku), ki(koeru)', 'meaning': 'to hear, to listen, to ask'},
        {'character': '母', 'onyomi': 'BO', 'kunyomi': 'haha', 'meaning': 'mother'},
        {'character': '北', 'onyomi': 'HOKU', 'kunyomi': 'kita', 'meaning': 'north'},
        {'character': '木', 'onyomi': 'BOKU, MOKU', 'kunyomi': 'ki, ko', 'meaning': 'tree, wood'},
        {'character': '本', 'onyomi': 'HON', 'kunyomi': 'moto', 'meaning': 'book, source, main-'},
        {'character': '毎', 'onyomi': 'MAI', 'kunyomi': '–', 'meaning': 'each, every'},
        {'character': '万', 'onyomi': 'MAN, BAN', 'kunyomi': '–', 'meaning': 'ten thousand, all, many'},
        {'character': '名', 'onyomi': 'MEI, MYOU', 'kunyomi': 'na', 'meaning': 'name, reputation'},
        {'character': '目', 'onyomi': 'MOKU', 'kunyomi': 'me', 'meaning': 'eye'},
        {'character': '友', 'onyomi': 'YUU', 'kunyomi': 'tomo', 'meaning': 'friend'},
        {'character': '来', 'onyomi': 'RAI', 'kunyomi': 'ku(ru), kita(ru), kita(su)', 'meaning': 'to come'},
        {'character': '立', 'onyomi': 'RITSU', 'kunyomi': 'ta(tsu), ta(teru)', 'meaning': 'to stand, to establish'},
        {'character': '六', 'onyomi': 'ROKU', 'kunyomi': 'mutt(su), mu(tsu), mu, mui', 'meaning': 'six'},
        {'character': '話', 'onyomi': 'WA', 'kunyomi': 'hanashi, hana(su)', 'meaning': 'speech, to talk, story, conversation'},
    ]

    # Categorize the kanji
    # Define the order for numbers explicitly to ensure increasing order
    number_order = ['一', 'ニ', '三', '四', '五', '六', '七', '八', '九', '十', '百', '千', '万']
    numbers = [k for k in kanji_data if k['character'] in number_order]
    # Sort numbers according to the defined order
    numbers = sorted(numbers, key=lambda k: number_order.index(k['character']))

    environment = [k for k in kanji_data if k['character'] in ['雨', '火', '花', '山', '川', '空', '月', '気', '魚', '金', '木', '水', '土', '日', '電', '天']]
    people = [k for k in kanji_data if k['character'] in ['人', '子', '女', '男', '父', '母', '友', '手', '足', '耳', '目', '口', '名', '生']]
    directions = [k for k in kanji_data if k['character'] in ['上', '下', '左', '右', '中', '外', '前', '後', '西', '東', '南', '北']]
    verbs = [k for k in kanji_data if k['character'] in ['飲', '会', '出', '見', '言', '休', '行', '書', '食', '入', '買', '聞', '読', '来', '立', '話', '学', '分']]
    adjectives = [k for k in kanji_data if k['character'] in ['安', '多', '大', '小', '少', '新', '古', '高', '長', '白', '半']]
    misc = [k for k in kanji_data if k['character'] not in (
        [k['character'] for k in numbers] + [k['character'] for k in environment] +
        [k['character'] for k in people] + [k['character'] for k in directions] +
        [k['character'] for k in verbs] + [k['character'] for k in adjectives]
    )]

    from django.shortcuts import render

    def n5kanji_chart(request):
        # Full list of 103 N5 kanji from your provided data
        kanji_data = [
            {'character': '安', 'onyomi': 'AN', 'kunyomi': 'yasu(i)', 'meaning': 'peace, cheap, safety'},
            {'character': '一', 'onyomi': 'ICHI, ITSU', 'kunyomi': 'hito(tsu), hito-', 'meaning': 'one'},
            {'character': '飲', 'onyomi': 'IN', 'kunyomi': 'no(mu)', 'meaning': 'to drink'},
            {'character': '右', 'onyomi': 'U, YUU', 'kunyomi': 'migi', 'meaning': 'right'},
            {'character': '雨', 'onyomi': 'U', 'kunyomi': 'ame', 'meaning': 'rain'},
            {'character': '駅', 'onyomi': 'EKI', 'kunyomi': '–', 'meaning': 'station'},
            {'character': '円', 'onyomi': 'EN', 'kunyomi': 'maru(i)', 'meaning': 'circle, Yen, round'},
            {'character': '火', 'onyomi': 'KA', 'kunyomi': 'hi', 'meaning': 'fire'},
            {'character': '花', 'onyomi': 'KA', 'kunyomi': 'hana', 'meaning': 'flower, blossom'},
            {'character': '下', 'onyomi': 'KA, GE', 'kunyomi': 'shimo, sa(geru), o(rosu), ku(daru)',
             'meaning': 'below, down'},
            {'character': '何', 'onyomi': 'KA', 'kunyomi': 'nani', 'meaning': 'what, how many, which'},
            {'character': '会', 'onyomi': 'KAI, E', 'kunyomi': 'a(u)', 'meaning': 'to meet, to come together, society'},
            {'character': '外', 'onyomi': 'GAI, GE', 'kunyomi': 'soto, hoka, hazu(reru), hazu(su)',
             'meaning': 'outside, other, disconnect'},
            {'character': '学', 'onyomi': 'GAKU', 'kunyomi': 'mana(bu)', 'meaning': 'school, science, learning'},
            {'character': '間', 'onyomi': 'KAN, KEN', 'kunyomi': 'aida', 'meaning': 'time, time span'},
            {'character': '気', 'onyomi': 'KI, KE', 'kunyomi': '–', 'meaning': 'soul, spirit'},
            {'character': '九', 'onyomi': 'KYUU, KU', 'kunyomi': 'kokono(tsu), kokono-', 'meaning': 'nine'},
            {'character': '休', 'onyomi': 'KYUU', 'kunyomi': 'yasu(mu)', 'meaning': 'to rest'},
            {'character': '魚', 'onyomi': 'GYO', 'kunyomi': 'sakana, uo', 'meaning': 'fish'},
            {'character': '金', 'onyomi': 'KIN, KON', 'kunyomi': 'kane', 'meaning': 'gold, metal, money'},
            {'character': '空', 'onyomi': 'KUU', 'kunyomi': 'sora, a(keru), kara',
             'meaning': 'sky, to become free, empty'},
            {'character': '月', 'onyomi': 'GETSU, GATSU', 'kunyomi': 'tsuki', 'meaning': 'month, moon'},
            {'character': '見', 'onyomi': 'KEN', 'kunyomi': 'mi(ru), mi(eru), mi(seru)',
             'meaning': 'to see, to be visible, to show'},
            {'character': '言', 'onyomi': 'GEN, GON', 'kunyomi': 'i(u)', 'meaning': 'word, to talk'},
            {'character': '古', 'onyomi': 'KO', 'kunyomi': 'furu(i)', 'meaning': 'old, used'},
            {'character': '五', 'onyomi': 'GO', 'kunyomi': 'itsu(tsu), itsu-', 'meaning': 'five'},
            {'character': '後', 'onyomi': 'GO, KOU', 'kunyomi': 'ato, oku(reru), nochi',
             'meaning': 'after, later, back, to stay behind'},
            {'character': '午', 'onyomi': 'GO', 'kunyomi': '–', 'meaning': 'noon'},
            {'character': '語', 'onyomi': 'GO', 'kunyomi': 'kata(ru), kata(rau)', 'meaning': 'word, to talk'},
            {'character': '校', 'onyomi': 'KOU', 'kunyomi': '–', 'meaning': 'school'},
            {'character': '口', 'onyomi': 'KOU, KU', 'kunyomi': 'kuchi', 'meaning': 'mouth'},
            {'character': '行', 'onyomi': 'KOU', 'kunyomi': 'i(ku), yu(ku), okona(u)',
             'meaning': 'to walk, to go, to do, to carry out'},
            {'character': '高', 'onyomi': 'KOU', 'kunyomi': 'taka(i), taka(maru), taka(meru)',
             'meaning': 'high, expensive, increase, quantity'},
            {'character': '国', 'onyomi': 'KOKU', 'kunyomi': 'kuni', 'meaning': 'country'},
            {'character': '今', 'onyomi': 'KON, KIN', 'kunyomi': 'ima', 'meaning': 'now'},
            {'character': '左', 'onyomi': 'SA', 'kunyomi': 'hidari', 'meaning': 'left'},
            {'character': '三', 'onyomi': 'SAN', 'kunyomi': 'mit(tsu), mi-', 'meaning': 'three'},
            {'character': '山', 'onyomi': 'SAN', 'kunyomi': 'yama', 'meaning': 'mountain'},
            {'character': '四', 'onyomi': 'SHI', 'kunyomi': 'yo(ttsu), yu(tsu), yo-, yon-', 'meaning': 'four'},
            {'character': '子', 'onyomi': 'SHI, SU', 'kunyomi': 'ko', 'meaning': 'child'},
            {'character': '耳', 'onyomi': 'JI', 'kunyomi': 'mimi', 'meaning': 'ear'},
            {'character': '時', 'onyomi': 'JI', 'kunyomi': 'toki', 'meaning': 'time, hour'},
            {'character': '七', 'onyomi': 'SHICHI', 'kunyomi': 'nana(tsu), nana-, nano-', 'meaning': 'seven'},
            {'character': '車', 'onyomi': 'SHA', 'kunyomi': 'kuruma', 'meaning': 'car, wheel'},
            {'character': '社', 'onyomi': 'SHA', 'kunyomi': 'yashiro', 'meaning': 'shinto shrine, society'},
            {'character': '手', 'onyomi': 'SHU', 'kunyomi': 'te', 'meaning': 'hand'},
            {'character': '週', 'onyomi': 'SHUU', 'kunyomi': '–', 'meaning': 'week'},
            {'character': '十', 'onyomi': 'JUU, JI', 'kunyomi': 'too, to-', 'meaning': 'ten, cross'},
            {'character': '出', 'onyomi': 'SHUTSU', 'kunyomi': 'da(su), de(ru)',
             'meaning': 'to leave, to get out, to take out'},
            {'character': '書', 'onyomi': 'SHO', 'kunyomi': 'ka(ku)', 'meaning': 'to write'},
            {'character': '女', 'onyomi': 'JO, NYO', 'kunyomi': 'onna, me', 'meaning': 'woman, female'},
            {'character': '小', 'onyomi': 'SHOU', 'kunyomi': 'chii(sai), ko-, o-', 'meaning': 'small'},
            {'character': '少', 'onyomi': 'SHOU', 'kunyomi': 'suko(shi), suku(nai)', 'meaning': 'a little'},
            {'character': '上', 'onyomi': 'SHOU, JOU', 'kunyomi': 'ue, kami, a(geru), a(garu)',
             'meaning': 'above, upper'},
            {'character': '食', 'onyomi': 'SHOKU', 'kunyomi': 'ta(beru), ku(ru), ku(rau)', 'meaning': 'to eat'},
            {'character': '新', 'onyomi': 'SHIN', 'kunyomi': 'atara(shii), ara(ta), nii-', 'meaning': 'new'},
            {'character': '人', 'onyomi': 'JIN, NIN', 'kunyomi': 'hito', 'meaning': 'person'},
            {'character': '水', 'onyomi': 'SUI', 'kunyomi': 'mizu', 'meaning': 'water'},
            {'character': '生', 'onyomi': 'SEI, SHOU', 'kunyomi': 'i(kiru), u(mu), ha(yasu), nama, ki',
             'meaning': 'to live, to grow, to be born, raw'},
            {'character': '西', 'onyomi': 'SEI, SAI', 'kunyomi': 'nishi', 'meaning': 'west'},
            {'character': '川', 'onyomi': 'SEN', 'kunyomi': 'kawa', 'meaning': 'river'},
            {'character': '千', 'onyomi': 'SEN', 'kunyomi': 'chi', 'meaning': 'thousand'},
            {'character': '先', 'onyomi': 'SEN', 'kunyomi': 'saki', 'meaning': 'before, in future'},
            {'character': '前', 'onyomi': 'ZEN', 'kunyomi': 'mae', 'meaning': 'before'},
            {'character': '足', 'onyomi': 'SOKU', 'kunyomi': 'ashi, ta(riru), ta(su)',
             'meaning': 'foot, to be sufficient, to add'},
            {'character': '多', 'onyomi': 'TA', 'kunyomi': 'oo(i)', 'meaning': 'many'},
            {'character': '大', 'onyomi': 'DAI, TAI', 'kunyomi': 'ou(kii), oo(i)', 'meaning': 'big, a lot'},
            {'character': '男', 'onyomi': 'DAN, NAN', 'kunyomi': 'otoko', 'meaning': 'man, male'},
            {'character': '中', 'onyomi': 'CHUU', 'kunyomi': 'naka', 'meaning': 'inner, center, between'},
            {'character': '長', 'onyomi': 'CHOU', 'kunyomi': 'naga(i)', 'meaning': 'long, leader'},
            {'character': '天', 'onyomi': 'TEN', 'kunyomi': 'ame, ama', 'meaning': 'sky'},
            {'character': '店', 'onyomi': 'TEN', 'kunyomi': 'mise', 'meaning': 'shop'},
            {'character': '電', 'onyomi': 'DEN', 'kunyomi': '–', 'meaning': 'electricity'},
            {'character': '土', 'onyomi': 'DO, TO', 'kunyomi': 'tsuchi', 'meaning': 'earth, ground'},
            {'character': '東', 'onyomi': 'TOU', 'kunyomi': 'higashi', 'meaning': 'east'},
            {'character': '道', 'onyomi': 'DOU', 'kunyomi': 'michi', 'meaning': 'street, path'},
            {'character': '読', 'onyomi': 'DOKU', 'kunyomi': 'yo(mu)', 'meaning': 'to read'},
            {'character': '南', 'onyomi': 'NAN', 'kunyomi': 'minami', 'meaning': 'south'},
            {'character': 'ニ', 'onyomi': 'NI', 'kunyomi': 'futa(tsu), futa-', 'meaning': 'two'},
            {'character': '日', 'onyomi': 'NICHI, JITSU', 'kunyomi': 'hi, -ka', 'meaning': 'day, sun'},
            {'character': '入', 'onyomi': 'NYUU', 'kunyomi': 'hai(ru), i(ru), i(reru)',
             'meaning': 'to enter, to insert'},
            {'character': '年', 'onyomi': 'NEN', 'kunyomi': 'toshi', 'meaning': 'year'},
            {'character': '買', 'onyomi': 'BAI', 'kunyomi': 'ka(u)', 'meaning': 'to buy'},
            {'character': '白', 'onyomi': 'HAKU, BYAKU', 'kunyomi': 'shiro(i), shiro', 'meaning': 'white'},
            {'character': '八', 'onyomi': 'HACHI', 'kunyomi': 'yat(tsu), ya(tsu), ya-, you-', 'meaning': 'eight'},
            {'character': '半', 'onyomi': 'HAN', 'kunyomi': 'naka(ba)', 'meaning': 'half, middle, semi-'},
            {'character': '百', 'onyomi': 'HYAKU', 'kunyomi': '–', 'meaning': 'hundred'},
            {'character': '父', 'onyomi': 'FU', 'kunyomi': 'chichi', 'meaning': 'father'},
            {'character': '分', 'onyomi': 'BUN, BU, FUN', 'kunyomi': 'wa(keru), wa(kareru), wa(karu)',
             'meaning': 'part, minute, to divide, to understand'},
            {'character': '聞', 'onyomi': 'BUN, MON', 'kunyomi': 'ki(ku), ki(koeru)',
             'meaning': 'to hear, to listen, to ask'},
            {'character': '母', 'onyomi': 'BO', 'kunyomi': 'haha', 'meaning': 'mother'},
            {'character': '北', 'onyomi': 'HOKU', 'kunyomi': 'kita', 'meaning': 'north'},
            {'character': '木', 'onyomi': 'BOKU, MOKU', 'kunyomi': 'ki, ko', 'meaning': 'tree, wood'},
            {'character': '本', 'onyomi': 'HON', 'kunyomi': 'moto', 'meaning': 'book, source, main-'},
            {'character': '毎', 'onyomi': 'MAI', 'kunyomi': '–', 'meaning': 'each, every'},
            {'character': '万', 'onyomi': 'MAN, BAN', 'kunyomi': '–', 'meaning': 'ten thousand, all, many'},
            {'character': '名', 'onyomi': 'MEI, MYOU', 'kunyomi': 'na', 'meaning': 'name, reputation'},
            {'character': '目', 'onyomi': 'MOKU', 'kunyomi': 'me', 'meaning': 'eye'},
            {'character': '友', 'onyomi': 'YUU', 'kunyomi': 'tomo', 'meaning': 'friend'},
            {'character': '来', 'onyomi': 'RAI', 'kunyomi': 'ku(ru), kita(ru), kita(su)', 'meaning': 'to come'},
            {'character': '立', 'onyomi': 'RITSU', 'kunyomi': 'ta(tsu), ta(teru)', 'meaning': 'to stand, to establish'},
            {'character': '六', 'onyomi': 'ROKU', 'kunyomi': 'mutt(su), mu(tsu), mu, mui', 'meaning': 'six'},
            {'character': '話', 'onyomi': 'WA', 'kunyomi': 'hanashi, hana(su)',
             'meaning': 'speech, to talk, story, conversation'},
        ]

        # Categorize the kanji
        # Define the order for numbers explicitly to ensure increasing order
        number_order = ['一', 'ニ', '三', '四', '五', '六', '七', '八', '九', '十', '百', '千', '万']
        numbers = [k for k in kanji_data if k['character'] in number_order]
        numbers = sorted(numbers, key=lambda k: number_order.index(k['character']))

        environment = [k for k in kanji_data if
                       k['character'] in ['雨', '火', '花', '山', '川', '空', '月', '気', '魚', '金', '木', '水', '土',
                                          '日', '電', '天']]
        people = [k for k in kanji_data if
                  k['character'] in ['人', '子', '女', '男', '父', '母', '友', '手', '足', '耳', '目', '口', '名',
                                     '生']]
        directions = [k for k in kanji_data if
                      k['character'] in ['上', '下', '左', '右', '中', '外', '前', '後', '西', '東', '南', '北']]
        verbs = [k for k in kanji_data if
                 k['character'] in ['飲', '会', '出', '見', '言', '休', '行', '書', '食', '入', '買', '聞', '読', '来',
                                    '立', '話', '学', '分']]
        adjectives = [k for k in kanji_data if
                      k['character'] in ['安', '多', '大', '小', '少', '新', '古', '高', '長', '白', '半']]
        misc = [k for k in kanji_data if k['character'] not in (
                [k['character'] for k in numbers] + [k['character'] for k in environment] +
                [k['character'] for k in people] + [k['character'] for k in directions] +
                [k['character'] for k in verbs] + [k['character'] for k in adjectives]
        )]

        # Context dictionary to pass to the template
        context = {
            'numbers': numbers,
            'environment': environment,
            'people': people,
            'directions': directions,
            'verbs': verbs,
            'adjectives': adjectives,
            'misc': misc,
        }

        return render(request, 'kanji/n5kanji_chart.html', context)

    # Context dictionary to pass to the template
    context = {
        'numbers': numbers,
        'environment': environment,
        'people': people,
        'directions': directions,
        'verbs': verbs,
        'adjectives': adjectives,
        'misc': misc,
    }

    return render(request, 'kanji/n5_kanji.html', context)


def n4(request):
    return render(request, 'level_detail.html', {'level': 'N4'})
def n4_quiz(request):
    return render(request, 'quiz.html', {'level': 'N4'})
def n4_kanji(request):
    return render(request, 'kanji_list.html', {'level': 'N4'})

def n3(request):
    return render(request, 'level_detail.html', {'level': 'N3'})
def n3_quiz(request):
    return render(request, 'quiz.html', {'level': 'N3'})
def n3_kanji(request):
    return render(request, 'kanji_list.html', {'level': 'N3'})

def n2(request):
    return render(request, 'level_detail.html', {'level': 'N2'})
def n2_quiz(request):
    return render(request, 'quiz.html', {'level': 'N2'})
def n2_kanji(request):
    return render(request, 'kanji_list.html', {'level': 'N2'})

def n1(request):
    return render(request, 'level_detail.html', {'level': 'N1'})
def n1_quiz(request):
    return render(request, 'quiz.html', {'level': 'N1'})
def n1_kanji(request):
    return render(request, 'kanji_list.html', {'level': 'N1'})

def about(request):
    return render(request, 'about.html')

def resources(request):
    return render(request, 'resources.html')

def logout_view(request):
    auth_logout(request)
    return redirect('home')  # Redirect to home page after logout

@login_required
def dashboard(request):
    average_progress = 0
    if request.user.is_authenticated:
        user_progress = UserProgress.objects.filter(user=request.user)
        if user_progress.exists():
            total_score = sum(up.quiz_score for up in user_progress if up.quiz_score is not None)
            count = user_progress.count()
            average_progress = total_score / count if count > 0 else 0

    context = {
        'average_progress': average_progress,
    }
    return render(request, 'dashboard.html', context)

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # Password validation
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return render(request, 'registration/register.html')

        if len(password1) < 8:
            messages.error(request, "Password must be at least 8 characters long.")
            return render(request, 'registration/register.html')

        if not re.search(r'\d', password1):
            messages.error(request, "Password must contain at least one number.")
            return render(request, 'registration/register.html')

        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password1):
            messages.error(request, "Password must contain at least one special character (e.g., !@#$%^&*).")
            return render(request, 'registration/register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return render(request, 'registration/register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return render(request, 'registration/register.html')

        # Create the user, but set is_active to False until email is confirmed
        user = User.objects.create_user(username=username, email=email, password=password1, is_active=False)
        user.save()

        # Create a user profile with a confirmation token
        token = default_token_generator.make_token(user)  # Use Django's token generator
        UserProfile.objects.create(user=user, confirmation_token=token)

        # Send confirmation email
        confirmation_url = request.build_absolute_uri(reverse('confirm_email', kwargs={'token': token}))
        subject = 'Confirm Your Email for Nihonow'
        message = f'Hi {username},\n\nPlease confirm your email by clicking the link below:\n{confirmation_url}\n\nThank you for joining Nihonow!'
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )

        # Log out the user to ensure they are not automatically logged in
        auth_logout(request)
        # Set the success message
        messages.success(request, "Registration successful! Please check your email to confirm your account.")
        # Redirect to the login page
        return redirect('login')  # Use namespaced URL to avoid conflicts

    return render(request, 'registration/register.html')

def confirm_email(request, token):
    logger.info(f"Attempting to confirm email with token: {token}")
    try:
        profile = UserProfile.objects.get(confirmation_token=token)
        logger.info(f"Found profile for user: {profile.user.username}")
        if profile.email_confirmed:
            messages.info(request, "Your email is already confirmed.")
        else:
            profile.email_confirmed = True
            profile.confirmation_token = None  # Clear the token
            profile.user.is_active = True
            profile.user.save()
            profile.save()
            messages.success(request, "Email confirmed! You can now log in.")
            # Updated message with a clickable link
            message = (
                'Email confirmed! You will be redirected to the login page in 3 seconds. '
                'If not redirected, <a href="' + reverse('login') + '" class="text-primary">click here to go to the login page</a>.'
            )
            return render(request, 'registration/confirm_email.html', {'message': message})
    except UserProfile.DoesNotExist:
        logger.error(f"Invalid confirmation token: {token}")
        messages.error(request, "Invalid confirmation link.")
    return redirect('login')

def custom_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('dashboard')
        else:
            try:
                user = User.objects.get(Q(username=username) | Q(email=username))
                if hasattr(user, 'profile') and not user.profile.email_confirmed:
                    messages.error(request, "Please confirm your email to log in. Check your inbox for the confirmation link.")
                else:
                    messages.error(request, "Invalid email/username or password.")
            except User.DoesNotExist:
                messages.error(request, "Invalid email/username or password.")
    return render(request, 'registration/login.html')

def resend_confirmation(request):
    if request.method == "POST":
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            profile = user.profile
            if user.is_active:
                messages.info(request, "This account is already verified.")
            else:
                # Check if a confirmation email was sent recently (within 5 minutes)
                if hasattr(profile, 'last_confirmation_sent') and (timezone.now() - profile.last_confirmation_sent).total_seconds() < 300:  # 300 seconds = 5 minutes
                    messages.warning(request, "A verification email was sent recently. Please wait 5 minutes before requesting another.")
                else:
                    # Generate a new token and update the profile
                    token = default_token_generator.make_token(user)
                    profile.confirmation_token = token
                    profile.last_confirmation_sent = timezone.now()  # Track the last sent time
                    profile.save()

                    # Send confirmation email
                    confirmation_url = request.build_absolute_uri(reverse('confirm_email', kwargs={'token': token}))
                    subject = 'Resend Verify Your Nihonow Account'
                    message = f'Hi {user.username},\n\nPlease confirm your email by clicking the link below:\n{confirmation_url}\n\nThank you for using Nihonow!'
                    send_mail(
                        subject,
                        message,
                        settings.EMAIL_HOST_USER,
                        [email],
                        fail_silently=False,
                    )
                    messages.success(request, "A verification link has been sent. Please check your inbox and spam folder. If not received in 5 minutes, resend again.")
        except User.DoesNotExist:
            messages.error(request, "User does not exist in our system.")
        except UserProfile.DoesNotExist:
            messages.error(request, "User profile not found. Please contact support.")
        return render(request, 'registration/resend_confirmation.html')

    return render(request, 'registration/resend_confirmation.html')

class CustomPasswordResetView(PasswordResetView):
    template_name = 'registration/password_reset_form.html'
    email_template_name = 'registration/password_reset_email.html'
    success_url = reverse_lazy('password_reset_done')

    def form_valid(self, form):
        email = form.cleaned_data['email']
        if not User.objects.filter(email=email).exists():
            messages.error(self.request, "This email is not registered with us.")
            return self.render_to_response(self.get_context_data(form=form))
        return super().form_valid(form)

def contact(request):
    submitted = False
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Validate the form data
        if not name or not email or not message:
            messages.error(request, 'Please fill out all fields.')
        else:
            # Prepare the email content
            subject = f'New Contact Form Submission from {name}'
            message_body = f'Name: {name}\nEmail: {email}\n\nMessage:\n{message}'
            from_email = settings.EMAIL_HOST_USER
            recipient_list = ['veerababusaviti2103@gmail.com']  # Your email

            try:
                # Send the email
                send_mail(
                    subject,
                    message_body,
                    from_email,
                    recipient_list,
                    fail_silently=False,
                )
                submitted = True  # Set submitted to True for confirmation
            except Exception as e:
                messages.error(request, f'Failed to send message. Error: {str(e)}')

    return render(request, 'contact.html', {'submitted': submitted})

def quiz(request, level):
    if not request.user.is_authenticated:
        return redirect('login')

    questions = QuizQuestion.objects.filter(level=level)
    if not questions:
        return render(request, 'quiz.html', {'level': level, 'error': 'No questions available for this level.'})

    if request.method == 'POST':
        score = 0
        total = questions.count()
        for question in questions:
            selected = request.POST.get(f'question_{question.id}')
            if selected == question.correct_answer:
                score += 1

        percentage = (score / total) * 100
        progress, created = UserProgress.objects.get_or_create(user=request.user, level=level)
        progress.quiz_score = percentage
        progress.save()

        return render(request, 'quiz.html', {'level': level, 'submitted': True, 'score': percentage})

    # Prepare questions with shuffled options
    questions_with_options = []
    for question in questions:
        options = [question.wrong_answer1, question.wrong_answer2, question.wrong_answer3, question.correct_answer]
        random.shuffle(options)  # Shuffle the options
        questions_with_options.append({
            'question': question,
            'options': options,
        })

    return render(request, 'quiz.html', {'level': level, 'questions_with_options': questions_with_options})

@login_required
def admin_bulk_upload(request):
    if not request.user.is_superuser:
        messages.error(request, "Only admins can access this page.")
        return redirect('home')

    if request.method == "POST":
        # Handle DailyWord upload
        if 'dailyword_csv' in request.FILES:
            csv_file = request.FILES['dailyword_csv']
            if not csv_file.name.endswith('.csv'):
                messages.error(request, "Please upload a CSV file for Daily Words.")
                return redirect('admin_bulk_upload')

            decoded_file = csv_file.read().decode("utf-8").splitlines()
            reader = csv.DictReader(decoded_file)
            required_headers = {"word", "reading", "english_meaning"}
            has_date = "date" in reader.fieldnames
            if not required_headers.issubset(reader.fieldnames):
                messages.error(request, "DailyWord CSV must have headers: word, reading, english_meaning (date optional)")
                return redirect('admin_bulk_upload')

            current_date = timezone.now().date()
            for i, row in enumerate(reader):
                try:
                    date = datetime.strptime(row["date"], "%Y-%m-%d").date() if has_date else current_date + timedelta(days=i)
                    DailyWord.objects.update_or_create(
                        date=date,
                        defaults={
                            "word": row["word"],
                            "reading": row["reading"],
                            "english_meaning": row["english_meaning"],
                        }
                    )
                except Exception as e:
                    messages.error(request, f"DailyWord row {i+1}: {str(e)}")
            messages.success(request, "Daily Words uploaded successfully!")

        # Handle Kanji upload
        elif 'kanji_csv' in request.FILES:
            csv_file = request.FILES['kanji_csv']
            if not csv_file.name.endswith('.csv'):
                messages.error(request, "Please upload a CSV file for Kanji.")
                return redirect('admin_bulk_upload')

            decoded_file = csv_file.read().decode("utf-8").splitlines()
            reader = csv.DictReader(decoded_file)
            required_headers = {"character", "level", "on_reading", "kun_reading", "meaning", "stroke_count"}
            if not required_headers.issubset(reader.fieldnames):
                messages.error(request, "Kanji CSV must have headers: character, level, on_reading, kun_reading, meaning, stroke_count")
                return redirect('admin_bulk_upload')

            for i, row in enumerate(reader):
                try:
                    Kanji.objects.update_or_create(
                        character=row["character"],
                        level=row["level"],
                        defaults={
                            "on_reading": row["on_reading"],
                            "kun_reading": row["kun_reading"],
                            "meaning": row["meaning"],
                            "stroke_count": int(row["stroke_count"]),
                        }
                    )
                except Exception as e:
                    messages.error(request, f"Kanji row {i+1}: {str(e)}")
            messages.success(request, "Kanji uploaded successfully!")

        # Handle QuizQuestion upload
        elif 'quiz_csv' in request.FILES:
            csv_file = request.FILES['quiz_csv']
            if not csv_file.name.endswith('.csv'):
                messages.error(request, "Please upload a CSV file for Quiz Questions.")
                return redirect('admin_bulk_upload')

            decoded_file = csv_file.read().decode("utf-8").splitlines()
            reader = csv.DictReader(decoded_file)
            required_headers = {"level", "question", "wrong_answer1", "wrong_answer2", "wrong_answer3", "correct_answer"}
            if not required_headers.issubset(reader.fieldnames):
                messages.error(request, "Quiz CSV must have headers: level, question, wrong_answer1, wrong_answer2, wrong_answer3, correct_answer")
                return redirect('admin_bulk_upload')

            for i, row in enumerate(reader):
                try:
                    QuizQuestion.objects.update_or_create(
                        level=row["level"],
                        question=row["question"],
                        defaults={
                            "wrong_answer1": row["wrong_answer1"],
                            "wrong_answer2": row["wrong_answer2"],
                            "wrong_answer3": row["wrong_answer3"],
                            "correct_answer": row["correct_answer"],
                        }
                    )
                except Exception as e:
                    messages.error(request, f"Quiz row {i+1}: {str(e)}")
            messages.success(request, "Quiz Questions uploaded successfully!")

        return redirect('admin_bulk_upload')

    return render(request, 'admin_bulk_upload.html')