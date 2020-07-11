import machine, time

np=machine.Neopixel(machine.Pin(5), 256, 0)

def rainbow(loops=120, delay=1, sat=1.0, bri=0.2):
    for pos in range(0, loops):
        for i in range(0, 256):
        #for i in range(0, 24):
            dHue = 360.0/256*(pos+i);
            hue = dHue % 360;
            np.setHSB(i, hue, sat, bri, 1, False)
        np.show()
        if delay > 0:
            time.sleep_ms(delay)

def blinkRainbow(loops=10, delay=250):
    for pos in range(0, loops):
        for i in range(0, 24):
            dHue = 360.0/256*(pos+i);
            hue = dHue % 360;
            np.setHSB(i, hue, 1.0, 0.1, 1, False)
        np.show()
        time.sleep_ms(delay)
        np.clear()
        time.sleep_ms(delay)
        
rainbow(loops=100, delay=1, bri=0.05)
#blinkRainbow(loops=1000, delay=1, bri=0.05)

'''
for index in range(256):
  np.set(position=index, color=0xFF0000)
  np.show()
  time.sleep_ms(100)
  '''
for index in range(0,256):
  print(index)
  np.set(index, 0x000000, 0, 1, False)
  time.sleep_ms(10)
  np.show()

print("Finish")


