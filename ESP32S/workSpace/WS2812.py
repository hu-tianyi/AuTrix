import machine, time, neopixel

print("aaaaaaaaaaaaa")
n = 256
p = 5

np = neopixel.NeoPixel(machine.Pin(p), n)

for index in range (256):
  np[index] = (20,0,0)
  np.write()
  time.sleep_ms(500)

for index in range (256):
  np[index] = (0,0,0)
np.write()



print("Executed WS2812 Command")







