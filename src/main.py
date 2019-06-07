import wifimgr

wlan = wifimgr.get_connection()
if wlan is None:
    print("Could not initialize the network connection.")
    while True:
        pass  # you shall not pass :D


# Main Code goes here, wlan is a working network.WLAN(STA_IF) instance.
print("ESP OK")

from tallyscreen import *
ts = TallyScreen()
ts.msg('TallyScreen OK')
#ts.loop()
