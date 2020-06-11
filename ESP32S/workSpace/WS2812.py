# Complete project details at https://RandomNerdTutorials.com

import machine, neopixel, time

n = 256
p = 5

np = neopixel.NeoPixel(machine.Pin(p), n)

'''
def set_color(r, g, b):
  for i in range(n):
    np[i] = (r, g, b)
  np.write()
  
r, g, b = 0, 0, 0
set_color(r, g, b)

while(1):
  if r < 20:
    r = r + 2;
  elif g < 20:
    g = g + 2
  elif b < 20:
    b = b + 2
  else:
    r, g, b = 0, 0, 0
  time.sleep_ms(100)
  set_color(r, g, b)

'''
def wheel(pos):
  #Input a value 0 to 255 to get a color value.
  #The colours are a transition r - g - b - back to r.
  if pos < 0 or pos > 255:
    return (0, 0, 0)
  if pos < 85:
    return (255 - pos * 3, pos * 3, 0)
  if pos < 170:
    pos -= 85
    return (0, 255 - pos * 3, pos * 3)
  pos -= 170
  return (pos * 3, 0, 255 - pos * 3)
  
def rainbow_cycle(wait):
  for j in range(255):
    for i in range(n):
      rc_index = (i * 256 // n) + j
      np[i] = wheel(rc_index & 255)
    np.write()
    time.sleep_ms(wait)
    
rainbow_cycle(100)

print("Executed WS2812 Command")



