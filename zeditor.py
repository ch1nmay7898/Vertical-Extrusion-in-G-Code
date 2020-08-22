import plotly.express as px
import tkinter as tk
from tkinter import ttk
import re
import pandas as pd
import os
import math
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
from tkinter import *
import PIL.Image
import matplotlib.image as mpimg

window = tk.Tk()
window.title("Zeditor")
container = tk.Frame(window)
canvas = tk.Canvas(container)
canvas.config(width=600, height=700)
scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)



frame1 = Frame(scrollable_frame)
frame2 = Frame(scrollable_frame)
frame3 = Frame(scrollable_frame)
frame4 = Frame(scrollable_frame)
frame5 = Frame(scrollable_frame)
frame1.pack()
frame2.pack()
frame3.pack()
frame4.pack()
frame5.pack()

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.update_idletasks()
canvas.configure(yscrollcommand=scrollbar.set)

greetings = tk.Label(frame1, text="G-Code Editor")
greetings.pack(pady=10)

entryX = tk.Entry(frame2, borderwidth = 3, relief="sunken")
entryX.insert(0, "Enter X Value")
entryY = tk.Entry(frame3, borderwidth = 3, relief="sunken")
entryY.insert(0, "Enter Y Value")
entryZ = tk.Entry(frame4, borderwidth = 3, relief="sunken")
text_box = tk.Text(frame1, borderwidth = 3, relief="sunken")
text_box.insert(END, "Paste the top layer code here.")

def cont_del(entry):
    return entry.delete(0, END)

def cont_01(entry):
    val_ini = entry.get()
    val_ini = float(val_ini)
    val_new = val_ini + 0.1
    val_new = f"{val_new:.2f}"
    cont_del(entry)
    return entry.insert(0, val_new)

def cont_1(entry):
    val_ini = entry.get()
    val_ini = float(val_ini)
    val_new = val_ini + 1
    val_new = str(val_new)
    cont_del(entry)
    return entry.insert(0, val_new)

def layer_counter(fullcode):
    matcher = r"Layer count: ([\d]*)"
    layer_count = re.findall(matcher, fullcode)
    layer_count = int(layer_count[0])
    layer_count = layer_count - 1
    return str(layer_count)

def top_code(fullcode, layer_finder):
    top_code = ""
    for line in fullcode.splitlines():
        if line != layer_finder:
            top_code = top_code+line+"\n"
        else:
            break;
    return top_code

def mid_code(fullcode, layer_finder):
    finder_flag = 0
    mid_code = ""
    for line in fullcode.splitlines():
        if line == layer_finder:
            finder_flag = 1
        if line == "; MatterSlice Completed Successfully" and finder_flag == 1:
            break;
        if finder_flag == 1:
            mid_code = mid_code+line+"\n"
    return mid_code

def end_code(fullcode, layer_finder):
    finder_flag = 0
    end_code = ""
    for line in fullcode.splitlines():
        if line == layer_finder:
            finder_flag = 1
        if line == "; MatterSlice Completed Successfully" and finder_flag == 1:
            finder_flag = 2
        if finder_flag == 2:
            end_code = end_code+line+"\n"
    return end_code

def regexer(string, var):
    regex = rf"{var}([\d]+\.?[\d]+)"
    matches = re.findall(regex, string)
    return matches

def xy_matcher(mid_code, var):
    values = []
    for line in mid_code.splitlines():
        if line == "M107":
            break;
        if (line != "" and line[0] == "G"):
            check = regexer(line, var)
            if (len(check) == 0):
                values.append(values[-1])
            else:
                values.append(float(check[0]))
    return values

def default_z(values_z, entry):
    len_z = len(values_z)
    if len_z > 1:
        max_z = max(values_z)
    else:
        max_z = values_z
    entry.insert(0, max_z)

def straight_movement(values_xy1, values_xy2, XY, var):
    available_points = []
    if (values_xy1 > values_xy2):
        xy = values_xy1
        low_xy = values_xy2

        while True:
            xy -= 1
            if var == "Y":
                f = ('%.2f'%xy, '%.2f'%XY)
            else:
                f = ('%.2f'%XY, '%.2f'%xy)
            available_points.append(f)
            T = xy
            if ((T-1) <= low_xy):
                break;
    else:
        xy = values_xy1
        high_xy = values_xy2
        while True:
            xy += 1
            if var == "Y":
                f = ('%.2f'%xy, '%.2f'%XY)
            else:
                f = ('%.2f'%XY, '%.2f'%xy)
            available_points.append(f)
            T = xy
            if ((T+1) >= high_xy):
                break;
    return available_points

