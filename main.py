# Heart Monitor display
#
# Display for educational purposes only.
# It does NOT function as real monitor control.
#
# System composed of monitor and user controls.
# Wired user control composed of pots and buttons to help instructor
# modify values on screen depending on desired needs.
# Cable to be around 2-3 meter long to help with simulation of actual
# monitoring patient in bed.
#
# Edgar Falcon
# copyright 2023
 
import PySimpleGUI as sg
from gpiozero import MCP3008, Button
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from time import sleep
import numpy as np

button_pin = 17
	
def read_potentiometers():
	
    pot1 = MCP3008(channel=1)
    pot2 = MCP3008(channel=0)
    button = Button(button_pin)
	
    sg.theme('LightGrey6')
    
    custom_font = 'Helvetica, 28'
    
    left_col = [
		[sg.Graph(canvas_size=(500,200), graph_bottom_left=(0,-100), graph_top_right=(600,150), background_color='yellow', key='-GRAPH1-')],
		[sg.Graph(canvas_size=(500,200), graph_bottom_left=(0,-100), graph_top_right=(600,1023), background_color='green', key='-GRAPH2-')]]
    
    right_col = [ 
		[sg.Text('Heart Rate',
				font=custom_font)],
				
		[sg.Text(key='Pot1Value',
				size=(3, 0),
				font=custom_font,
				text_color='Blue'),sg.Text('LPM', size=(0,1))],
				
		[sg.Text('Oxygen',
				font=custom_font,
				size=(8,1))],
				
		[sg.Text(key='Pot2Value',
				size=(3, 2),
				font=custom_font,
				text_color='orange'), sg.Text('% SpO2', size=(0,5))],
				
		[sg.VPush(), sg.Button('Exit')],
		[sg.Canvas(key='-CANVAS-')],
    ]
    
    layout = [
    
		[sg.Column(left_col),
		sg.VSeperator(),
		sg.Column(right_col, element_justification = 'r')]
    ]
    
    #screen_width, screen_height = sg.Window.get_screen_size()
    screen_width, screen_height = 800,576
    window = sg.Window('Vitals Monitor', layout, size=(screen_width, screen_height), finalize=True)
    
    last_x1 = 0 # Store the alst x-position to draw lines
    last_x2 = 0
    last_y1 = 0 # Store the alst y-position to draw lines
    last_y2 = 0
    

    while True:                    
        # Read the potentiometer values
        pot1_current_value = round(pot1.value * 200)  # Scale the value to a range of 0 to 100
        pot2_current_value = round(pot2.value * 100)  # Scale the value to a range of 0 to 100
        
        #update graph for Pot1
        graph1 = window['-GRAPH1-']
        current_x1 = last_x1 + 1 # Increment x position
        graph1.draw_line((last_x1, last_y2), (current_x1, pot1_current_value), color='black', width=2)
        last_x1 = current_x1
        last_y1 = pot2_current_value
 

        #update graph for Pot2
        graph2 = window['-GRAPH2-']
        current_x2 = last_x2 + 1 # Increment x position
        graph2.draw_line((last_x2, last_y2), (current_x2, pot2_current_value), color='black', width=2)
        last_x2 = current_x2
        last_y2 = pot2_current_value
        
        # Check if the button is pressed
        if button.is_pressed:
            #sg.popup("Button pressed! Resetting values to 0.")
            pot1_current_value = 0
            pot2_current_value = 0
            window['Pot1Value'].update(f'{pot1_current_value:.0f}')
            window['Pot2Value'].update(f'{pot2_current_value:.0f}')
            sleep(0.2)  # Add a small delay to debounce the button

        # Update the GUI window
        window['Pot1Value'].update(f'{pot1_current_value:.0f}')
        window['Pot2Value'].update(f'{pot2_current_value:.0f}')

        event, values = window.read(timeout=100)  # Timeout to allow the window to refresh

        if event == sg.WIN_CLOSED or event == 'Exit':
            break

        # if event == 'Clear All':
            # #sg.popup("Button pressed! Resetting values to 0.")
            # pot1_current_value = 0
            # pot1_current_value = 0

        sleep(0.1)

    window.close()

if __name__ == "__main__":
    read_potentiometers()
