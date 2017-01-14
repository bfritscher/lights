# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
import gc
import webrepl
from config import SSID, SHARED_KEY
webrepl.start()
gc.collect()

def do_connect():
    import network
    sta_if = network.WLAN(network.STA_IF)
    ap_if = network.WLAN(network.AP_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(SSID, SHARED_KEY)
        while not sta_if.isconnected():
            pass
        ap_if.active(False)
    print('network config:', sta_if.ifconfig())
    import ntptime
    ntptime.settime()
do_connect()
