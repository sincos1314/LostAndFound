from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from accounts.models import Profile, GENDER_CHOICES

class RegisterForm(forms.Form):
    student_id = forms.CharField(label='学号', max_length=32)
    username = forms.CharField(label='用户名', max_length=150)
    college = forms.CharField(label='学院', max_length=64)
    class_name = forms.CharField(label='班级', max_length=64)
    gender = forms.ChoiceField(label='性别', choices=GENDER_CHOICES)
    email = forms.EmailField(label='邮箱(可选)', required=False)
    phone = forms.CharField(label='手机号(可选)', max_length=20, required=False)
    password = forms.CharField(label='密码', widget=forms.PasswordInput)
    password2 = forms.CharField(label='确认密码', widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('该用户名已存在')
        return username

    def clean_student_id(self):
        sid = self.cleaned_data['student_id']
        if Profile.objects.filter(student_id=sid).exists():
            raise forms.ValidationError('该学号已注册')
        return sid

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError('该邮箱已绑定其他账户')
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get('phone') or None
        if phone and Profile.objects.filter(phone=phone).exists():
            raise forms.ValidationError('该手机号已绑定其他账户')
        return phone

    def clean(self):
        cleaned = super().clean()
        pwd = cleaned.get('password')
        pwd2 = cleaned.get('password2')
        if pwd and pwd2 and pwd != pwd2:
            self.add_error('password2', '两次密码不一致')
        if pwd:
            validate_password(pwd)
        return cleaned

class EditProfileForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=150)
    gender = forms.ChoiceField(label='性别', choices=GENDER_CHOICES)
    email = forms.EmailField(label='邮箱(可选)', required=False)
    phone = forms.CharField(label='手机号(可选)', max_length=20, required=False)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exclude(pk=self.user.pk).exists():
            raise forms.ValidationError('该用户名已存在')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exclude(pk=self.user.pk).exists():
            raise forms.ValidationError('该邮箱已被其他账户绑定')
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get('phone') or None
        if phone and Profile.objects.filter(phone=phone).exclude(user=self.user).exists():
            raise forms.ValidationError('该手机号已被其他账户绑定')
        return phone