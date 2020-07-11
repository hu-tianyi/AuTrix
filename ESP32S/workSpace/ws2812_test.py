import uctypes

RMT_BASE = 0x3ff56000

conf = uctypes.struct(RMT_BASE+0x20, (uctypes.ARRAY | 0, 8,
    {"mem_pd":         uctypes.BFUINT32 | 0 | 30<<uctypes.BF_POS | 1<<uctypes.BF_LEN, # Only for ch0
     "carrier_out_lv": uctypes.BFUINT32 | 0 | 29<<uctypes.BF_POS | 1<<uctypes.BF_LEN,
     "carrier_en":     uctypes.BFUINT32 | 0 | 28<<uctypes.BF_POS | 1<<uctypes.BF_LEN,
     "mem_size":       uctypes.BFUINT32 | 0 | 24<<uctypes.BF_POS | 4<<uctypes.BF_LEN,
     "idle_thres":     uctypes.BFUINT32 | 0 | 8<<uctypes.BF_POS  | 16<<uctypes.BF_LEN,
     "div_cnt":        uctypes.BFUINT32 | 0 | 0<<uctypes.BF_POS  | 8<<uctypes.BF_LEN,

     "idle_out_en":    uctypes.BFUINT32 | 4 | 19<<uctypes.BF_POS | 1<<uctypes.BF_LEN,
     "idle_out_lv":    uctypes.BFUINT32 | 4 | 18<<uctypes.BF_POS | 1<<uctypes.BF_LEN,
     "ref_always_on":  uctypes.BFUINT32 | 4 | 17<<uctypes.BF_POS | 1<<uctypes.BF_LEN,
     "ref_cnt_rst":    uctypes.BFUINT32 | 4 | 16<<uctypes.BF_POS | 1<<uctypes.BF_LEN,
     "rx_filter_thres":uctypes.BFUINT32 | 4 | 8<<uctypes.BF_POS  | 8<<uctypes.BF_LEN,
     "rx_filter_en":   uctypes.BFUINT32 | 4 | 7<<uctypes.BF_POS  | 1<<uctypes.BF_LEN,
     "tx_conti_mode":  uctypes.BFUINT32 | 4 | 6<<uctypes.BF_POS  | 1<<uctypes.BF_LEN,
     "mem_owner":   uctypes.BFUINT32 | 4 | 5<<uctypes.BF_POS  | 1<<uctypes.BF_LEN,
     "mem_rd_rst":     uctypes.BFUINT32 | 4 | 3<<uctypes.BF_POS  | 1<<uctypes.BF_LEN,
     "mem_wr_rst":     uctypes.BFUINT32 | 4 | 2<<uctypes.BF_POS  | 1<<uctypes.BF_LEN,
     "rx_en":          uctypes.BFUINT32 | 4 | 1<<uctypes.BF_POS  | 1<<uctypes.BF_LEN,
     "tx_start":       uctypes.BFUINT32 | 4 | 0<<uctypes.BF_POS  | 1<<uctypes.BF_LEN}))

# Interrupt registers not covered yet

carrier_duty = uctypes.struct(RMT_BASE + 0xb0, (uctypes.ARRAY | 0, 8,
    {"low":  uctypes.BFUINT32 | 0 |  0<<uctypes.BF_POS | 16<<uctypes.BF_LEN,
     "high": uctypes.BFUINT32 | 0 | 16<<uctypes.BF_POS | 16<<uctypes.BF_LEN}))

apb_conf = uctypes.struct(RMT_BASE + 0xf0, {
    'fifo_mask': uctypes.BFUINT32 | 0 | 0<<uctypes.BF_POS | 1<<uctypes.BF_LEN,
    'mem_tx_wrap_en': uctypes.BFUINT32 | 0 | 1<<uctypes.BF_POS | 1<<uctypes.BF_LEN,
})

# RMT RAM is divided into 8 blocks of 64 words, each holding 2 entries. 
ram = uctypes.struct(RMT_BASE+0x800, (uctypes.ARRAY | 0x0, uctypes.UINT32 | 64*8))


