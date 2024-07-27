import serial
from helpers import jsonHelper
config = jsonHelper.loadConfig()
arduino = serial.Serial(port=config["port"], baudrate=115200, timeout=.1)