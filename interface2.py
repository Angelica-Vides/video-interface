#YUV Video Interface

#Copyright © 2022 2022-Grp17-Fast-Histograms

#Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated 
#documentation files (the "Software"), to deal in the Software without restriction, including without limitation 
#the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and 
#to permit persons to whom the Software is furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in all copies or substantial portions of 
#the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO 
#THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, 
#TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# the libraries
import PySimpleGUI as sg
from tkinter import *
import cv2 as cv
import os
import numpy as np
import time
import threading


width, height = 1920, 1080
frame_size = width * height * 3 // 2
current_frame = 0
stop = False



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
        window2['video'].update(filename='bgr.png', visible=True, subsample=2)
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
    window2['video'].update(filename='bgr.png', visible=True, subsample=2)




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
            
            [sg.Image(filename='bgr.png', key='video', subsample=2)],
            [sg.Button('<<'),
             sg.Button('Play'),
             sg.Button('Pause'),
             sg.Button('>>')]
            

            
            ]
        
        window2 = sg.Window('Window 2', layout2, finalize=True, element_justification='c')
       
        
        while True:

            event2, values = window2.Read()
            
            if event2 == '>>':
                current_frame += 1
                updateFrame(f, window2)

            elif event2 == 'Play':
                stop = False
                threading.Thread(target=update, args=(n_frames, f, window2)).start()
                             

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

                
                    

        
           