def x_per_unit_hyp(x1, x2, y1, y2):
    hyp = math.sqrt(((x1 - x2)**2) + ((y1 - y2)**2))
    dist_X = x2 - x1
    x_per_unit_hyp = dist_X / hyp
    return x_per_unit_hyp
def point_slope_form(slope, x2, x1, y1):
    y2 = (slope*(x2 - x1)) + y1
    return ('%.2f'%x2, '%.2f'%y2), y2

def diag_right_up_down(x1, x2, y1, y2, slope, x_per_unit_hyp, up_down):
    available_points = []
    X, high_Y, high_X, low_Y = x1, y2, x2, y2
    while True:
        X += (1*x_per_unit_hyp)
        Y = (slope*(X - x1)) + y1
        f = ('%.2f'%X, '%.2f'%Y)
        available_points.append(f)
        if up_down == "up":
            if (Y >= high_Y or X >= high_X):
                return available_points
        else:
            if (Y <= low_Y or X >= high_X):
                return available_points

def diag_left_up_down(x1, x2, y1, y2, slope, x_per_unit_hyp, up_down):
    available_points = []
    X, high_Y, low_X, low_Y = x1, y2, x2, y2
    while True:
        X -= (1*x_per_unit_hyp)
        Y = (slope*(X - x1)) + y1
        f = ('%.2f'%X, '%.2f'%Y)
        available_points.append(f)
        if up_down == "up":
            if (Y >= high_Y or X <= low_X):
                return available_points
        else:
            if (Y <= low_Y or X <= low_X):
                return available_points
def renderer(all_values):
    x, y = zip(*all_values)
    x, y = list(map(float, x)), list(map(float, y))
    df = pd.DataFrame()
    df['X'], df['Y'] = x, y
    fig_inter = px.scatter(df, x = "X", y = "Y")
    fig_inter.show(renderer="browser")

def avail_points():
    fullcode = text_box.get("1.0", tk.END)
    layer_count = layer_counter(fullcode)
    layer_finder = "; LAYER:"+layer_count
    mid_code1 = mid_code(fullcode, layer_finder)
    values_X = xy_matcher(mid_code1, "X")
    values_Y = xy_matcher(mid_code1, "Y")
    values_Z = list(map(float, regexer(mid_code1, "Z")))
    default_z(values_Z, entryZ)
    count_X = len(values_X)
    n = count_X - 1

    all_values = []
    available_points = []
    for i in range(n):
        if (values_Y[i] == values_Y[i+1]):
            Y = values_Y[i]
            available_points.extend(straight_movement(values_X[i], values_X[i+1], Y, "Y"))
        elif (values_X[i] == values_X[i+1]):
            X = values_X[i]
            available_points.extend(straight_movement(values_Y[i], values_Y[i+1], X, "X"))
        else:
            m = ((values_Y[i+1] - values_Y[i])/(values_X[i+1] - values_X[i]))

            if ((values_X[i+1] > values_X[i]) and (values_Y[i+1] > values_Y[i])):
                X_per_unit_hyp = x_per_unit_hyp(values_X[i], values_X[i+1], values_Y[i], values_Y[i+1])
                available_points.extend(diag_right_up_down(values_X[i], values_X[i+1], values_Y[i], values_Y[i+1], m, X_per_unit_hyp, "up"))
            elif ((values_X[i+1] < values_X[i]) and (values_Y[i+1] > values_Y[i])):
                X_per_unit_hyp = x_per_unit_hyp(values_X[i+1], values_X[i], values_Y[i], values_Y[i+1])
                available_points.extend(diag_left_up_down(values_X[i], values_X[i+1], values_Y[i], values_Y[i+1], m, X_per_unit_hyp, "up"))
            elif ((values_X[i+1] > values_X[i]) and (values_Y[i+1] < values_Y[i])):
                X_per_unit_hyp = x_per_unit_hyp(values_X[i], values_X[i+1], values_Y[i], values_Y[i+1])
                available_points.extend(diag_right_up_down(values_X[i], values_X[i+1], values_Y[i], values_Y[i+1], m, X_per_unit_hyp, "down"))
            elif ((values_X[i+1] < values_X[i]) and (values_Y[i+1] < values_Y[i])):
                X_per_unit_hyp = x_per_unit_hyp(values_X[i+1], values_X[i], values_Y[i], values_Y[i+1])
                available_points.extend(diag_left_up_down(values_X[i], values_X[i+1], values_Y[i], values_Y[i+1], m, X_per_unit_hyp, "down"))
        all_values.extend(available_points)
        available_points.clear()
    renderer(all_values)

def e_per_point(e1, e2, x1, x2, y1, y2):
    E_val_diff = e2 - e1
    point_dist = math.sqrt(((x1 - x2)**2) + ((y1 - y2)**2))
    return (E_val_diff / point_dist)

