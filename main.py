from m5stack import *
from m5ui import *
import i2c_bus

clear_bg(0x222222)

btnA = M5Button(name="ButtonA", text="ButtonA", visibility=False)
btnB = M5Button(name="ButtonB", text="ButtonB", visibility=False)
btnC = M5Button(name="ButtonC", text="ButtonC", visibility=False)


i2c_l = i2c_bus.get(i2c_bus.PORTA)
i2cAddr = (0x22 >> 1)

def register_short(register, value=None, buf=bytearray(2)):
  if value is None:
    i2c_l.readfrom_mem_into(i2cAddr, register, buf)
    return buf[0]*256 + buf[1]
  buf[0] = (value & 0xff00) >> 8
  buf[1] = value & 0x00ff
  i2c_l.writeto_mem(i2cAddr, register, buf)

def write_u16(address, val):
  return register_short(address, val)

def read_u16(address):
  return register_short(address)

def updateRegister(reg, mask, value):
  write_u16(reg, (read_u16(reg) & ~mask | value))

RDA5807M_BAND_WEST = (0x0 << 2)
RDA5807M_BAND_JAPAN = (0x1 << 2)
RDA5807M_BAND_WORLD = (0x2 << 2)
RDA5807M_BAND_EAST = (0x3 << 2)
RDA5807M_REG_CHIPID = 0x00  
RDA5807M_REG_CONFIG = 0x02
RDA5807M_REG_TUNING = 0x03
RDA5807M_REG_VOLUME = 0x05
RDA5807M_VOLUME_MASK = 0x000F
RDA5807M_FLG_SEEKUP = 0x0200
RDA5807M_FLG_SEEK = 0x0100
RDA5807M_FLG_SKMODE = 0x0080
RDA5807M_FLG_RDS = 0x0008
RDA5807P_FLG_I2SSLAVE = 0x1000
RDA5807M_STATUS_STC = 0x4000
RDA5807M_FLG_DHIZ = 0x8000
RDA5807M_FLG_NEW = 0x0004
RDA5807M_FLG_ENABLE = 0x0001
RDA5807M_BAND_MASK = 0x000C
RDA5807M_FLG_DMUTE = 0x4000
RDA5807M_VOLUME_MASK = 0x000F
MUTE = False

#lcd.clear()
#lcd.print(volume, 0, 0, 0xffffff)

def seekDown():
  updateRegister(RDA5807M_REG_CONFIG, (RDA5807M_FLG_SEEKUP | RDA5807M_FLG_SEEK | RDA5807M_FLG_SKMODE), (RDA5807M_REG_CHIPID | RDA5807M_FLG_SEEK | RDA5807M_FLG_SEEK | RDA5807M_FLG_SKMODE))

def seekUp():
  updateRegister(RDA5807M_REG_CONFIG, (RDA5807M_FLG_SEEKUP | RDA5807M_FLG_SEEK | RDA5807M_FLG_SKMODE), (RDA5807M_FLG_SEEKUP | RDA5807M_FLG_SEEK | RDA5807M_FLG_SKMODE))

def mute(m):
  global MUTE
  if m == True:
    updateRegister(RDA5807M_REG_CONFIG, RDA5807M_FLG_DMUTE, 0x00)
    MUTE = True
  else:
    updateRegister(RDA5807M_REG_CONFIG, RDA5807M_FLG_DMUTE, RDA5807M_FLG_DMUTE)
    MUTE = False

def volumeDown():
  volume = read_u16(RDA5807M_REG_VOLUME) & RDA5807M_VOLUME_MASK
  volume = volume - 1 if volume - 1 > -1 else 0
  updateRegister(RDA5807M_REG_VOLUME, RDA5807M_VOLUME_MASK, volume)
  if volume == 0:
    mute(True)
  return volume
  
def volumeUp():
  volume = read_u16(RDA5807M_REG_VOLUME) & RDA5807M_VOLUME_MASK
  volume = volume + 1 if volume + 1 <= 15 else 15
  updateRegister(RDA5807M_REG_VOLUME, RDA5807M_VOLUME_MASK, volume)
  if MUTE == True:
    mute(False)
  return volume

write_u16(RDA5807M_REG_CONFIG, (RDA5807M_FLG_DHIZ | RDA5807M_STATUS_STC | RDA5807P_FLG_I2SSLAVE | RDA5807M_FLG_SEEKUP | RDA5807M_FLG_RDS | RDA5807M_FLG_NEW | RDA5807M_FLG_ENABLE))
updateRegister(RDA5807M_REG_TUNING, RDA5807M_BAND_MASK, RDA5807M_BAND_WEST)

def buttonA_pressed():
  volumeDown()
  
def buttonB_pressed():
  seekUp()

def buttonC_pressed():
  volumeUp()

buttonA.wasPressed(callback=buttonA_pressed)
buttonB.wasPressed(callback=buttonB_pressed)
buttonC.wasPressed(callback=buttonC_pressed)