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

var1 = tk.IntVar()
c1 = tk.Checkbutton(frame5, text='Use Extrusion',variable=var1, onvalue=1, offvalue=0)

text_box = tk.Text(frame1, borderwidth = 3, relief="sunken")
text_box.insert(END, "Paste the top layer code here.")

def cont_X_del():
    return entryX.delete(0, END)

def cont_X_01():
    val_ini = entryX.get()
    val_ini = float(val_ini)
    val_new = val_ini + 0.1
    val_new = str(val_new)
    cont_X_del()
    return entryX.insert(0, val_new)

def cont_X_1():
    val_ini = entryX.get()
    val_ini = float(val_ini)
    val_new = val_ini + 1
    val_new = str(val_new)
    cont_X_del()
    return entryX.insert(0, val_new)

def cont_Y_del():
    return entryY.delete(0, END)

def cont_Y_01():
    val_ini = entryY.get()
    val_ini = float(val_ini)
    val_new = val_ini + 0.1
    val_new = str(val_new)
    cont_Y_del()
    return entryY.insert(0, val_new)

def cont_Y_1():
    val_ini = entryY.get()
    val_ini = float(val_ini)
    val_new = val_ini + 1
    val_new = str(val_new)
    cont_Y_del()
    return entryY.insert(0, val_new)

def cont_Z_del():
    return entryZ.delete(0, END)

def cont_Z_01():
    val_ini = entryZ.get()
    val_ini = float(val_ini)
    val_new = val_ini + 0.1
    val_new = str(val_new)
    cont_Z_del()
    return entryZ.insert(0, val_new)

def cont_Z_1():
    val_ini = entryZ.get()
    val_ini = float(val_ini)
    val_new = val_ini + 1
    val_new = str(val_new)
    cont_Z_del()
    return entryZ.insert(0, val_new)

def count_layer():
    full_gcode = text_box.get("1.0", tk.END)
    layer_count = r"Layer count: ([\d]*)"
    return layer_count



