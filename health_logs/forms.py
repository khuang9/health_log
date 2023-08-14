from django import forms
from .models import Topic, Entry, LogTopic, LogEntry, GoalTopic, GoalEntry, WorkoutTopic, WorkoutEntry

# Create your models here.

class TopicForm(forms.ModelForm):
  
  class Meta:
    model = Topic
    fields = ['text']
    labels = {'text' : ''}
    

class EntryForm(forms.ModelForm):
  
  class Meta:
    model = Entry
    fields = ['section', 'text']
    labels = {'text' : 'Info', 'section' : '11'}
    widgets = {'section' : forms.Textarea(attrs={'cols' : 100, 'rows' : 1}), 'text' : forms.Textarea(attrs={'cols' : 10, 'rows' : 1})}
    

  
class LogTopicForm(forms.ModelForm):
  
  class Meta:
    model = LogTopic
    fields = ['text']
    labels = {'text' : ''}
    

class LogEntryForm(forms.ModelForm):
  
  class Meta:
    model = LogEntry
    fields = ['section', 'text']
    labels = {'text' : 'Info', 'section' : '11'}
    widgets = {'section' : forms.Textarea(attrs={'cols' : 100, 'rows' : 1}), 'text' : forms.Textarea(attrs={'cols' : 100})}
    
    
    
class GoalTopicForm(forms.ModelForm):
  
  class Meta:
    model = GoalTopic
    fields = ['text']
    labels = {'text' : ''}
    

class GoalEntryForm(forms.ModelForm):
  
  class Meta:
    model = GoalEntry
    fields = ['section', 'text']
    labels = {'text' : 'Info', 'section' : '11'}
    widgets = {'section' : forms.Textarea(attrs={'cols' : 100, 'rows' : 1}), 'text' : forms.Textarea(attrs={'cols' : 100})}
    
    
    
class WorkoutTopicForm(forms.ModelForm):
  
  class Meta:
    model = WorkoutTopic
    fields = ['text']
    labels = {'text' : ''}
    

class WorkoutEntryForm(forms.ModelForm):
  
  class Meta:
    model = WorkoutEntry
    fields = ['exercise', 'duration', 'sets', 'rest']
    labels = {'exercise' : '', 'duration' : '', 'sets' : '', 'rest' : ''}
    widgets = {'exercise' : forms.Textarea(attrs={'cols' : 100, 'rows' : 1}), 'duration' : forms.Textarea(attrs={'cols' : 10, 'rows' : 1}), 'sets' : forms.Textarea(attrs={'cols' : 10, 'rows' : 1}), 'rest' : forms.Textarea(attrs={'cols' : 10, 'rows' : 1})}