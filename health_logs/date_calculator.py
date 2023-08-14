# -*- coding: utf-8 -*-
"""
Created on Mon Aug 14 03:35:35 2023

@author: kevinh
"""



days_in_months = {"01":31, "02":28, "02leap":29, "03":31, "04":30, "05":31, "06":30, "07":31, "08":31, "09":30, "10":31, "11":30, "12":31}

def days_since(start_date, current_date):
  
  start_year = start_date[0:4]
  start_month = start_date[4:6]
  start_day = start_date[6:8]
  
  current_year = current_date[0:4]
  current_month = current_date[4:6]
  current_day = current_date[6:8]
  
  return full_years_range(start_year, start_month, start_day, current_year, current_month, current_day)
    
    
def full_years_range(start_year, start_month, start_day, current_year, current_month, current_day):
  first_year = int(start_year) + 1
  last_year = int(current_year) - 1
  
  if start_month + start_day == '0101':
    first_year -= 1
  if current_month + current_day == '1231':
    last_year += 1
    
  
  num_leap_years = 0
    
  for year in range(int(first_year / 4 + 0.9) * 4, int(last_year / 4) * 4 + 1, 4):
    if is_leap_year(year):
      num_leap_years += 1
      
  if is_leap_year(start_year) and start_year == current_year:
    num_leap_years = -1
      
  years_days_amount = 365 * (last_year - first_year + 1) + num_leap_years
  remaining_days_amount = full_months_range(start_month, start_day, '12', '31', start_year) + full_months_range('01', '01', current_month, current_day, current_year)
  
    
  return years_days_amount + remaining_days_amount - 1

def full_months_range(start_month, start_day, current_month, current_day, year):
  if [start_month, start_day, current_month, current_day] == ['01', '01', '12', '31']:
    return 0
  
  first_month = int(start_month) + 1
  last_month = int(current_month) - 1
  
  
    
  if is_leap_year(year):
    if start_month == '02':
      start_month += 'leap'
    if current_month == '02':
      current_month += 'leap'
      
  if start_day == '01':
    first_month -= 1
  if int(current_day) == days_in_months[current_month]:
    last_month += 1
    
  months_days_amount = calculate_months_days(first_month, last_month, year)
  
  if current_month == '12' and start_day != '01':
    remaining_days_amount = days_amount(start_day, days_in_months[start_month])
  elif int(current_day) != days_in_months[current_month]:
    remaining_days_amount = days_amount(1, current_day)
  else:
    remaining_days_amount = 0
    
    
  return months_days_amount + remaining_days_amount

def is_leap_year(year):
  year = int(year)
  if year % 4 == 0 and year % 100 != 0 or year % 400 == 0:
    return True

def calculate_months_days(first_month, last_month, year):
  total_days = 0
  
  for month in range(int(first_month), int(last_month) + 1):
    month = str(month)
    if len(month) < 2:
      month = '0' + month
      
    if month == '02' and is_leap_year(year):
      month += 'leap'
      
    total_days += days_in_months[month]
    
  return total_days
    
      

def days_amount(start_day, current_day):
  return int(current_day) - int(start_day) + 1
  