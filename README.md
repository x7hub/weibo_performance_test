## weibo_performance_test

for sina weibo.

## python

python版本的测试脚本



## shell

shell版本的测试脚本


#### onekey_test.sh

- 直接运行的入口
- 测试4个页面的数据，保存到result目录下，以时间戳为子目录


#### card_performance_test.sh [-f] [-p topic|hot|find|music|home|twitter]

- 被onekey_test.sh调用，测试单个页面gfxinfo
- -f 表示快速翻页
- -p 指定要测试的页面
- *画图用到软件`gnuplot`*

#### systrace_test.sh

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

## test_data

用于对比测试的json数据

#### create_feed_data_from_topic.php

- php脚本，将话题的数据改为首页feed流的格式
- 原数据为`test_data/feeds.json`和`test_data/huati.json`，输出到标准输出
