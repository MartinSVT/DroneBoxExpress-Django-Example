from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from DroneBoxExpressApp.UserAccount.models import DroneBoxProfile

UserModel = get_user_model()


class DroneBoxUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs["class"] = "test_class"
        self.fields["email"].widget.attrs["class"] = "test_class"
        self.fields["password1"].widget.attrs["class"] = "test_class"
        self.fields["password2"].widget.attrs["class"] = "test_class"

    class Meta(UserCreationForm.Meta):
        model = UserModel
        fields = ('username', 'email')
        labels = {
            "username": "Username:"
        }


class DroneBoxLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs["class"] = "test_class"
        self.fields["password"].widget.attrs["class"] = "test_class"


class DroneBoxProfileEditForm(forms.ModelForm):
    class Meta:
        model = DroneBoxProfile
        fields = ["first_name", "last_name", "date_of_birth", "profile_picture"]
        widgets = {
            "profile_picture": forms.ClearableFileInput()
        }
