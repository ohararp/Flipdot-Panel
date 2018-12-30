import serial
import fcntl
import struct
import time
import numpy as np
import sys
import random
import ntplib
from datetime import datetime,tzinfo,timedelta
import socket, fcntl, struct
import pytz
from pytz import timezone

#*******************************************************************************
# Load a FontTable
#*******************************************************************************
abc=[
    0x00, 0x00, 0x00, 0x00, 0x00, # (space)
	0x00, 0x00, 0x5F, 0x00, 0x00, # !
	0x00, 0x07, 0x00, 0x07, 0x00, # "
	0x14, 0x7F, 0x14, 0x7F, 0x14, # #
	0x24, 0x2A, 0x7F, 0x2A, 0x12, # $
	0x23, 0x13, 0x08, 0x64, 0x62, # %
	0x36, 0x49, 0x55, 0x22, 0x50, # &
	0x00, 0x05, 0x03, 0x00, 0x00, # '
	0x00, 0x1C, 0x22, 0x41, 0x00, # (
	0x00, 0x41, 0x22, 0x1C, 0x00, # )
	0x08, 0x2A, 0x1C, 0x2A, 0x08, # *
	0x08, 0x08, 0x3E, 0x08, 0x08, # +
	0x00, 0x50, 0x30, 0x00, 0x00, # ,
	0x08, 0x08, 0x08, 0x08, 0x08, # -
	0x00, 0x60, 0x60, 0x00, 0x00, # .
	0x20, 0x10, 0x08, 0x04, 0x02, # /
	0x3E, 0x51, 0x49, 0x45, 0x3E, # 0
	0x00, 0x42, 0x7F, 0x40, 0x00, # 1
	0x42, 0x61, 0x51, 0x49, 0x46, # 2
	0x21, 0x41, 0x45, 0x4B, 0x31, # 3
	0x18, 0x14, 0x12, 0x7F, 0x10, # 4
	0x27, 0x45, 0x45, 0x45, 0x39, # 5
	0x3C, 0x4A, 0x49, 0x49, 0x30, # 6
	0x01, 0x71, 0x09, 0x05, 0x03, # 7
	0x36, 0x49, 0x49, 0x49, 0x36, # 8
	0x06, 0x49, 0x49, 0x29, 0x1E, # 9
	0x00, 0x36, 0x36, 0x00, 0x00, # :
	0x00, 0x56, 0x36, 0x00, 0x00, # ;
	0x00, 0x08, 0x14, 0x22, 0x41, # <
	0x14, 0x14, 0x14, 0x14, 0x14, # =
	0x41, 0x22, 0x14, 0x08, 0x00, # >
	0x02, 0x01, 0x51, 0x09, 0x06, # ?
	0x32, 0x49, 0x79, 0x41, 0x3E, # @
	0x7E, 0x11, 0x11, 0x11, 0x7E, # A
	0x7F, 0x49, 0x49, 0x49, 0x36, # B
	0x3E, 0x41, 0x41, 0x41, 0x22, # C
	0x7F, 0x41, 0x41, 0x22, 0x1C, # D
	0x7F, 0x49, 0x49, 0x49, 0x41, # E
	0x7F, 0x09, 0x09, 0x01, 0x01, # F
	0x3E, 0x41, 0x41, 0x51, 0x32, # G
	0x7F, 0x08, 0x08, 0x08, 0x7F, # H
	0x00, 0x41, 0x7F, 0x41, 0x00, # I
	0x20, 0x40, 0x41, 0x3F, 0x01, # J
	0x7F, 0x08, 0x14, 0x22, 0x41, # K
	0x7F, 0x40, 0x40, 0x40, 0x40, # L
	0x7F, 0x02, 0x04, 0x02, 0x7F, # M
	0x7F, 0x04, 0x08, 0x10, 0x7F, # N
	0x3E, 0x41, 0x41, 0x41, 0x3E, # O
	0x7F, 0x09, 0x09, 0x09, 0x06, # P
	0x3E, 0x41, 0x51, 0x21, 0x5E, # Q
	0x7F, 0x09, 0x19, 0x29, 0x46, # R
	0x46, 0x49, 0x49, 0x49, 0x31, # S
	0x01, 0x01, 0x7F, 0x01, 0x01, # T
	0x3F, 0x40, 0x40, 0x40, 0x3F, # U
	0x1F, 0x20, 0x40, 0x20, 0x1F, # V
	0x7F, 0x20, 0x18, 0x20, 0x7F, # W
	0x63, 0x14, 0x08, 0x14, 0x63, # X
	0x03, 0x04, 0x78, 0x04, 0x03, # Y
	0x61, 0x51, 0x49, 0x45, 0x43, # Z
	0x00, 0x00, 0x7F, 0x41, 0x41, # [
	0x02, 0x04, 0x08, 0x10, 0x20, # "\"
	0x41, 0x41, 0x7F, 0x00, 0x00, # ]
	0x04, 0x02, 0x01, 0x02, 0x04, # ^
	0x40, 0x40, 0x40, 0x40, 0x40, # _
	0x00, 0x01, 0x02, 0x04, 0x00, # `
	0x20, 0x54, 0x54, 0x54, 0x78, # a
	0x7F, 0x48, 0x44, 0x44, 0x38, # b
	0x38, 0x44, 0x44, 0x44, 0x20, # c
	0x38, 0x44, 0x44, 0x48, 0x7F, # d
	0x38, 0x54, 0x54, 0x54, 0x18, # e
	0x08, 0x7E, 0x09, 0x01, 0x02, # f
	0x08, 0x14, 0x54, 0x54, 0x3C, # g
	0x7F, 0x08, 0x04, 0x04, 0x78, # h
	0x00, 0x44, 0x7D, 0x40, 0x00, # i
	0x20, 0x40, 0x44, 0x3D, 0x00, # j
	0x00, 0x7F, 0x10, 0x28, 0x44, # k
	0x00, 0x41, 0x7F, 0x40, 0x00, # l
	0x7C, 0x04, 0x18, 0x04, 0x78, # m
	0x7C, 0x08, 0x04, 0x04, 0x78, # n
	0x38, 0x44, 0x44, 0x44, 0x38, # o
	0x7C, 0x14, 0x14, 0x14, 0x08, # p
	0x08, 0x14, 0x14, 0x18, 0x7C, # q
	0x7C, 0x08, 0x04, 0x04, 0x08, # r
	0x48, 0x54, 0x54, 0x54, 0x20, # s
	0x04, 0x3F, 0x44, 0x40, 0x20, # t
	0x3C, 0x40, 0x40, 0x20, 0x7C, # u
	0x1C, 0x20, 0x40, 0x20, 0x1C, # v
	0x3C, 0x40, 0x30, 0x40, 0x3C, # w
	0x44, 0x28, 0x10, 0x28, 0x44, # x
	0x0C, 0x50, 0x50, 0x50, 0x3C, # y
	0x44, 0x64, 0x54, 0x4C, 0x44, # z
	0x00, 0x08, 0x36, 0x41, 0x00, # {
	0x00, 0x00, 0x7F, 0x00, 0x00, # |
	0x00, 0x41, 0x36, 0x08, 0x00, # }
	0x08, 0x08, 0x2A, 0x1C, 0x08, # ->
	0x08, 0x1C, 0x2A, 0x08, 0x08, # <-
]
abcIdx=np.arange(0,96*5,5)
#*******************************************************************************
# Setup RS-485 Port
#*******************************************************************************
ser = serial.Serial(
    port='/dev/ttyO4', 
    baudrate=38400, 
    timeout=1,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)
 
