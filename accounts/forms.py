from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User

class UserCustomChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name',]
        