from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required
from django.http import Http404

from .models import Topic, Entry, LogTopic, LogEntry, GoalTopic, GoalEntry, WorkoutTopic, WorkoutEntry
from .forms import TopicForm, EntryForm, LogTopicForm, LogEntryForm, GoalTopicForm, GoalEntryForm, WorkoutTopicForm, WorkoutEntryForm

from . import ai_improver

from datetime import datetime
from . import trend_calculator
from . import date_calculator

from .ai_advisor import ai_answer

from fpdf import FPDF

TEMPLATE_FILE = '123.txt'
RESULT_FILE = 'resume.pdf'

ai_suggested_text = ""
ai_suggested_texts = [""]

workout_topic_id = 1

from django.db import models
import openai

# Replace 'YOUR_API_KEY' with your actual API key or token
api_key = "fake_key"
openai.api_key = api_key


# def generate_text(section, text):
    
#     """
#     response = openai.Completion.create(
#         engine="text-davinci-002",  # Use the GPT-3.5 engine
#         prompt=prompt,
#         max_tokens=150,  # Control the length of the generated text
#         temperature=0.7  # Controls the randomness of the generated text
#     )
#     result_text = response.choices[0].text.strip()
#     """
    
#     result_text = "Software Engineer with 5+ years of experience developing web applications. Strong understanding of various programming languages and frameworks. Detail-oriented problem solver with excellent communication skills.\n\nExperience\n\nWeb Application Developer, ABC Company, Jan 2010 – Present\n\nDeveloped various web applications using PHP, Ruby on Rails, and JavaScript.\n\nOptimized applications for performance and scalability.\n\nFixed bugs and resolved issues in a timely manner.\n\nProvided support and maintenance for existing applications.\n\nSoftware Engineer, XYZ Company, Nov 2007 – Dec 2009\n\nDeveloped various web applications using ASP.NET and C#.\n\nInvolved in the full software development life cycle, from requirements gathering to testing and deployment."

#     if False:
#       if section == 'SUMMARY':
#         result_text = ai_improver.summary_corrector(text)
#       elif section == 'EDUCATION':
#         result_text = ai_improver.single_experience_corrector(text)
#       elif section == 'TEST SCORES':
#         result_text = ai_improver.single_experience_corrector(text)
#       elif section == 'COURSES':
#         result_text = ai_improver.single_experience_corrector(text)
#       elif section == 'EXTRACURRICULARS':
#         result_text = ai_improver.single_experience_corrector(text)
#       elif section == 'VOLUNTEERING':
#         result_text = ai_improver.single_experience_corrector(text)
#       else:
#         result_text = "Invalid section name!"
    
#     return section# + "\n" + result_text


# # Example prompt for generating a resume
# resume_prompt = """
# You are a highly skilled software engineer with a passion for technology. You have experience in developing web applications and a deep understanding of various programming languages and frameworks. You are detail-oriented, a problem solver, and have excellent communication skills. Please write a resume that highlights your skills, experience, and achievements.
# """


# Create your views here.
def index(request):
  return render(request, 'health_logs/index.html')

@login_required
def topics(request):
  topics = Topic.objects.filter(owner=request.user).order_by('date_added')
  context = {'topics' : topics}
  return render(request, 'health_logs/topics.html', context)
  
    
    

def get_metric_data(topic_id):
    topic = Topic.objects.get(id=topic_id)
    entries = topic.entry_set.order_by('date_added')
    
    days = []
    stats = []
    
    for entry in entries:
      days.append(entry.date_added)
      stats.append(int(entry.text))
      
    return days, stats
    
    
def functionize(xs, ys):
  if xs == []:
    return [], []
  
  new_xs = []
  new_ys = []
  
  start_index = 0
  
  for end_index in range(len(xs)):
    if xs[end_index] != xs[start_index]:
      new_xs.append(xs[start_index])
      new_ys.append(sum(ys[start_index:end_index]) / (end_index - start_index))
      start_index = end_index
      
  end_index = len(xs)
  
  new_xs.append(xs[start_index])
  new_ys.append(sum(ys[start_index:]) / (end_index - start_index))
      
  return new_xs, new_ys
    
