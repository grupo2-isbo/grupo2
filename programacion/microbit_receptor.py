from microbit import
import radio

radio_group = 5

def set_color(r, g, b): #set color in leds
    pins.analog_write_pin(AnalogPin.P1, r) # P1 is the pin number 1 of the microbit/arduino
    pins.analog_write_pin(AnalogPin.P2, g)
    pins.analog_write_pin(AnalogPin.P4, b)

def sColor(color):
    if color == "Red":
        set_color(1023, 0, 0) # Red
    elif color == "Green":
        set_color(0, 1023, 0) # Green
    elif color == "Blue":
        set_color(0, 0, 1023) # Blue
    elif color == "White":
        set_color(1023, 1023, 1023) # White
    else:
        raise("Invalid Color.")

def radioReceiver(name, ruido):
    if ruido <= 86:
        sColor("Green") # Green
        basic.show_string("G")
        print("G")
        basic.pause(300)
    elif ruido > 86 and ruido <= 171:
        sColor("Orange") # Orange, like in a traffic light
        print("O")
        basic.show_string("O")
        basic.pause(300)
    elif ruido > 171:
        sColor("Red") # Red
        print("R")
        basic.show_string("R")
        basic.pause(300)
    else:
        sColor("White") # White
        print("W")
        basic.show_string("W")
        basic.pause(300)

def on_forever():
    radio.set_group(radio_group)
    radio.on_received_value(radioReceiver)

basic.forever(on_forever)
