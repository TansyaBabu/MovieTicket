from django.contrib.auth.decorators import user_passes_test

def is_theatre_owner(user):
    return user.is_authenticated and user.role == 'theatre_owner'