# Standard Linux RS485 ioctl:
TIOCSRS485 = 0x542F
 
# define serial_rs485 struct per Michael Musset's patch that adds gpio RE/DE 
# control:
# (https:#github.com/RobertCNelson/bb-kernel/blob/am33x-v3.8/patches/fixes/0007-omap-RS485-support-by-Michael-Musset.patch#L30)
SER_RS485_ENABLED         = (1 << 0)
SER_RS485_RTS_ON_SEND     = (1 << 1)
SER_RS485_RTS_AFTER_SEND  = (1 << 2)
SER_RS485_RTS_BEFORE_SEND = (1 << 3)
SER_RS485_USE_GPIO        = (1 << 5)
 
# Enable RS485 mode using a GPIO pin to control RE/DE: 
RS485_FLAGS = SER_RS485_ENABLED | SER_RS485_USE_GPIO 
# With this configuration the GPIO pin will be high when transmitting and low
# when not
 
# If SER_RS485_RTS_ON_SEND and SER_RS485_RTS_AFTER_SEND flags are included the
# RE/DE signal will be inverted, i.e. low while transmitting
 
# The GPIO pin to use, using the Kernel numbering: 
RS485_RTS_GPIO_PIN = 48 # GPIO1_16 -> GPIO(1)_(16) = (1)*32+(16) = 48
 
# Pack the config into 8 consecutive unsigned 32-bit values:
# (per  struct serial_rs485 in patched serial.h)
serial_rs485 = struct.pack('IIIIIIII', 
                           RS485_FLAGS,        # config flags
                           0,                  # delay in us before send
                           0,                  # delay in us after send
                           RS485_RTS_GPIO_PIN, # the pin number used for DE/RE
                           0, 0, 0, 0          # padding - space for more values 
                           )
 
# Apply the ioctl to the open ttyO4 file descriptor:
fd=ser.fileno()
fcntl.ioctl(fd, TIOCSRS485, serial_rs485)

#*******************************************************************************
def sendPack (cmd, addr, data):
    # Packet Information 
    # 0x80 beginning 
    #-----
    # 0x81 - 112 bytes / no refresh / C+3E
    # 0x82 - refresh
    # 0x83 - 28 bytes of data / refresh / 2C
    # 0x84 - 28 bytes of data / no refresh / 2C
    # 0x85 - 56 bytes of data / refresh / C+E
    # 0x86 - 56 bytes of data / no refresh / C+E
    ByteHeader  = 0x80     
    ByteEnd     = 0x8F    
    ByteCols    = 28
    ser.write(chr(ByteHeader))
    ser.write(chr(cmd))
    ser.write(chr(addr))
    for n in range (0,ByteCols):
        ser.write(chr(data[n]))
    
    ser.write(chr(ByteEnd))

