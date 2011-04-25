from agile.models import *
from django import forms

class ProjectForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        label_from_instance = lambda obj: obj.agile_get_name()
        self.fields['members'].label_from_instance = label_from_instance
    
    class Meta:
        model = Project
        exclude = ('owner', 'is_active',)
        
class PhaseForm(forms.ModelForm):
    class Meta:
        model = Phase
        exclude = ('project', 'is_backlog', 'is_archive', 'index')
        
class StoryForm(forms.ModelForm):
    
    def __init__(self, project=None, *args, **kwargs):
        super(StoryForm, self).__init__(*args, **kwargs)
        if project:
            users = project.users
            self.fields['creator'].queryset = users
            self.fields['owner'].queryset = users
            self.fields['phase'].queryset = project.phases
        
        label_from_instance = lambda obj: obj.agile_get_name()
        self.fields['creator'].label_from_instance = label_from_instance
        self.fields['owner'].label_from_instance = label_from_instance
        
    class Meta:
        model = Story
        exclude = ('index', 'number', 'blocked', 'color', 'ready')
        
class TaskForm(forms.ModelForm):
    
    def __init__(self, project=None, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        if project:
            self.fields['finished_by'].queryset = project.users
            self.fields['story'].queryset = project.stories
    
    class Meta:
        model = Task
        
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ('user', 'story',)
        
class FilterForm(forms.ModelForm):
    class Meta:
        model = Filter
        
class UserDataForm(forms.ModelForm):
    class Meta:
        model = User
        exclude = ('username', 'password', 'is_staff',
                   'is_active', 'is_superuser', 'last_login',
                   'date_joined', 'groups', 'user_permissions')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user',)