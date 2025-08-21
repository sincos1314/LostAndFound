from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from accounts.models import Profile

class MultiIdentifierBackend(BaseBackend):
    def authenticate(self, request, identifier=None, password=None, method=None, **kwargs):
        user = None
        if method == 'username':
            try:
                user = User.objects.get(username=identifier)
            except User.DoesNotExist:
                return None
        elif method == 'student_id':
            try:
                profile = Profile.objects.get(student_id=identifier)
                user = profile.user
            except Profile.DoesNotExist:
                return None
        elif method == 'email':
            try:
                user = User.objects.get(email=identifier)
            except User.DoesNotExist:
                return None
        elif method == 'phone':
            try:
                profile = Profile.objects.get(phone=identifier)
                user = profile.user
            except Profile.DoesNotExist:
                return None
        else:
            return None

        if user and user.check_password(password):
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None