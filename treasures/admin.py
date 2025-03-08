from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import UserProgress, QuizQuestion, DailyWord, UserProfile

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

# Unregister the default UserAdmin and register the custom one
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(UserProgress)
admin.site.register(QuizQuestion)
admin.site.register(DailyWord)
admin.site.register(UserProfile)