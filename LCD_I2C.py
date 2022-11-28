import I2C_LCD_driver
from time import *
#import subprocess
import time
mylcd = I2C_LCD_driver.lcd()
#mylcd.lcd_write(LCD_DISPLAYCONTROL |  LCD_DISPLAYOFF)

#IP =subprocess.check_output(["hostname","-I"]).split()[0]
mylcd.backlight(0)
fontdata1 =[
	[   0x0E,
  0x00,
  0x11,
  0x19,
  0x1D,
  0x17,
  0x13,
  0x11]
]

mylcd.lcd_load_custom_chars(fontdata1)
#mylcd.lcd_display_string("IP", 1)
#mylcd.lcd_display_string(str(IP),2)
mylcd.lcd_write(0)
sleep(5)
mylcd.lcd_clear()


while True:
	mylcd.lcd_display_string("Hora: %s"  %time.strftime("%H:%M:%S"), 1)
	mylcd.lcd_display_string("Fecha:%s" %time.strftime("%m/%d/%Y"), 2)

