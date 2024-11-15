# admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.conf import settings
import random
import string
from .models import User

token_generator = PasswordResetTokenGenerator()

def generate_random_password(length=10):
    characters = string.ascii_letters + string.digits + "!@#$%^&*()"
    return ''.join(random.choice(characters) for _ in range(length))

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_student', 'is_teacher', 'is_admin')
    list_filter = ('is_student', 'is_teacher', 'is_admin')
  
    add_fieldsets = (
        (None, {
            'fields': ('username', 'email', 'password1', 'password2', 'is_student', 'is_teacher', 'is_admin'),
        }),
    )

    def save_model(self, request, obj, form,change): 
        if not change and obj.is_teacher:
            random_password = generate_random_password()
            obj.set_password(random_password)
            super().save_model(request, obj, form, change)
            
            
            uid = urlsafe_base64_encode(force_bytes(obj.pk))
            token = token_generator.make_token(obj)
            password_reset_link = request.build_absolute_uri(
                reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
            )
            
            
            
            send_mail(
                'Your Teacher Account Has Been Created',
                f'Hello {obj.first_name},\n\n'
                f'Your teacher account has been created.\n'
                f'Username: {obj.username}\n'
                f'Temporary Password: {random_password}\n\n'
                f'To set your password, click the link below:\n'
                f'{password_reset_link}\n\n'
                f'Best regards,\nAdmin Team',
                settings.DEFAULT_FROM_EMAIL,
                [obj.email],
                fail_silently=False,
            )
        else:
            super().save_model(request, obj, form, change)

admin.site.register(User, CustomUserAdmin)


