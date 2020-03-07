# -*- coding: utf-8 -*-


import re
import pandas as pd
import os
import math
import numpy as np
import matplotlib.pyplot as plt


f1 = open("sample.txt", "rt")
regex_X = r"X([\d]*\.?[\d]*)"
matches_X = re.findall(regex_X, f1.read())
f1.close()

f1 = open("sample.txt", "rt")
regex_Y = r"Y([\d]*\.?[\d]*)"
matches_Y = re.findall(regex_Y, f1.read())
f1.close()

f1 = open("sample.txt", "rt")
regex_Z = r"Z([\d]*\.?[\d]*)"
matches_Z = re.findall(regex_Z, f1.read())
f1.close()

f1 = open("sample.txt", "rt")
regex_E = r"E([\d]*\.?[\d]*)"
matches_E = re.findall(regex_E, f1.read())
f1.close()

f1 = open("sample.txt", "rt")
regex_F = r"F([\d]*\.?[\d]*)"
matches_F = re.findall(regex_F, f1.read())
f1.close()

values_X = []
values_Y = []
values_Z = []
values_E = []
values_F = []
for match in matches_X:
    values_X.append(float(match))

for match in matches_Y:
    values_Y.append(float(match))

for match in matches_Z:
    values_Z.append(float(match))

for match in matches_E:
    values_E.append(float(match))

for match in matches_F:
    values_F.append(float(match))

E_val_diff = values_E[-1] - values_E[-2]
point_dist = math.sqrt(((values_X[-1] - values_X[-2])**2) + ((values_Y[-1] - values_Y[-2])**2))
E_per_point = (E_val_diff / point_dist)

count_X = len(values_X)
count_Y = len(values_Y) 
count_Z = len(values_Z) 
count_E = len(values_E)
n = count_X - 1



all_values = []
available_points = []
for i in range(n): 
  if (values_X[i] != values_X[i+1]):
    m = ((values_Y[i+1] - values_Y[i])/(values_X[i+1] - values_X[i]))
    temp_X1 = (values_X[i] * 10)
    temp_X2 = (values_X[i+1] * 10)
    temp_X = abs(temp_X2 - temp_X1)
    temp_X = int(temp_X)
    if (values_X[i] > values_X[i+1]):
      X = values_X[i+1]
    else:
      X = values_X[i]
    for j in range(temp_X):
      if (values_X[i] < values_X[i+1]):
        X -= 0.1 
      else:
        X += 0.1
      Y = (m*(X - values_X[i])) + values_Y[i]
      #f = "|" + str('%.2f'%X) + "," + str('%.2f'%Y) + "|"
      f = ('%.2f'%X, '%.2f'%Y)
      available_points.append(f)
      #print('%.2f'%X, '%.2f'%Y, sep=",")

  else:
    temp_Y1 = (values_Y[i] * 10)
    temp_Y2 = (values_Y[i+1] * 10)
    temp_Y = abs(temp_Y2 - temp_Y1)
    temp_Y = int(temp_Y)
    if (values_Y[i] > values_Y[i+1]):
      Y = values_Y[i+1]
    else:
      Y = values_Y[i]
    for k in range(temp_Y):
      X = values_X[i]
      if (values_Y[i] > values_Y[i+1]):
        Y -= 0.1 
      else:
        Y += 0.1
      #f = "|" + str('%.2f'%X) + "," + str('%.2f'%Y) + "|"
      f = ('%.2f'%X, '%.2f'%Y)
      available_points.append(f)
      #print('%.2f'%X, '%.2f'%Y, sep=" , ")
  print(available_points)
  all_values.extend(available_points)
  available_points.clear()
  #print("____________________________________________________________________________________________________________________")

x, y = zip(*all_values)



plt.scatter(x, y)
plt.show()

def Z_motion(a, b, c, t, f):
  if (t == 1):
    high_Z = max(values_Z) + 0.1
    current_X = values_X[-1]
    current_Y = values_Y[-1]
    line1 = "G1 "+"X"+str(current_X)+" Y"+str(current_Y)+" Z"+str('%.2f'%high_Z)+" F"+str(f)
    line2 = "G1 "+"X"+str(a)+" Y"+str(b)+" Z"+str('%.2f'%high_Z)+" F"+str(f)
    line3 = "G1 "+"X"+str(a)+" Y"+str(b)+" Z"+str('%.2f'%(high_Z - 0.1))+" F"+str(f)
    e = (E_per_point * c) + values_E[-1]
    line4 = "G1 "+"X"+str(a)+" Y"+str(b)+" Z"+str(c)+" E"+str('%.3f'%e)+" F"+str(f)
    code_addition = line1+"\n"+line2+"\n"+line3+"\n"+line4
    return code_addition
  elif (t == 0):
    high_Z = max(values_Z) + 0.1
    current_X = values_X[-1]
    current_Y = values_Y[-1]
    line1 = "G1 "+"X"+str(current_X)+" Y"+str(current_Y)+" Z"+str('%.2f'%high_Z)+" F"+str(f)
    line2 = "G1 "+"X"+str(a)+" Y"+str(b)+" Z"+str('%.2f'%high_Z)+" F"+str(f)
    line3 = "G1 "+"X"+str(a)+" Y"+str(b)+" Z"+str('%.2f'%(high_Z - 0.1))+" F"+str(f)
    line4 = "G1 "+"X"+str(a)+" Y"+str(b)+" Z"+str(c)+" E"+str(e)+" F"+str(f)
    code_addition = line1+"\n"+line2+"\n"+line3+"\n"+line4
    return code_addition
  else:
    return (print("Enter 1 or 0"))

f1.close()
f1 = open("sample.txt", "at")


added_code = Z_motion(87.35, 81.69, 23, 1, values_F[-1])

f1.write(added_code)
f1.close()



#os.remove("sample.txt")

all_values.clear()

values_X.clear()
values_Y.clear()
values_Z.clear()
values_E.clear()
values_F.clear()