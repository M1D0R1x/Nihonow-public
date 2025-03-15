from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import UserProgress, QuizQuestion, DailyWord, UserProfile, Kanji, DailyKanji

# Inline to show UserProfile details
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'

# Customize UserAdmin to include UserProfile
class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'is_active', 'date_joined', 'get_email_confirmed')
    list_filter = ('is_active', 'date_joined')

    def get_email_confirmed(self, obj):
        return obj.profile.email_confirmed if hasattr(obj, 'profile') else False

    get_email_confirmed.short_description = 'Email Confirmed'
    get_email_confirmed.admin_order_field = 'profile__email_confirmed'

# Register QuizQuestion model
@admin.register(QuizQuestion)
class QuizQuestionAdmin(admin.ModelAdmin):
    list_display = ('level', 'question', 'correct_answer')
    list_filter = ('level',)
    search_fields = ('question', 'correct_answer')
    list_per_page = 25

# Register Kanji model
@admin.register(Kanji)
class KanjiAdmin(admin.ModelAdmin):
    list_display = ('character', 'level', 'on_reading', 'kun_reading', 'stroke_count')
    list_filter = ('level',)
    search_fields = ('character', 'on_reading', 'kun_reading', 'meaning')
    list_per_page = 25

# Register UserProgress model
@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'level', 'lessons_completed', 'total_lessons', 'quiz_score', 'updated_at', 'progress_percentage')
    list_filter = ('level', 'updated_at')
    search_fields = ('user__username',)
    list_per_page = 25

    def progress_percentage(self, obj):
        return (obj.lessons_completed / obj.total_lessons) * 100 if obj.total_lessons > 0 else 0

    progress_percentage.short_description = 'Progress (%)'

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_upload_button'] = True
        return super().change_view(request, object_id, form_url, extra_context=extra_context)

    def add_view(self, request, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_upload_button'] = True
        return super().add_view(request, form_url, extra_context=extra_context)

# Register DailyWord model
@admin.register(DailyWord)
class DailyWordAdmin(admin.ModelAdmin):
    list_display = ('date', 'word', 'reading', 'english_meaning')
    list_filter = ('date',)
    search_fields = ('word', 'reading', 'english_meaning')
    list_per_page = 25

# Register DailyKanji model
@admin.register(DailyKanji)
class DailyKanjiAdmin(admin.ModelAdmin):
    list_display = ('date', 'kanji', 'example_sentence', 'example_translation')
    list_filter = ('date',)
    search_fields = ('kanji__character', 'example_sentence', 'example_translation')
    list_per_page = 25

# Register UserProfile model
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'email_confirmed', 'confirmation_token')
    list_filter = ('email_confirmed',)
    search_fields = ('user__username',)

# Unregister the default UserAdmin and register the custom one
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)