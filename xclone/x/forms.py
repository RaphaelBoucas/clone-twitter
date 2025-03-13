from django import forms
from .models import Tweet, CustomUser
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
# from django.contrib.auth.models import User
# from django.contrib.auth.models import AbstractUser

class TweetForm(forms.ModelForm):
    body = forms.CharField(required=True, widget=forms.widgets.Textarea(
        attrs={
            "placeholder" : "Enter your message...",
            "class":"form-control",
            }
        ),
        label="",
    
    )
    class Meta:
        model = Tweet
        exclude = ("user", "likes")


class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="E-mail", 
                             widget=forms.TextInput(
        attrs={
            'class':'form-control mt-2',
            'placeholder':'E-mail address'
        }
    ))

    first_name = forms.CharField(label="First name", 
                                 max_length= 100,
                                 widget=forms.TextInput(
        attrs={
            'class':'form-control mt-2',
            'placeholder':'First name'
        }
    ))    

    last_name = forms.CharField(label="Last name", 
                                 max_length= 100,
                                 widget=forms.TextInput(
        attrs={
            'class':'form-control mt-2',
            'placeholder':'Last name'
        }
    ))

    profile_image = forms.ImageField(label="Profile picture", 
                             widget=forms.ClearableFileInput(
        attrs={
            'class':'form-control mt-2 ',
            
        }
    )
    )

    profile_bio = forms.CharField(label="Profile bio", 
                                 max_length= 500,
                                 widget=forms.Textarea(
        attrs={
            'class':'form-control mt-2',
            
        }
    ))
    homepage_link = forms.CharField(label="Homepage", 
                                 max_length= 150,
                                 widget=forms.TextInput(
        attrs={
            'class':'form-control mt-2',
            
        }
    ))
    facebook_link = forms.CharField(label="Facebook", 
                                 max_length= 150,
                                 widget=forms.TextInput(
        attrs={
            'class':'form-control mt-2',
            
        }
    ))
    instagram_link = forms.CharField(label="Instagram", 
                                 max_length= 150,
                                 widget=forms.TextInput(
        attrs={
            'class':'form-control mt-2',
            
        }
    ))
    linkedin_link = forms.CharField(label="Linkedin", 
                                 max_length= 150,
                                 widget=forms.TextInput(
        attrs={
            'class':'form-control mt-2',
            
        }
    ))


    class Meta:
        model = CustomUser
        fields = ( 'username', 
                  'first_name',
                  'last_name',
                  'email', 
                  'password1', 
                  'password2', 
                  'profile_image', 
                  'profile_bio',
                  'homepage_link',
                  'facebook_link',
                  'instagram_link',
                  'linkedin_link',
                  )

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control mt-2'
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['username'].label = 'Username'
        self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

        self.fields['password1'].widget.attrs['class'] = 'form-control mt-2'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = 'Password'
        self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

        self.fields['password2'].widget.attrs['class'] = 'form-control mt-2'
        self.fields['password2'].widget.attrs['placeholder'] = 'Repeat password'
        self.fields['password2'].label = 'Repeat password'
        self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if CustomUser.objects.exclude(pk=self.instance.pk).filter(username=username).exists():
            raise forms.ValidationError("A user with that username already exists.")
        return username
    


# class UpdateUserForm(UserChangeForm):
#     password = forms.CharField(widget=forms.HiddenInput(), required=False)

#     email = forms.EmailField(label="", 
#                              widget=forms.TextInput(
#         attrs={
#             'class':'form-control',
#             'placeholder':'E-mail address'
#         }
#     ))

#     first_name = forms.CharField(label="", 
#                                  max_length= 100,
#                                  widget=forms.TextInput(
#         attrs={
#             'class':'form-control',
#             'placeholder':'Fisrt name'
#         }
#     ))    

#     last_name = forms.CharField(label="", 
#                                  max_length= 100,
#                                  widget=forms.TextInput(
#         attrs={
#             'class':'form-control',
#             'placeholder':'Fisrt name'
#         }
#     ))

#     profile_image = forms.ImageField(label="Profile picture",
#                                      required=False, 
#                              widget=forms.ClearableFileInput(
#         attrs={
#             'class':'form-control',
            
#         }
#     )
#     )

#     class Meta:
#         model = CustomUser
#         fields = ( 'username', 'first_name','last_name','email', 'profile_image',)

#     def __init__(self, *args, **kwargs):
#         super(UserChangeForm, self).__init__(*args, **kwargs)

#         self.fields['username'].widget.attrs['class'] = 'form-control'
#         self.fields['username'].widget.attrs['placeholder'] = 'Username'
#         self.fields['username'].label = ''
#         self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

#         # self.fields['password1'].widget.attrs['class'] = 'form-control'
#         # self.fields['password1'].widget.attrs['placeholder'] = 'Password'
#         # self.fields['password1'].label = ''
#         # self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

#         # self.fields['password2'].widget.attrs['class'] = 'form-control'
#         # self.fields['password2'].widget.attrs['placeholder'] = 'Repeat password'
#         # self.fields['password2'].label = ''
#         # self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'

#     def clean_username(self):
#         username = self.cleaned_data.get('username')
#         if CustomUser.objects.exclude(pk=self.instance.pk).filter(username=username).exists():
#             raise forms.ValidationError("A user with that username already exists.")
#         return username


