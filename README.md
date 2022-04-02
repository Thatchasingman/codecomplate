# 暨南大学自动打卡服务

## 基本配置

- python 3.8 以上的环境下运行
- 使用火狐驱动器，gecko-webdriver
- 安装selenium, opencv-python库
- 
## 功能介绍

技术难点在网易yidun滑块，其他的都是selenium基础操作
主要分成两个模块，一个就是滑块验证，另外一个就是打卡操作类。
滑块验证在image_match.py
打卡操作类在dacard.py

**仅适用于网页打卡**
手机打卡请用autojs写哈。

## 使用

使用很脑残，配置好了环境，从github下拷贝代码，在dacard.py
输入username,password就行了，明文密码，反正在本地运行

尝试运行一下，可以就可以在电脑上的计时任务程序那里设置计时打卡。

## 后记

这个仅仅是纪念一下我的三年，疫情两年的成果。
