from agile.models import *
from django import forms

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ('owner', 'is_active',)
        
class StoryForm(forms.ModelForm):
    
    def __init__(self, project=None, *args, **kwargs):
        super(StoryForm, self).__init__(*args, **kwargs)
        if project:
            users = project.users
            self.fields['creator'].queryset = users
            self.fields['owner'].queryset = users
            self.fields['phase'].queryset = project.phases
        
    class Meta:
        model = Story
        exclude = ('index', 'number', 'blocked', 'color',)
        
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