def extrapolate(xs, ys):
  new_xs = []
  new_ys = []
  
  for i in range(len(xs)):
    new_xs.append(xs[i])
    new_ys.append(ys[i])
    
    try:
      if xs[i+1] - xs[i] > 1:
        daily_change = (ys[i+1] - ys[i]) / (xs[i+1] - xs[i])
        
        for day in range(xs[i] + 1, xs[i+1]):
          new_xs.append(day)
          new_ys.append(new_ys[-1] + daily_change)
          
    except IndexError:
      pass
        
  return new_xs, new_ys

def count_workouts(workout_days):
  new_workout_days = [workout_days[0]]
  counter = [0]*(max(workout_days) + 1)
  
  for i in range(len(workout_days)):
    counter[workout_days[i]] += 1
    
    try:
      if workout_days[i+1] != workout_days[i]:
        new_workout_days.append(workout_days[i+1])
    
    except IndexError:
      pass
    
  return counter, new_workout_days
    
  
@login_required
def topic(request, topic_id, wrkt_topic_id):
    """Show a single topic and all its entries."""
    global workout_topic_id
    
    if wrkt_topic_id != 0:
      workout_topic_id = wrkt_topic_id
    

    topic = Topic.objects.get(id=topic_id)
    
    if topic.owner != request.user:
      raise Http404
      
    days, stats = get_metric_data(topic_id)
    
    entries_found = True
    
    try:
      first_day = days[0]
    except IndexError:
      entries_found = False
    
    trend, slope, y_int, xs, ys = trend_calculator.calculate_trend(stats, days)
    trend = f"Your daily values for '{topic}' are currently {trend}"
    
    xs, ys = functionize(xs, ys)
    xs, ys = extrapolate(xs, ys)
    
    for i in range(len(xs)):
      xs[i] = str(xs[i])
      ys[i] = str(ys[i])
      
    xs = ' '.join(xs)
    ys = ' '.join(ys)
        
    if not entries_found:
      entries = topic.entry_set.order_by('-date_added')
      context = {'workout_topic_id' : workout_topic_id, 'topic': topic, 'entries': entries, 'trend' : trend, 'slope' : slope, 'y_int' : y_int, 'xs' : xs, 'ys' : ys}
      return render(request, 'health_logs/topic.html', context)
        
    workout_topic = WorkoutTopic.objects.get(id=workout_topic_id)
    
    if workout_topic.owner != request.user:
      raise Http404
      
    workout_days = []
    for day in workout_topic.completion_timestamps:
      workout_days.append(day)
      
    
    for i in range(len(workout_days)):
      workout_days[i] = date_calculator.days_since(trend_calculator.format_day(first_day), workout_days[i][:4] + workout_days[i][5:7] + workout_days[i][8:10])
      
    workouts_per_day, workout_days = count_workouts(workout_days)
    
    for i in range(len(xs)):
      workout_days[i] = str(workout_days[i])
      workouts_per_day[i] = str(workouts_per_day[i])
      
    workout_days = ' '.join(workout_days)
    workouts_per_day = ' '.join(workouts_per_day)
      


    entries = topic.entry_set.order_by('-date_added')
    context = {'workout_topic_id' : workout_topic_id, 'topic': topic, 'entries': entries, 'trend' : trend, 'slope' : slope, 'y_int' : y_int, 'xs' : xs, 'ys' : ys, 'workout_days' : workout_days, 'workouts_per_day' : workouts_per_day, 'ai_suggested_texts' : ai_suggested_texts}
    return render(request, 'health_logs/topic.html', context)
  
@login_required
def link_workouts(request, topic_id):
  topics = WorkoutTopic.objects.filter(owner=request.user).order_by('-times_completed')
  context = {'topics' : topics, 'topic_id' : topic_id}#############changed

  return render(request, 'health_logs/link_workouts.html', context)
  
@login_required
def new_topic(request):
    """Add a new topic."""
    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = TopicForm()
    else:
        # POST data submitted; process data.
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect('health_logs:topics')

    # Display a blank or invalid form.
    context = {'form': form}
    return render(request, 'health_logs/new_topic.html', context)

