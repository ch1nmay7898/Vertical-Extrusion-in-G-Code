import tkinter as tk
import re
import pandas as pd
import os
import math
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
from tkinter import *

window = tk.Tk()
count = 0
def func(c):
    init_gcode1 = text_box1.get("1.0", tk.END)
    regex_X = r"X([\d]*\.?[\d]*)"
    matches_X = re.findall(regex_X, init_gcode1)
    regex_Y = r"Y([\d]*\.?[\d]*)"
    matches_Y = re.findall(regex_Y, init_gcode1)
    regex_Z = r"Z([\d]*\.?[\d]*)"
    matches_Z = re.findall(regex_Z, init_gcode1)
    regex_E = r"E([\d]*\.?[\d]*)"
    matches_E = re.findall(regex_E, init_gcode1)
    regex_F = r"F([\d]*\.?[\d]*)"
    matches_F = re.findall(regex_F, init_gcode1)

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
    count += 1
    text_box2.insert(tk.END, E_per_point)

def counter():
    text_box2.insert(tk.END, "\n")
    text_box2.insert(tk.END, count)
text_box1 = tk.Text()
text_box2 = tk.Text()
button = tk.Button(text="hello", command=func(count))
button2 = tk.Button(text="hello2", command=counter)
entry = tk.Entry()

text_box1.pack()
button.pack()
button2.pack()
text_box2.pack()
entry.pack()
window.mainloop()