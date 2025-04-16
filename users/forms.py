from allauth.account.forms import SignupForm, LoginForm, ResetPasswordForm, ChangePasswordForm
from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, required=True,
                                 widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'})
                                 )
    last_name = forms.CharField(max_length=30, required=True,
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'})
                                )
    phone_number = forms.CharField(max_length=20, required=False,
                                   widget=forms.TextInput(
                                       attrs={'class': 'form-control', 'placeholder': 'Phone Number'})
                                   )
    address = forms.CharField(required=False, widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Address',
        'rows': 3
    })
                              )
    profile_image = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'form-control'}))

    def save(self, request):
        user = super().save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.phone_number = self.cleaned_data.get('phone_number')
        user.address = self.cleaned_data.get('address')
        if 'profile_image' in self.cleaned_data:
            user.profile_image = self.cleaned_data['profile_image']
        user.save()
        return user


class CustomLoginForm(LoginForm):
    login = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email or Username'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password'
        })
    )
    remember = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )


class CustomResetPasswordForm(ResetPasswordForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your Email'
        })
    )


class CustomChangePasswordForm(ChangePasswordForm):
    oldpassword = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Current Password'
        })
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'New Password'
        })
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'New Password (again)'
        })
    )