@login_required
def new_entry(request, topic_id):
    """Add a new entry for a particular topic."""
    topic = Topic.objects.get(id=topic_id)
    
    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = EntryForm()
    else:
        # POST data submitted; process data.
        form = EntryForm(data=request.POST)
        
        if form.is_valid():
            
            
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('health_logs:topic', topic_id=topic_id, wrkt_topic_id=0)
          
            # for entry_id in range(1, 2):
            #   try:
            #     entry = Entry.objects.get(id=entry_id)
                
            #   except Exception:
            #     print("a")
                
            #   else:
            #     print(entry_id, int(entry.text), entry.topic)
            
            # try:
            #   int(new_entry.text)
            # except ValueError:
            #   context = {'topic': topic, 'form': form}
            #   return render(request, 'health_logs/new_entry.html', context)
            # else:
            #   new_entry.save()
            #   return redirect('health_logs:topic', topic_id=topic_id)

    # Display a blank or invalid form.
    context = {'topic': topic, 'form': form}
    return render(request, 'health_logs/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    """Edit an existing entry."""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    
    if topic.owner != request.user:
      raise Http404

    if request.method != 'POST':
        # Initial request; pre-fill form with the current entry.
        form = EntryForm(instance=entry)
    else:
        # POST data submitted; process data.
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('health_logs:topic', topic_id=topic.id, wrkt_topic_id=0)

    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'health_logs/edit_entry.html', context)
  
  
@login_required
def topics_logs(request):
  topics = LogTopic.objects.filter(owner=request.user).order_by('date_added')
  context = {'topics' : topics}
  return render(request, 'health_logs/topics_logs.html', context)

@login_required
def topic_logs(request, topic_id):
    """Show a single topic and all its entries."""
    topic = LogTopic.objects.get(id=topic_id)
    
    if topic.owner != request.user:
      raise Http404

    entries = topic.logentry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries, 'ai_suggested_texts' : ai_suggested_texts}
    return render(request, 'health_logs/topic_logs.html', context)
  
@login_required
def new_topic_logs(request):
    """Add a new topic."""
    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = LogTopicForm()
    else:
        # POST data submitted; process data.
        form = LogTopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect('health_logs:topics_logs')

    # Display a blank or invalid form.
    context = {'form': form}
    return render(request, 'health_logs/new_topic_logs.html', context)

@login_required
def new_entry_logs(request, topic_id):
    """Add a new entry for a particular topic."""
    topic = LogTopic.objects.get(id=topic_id)
    
    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = LogEntryForm()
    else:
        # POST data submitted; process data.
        form = LogEntryForm(data=request.POST)
        
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('health_logs:topic_logs', topic_id=topic_id)

    # Display a blank or invalid form.
    context = {'topic': topic, 'form': form}
    return render(request, 'health_logs/new_entry_logs.html', context)

@login_required
def edit_entry_logs(request, entry_id):
    """Edit an existing entry."""
    entry = LogEntry.objects.get(id=entry_id)
    topic = entry.topic
    
    if topic.owner != request.user:
      raise Http404

    if request.method != 'POST':
        # Initial request; pre-fill form with the current entry.
        form = LogEntryForm(instance=entry)
    else:
        # POST data submitted; process data.
        form = LogEntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('health_logs:topic_logs', topic_id=topic.id)

    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'health_logs/edit_entry_logs.html', context)
  
  
@login_required
def topics_goals(request):
  topics = GoalTopic.objects.filter(owner=request.user).order_by('date_added')
  context = {'topics' : topics, 'time_intervals' : '3 1 4 1 5', 'above' : 'Push Ups,Rest,Sit Ups,Rest,Squats', 'below' : ',Next: Sit Ups,,Next: Squats,'}#############changed
  # todo: move timer to workouts page, add 'back to workouts' button
  # todo: favorite workouts, show how many times each workout has been done
  # workout flow: topics (workout names) --> add exercises (time, sets, rest), start workout --> new form with timer
  # todo: add chart
  # todo: link metrics/logs to goals
  # todo: option for reps/distance instead of time
  # todo: link metrics to workouts
  return render(request, 'health_logs/topics_goals.html', context)

