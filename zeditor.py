import plotly.express as px
import tkinter as tk
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
window.title("Vertical 3D Printing")
frame1 = Frame(window)
frame2 = Frame(window)
frame3 = Frame(window)
frame4 = Frame(window)
frame5 = Frame(window)
frame1.pack()
frame2.pack()
frame3.pack()
frame4.pack()
frame5.pack()
scrollbar = Scrollbar(window)

greetings = tk.Label(frame1, text="G-Code Editor")
greetings.pack(pady=10)



entryX = tk.Entry(frame2, borderwidth = 3, relief="sunken")
entryX.insert(0, "Enter X Value")
entryY = tk.Entry(frame3, borderwidth = 3, relief="sunken")
entryY.insert(0, "Enter Y Value")
entryZ = tk.Entry(frame4, borderwidth = 3, relief="sunken")
entryZ.insert(0, "Enter Z Value")

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

def avail_points():
    init_gcode = text_box.get("1.0", tk.END)
    regex_X = r"X([\d]*\.?[\d]*)"
    matches_X = re.findall(regex_X, init_gcode)
    regex_Y = r"Y([\d]*\.?[\d]*)"
    matches_Y = re.findall(regex_Y, init_gcode)
    regex_Z = r"Z([\d]*\.?[\d]*)"
    matches_Z = re.findall(regex_Z, init_gcode)
    regex_E = r"E([\d]*\.?[\d]*)"
    matches_E = re.findall(regex_E, init_gcode)
    regex_F = r"F([\d]*\.?[\d]*)"
    matches_F = re.findall(regex_F, init_gcode)

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
    
    def openNewWindow(): 
        newWindow = Toplevel(window) 
    
        newWindow.title("New Window") 
    
        load = PIL.Image.open("foo.png")
        render = ImageTk.PhotoImage(load)
        img = Label(newWindow, image=render)
        img.image = render
        img.pack()
    #openNewWindow()
    


def add_extru(a, b, c, t):
    init_gcode1 = text_box.get("1.0", tk.END)
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
        return text_box.insert(tk.END, code_addition)
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
        return text_box.insert(tk.END, code_addition)




button1 = tk.Button(frame1, text="Show Available Points",command=avail_points, borderwidth = 3, relief="raised", bg='blue')

button2 = tk.Button(frame5, text="Add Movement", command= lambda: add_extru(entryX.get(), entryY.get(), entryZ.get(), var1.get()))

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
button2.pack(pady=10)

window.mainloop()


