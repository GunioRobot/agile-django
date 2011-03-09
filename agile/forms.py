from agile.models import *
from django import forms

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ('owner', 'is_active',)
        
class StoryForm(forms.ModelForm):
    class Meta:
        model = Story
        
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        
class FilterForm(forms.ModelForm):
    class Meta:
        model = Filter
        
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        exclude = ('username', 'password', 'is_staff',
                   'is_active', 'is_superuser', 'last_login',
                   'date_joined', 'groups', 'user_permissions')