@login_required
def topic_goals(request, topic_id):
    """Show a single topic and all its entries."""
    topic = GoalTopic.objects.get(id=topic_id)
    
    if topic.owner != request.user:
      raise Http404

    entries = topic.goalentry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries, 'ai_suggested_texts' : ai_suggested_texts}
    return render(request, 'health_logs/topic_goals.html', context)
  
@login_required
def new_topic_goals(request):
    """Add a new topic."""
    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = GoalTopicForm()
    else:
        # POST data submitted; process data.
        form = GoalTopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect('health_logs:topics_goals')

    # Display a blank or invalid form.
    context = {'form': form}
    return render(request, 'health_logs/new_topic_goals.html', context)

@login_required
def new_entry_goals(request, topic_id):
    """Add a new entry for a particular topic."""
    topic = GoalTopic.objects.get(id=topic_id)
    
    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = GoalEntryForm()
    else:
        # POST data submitted; process data.
        form = GoalEntryForm(data=request.POST)
        
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('health_logs:topic_goals', topic_id=topic_id)

    # Display a blank or invalid form.
    context = {'topic': topic, 'form': form}
    return render(request, 'health_logs/new_entry_goals.html', context)

@login_required
def edit_entry_goals(request, entry_id):
    """Edit an existing entry."""
    entry = GoalEntry.objects.get(id=entry_id)
    topic = entry.topic
    
    if topic.owner != request.user:
      raise Http404

    if request.method != 'POST':
        # Initial request; pre-fill form with the current entry.
        form = GoalEntryForm(instance=entry)
    else:
        # POST data submitted; process data.
        form = GoalEntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('health_logs:topic_goals', topic_id=topic.id)

    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'health_logs/edit_entry_goals.html', context)
  
  
@login_required
def topics_workouts(request):
  topics = WorkoutTopic.objects.filter(owner=request.user).order_by('date_added')
  context = {'topics' : topics, 'time_intervals' : '3 1 4 1 5', 'above' : 'Push Ups,Rest,Sit Ups,Rest,Squats', 'below' : ',Next: Sit Ups,,Next: Squats,'}#############changed
  #done todo: move timer to workouts page, add 'back to workouts' button
  #done todo: show how many times each workout has been done
  #done workout flow: topics (workout names) --> add exercises (time, sets, rest), start workout --> new form with timer
  #done todo: add chart
  # todo: link metrics/logs to goals
  #* todo: option for reps/distance instead of time
  # todo: link metrics to workouts
  #* todo: favorite workouts, 
  return render(request, 'health_logs/topics_workouts.html', context)

def obtain_workout(topic):
  entry_id = 1
  workout = {}
  
  while True:
    try:
      entry = WorkoutEntry.objects.get(id=entry_id)
      
    except Exception:
      break
    
    else:
      if entry.topic == topic:
        if entry.exercise not in workout:
          workout[entry.exercise] = {'duration' : [], 'sets' : [], 'rest' : []}
          
        workout[entry.exercise]['duration'].append(entry.duration)
        workout[entry.exercise]['sets'].append(entry.sets)
        workout[entry.exercise]['rest'].append(entry.rest)
        
      entry_id += 1
      
  return workout
      
def format_workout(workout):
  formatted_workout = ""
  
  for exercise in workout:
    formatted_workout += f"<h3>{exercise}</h3>,"
    for i in range(len(workout[exercise]['duration'])):
      formatted_workout += f"<li>{workout[exercise]['sets'][i]} sets x {workout[exercise]['duration'][i]} seconds with {workout[exercise]['rest'][i]} seconds of rest in between</li>,"
    
  return formatted_workout
  
@login_required
def topic_workouts(request, topic_id):
    """Show a single topic and all its entries."""
    topic = WorkoutTopic.objects.get(id=topic_id)
    
    if topic.owner != request.user:
      raise Http404

    entries = topic.workoutentry_set.order_by('date_added')
    
    workout = obtain_workout(topic)
    formatted_workout = format_workout(workout)
      
    context = {'topic': topic, 'entries': entries, 'formatted_workout': formatted_workout, 'ai_suggested_texts' : ai_suggested_texts}
    return render(request, 'health_logs/topic_workouts.html', context)
  