def avail_points():
    fullcode = text_box.get("1.0", tk.END)
    matcher = r"Layer count: ([\d]*)"
    layer_count = re.findall(matcher, fullcode)
    layer_count = int(layer_count[0])
    layer_count = layer_count - 1
    layer_count = str(layer_count)
    layer_finder = "; LAYER:"+layer_count
    top_code="\n"
    init_gcode="\n"
    low_code="\n"
    finder_flag=0
    for lines in fullcode.splitlines():
        if lines != layer_finder and finder_flag == 0:
            top_code = top_code+lines+"\n"
        if lines == layer_finder:
            finder_flag = 1
        if lines == "; MatterSlice Completed Successfully" and finder_flag == 1:
            finder_flag = 2
        if finder_flag == 1:
            init_gcode = init_gcode+lines+"\n"
        if finder_flag == 2:
            low_code = low_code+lines+"\n"
    """
    #regex_G = r"G([\d]*\.?[\d]*)"
    #matches_G = re.findall(regex_G, init_gcode)
    #line_count = matches_G.count()
    
    regex_X = r"X([\d]+\.?[\d]+)"
    matches_X = re.findall(regex_X, low_code)
    regex_Y = r"Y([\d]+\.?[\d]+)"
    matches_Y = re.findall(regex_Y, low_code)
    """
    regex_Z = r"Z([\d]+\.?[\d]+)"
    matches_Z = re.findall(regex_Z, init_gcode)
    regex_E = r"E([\d]+\.?[\d]+)"
    matches_E = re.findall(regex_E, init_gcode)
    regex_F = r"F([\d]+\.?[\d]+)"
    matches_F = re.findall(regex_F, init_gcode)

    values_X = []
    values_Y = []
    values_Z = []
    values_E = []
    values_F = []

    for lines in init_gcode.splitlines():
        if lines == "M107":
            break;

        if (lines != "" and lines[0] == "G"):
            X_reg = r"X([\d]+\.?[\d]+)"
            X_check = re.findall(X_reg, lines)
            Y_reg = r"Y([\d]+\.?[\d]+)"
            Y_check = re.findall(Y_reg, lines)
            
            if (len(X_check) == 0):
                values_X.append(values_X[-1])
            else:
                values_X.append(float(X_check[0]))
            
            if (len(Y_check) == 0):
                values_Y.append(values_Y[-1])
            else:
                values_Y.append(float(Y_check[0]))


    for match in matches_Z:
        values_Z.append(float(match))

    for match in matches_E:
        values_E.append(float(match))

    for match in matches_F:
        values_F.append(float(match))
    
    len_z = len(values_Z)
    if len_z > 1:
        max_z = max(values_Z)
    else:
        max_z = values_Z
    entryZ.insert(0, max_z)
    count_X = len(values_X)
    count_Y = len(values_Y) 
    count_Z = len(values_Z) 
    count_E = len(values_E)
    n = count_X - 1

    all_values = []
    available_points = []
    for i in range(n):
        if (values_Y[i] == values_Y[i+1]):
            Y = values_Y[i]
            """
            temp_X1 = (values_X[i] * 10)
            temp_X2 = (values_X[i+1] * 10)
            temp_X = abs(temp_X2 - temp_X1)
            temp_X = int(temp_X/10)
            """
            if (values_X[i] > values_X[i+1]):
                X = values_X[i]
                low_X = values_X[i+1]

                while True:
                    X -= 1
                    f = ('%.2f'%X, '%.2f'%Y)
                    available_points.append(f)
                    T = X
                    if ((T+1) <= low_X):
                        break;
            else:
                X = values_X[i]
                high_X = values_X[i+1]
                while True:
                    X += 1
                    f = ('%.2f'%X, '%.2f'%Y)
                    available_points.append(f)
                    T = X
                    if ((T+1) >= high_X):
                        break;
            

        elif (values_X[i] == values_X[i+1]):
            X = values_X[i]
            
            if (values_Y[i] > values_Y[i+1]):
                Y = values_Y[i]
                low_Y = values_Y[i+1]
                while True:
                    Y -= 1
                    f = ('%.2f'%X, '%.2f'%Y)
                    available_points.append(f)
                    T = Y
                    if ((T+1) <= low_Y):
                        break;
            else:
                Y = values_Y[i]
                high_Y = values_Y[i+1]
                while True:
                    Y += 1
                    f = ('%.2f'%X, '%.2f'%Y)
                    available_points.append(f)
                    T = Y
                    if ((T+1) >= high_Y):
                        break;

        else:
            m = ((values_Y[i+1] - values_Y[i])/(values_X[i+1] - values_X[i]))

            if ((values_X[i+1] > values_X[i]) and (values_Y[i+1] > values_Y[i])):
                hyp = math.sqrt(((values_X[i] - values_X[i+1])**2) + ((values_Y[i] - values_Y[i+1])**2))
                dist_X = values_X[i+1] - values_X[i]
                X_per_unit_hyp = dist_X / hyp
                X = values_X[i]
                high_Y = values_Y[i+1]
                high_X = values_X[i+1]
                while True:
                    X += (1*X_per_unit_hyp)
                    Y = (m*(X - values_X[i])) + values_Y[i]
                    f = ('%.2f'%X, '%.2f'%Y)
                    available_points.append(f)
                    if (Y >= high_Y or X >= high_X):
                        break;

            elif ((values_X[i+1] < values_X[i]) and (values_Y[i+1] > values_Y[i])):
                hyp = math.sqrt(((values_X[i] - values_X[i+1])**2) + ((values_Y[i] - values_Y[i+1])**2))
                dist_X = values_X[i] - values_X[i+1]
                X_per_unit_hyp = dist_X / hyp
                X = values_X[i]
                high_Y = values_Y[i+1]
                low_X = values_X[i+1]
                while True:
                    X -= (1*X_per_unit_hyp)
                    Y = (m*(X - values_X[i])) + values_Y[i]
                    f = ('%.2f'%X, '%.2f'%Y)
                    available_points.append(f)
                    if (Y >= high_Y or X <= low_X):
                        break;
            
            elif ((values_X[i+1] > values_X[i]) and (values_Y[i+1] < values_Y[i])):
                hyp = math.sqrt(((values_X[i] - values_X[i+1])**2) + ((values_Y[i] - values_Y[i+1])**2))
                dist_X = values_X[i+1] - values_X[i]
                X_per_unit_hyp = dist_X / hyp
                X = values_X[i]
                low_Y = values_Y[i+1]
                high_X = values_X[i+1]
                while True:
                    X += (1*X_per_unit_hyp)
                    Y = (m*(X - values_X[i])) + values_Y[i]
                    f = ('%.2f'%X, '%.2f'%Y)
                    available_points.append(f)
                    if (Y <= low_Y or X >= high_X):
                        break;
            
            elif ((values_X[i+1] < values_X[i]) and (values_Y[i+1] < values_Y[i])):
                hyp = math.sqrt(((values_X[i] - values_X[i+1])**2) + ((values_Y[i] - values_Y[i+1])**2))
                dist_X = values_X[i] - values_X[i+1]
                X_per_unit_hyp = dist_X / hyp
                X = values_X[i]
                low_Y = values_Y[i+1]
                low_X = values_X[i+1]
                while True:
                    X -= (1*X_per_unit_hyp)
                    Y = (m*(X - values_X[i])) + values_Y[i]
                    f = ('%.2f'%X, '%.2f'%Y)
                    available_points.append(f)
                    if (Y <= low_Y or X <= low_X):
                        break;

        all_values.extend(available_points)
        available_points.clear()

    x, y = zip(*all_values)
    x = list(map(float, x))
    y = list(map(float, y))
    
    #plt.scatter(x, y)
    #plt.savefig('foo.png', bbox_inches='tight')
    df = pd.DataFrame()
    df['X'] = x
    df['Y'] = y
    fig_inter = px.scatter(df, x = "X", y = "Y")
    fig_inter.show(renderer="browser")
    
    """
    def openNewWindow(): 
        newWindow = Toplevel(window) 
    
        newWindow.title("New Window") 
    
        load = PIL.Image.open("foo.png")
        render = ImageTk.PhotoImage(load)
        img = Label(newWindow, image=render)
        img.image = render
        img.pack()
    #openNewWindow()
    """


