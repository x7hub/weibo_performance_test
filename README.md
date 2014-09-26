## weibo_performance_test

for sina weibo.

### python

python测试脚本，这个是在Shell脚本之后完成的，比Shell脚本更稳定且更适应多个平台，但是没有自动测试的功能，需要手动滑动屏幕，能测试得到每个Activity分别的性能数据。

需要python2，已经在`ArchLinux i686 + Python 2.7.8`和`Windows7 32bit + Python 2.7.8`测试通过


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


### shell

shell测试脚本，能自动测试滑动屏幕，比手动更能控制对比。

在`ArchLinux i686`测试可以正常使用。

onekey_test.sh

- 直接运行的入口
- 测试4个页面的数据，保存到result目录下，以时间戳为子目录

card_performance_test.sh [-f] [-p topic|hot|find|music|home|twitter]

- 被onekey_test.sh调用，测试单个页面gfxinfo
- -f 表示快速翻页
- -p 指定要测试的页面
- *画图用到软件`gnuplot`*

systrace_test.sh

- 被onekey_test.sh调用，测试单个页面systrace
- *需要修改`DIR_SYSTRACE`为sdk中systrace脚本的位置*
- *需要python2，开头的如下代码已经做了处理，如果默认python已经是python2则注释掉这段*

```shell
if [ ! -s ~/bin/python ]
then
    mkdir ~/bin
    ln -s /usr/bin/python2 ~/bin/python
    ln -s /usr/bin/python2-config ~/bin/python-config
fi
export PATH=~/bin:$PATH
```


### test_data

用于对比测试的json数据

create_feed_data_from_topic.php

- php脚本，将话题的数据改为首页feed流的格式
- 原数据为`test_data/feeds.json`和`test_data/huati.json`，输出到标准输出


