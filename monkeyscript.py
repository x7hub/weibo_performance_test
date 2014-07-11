# Imports the monkeyrunner modules used by this program
from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice

# Connects to the current device, returning a MonkeyDevice object
device = MonkeyRunner.waitForConnection()

#device.startActivity(component=package + '/' + mainActivity)

device.startActivity(uri='sinaweibo://cardlist?containerid=102803&cache_need=1&count=10')

MonkeyRunner.sleep(10)

device.drag((250,850),(250,110),0.1,10)
