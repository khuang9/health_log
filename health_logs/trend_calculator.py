# -*- coding: utf-8 -*-
"""
Created on Mon Aug 14 03:15:54 2023

@author: kevinh
"""

from . import date_calculator

def format_day(day):
  day = day.isoformat()
  formatted_day = day[:4] + day[5:7] + day[8:10]
  return formatted_day

def calculate_trend(stats, days):
  
  if len(days) == 0:
    return "unavailable.", "undefined", "undefined", [], []
  
  start_day = format_day(days[0])
  
  for i in range(len(days)):
    days[i] = format_day(days[i])
    days[i] = date_calculator.days_since(start_day, days[i])
    
  if len(stats) == 0:
    return "", "", "", [], days
  
  xs = days
  ys = stats
  
  meanX = sum(xs) / len(xs)
  meanY = sum(ys) / len(ys)
  
  sigmaNum = 0
  sigmaDenom = 0
  
  for i in range(len(xs)):
    x = xs[i]
    y = ys[i]
    
    dx = x - meanX
    dy = y - meanY
    
    sigmaNum += dx * dy
    sigmaDenom += dx**2
    
  if sigmaDenom == 0:
    return "following an undefined trend.", "undefined", "undefined", xs, ys
    
  slope = sigmaNum / sigmaDenom
  y_int = meanY - slope * meanX
  
  if slope > 0:
    return f"trending upwards at an average rate of {round(slope, 2)} per day.", slope, y_int, xs, ys
  
  elif slope < 0:
    return f"trending downwards at an average rate of {round(slope, 2)} per day.", slope, y_int, xs, ys
  
  else:
    return "not showing any upwards or downwards trend.", slope, y_int, xs, ys
