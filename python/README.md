## weibo_performance_test

for sina weibo.

### python

python测试脚本

GfxinfoMonitor.py

- 监控类
- 通过`start()`方法开始监控，`Ctrl-C`或调用`getResult(interrupt = True)`停止
- 通过`getResult()`方法获取结果，字典结构，键为Activity名，值为每帧加载时间的列表

