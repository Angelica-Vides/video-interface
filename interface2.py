# the libraries
import PySimpleGUI as sg
from tkinter import *
import cv2 as cv
import os
import numpy as np
import time
import threading
import csv
import matplotlib
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

width, height = 1920, 1080
frame_size = width * height * 3 // 2
current_frame = 0
stop = False

matplotlib.use('TkAgg')
w, h = figsize = (5, 3)     # figure size
fig = matplotlib.figure.Figure(figsize=figsize)
dpi = fig.get_dpi()
size = (w*dpi, h*dpi) 

def update(n_frames, f, window2):
    global current_frame
    global stop
    for i in range(n_frames - current_frame):
        if (stop):
            break
        f.seek(current_frame * frame_size)
        yuv = np.frombuffer(f.read(frame_size), dtype=np.uint8).reshape((height * 3 // 2, width))
        bgr = cv.cvtColor(yuv, cv.COLOR_YUV2BGR_I420)
        # converts to png file
        image = cv.imwrite('bgr.png', bgr)
        window2['video'].update(filename='bgr.png', visible=True, subsample=3)
        current_frame += 1
        time.sleep(1)


def updateFrameLoop():
    global current_frame
    if (current_frame >= n_frames):
        current_frame = 0
    elif (current_frame < 0):
        current_frame = n_frames - 1

def updateFrame(f, window2):
    updateFrameLoop()
    f.seek(current_frame * frame_size)
    yuv = np.frombuffer(f.read(frame_size), dtype=np.uint8).reshape((height * 3 // 2, width))
    bgr = cv.cvtColor(yuv, cv.COLOR_YUV2BGR_I420)
    # converts to png file
    image = cv.imwrite('bgr.png', bgr)
    window2['video'].update(filename='bgr.png', visible=True, subsample=3)

def get_list(string_name):
    file = open(string_name,'r', encoding='utf-8-sig')
    type(file)
    csvreader = csv.reader(file)
    dataSet = []
    for row in csvreader:
        dataSet.append(row)
    dataSet
    file.close

    dataSet_final = [list(map(int, i)) for i in dataSet]
    return dataSet_final

def get_histogram(frame):

    barWidth = 0.25
    fig = plt.subplots(figsize = (12,8))

    Values_for_Y = 'AVERAGE_HISTOGRAM_Y.csv'
    Values_for_U = 'AVERAGE_HISTOGRAM_U.csv'
    Values_for_v = 'AVERAGE_HISTOGRAM_V.csv'

    Varince_for_Y = 'VARIANCE_HISTOGRAM_Y.csv'
    Varince_for_U = 'VARIANCE_HISTOGRAM_U.csv'
    Varince_for_V = 'VARIANCE_HISTOGRAM_V.csv'


    XforYvalues = get_list(Values_for_Y)
    XforUvalues = get_list(Values_for_U)
    XforVvaleus = get_list(Values_for_v)

    xforYforVarience = get_list(Varince_for_Y)
    xforUforVarience = get_list(Varince_for_U)
    xforVforVarience = get_list(Varince_for_V)

    y = []
    for i in range(0, 16):
        y.append(str(i + 1))

    print(y)

    print(XforYvalues[frame])
    print(xforYforVarience[frame])


    x =  [str(z) for z in y]
    barWidth =.25
    bar1 = np.arange(len(y))
    bar2 = [x + barWidth for x in bar1]
    bar3 = [x + barWidth for x in bar2]
    ##r1 = np.arange()

    plt.subplot(1,2,1)
    plt.bar(bar1,XforYvalues[frame], color = 'g', width = barWidth, edgecolor = 'grey', label = 'Y')
    plt.bar(bar2,XforUvalues[frame], color = 'b', width = barWidth,edgecolor = 'grey', label = 'U')
    plt.bar(bar3,XforVvaleus[frame], color = 'r', width = barWidth,edgecolor = 'grey', label = 'v')
    plt.xlabel('Bins', fontweight = 'bold', fontsize = 20)


    plt.title("{Frame "+str(current_frame)+'} 8x8 Average 16 Bins')
    plt.legend()

    ##res = [eval(i) for i in dataSet[0]]

    plt.subplot(1,2,2)
    plt.bar(bar1,xforYforVarience[frame], color = 'g', width = barWidth, edgecolor = 'grey', label = 'Y')
    plt.bar(bar2,xforUforVarience[frame], color = 'b', width = barWidth, edgecolor = 'grey', label = 'U')
    plt.bar(bar3,xforUforVarience[frame], color = 'r', width = barWidth, edgecolor = 'grey', label = 'V')
    plt.title('8x8 Variance 16 Bins')
    plt.xlabel('Bins', fontweight = 'bold', fontsize = 20)


    plt.legend()
    return plt.gcf()


def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg


# the color of the background
sg.theme("DarkTeal")

# The menu that is found at the top after starting the interface
menu_def = [
    ['File', ['Open', 'Save', 'Exit']],
    ['Edit', ['Paste', ['Special', 'Normal', ], 'Undo']],
    ['Help', 'About...']
]

# the layout/design of the window
layout = [
    [sg.Text('Video Interface', size=(40,0))],
    [sg.Multiline(size=(80, 10))],
    [sg.Button('Open'), sg.Button('Exit')]
]

# when window1 is opened the title of the interface and layout is displayed
window1 = sg.Window('Video Interface', layout)

# window2 is inactive when window1 is open
window2_active = False

while True:
    event, values = window1.read()
    if event in (sg.WIN_CLOSED, 'Exit'):
        break
    elif event == 'Open':

        # when the open button is clicked then a popup will appear to prompt the use to open
        # a file
        text = sg.PopupGetFile('Please enter a file name')
        sg.Popup('Results', text)

        # window1 will then close and window2 will open
        window2_active = True
        window1.Hide()

        file_size = os.path.getsize(text)
        n_frames = file_size // (frame_size)

        f = open(text, 'rb')
        yuv = np.frombuffer(f.read(frame_size), dtype=np.uint8).reshape((height * 3 // 2, width))
        bgr = cv.cvtColor(yuv, cv.COLOR_YUV2BGR_I420)

        # converts to png file
        image = cv.imwrite('bgr.png', bgr)
        
        layout2 = [
            
            [sg.Image(filename='bgr.png', key='video', subsample=3)],
            [sg.Button('<<'),
             sg.Button('Play'),
             sg.Button('Pause'),
             sg.Button('>>')],
            [sg.Canvas(size=size, key='-CANVAS-')]

            
            ]
        
        window2 = sg.Window('Window 2', layout2, finalize=True, size=(850, 650), element_justification='c')
        draw_figure(window2['-CANVAS-'].TKCanvas, get_histogram(current_frame))
        
        while True:

            event2, values = window2.Read()
            
            if event2 == '>>':
                current_frame += 1
                updateFrame(f, window2)

            elif event2 == 'Play':
                stop = False
                threading.Thread(target=update, args=(n_frames, f, window2)).start()
                get_histogram(n_frames) 
                #draw_figure(canvas, figure)               

            elif event2 == 'Pause':
                stop = True


            elif event2 == '<<':
                current_frame -= 1
                updateFrame(f, window2)

            elif event2 is None:
                        window2.Close()  
                        window2_active = False  
                        window1.UnHide()  
                        break

                
                    

        
           