from microbit import *
import radio

def on_forever():
    ruido = Environment.read_noise(AnalogPin.P1)
    #serial.write_value("ruido", ruido)

    radio.set_group(5)
    radio.send_value("ruido", ruido)

    if ruido > 10:
        basic.show_string("W") # works
    else:
        basic.show_string("E") # error

basic.forever(on_forever)