def add_movements(values_z, input_x, input_y, input_z, current_x, current_y, top_code, mid_code, end_code, f, e):
    high_Z = max(values_z) + 0.1
    low_Z = min(values_z)
    line1 = "G1 "+"X"+str(current_x)+" Y"+str(current_y)+" Z"+str('%.2f'%high_Z)+" F"+str(f)
    line2 = "G1 "+"X"+str(input_x)+" Y"+str(input_y)+" Z"+str('%.2f'%high_Z)+" F"+str(f)
    line3 = "G1 "+"X"+str(input_x)+" Y"+str(input_y)+" Z"+str('%.2f'%(low_Z))+" F"+str(f)
    line4 = "G1 "+"X"+str(input_x)+" Y"+str(input_y)+" Z"+str(input_z)+" E"+str('%.3f'%e)+" F"+str(f)
    code_addition = "\n"+line1+"\n"+line2+"\n"+line3+"\n"+line4+"\n"
    final_code = top_code+mid_code+code_addition+end_code
    text_box.delete("1.0", "end")
    return text_box.insert(END, final_code)

def add_extru(a, b, c): 
    fullcode = text_box.get("1.0", tk.END)
    layer_count = layer_counter(fullcode)
    layer_finder = "; LAYER:"+layer_count
    top_code1 = top_code(fullcode, layer_finder)
    init_gcode1 = mid_code(fullcode, layer_finder)
    low_code = end_code(fullcode, layer_finder)
    values_X = xy_matcher(init_gcode1, "X")
    values_Y = xy_matcher(init_gcode1, "Y")
    values_Z = list(map(float, regexer(init_gcode1, "Z")))
    values_E = list(map(float, regexer(init_gcode1, "E")))
    values_F = list(map(float, regexer(init_gcode1, "F")))
    E_per_point = e_per_point(values_E[0], values_E[1], values_X[1], values_X[2], values_Y[1], values_Y[2])
    e = (E_per_point * float(c)) + values_E[-1]
    add_movements(values_Z, a, b, c, values_X[-1], values_Y[-1], top_code1, init_gcode1, low_code, values_F[-1], e)

def finish():
    fullcode = text_box.get("1.0", tk.END)
    layer_count = layer_counter(fullcode)
    layer_finder = "; LAYER:"+layer_count
    top_code1 = top_code(fullcode, layer_finder)
    init_gcode1 = mid_code(fullcode, layer_finder)
    low_code = end_code(fullcode, layer_finder)
    m400 = "M400 \n"
    text_box.delete("1.0", "end")
    final_code = top_code1+init_gcode1+m400+low_code
    return text_box.insert(END, final_code)
    
button1 = tk.Button(frame1, text="Show Available Points",command=avail_points, borderwidth = 3, relief="raised")

button2 = tk.Button(frame5, text="Add Movement", command= lambda: add_extru(entryX.get(), entryY.get(), entryZ.get()), relief="raised")
button3 = tk.Button(frame5, text="Finish", command=finish, relief="raised")

cont_X_pt = tk.Button(frame2, text="+0.1", command= lambda: cont_01(entryX), width=10)
cont_X = tk.Button(frame2, text="+1", command= lambda: cont_1(entryX), width=10)

cont_Y_pt = tk.Button(frame3, text="+0.1", command= lambda: cont_01(entryY), width=10)
cont_Y = tk.Button(frame3, text="+1", command= lambda: cont_1(entryY), width=10)

cont_Z_pt = tk.Button(frame4, text="+0.1", command= lambda: cont_01(entryZ), width=10)
cont_Z = tk.Button(frame4, text="+1", command= lambda: cont_1(entryZ), width=10)


text_box.pack(padx=10)
button1.pack(padx = 10, pady = 10)
entryX.pack(padx=5, pady=10, side=tk.LEFT)
cont_X_pt.pack(padx=5, pady=20, side=tk.LEFT)
cont_X.pack(padx=5, pady=20, side=tk.LEFT)

entryY.pack(padx=5, pady=10, side=tk.LEFT)
cont_Y_pt.pack(padx=5, pady=20, side=tk.LEFT)
cont_Y.pack(padx=5, pady=20, side=tk.LEFT)

entryZ.pack(padx=5, pady=10, side=tk.LEFT)
cont_Z_pt.pack(padx=5, pady=20, side=tk.LEFT)
cont_Z.pack(padx=5, pady=20, side=tk.LEFT)

button2.pack(padx=5, pady=10, side=tk.LEFT)
button3.pack(padx=5, pady=10, side=tk.LEFT)

container.pack()
canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

window.mainloop()