@login_required
def update_workout_info(request, topic_id):
  topic = WorkoutTopic.objects.get(id=topic_id)
  
  if topic.owner != request.user:
    raise Http404
    
  topic.times_completed += 1
  topic.completion_timestamps.append(datetime.now().isoformat()[:10])
  topic.save()
  
  return redirect('health_logs:topic_workouts', topic_id=topic_id)
    
  
  
@login_required
def exercises_workouts(request, topic_id):
  """Show each individual exercise in a workout."""
  topic = WorkoutTopic.objects.get(id=topic_id)
  
  if topic.owner != request.user:
    raise Http404

  entries = topic.workoutentry_set.order_by('date_added')
  context = {'topic': topic, 'entries': entries, 'ai_suggested_texts' : ai_suggested_texts}
  return render(request, 'health_logs/exercises_workouts.html', context)
  

@login_required
def new_topic_workouts(request):
    """Add a new topic."""
    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = WorkoutTopicForm()
    else:
        # POST data submitted; process data.
        form = WorkoutTopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect('health_logs:topics_workouts')

    # Display a blank or invalid form.
    context = {'form': form}
    return render(request, 'health_logs/new_topic_workouts.html', context)

@login_required
def new_entry_workouts(request, topic_id):
    """Add a new entry for a particular topic."""
    topic = WorkoutTopic.objects.get(id=topic_id)
    
    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = WorkoutEntryForm()
    else:
        # POST data submitted; process data.
        form = WorkoutEntryForm(data=request.POST)
        
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('health_logs:topic_workouts', topic_id=topic_id)

    # Display a blank or invalid form.
    context = {'topic': topic, 'form': form}
    return render(request, 'health_logs/new_entry_workouts.html', context)

@login_required
def edit_entry_workouts(request, entry_id):
    """Edit an existing entry."""
    entry = WorkoutEntry.objects.get(id=entry_id)
    topic = entry.topic
    
    if topic.owner != request.user:
      raise Http404

    if request.method != 'POST':
        # Initial request; pre-fill form with the current entry.
        form = WorkoutEntryForm(instance=entry)
    else:
        # POST data submitted; process data.
        form = WorkoutEntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('health_logs:exercises_workouts', topic_id=topic.id)

    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'health_logs/edit_entry_workouts.html', context)
  
def prepare_workout(workout):
  time_intervals = '5 '
  above_texts = 'Get Ready,'
  below_texts = ''
  
  for exercise in workout:
    for i in range(len(workout[exercise]['duration'])):
      for s in range(workout[exercise]['sets'][i]):
        time_intervals += f"{workout[exercise]['duration'][i]} {workout[exercise]['rest'][i]} "
        above_texts += f"{exercise},Rest,"
        below_texts += f"Next exercise: {exercise},,"
        
  time_intervals = time_intervals[:-1]
  above_texts = above_texts[:-1]
  
  return time_intervals, above_texts, below_texts
      
  
@login_required
def do_workout(request, topic_id):
  topic = WorkoutTopic.objects.get(id=topic_id)
  
  workout = obtain_workout(topic)
  
  time_intervals, above_texts, below_texts = prepare_workout(workout)
  
  context = {'topic' : topic, 'time_intervals' : time_intervals, 'above_texts' : above_texts, 'below_texts' : below_texts}
  return render(request, 'health_logs/do_workout.html', context)
  
@login_required
def collect_data():
  entry_id = 1
  data = {}
  
  while True:
    try:
      entry = Entry.objects.get(id=entry_id)
    
    except Exception:
      break
    
    else:
      topic = entry.topic
      text = int(entry.text)
      
      if topic not in data:
        data[topic] = []
        
      data[topic].append(text)
      
      entry_id += 1
      
  return data

@login_required
def ai_advisor(request):
    """Handle use's question"""
    if request.method != 'POST':
        # No data submitted; create a blank form.
        pass

    else:
      print(request.POST['editBox1'] + "--------------")
     
     
      from langchain.document_loaders import TextLoader

      answer = ai_answer(request.POST['editBox1'])
      topics = Topic.objects.filter(owner=request.user).order_by('date_added')
     
      context = {'topics' : topics, 'ai_answer' : answer}
      return render(request, 'resume_logs/topics.html', context)


