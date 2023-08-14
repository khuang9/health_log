from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Topic(models.Model):
  text = models.CharField(max_length = 200)
  date_added = models.DateTimeField(auto_now_add = True)
  owner = models.ForeignKey(User, on_delete=models.CASCADE)
  
  def __str__(self):
    """ Return a string representation of the model. """
    return self.text
  
class LogTopic(models.Model):
  text = models.CharField(max_length = 200)
  date_added = models.DateTimeField(auto_now_add = True)
  owner = models.ForeignKey(User, on_delete=models.CASCADE)
  
  def __str__(self):
    """ Return a string representation of the model. """
    return self.text
  
class GoalTopic(models.Model):
  text = models.CharField(max_length = 200)
  date_added = models.DateTimeField(auto_now_add = True)
  owner = models.ForeignKey(User, on_delete=models.CASCADE)
  
  def __str__(self):
    """ Return a string representation of the model. """
    return self.text
  
class WorkoutTopic(models.Model):
  text = models.CharField(max_length = 200)
  times_completed = models.PositiveIntegerField(default=0)
  completion_timestamps = models.JSONField(default=list)
  
  date_added = models.DateTimeField(auto_now_add = True)
  owner = models.ForeignKey(User, on_delete=models.CASCADE)
  
  def __str__(self):
    """ Return a string representation of the model. """
    return self.text
  

class Entry(models.Model):
  topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
  section = models.TextField()
  text = models.IntegerField()
  gpt = models.TextField()
  date_added = models.DateTimeField(auto_now_add = True)
  
  class Meta:
    verbose_name_plural = 'entries'
    
  def __str__(self):
    return f"{self.text[:50]}..."
  
class LogEntry(models.Model):
  topic = models.ForeignKey(LogTopic, on_delete=models.CASCADE)
  section = models.TextField()
  text = models.TextField()
  gpt = models.TextField()
  date_added = models.DateTimeField(auto_now_add = True)
  
  class Meta:
    verbose_name_plural = 'entries'
    
  def __str__(self):
    return f"{self.text[:50]}..."
  
class GoalEntry(models.Model):
  topic = models.ForeignKey(GoalTopic, on_delete=models.CASCADE)
  section = models.TextField()
  text = models.TextField()
  gpt = models.TextField()
  date_added = models.DateTimeField(auto_now_add = True)
  
  class Meta:
    verbose_name_plural = 'entries'
    
  def __str__(self):
    return f"{self.text[:50]}..."
  
class WorkoutEntry(models.Model):
  topic = models.ForeignKey(WorkoutTopic, on_delete=models.CASCADE)
  exercise = models.TextField()
  duration = models.IntegerField()
  sets = models.IntegerField()
  rest = models.IntegerField()
  gpt = models.TextField()
  date_added = models.DateTimeField(auto_now_add = True)
  
  class Meta:
    verbose_name_plural = 'entries'
    
  def __str__(self):
    return f"{self.text[:50]}..."
  
