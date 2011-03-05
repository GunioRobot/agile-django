from agile.models import *
from django import forms

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ('owner',)
        
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