def add_extru(a, b, c, t): 
    fullcode = text_box.get("1.0", tk.END)
    matcher = r"Layer count: ([\d]*)"
    layer_count = re.findall(matcher, fullcode)
    layer_count = int(layer_count[0])
    layer_count = layer_count - 1
    layer_count = str(layer_count)
    layer_finder = "; LAYER:"+layer_count
    top_code="\n"
    init_gcode1="\n"
    low_code="\n"
    finder_flag=0
    for lines in fullcode.splitlines():
        if lines != layer_finder and finder_flag == 0:
            top_code = top_code+lines+"\n"
        if lines == layer_finder:
            finder_flag = 1
        if lines == "M107" and finder_flag == 1:
            finder_flag = 2
        if finder_flag == 1:
            init_gcode1 = init_gcode1+lines+"\n"
        if finder_flag == 2:
            low_code = low_code+lines+"\n"
    regex_Z = r"Z([\d]+\.?[\d]+)"
    matches_Z = re.findall(regex_Z, init_gcode1)
    regex_E = r"E([\d]+\.?[\d]+)"
    matches_E = re.findall(regex_E, init_gcode1)
    regex_F = r"F([\d]+\.?[\d]+)"
    matches_F = re.findall(regex_F, init_gcode1)

    values_X = []
    values_Y = []
    values_Z = []
    values_E = []
    values_F = []

    for lines in init_gcode1.splitlines():
        if lines == "; MatterSlice Completed Successfully":
            break;

        if (lines != "" and lines[0] == "G"):
            X_reg = r"X([\d]+\.?[\d]+)"
            X_check = re.findall(X_reg, lines)
            Y_reg = r"Y([\d]+\.?[\d]+)"
            Y_check = re.findall(Y_reg, lines)
            
            if (len(X_check) == 0):
                values_X.append(values_X[-1])
            else:
                values_X.append(float(X_check[0]))
            
            if (len(Y_check) == 0):
                values_Y.append(values_Y[-1])
            else:
                values_Y.append(float(Y_check[0]))


    for match in matches_Z:
        values_Z.append(float(match))

    for match in matches_E:
        values_E.append(float(match))

    for match in matches_F:
        values_F.append(float(match))
    
    E_val_diff = values_E[1] - values_E[0]
    point_dist = math.sqrt(((values_X[1] - values_X[2])**2) + ((values_Y[1] - values_Y[2])**2))
    E_per_point = (E_val_diff / point_dist)
        
    if (t == 1):
        high_Z = max(values_Z) + 0.1
        low_Z = min(values_Z)
        current_X = values_X[-1]
        current_Y = values_Y[-1]
        line1 = "G1 "+"X"+str(current_X)+" Y"+str(current_Y)+" Z"+str('%.2f'%high_Z)+" F"+str(values_F[-1])
        line2 = "G1 "+"X"+str(a)+" Y"+str(b)+" Z"+str('%.2f'%high_Z)+" F"+str(values_F[-1])
        line3 = "G1 "+"X"+str(a)+" Y"+str(b)+" Z"+str('%.2f'%(low_Z))+" F"+str(values_F[-1])
        e = (E_per_point * float(c)) + values_E[-1]
        line4 = "G1 "+"X"+str(a)+" Y"+str(b)+" Z"+str(c)+" E"+str('%.3f'%e)+" F"+str(values_F[-1])
        code_addition = "\n"+line1+"\n"+line2+"\n"+line3+"\n"+line4
        final_code = top_code+init_gcode1+code_addition+low_code
        text_box.delete("1.0", "end")
        return text_box.insert(END, final_code)
    elif (t == 0):
        high_Z = max(values_Z) + 0.1
        low_Z = min(values_Z)
        current_X = values_X[-1]
        current_Y = values_Y[-1]
        line1 = "G1 "+"X"+str(current_X)+" Y"+str(current_Y)+" Z"+str('%.2f'%high_Z)+" F"+str(values_F[-1])
        line2 = "G1 "+"X"+str(a)+" Y"+str(b)+" Z"+str('%.2f'%high_Z)+" F"+str(values_F[-1])
        line3 = "G1 "+"X"+str(a)+" Y"+str(b)+" Z"+str('%.2f'%(low_Z))+" F"+str(values_F[-1])
        line4 = "G1 "+"X"+str(a)+" Y"+str(b)+" Z"+str(c)+" F"+str(values_F[-1])
        code_addition = "\n"+line1+"\n"+line2+"\n"+line3+"\n"+line4
        final_code = top_code+init_gcode1+code_addition+low_code
        text_box.delete("1.0", "end")
        return text_box.insert(END, final_code)