# @login_required
# def generate_section(request, entry_id):
#     global ai_suggested_text
#     global ai_suggested_texts
    
#     while len(ai_suggested_texts) <= entry_id:
#       ai_suggested_texts.append("")
      
#     """Generate the AI text."""
#     entry = Entry.objects.get(id=entry_id)
#     topic = entry.topic
    
#     if topic.owner != request.user:
#       raise Http404

#     ai_suggested_text = "AI suggested:\n" + generate_text(entry.section, entry.text)
#     ai_suggested_texts[entry_id] = "AI suggested:\n" + generate_text(entry.section, entry.text)
#     print(ai_suggested_texts)
#     return redirect('health_logs:topic', topic_id=topic.id)
# 	
# from django.http import HttpResponse
# from django.conf import settings
# import os

# @login_required
# def download_template(request):    
#     file_path = os.path.join(settings.MEDIA_ROOT, TEMPLATE_FILE)

#     # Open the file for reading
#     with open(file_path, 'rb') as file:
#         response = HttpResponse(file.read(), content_type='application/octet-stream')
#         response['Content-Disposition'] = f'attachment; filename=' + TEMPLATE_FILE
#         return response

# @login_required
# def download_result(request):
#     pdf = FPDF()
#     pdf.add_page()

#     sections = {}
#     firstline = True
#     pdf.set_font("Arial", style='B', size=12)
#     for entry in Entry.objects.all():
#       topic = entry.topic

#       if topic.owner == request.user:
#         print('<' + entry.section + '>')
#         if entry.section == 'Personal Information':
#           lines = entry.text.split('\n')
          
#           for line in lines:
#             pdf.cell(200,5, txt = line, ln=True, align='C')
#             if firstline:
#               firstline = False
#               pdf.set_font("Arial", size=10)
          
#         else:
#           sections[entry.section] = entry.text.split('\n')

#     pdf.set_font("Arial", size=10)
#     for line in sections['SUMMARY']:
#       pdf.cell(200,10, txt = line, ln=True, align='L')

#     pdf.set_font("Arial", style='B', size=12)
#     pdf.cell(200, 10, txt = 'EDUCATION', ln=True, align='L')
#     pdf.set_font("Arial", size=10)
#     for line in sections['EDUCATION']:
#       pdf.cell(200,5, txt = line, ln=True, align='L')

#     pdf.set_font("Arial", style='B', size=12)
#     pdf.cell(200, 10, txt = 'TEST SCORES', ln=True, align='L')
#     pdf.set_font("Arial", size=10)
#     for line in sections['TEST SCORES']:
#       pdf.cell(200,5, txt = line, ln=True, align='L')

#     pdf.set_font("Arial", style='B', size=12)
#     pdf.cell(200, 10, txt = 'COURSES', ln=True, align='L')
#     pdf.set_font("Arial", size=10)
#     for line in sections['COURSES']:
#       pdf.cell(200,5, txt = line, ln=True, align='L')

#     pdf.set_font("Arial", style='B', size=12)
#     pdf.cell(200, 10, txt = 'EXTRACURRICULARS', ln=True, align='L')
#     pdf.set_font("Arial", size=10)
#     for line in sections['EXTRACURRICULARS']:
#       pdf.cell(200,5, txt = line, ln=True, align='L')

#     pdf.set_font("Arial", style='B', size=12)
#     pdf.cell(200, 10, txt = 'VOLUNTEERING', ln=True, align='L')
#     pdf.set_font("Arial", size=10)
#     for line in sections['VOLUNTEERING']:
#       pdf.cell(200,5, txt = line, ln=True, align='L')

#     file_path = os.path.join(settings.MEDIA_ROOT, RESULT_FILE)
#     pdf.output(file_path)

#     # Open the file for reading
#     with open(file_path, 'rb') as file:
#         response = HttpResponse(file.read(), content_type='application/octet-stream')
#         response['Content-Disposition'] = f'attachment; filename=' + RESULT_FILE
#         return response