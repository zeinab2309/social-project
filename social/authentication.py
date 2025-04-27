from social.models import User

class PhoneAuthBackend():
    def authenticate(self,request, username=None , password=None):
        try:
            user=User.objects.get(phone=username)
            if user.check_password(password):
                return user
            return None
        except(User.DoesNotExit,user.MultipleObjectsReturned):
            return None
    def get_user(self,user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExit:
            return None
