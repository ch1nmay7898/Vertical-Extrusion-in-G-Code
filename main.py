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
scrollbar = Scrollbar(window)

greetings = tk.Label(text="Hello")
greetings.pack()

entryX = tk.Entry()
entryX.insert(0, "Enter X Value")
entryY = tk.Entry()
entryY.insert(0, "Enter Y Value")
entryZ = tk.Entry()
entryZ.insert(0, "Enter Z Value")

var1 = tk.IntVar()
c1 = tk.Checkbutton(window, text='Use Extrusion',variable=var1, onvalue=1, offvalue=0)

text_box = tk.Text()


#def counter(co):
    #count = co+1
    #return count


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
            """
            for k in range(temp_X):
            Y = values_Y[i]
            X += 1
            #f = "|" + str('%.2f'%X) + "," + str('%.2f'%Y) + "|"
            f = ('%.2f'%X, '%.2f'%Y)
            available_points.append(f)
            #print('%.2f'%X, '%.2f'%Y, sep=" , ")
            """

        elif (values_X[i] == values_X[i+1]):
            X = values_X[i]
            """
            temp_Y1 = (values_Y[i] * 10)
            temp_Y2 = (values_Y[i+1] * 10)
            temp_Y = abs(temp_Y2 - temp_Y1)
            temp_Y = int(temp_Y/10)
            """
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
            """
            for k in range(temp_Y):
            X = values_X[i]
            if (values_Y[i] > values_Y[i+1]):
                Y -= 1 
            else:
                Y += 1
            #f = "|" + str('%.2f'%X) + "," + str('%.2f'%Y) + "|"
            f = ('%.2f'%X, '%.2f'%Y)
            available_points.append(f)
            #print('%.2f'%X, '%.2f'%Y, sep=" , ")
            """

        else:
            m = ((values_Y[i+1] - values_Y[i])/(values_X[i+1] - values_X[i]))
            """
            temp_X1 = (values_X[i] * 10)
            temp_X2 = (values_X[i+1] * 10)
            temp_X = abs(temp_X2 - temp_X1)
            temp_X = int(temp_X/10)
            """

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


            """
            if (values_X[i] > values_X[i+1]):
            X = values_X[i+1]
            else:
            X = values_X[i]

            for j in range(temp_X):
            if (values_X[i] < values_X[i+1]):
                dist_X = values_X[i+1] - values_X[i]
                hyp = math.sqrt(((values_X[i] - values_X[i+1])**2) + ((values_Y[i] - values_Y[i+1])**2))
                X_per_unit_hyp = dist_X / hyp
                X -= (0.1*X_per_unit_hyp) 
            else:
                dist_X = values_X[i] - values_X[i+1]
                hyp = math.sqrt(((values_X[i] - values_X[i+1])**2) + ((values_Y[i] - values_Y[i+1])**2))
                X_per_unit_hyp = dist_X / hyp
                X += (0.1*X_per_unit_hyp)
            Y = (m*(X - values_X[i])) + values_Y[i]
            #f = "|" + str('%.2f'%X) + "," + str('%.2f'%Y) + "|"
            f = ('%.2f'%X, '%.2f'%Y)
            available_points.append(f)
            #print('%.2f'%X, '%.2f'%Y, sep=",")
            """
        #print(available_points)
        all_values.extend(available_points)
        available_points.clear()
    #print("____________________________________________________________________________________________________________________")

    x, y = zip(*all_values)
    x = list(map(float, x))
    y = list(map(float, y))
    plt.scatter(x, y)
    plt.savefig('foo.png', bbox_inches='tight')
    
    def openNewWindow(): 
        newWindow = Toplevel(window) 
    
        newWindow.title("New Window") 
    
        load = PIL.Image.open("foo.png")
        render = ImageTk.PhotoImage(load)
        img = Label(newWindow, image=render)
        img.image = render
        img.pack()
    openNewWindow()
    
    
    
    """
    all_values = []
    available_points = []
    for i in range(n):
        f_init = ('%.2f'%values_X[i], '%.2f'%values_Y[i])
        available_points.append(f_init)
        f_fin = ('%.2f'%values_X[i+1], '%.2f'%values_Y[i+1])
        available_points.append(f_fin)

        if (values_Y[i] == values_Y[i+1]):
            temp_X1 = (values_X[i] * 10)
            temp_X2 = (values_X[i+1] * 10)
            temp_X = abs(temp_X2 - temp_X1)
            temp_X = int(temp_X/10)
            if (values_X[i] > values_X[i+1]):
                X = values_X[i+1]
            else:
                X = values_X[i]
            for k in range(temp_X):
                Y = values_Y[i]
                X += 1
                #f = "|" + str('%.2f'%X) + "," + str('%.2f'%Y) + "|"
                f = ('%.2f'%X, '%.2f'%Y)
                available_points.append(f)
                #print('%.2f'%X, '%.2f'%Y, sep=" , ")

        elif (values_X[i] == values_X[i+1]):
            temp_Y1 = (values_Y[i] * 10)
            temp_Y2 = (values_Y[i+1] * 10)
            temp_Y = abs(temp_Y2 - temp_Y1)
            temp_Y = int(temp_Y/10)
            if (values_Y[i] > values_Y[i+1]):
                Y = values_Y[i+1]
            else:
                Y = values_Y[i]
            for k in range(temp_Y):
                X = values_X[i]
                if (values_Y[i] > values_Y[i+1]):
                    Y -= 1 
                else:
                    Y += 1
                #f = "|" + str('%.2f'%X) + "," + str('%.2f'%Y) + "|"
                f = ('%.2f'%X, '%.2f'%Y)
                available_points.append(f)
                #print('%.2f'%X, '%.2f'%Y, sep=" , ")

        else:
            m = ((values_Y[i+1] - values_Y[i])/(values_X[i+1] - values_X[i]))
            temp_X1 = (values_X[i] * 10)
            temp_X2 = (values_X[i+1] * 10)
            temp_X = abs(temp_X2 - temp_X1)
            temp_X = int(temp_X/10)
            if (values_X[i] > values_X[i+1]):
                X = values_X[i+1]
            else:
                X = values_X[i]

            for j in range(temp_X):
                if (values_X[i] < values_X[i+1]):
                    dist_X = values_X[i+1] - values_X[i]
                    hyp = math.sqrt(((values_X[i] - values_X[i+1])**2) + ((values_Y[i] - values_Y[i+1])**2))
                    X_per_unit_hyp = dist_X / hyp
                    X -= (0.1*X_per_unit_hyp) 
                else:
                    dist_X = values_X[i] - values_X[i+1]
                    hyp = math.sqrt(((values_X[i] - values_X[i+1])**2) + ((values_Y[i] - values_Y[i+1])**2))
                    X_per_unit_hyp = dist_X / hyp
                    X += (0.1*X_per_unit_hyp)
                Y = (m*(X - values_X[i])) + values_Y[i]
                #f = "|" + str('%.2f'%X) + "," + str('%.2f'%Y) + "|"
                f = ('%.2f'%X, '%.2f'%Y)
                available_points.append(f)
                #print('%.2f'%X, '%.2f'%Y, sep=",")

        #print(available_points)
        all_values.extend(available_points)
        available_points.clear()
    """

  
    


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




button1 = tk.Button(text="View Points",command=avail_points)
button2 = tk.Button(text="Add Z-Movement", command= lambda: add_extru(entryX.get(), entryY.get(), entryZ.get(), var1.get()))

text_box.pack()
button1.pack()
entryX.pack()
entryY.pack()
entryZ.pack()
c1.pack()
button2.pack()

window.mainloop()


