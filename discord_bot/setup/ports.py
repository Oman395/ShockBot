import serial.tools.list_ports
ports = serial.tools.list_ports.comports(include_links=False)
for port in ports :
    print(port.device)