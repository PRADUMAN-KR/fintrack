# from django.contrib.auth.backends import ModelBackend
# from .models import custom_user  # Make sure to import your custom user model

# class EmailBackend(ModelBackend):
#     def authenticate(self, request, email=None, password=None, **kwargs):
#         try:
#             user = custom_user.objects.get(email=email)
#             if user.check_password(password):
#                 return user
#         except custom_user.DoesNotExist:
#             return None