def finish():
    fullcode = text_box.get("1.0", tk.END)
    matcher = r"Layer count: ([\d]*)"
    layer_count = re.findall(matcher, fullcode)
    layer_count = int(layer_count[0])
    layer_count = layer_count - 1
    layer_count = str(layer_count)
    layer_finder = "; LAYER:"+layer_count
    top_code="\n"
    init_gcode1="\n"
    low_code="\n"
    finder_flag=0
    for lines in fullcode.splitlines():
        if lines != layer_finder and finder_flag == 0:
            top_code = top_code+lines+"\n"
        if lines == layer_finder:
            finder_flag = 1
        if lines == "M107" and finder_flag == 1:
            finder_flag = 2
        if finder_flag == 1:
            init_gcode1 = init_gcode1+lines+"\n"
        if finder_flag == 2:
            low_code = low_code+lines+"\n"
    m400 = "M400 \n"
    text_box.delete("1.0", "end")
    final_code = top_code+init_gcode1+m400+low_code
    return text_box.insert(END, final_code)
    

#button0 = tk.Button(frame1, text="Fetch Top Layer", command=fetch_top, relief="raised")
button1 = tk.Button(frame1, text="Show Available Points",command=avail_points, borderwidth = 3, relief="raised")

button2 = tk.Button(frame5, text="Add Movement", command= lambda: add_extru(entryX.get(), entryY.get(), entryZ.get(), var1.get()), relief="raised")
button3 = tk.Button(frame5, text="Finish", command=finish, relief="raised")

cont_X_pt = tk.Button(frame2, text="+0.1", command=cont_X_01, width=10)
cont_X = tk.Button(frame2, text="+1", command=cont_X_1, width=10)

cont_Y_pt = tk.Button(frame3, text="+0.1", command=cont_Y_01, width=10)
cont_Y = tk.Button(frame3, text="+1", command=cont_Y_1, width=10)

cont_Z_pt = tk.Button(frame4, text="+0.1", command=cont_Z_01, width=10)
cont_Z = tk.Button(frame4, text="+1", command=cont_Z_1, width=10)


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

c1.pack(pady=10)
button2.pack(padx=5, pady=10, side=tk.LEFT)
button3.pack(padx=5, pady=10, side=tk.LEFT)

container.pack()
canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

window.mainloop()