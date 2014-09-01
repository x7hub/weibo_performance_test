## weibo_performance_test

for sina weibo.

### python

python测试脚本，需要python2，已经在`ArchLinux i686 + Python 2.7.8`和`Windows7 32bit + Python 2.7.8`测试通过


StartTest.py

- 测试入口，直接运行开始测试
- 统计结果打印到输出，并与原始数据一起保存到`result`文件夹，文件以时间戳命名


GfxinfoMonitor.py

- 监控器类
- 通过`start()`方法开始监控，调用`interrupt()`停止
- 通过`getResult()`方法获取结果，字典结构，键为Activity名，值为每帧加载时间的列表
- 通过`getResultInSum()`方法获取结果，字典结构，键为Activity名，值为每帧加载时间的列表，已经将三个列求和

adb

- 内置了Linux和Windows需要的adb二进制文件，MacOS的adb未经测试
- 经过验证Linux和Windows版本的adb对于x86和x86_64系统没有区别
