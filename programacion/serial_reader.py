import time as t
from datetime import datetime
import serial
import serial.tools.list_ports as list_ports
import subprocess
import sys
import os

def openWebsite():
    html_path = os.path.abspath('./microbit.html')
    
    if sys.platform.startswith('linux'):
        subprocess.run(['sudo', '-u', os.getenv('SUDO_USER', 'fabrizio'),
                        'xdg-open', html_path])
    elif sys.platform.startswith('win'):
        pass
        subprocess.run(['start', html_path], shell=True)
    elif sys.platform.startswith('darwin'):
        pass
        subprocess.run(['open', html_path])
    else:
        print("Sistema operativo no reconocido.")


PID_MICROBIT = 516
VID_MICROBIT = 3368
TIMEOUT = 0.1

def find_comport(pid, vid, baud):
    ser_port = serial.Serial(timeout=TIMEOUT)
    ser_port.baudrate = baud
    ports = list(list_ports.comports())
    for p in ports:
        try:
            if (p.pid == pid) and (p.vid == vid):
                ser_port.port = str(p.device)
                return ser_port
        except AttributeError:
            continue
    return None


def main():
    print('Buscando micro:bit...')
    ser_micro = find_comport(PID_MICROBIT, VID_MICROBIT, 115200)
    if not ser_micro:
        print('micro:bit no encontrado')
        return
    else:
        print("micro:bit encontrado. Abriendo servicio web...")
        openWebsite()


    ser_micro.open()
    oldLines = []
    line = ""

    while True:
        t.sleep(1.4)
        nline = ser_micro.readline().decode('utf-8').strip()
        if nline=="G":
            line = "🟩"
        elif nline == "R":
            line = "🟥"
        elif nline == "O":
            line = "🟨"
        else:
            line = "⬜"

        line += datetime.now().strftime(" %Y-%m-%d %H:%M:%S")

        print(nline)
        #oldLines += "<p>" + line + "\n </p>"

        if not line:
            continue
        if line == 'EXIT':
            break

        #
        print(line)


        oldLines.append(f"<p>{line}</p>")

        if len(oldLines) > 10:
            oldLines.pop(0)

        # Crea un HTML nuevo en cada lectura
        with open('microbit.html', 'w') as f:
            f.write(f"""
            <html>
                <head>
                    <title>Micro:bit</title>
                    <meta http-equiv="refresh" content="1">
                </head>
                <body>
                    
                    <h2>Último valor recibido:</h2>
                    <strong style="color: green;">{line}</strong>
                    <h3>Ultimos 10 valores recibidos:</h3>
                    <div style="color: red;">
                    {''.join(oldLines)}
                    </div>
                </body>
            </html>
            """)


    ser_micro.close()
    print("EXIT from program")
    sys.exit(0)





if __name__ == "__main__":
    main()
