import network, time

print('RUN: main.py')

# ---------------Wifi Shtuff--------------- #
# Enable station and station interface
station = network.WLAN(network.STA_IF)
station.active(True)
station.connect("TP-Link_E458", "62265317")
