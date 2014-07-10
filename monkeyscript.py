# Imports the monkeyrunner modules used by this program
from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice

# Connects to the current device, returning a MonkeyDevice object
device = MonkeyRunner.waitForConnection()

# sets a variable with the package's internal name
package = 'com.sina.weibo'

# sets a variable with the name of an Activity in the package
#mainActivity = 'com.sina.weibo.MainTabActivity'
#cardActivity = 'com.sina.weibo.CardListActivity'

#device.startActivity(component=package + '/' + mainActivity)
#MonkeyRunner.sleep(3)
#device.startActivity(component=package + '/' + cardActivity)

device.drag((250,850),(250,110),0.1,10)
