from django.test import override_settings

common_settings = override_settings(
    PASSWORD_HASHERS=[
        'django.contrib.auth.hashers.MD5PasswordHasher',
    ],
)