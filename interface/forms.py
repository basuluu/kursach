from django import forms
from .models import product_card, journal_request, journal_supplier, income
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, get_user_model, login, logout

class ItemForm(forms.ModelForm):
    class Meta:
        model = product_card
        fields = '__all__'

class SupForm(forms.ModelForm):
    class Meta:
        model = journal_supplier
        fields = '__all__'

class ReqForm(forms.ModelForm):
    class Meta:
        model = journal_request
        fields = '__all__'

class IncomeForm(forms.ModelForm):
    class Meta:
        model = income
        fields = '__all__'

class JRForm(forms.ModelForm):
    class Meta:
        model = journal_request
        fields = ('name', 'phone', 'address',)

class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        if username and password:
            if not user:
                raise forms.ValiedationError("This user does not exist")
            if not user.check_password(password):
                raise forms.ValiedationError("Incorrect password")
            if not user.is_active:
                raise forms.ValiedationError("This user is not longer active")
        return super(UserLoginForm, self).clean()

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
        ]