#*******************************************************************************
# Declare a Random Data Array
def flipRand (size):
    result = [0] * size
    for n in range (0,size):
        result[n] = random.randrange(0,256,1)
    return result
#*******************************************************************************
# Allow to shift an array to the left of right
def shift(key, array):
    return array[key % len(array):] + array[:key % len(array)]
    
#*******************************************************************************
# Read a character in and spit out np.array of font 1x5 format
def charLook (char0):
    char0int = ord(char0)           # lookup int value of character
    char0offset = char0int - 32     # subtract 32 to match abc font table
    char0array = [0]*6              # create empty array
    for x in range(0,5):
        char0array[x] = abc[abcIdx[char0offset]+x]
    char0array[5] = 0               #pad with a space at the end
    return char0array
#*******************************************************************************
# Read a character in and spit out np.array of font 1x6 format
def loadMessage (mString):
    result = [0] * len(mString) * 6
    ctr = 0
    for m in range (0,len(mString)):
        # print mString[m]
        charData = charLook(mString[m])
        # print charData
        for n in range (0,6):
            result[ctr]=charData[n]
            ctr += 1
    return result
#*******************************************************************************
# Index Message Data to the Frame
def loadFrame(size,data):
    result = [0] * size
    for m in range (0,size):
        if m < len(data):
            result[m] = data[m]
        else:
            result[m] = 0
    return result
#*******************************************************************************
# Get Ip Address Function   
def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])    
#*******************************************************************************
# Setup 
#*******************************************************************************

# FlipDot Display Setup
cols   = 56
rows   = 7
cmd = 0x83
adr0 = 0x00
adr1 = 0x01

# Visual Data
flipWht = [255] * cols
flipBlk = [0] * cols
flipOne = flipBlk
flipOne[0]= 255


# Message Display Variables
maxLength = 140            # Max Length of a message    
maxData = [0] * maxLength * 6 # Create an array 6x (width of 5x7 font) the # of chars
msgPad = '          ' # 10 characters = 60 cols
msg = msgPad + 'Time to Read Books!!!'
msgData = [0] * 140 * 6
msgPad = [0]*cols

#Blank the Display
for x in range(0,5):
	sendPack(cmd,adr0,flipWht[28:56])
	sendPack(cmd,adr1,flipWht[28:56])
	time.sleep(1)
	sendPack(cmd,adr0,flipBlk[28:56])
	sendPack(cmd,adr1,flipBlk[28:56])


# Setup Initial Call to NTP Server and Get Time
class Zone(tzinfo):
    def __init__(self,offset,isdst,name):
        self.offset = offset
        self.isdst = isdst
        self.name = name
    def utcoffset(self, dt):
        return timedelta(hours=self.offset) + self.dst(dt)
    def dst(self, dt):
            return timedelta(hours=1) if self.isdst else timedelta(0)
    def tzname(self,dt):
         return self.name

GMT = Zone(0,False,'GMT')
EST = Zone(-5,False,'EST')
EDT = Zone(-4,False,'EDT')
x = ntplib.NTPClient()
datetime.utcfromtimestamp(x.request('pool.ntp.org').tx_time)
print datetime.utcnow().strftime('UTC = %m/%d/%Y %H:%M:%S %Z')
print datetime.now(GMT).strftime('GMT = %m/%d/%Y %H:%M:%S %Z')
print datetime.now(EST).strftime('EST = %m/%d/%Y %H:%M:%S %Z')
print datetime.now(EST).strftime('MSG = %H:%M %a')

# Setup PYTZ
eastern = timezone('US/Eastern')

utc_dt=datetime.now(pytz.utc)
loc_dt=utc_dt.astimezone(eastern)
msgDst =loc_dt.strftime('%H:%M %a')
print msgDst


# Get IP Address and Dispay this
print get_ip_address('wlan2')
msg = ' ' + get_ip_address('wlan2') + ' ' 
msgData = loadMessage(msg)

for m in range (0,125):
    msgData = shift(1,msgData)
    frame = loadFrame(cols,msgData)
    sendPack(cmd,adr0,frame[0:28])
    sendPack(cmd,adr1,frame[28:56])
    time.sleep(.1)

#*******************************************************************************
# Main 
#*******************************************************************************

while 1:
	
	utc_dt=datetime.now(pytz.utc)
	loc_dt=utc_dt.astimezone(eastern)
	msgDst =loc_dt.strftime('%H:%M %a')
	
	msgData = loadMessage(msgDst)
	frame = loadFrame(cols,msgData)
	sendPack(cmd,adr0,frame[0:28])
	sendPack(cmd,adr1,frame[28:56])
	time.sleep(0.9)
ser.close()