# Driving the neopixel might be possible.
# We have an 80MHz APB clock, usable if we set ref_always_on=1.
# We can use one word per bit, containing the on and off pulses.
# Finish with >50µs then halt.
# At 80MHz, we have 80 ticks per µs, and timings use 0.05µs (20).
# So without dividing we get multiples of 4. Convenient. 50µs is 50*80=400,
# which still easily fits within 15 bits.
WS2812_0 = 1<<15 | 4*8<<0  | 0<<31 | 4*17<<16
WS2812_1 = 1<<15 | 4*16<<0 | 0<<31 | 4*9<<16
WS2811_0 = 1<<15 | 4*10<<0 | 0<<31 | 4*40<<16
WS2811_1 = 1<<15 | 4*24<<0 | 0<<31 | 4*26<<16
WS_RES   = 0<<15 | 4*20*50<<0 | 0<<31 | 0<<16  # ends transfer
# Transfer GRB, MSB first, 24 bit, closest pixel first.
# This uses 24*pixels+1 words, meaning mem_size needs to be extended for >2 pixels.
def ws_conf(ch=0):
    conf[ch].rx_en = 0
    conf[ch].mem_rd_rst = 1
    conf[ch].mem_owner = 0
    conf[ch].tx_conti_mode = 0       # if 1, the transmission will loop
    conf[ch].ref_always_on = 1       # use 80MHz clock
    conf[ch].idle_out_lv = 0
    conf[ch].div_cnt = 1             # divider. could go as high as 4
    conf[ch].mem_size = 1
    conf[ch].carrier_en = 0
    conf[ch].mem_pd = 0
def ws_rgb(ch,r,g,b):
    base=ch*64
    #conf[ch].mem_wr_rst = 1
    apb_conf.fifo_mask = 1	# If 0, RAM access is in FIFO mode
    # Though I suppose fifo mode has its attractions; no need to calculate offsets
    for i in range(8):
        ram[base   +i] = WS2812_1 if g&(0x80>>i) else WS2812_0
        ram[base+ 8+i] = WS2812_1 if r&(0x80>>i) else WS2812_0
        ram[base+16+i] = WS2812_1 if b&(0x80>>i) else WS2812_0
    ram[base+3*8] = WS_RES
    #conf[ch].mem_rd_rst = 1
    #print([hex(ram[base+i]) for i in range(25)])
    conf[ch].mem_rd_rst = 1
    conf[ch].mem_owner = 0
    conf[ch].tx_start = 1
# Finally, we need to connect the output.
# The onboard WS2812 is connected to P2=GPIO0.
def ws_lopy(ch=0):
    import esp32, machine
    #muxi = esp32.IOmux_order.index("GPIO0")
    pin = machine.Pin(5, machine.Pin.OUT)
    # Inputs are 83+ch, outputs are 87+ch
    # Also, P2 is GPIO0
    esp32.GPIO.func_out_sel_cfg[0].func = 87+ch
    # This is routed through the GPIO matrix, not the IO mux.
    # Enable the clock and disable reset for the RMT block
    DPORT.perip_clk_en.rmt = 1
    DPORT.perip_rst_en.rmt = 0
    return pin

# First stage experiment failed; I didn't get the LED to react.
# Trying to read the RAM shows all as 0xab29b071, so that's probably the first thing to debug.
# Looks like the peripheral must be enabled via DPORT.
# Also, DPort is restricted to PID 0/1, and micropython seems to run privileged.
DPORT = uctypes.struct(0x3ff00000, {
    'perip_clk_en': (0x0c0, {'rmt': uctypes.BFUINT32 | 0 | 9<<uctypes.BF_POS | 1<<uctypes.BF_LEN}),
    'perip_rst_en': (0x0c4, {'rmt': uctypes.BFUINT32 | 0 | 9<<uctypes.BF_POS | 1<<uctypes.BF_LEN}),
})
# Setting clk_en then clearing rst_en did permit writing RAM.
# Remains to figure out how to fire it up properly, but there is example code:
# https://github.com/espressif/esp-idf/blob/master/components/driver/periph_ctrl.c
# https://github.com/espressif/esp-idf/blob/master/components/driver/rmt.c

# ws_lopy()
# 
def test_led(ch=5):
    # Reset the RMT block
    DPORT.perip_rst_en.rmt = 1
    DPORT.perip_clk_en.rmt = 1
    DPORT.perip_rst_en.rmt = 0
    ws_lopy(ch)
    ws_conf(ch)
    ws_rgb(ch,255,128,32)
    
test_led()
