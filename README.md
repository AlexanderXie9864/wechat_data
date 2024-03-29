# wechat_data
## 注：本项目是作者的早期作品，部分功能可能已经失效，建议整个项目读者自己组建

## 简介
本文利用Python针对校园微信好友数据进行分析，提取有用信息和形成结论而对数据加以详细研究和概括总结，以求最大化地开发数据的功能，发挥数据的作用。基于Django+Nginx+uWSGI搭建数据采集与分析网站，面向全院采集数据，并对每个人的数据进行清理、可视化分析。

基于WEB的校园好友微信数据采集与分析系统（以下称数据采集系统）给采集数据提供了方便快捷的平台，学生可以通过网页扫码来采集自己的微信好友数据，采集完成后学生可以通过网页链接访问查看自己的可视化数据；每天晚上12点半定时将数据从缓存导入数据库，方便后期总体数据分析。后期总体数据分析，利用Spyder编写python代码做分析报表。

总体规划：数据采集系统是应用Django框架和数据库开发的Web端应用程序，主要用于采集数据，以及对所采集的数据进行初步分析，反馈给用户所采集的数据总体情况，每天12点30分定时将一天所采集的数据从缓存数据库录入关系型数据库储存，后期利用Python进行总体分析。系统分为前台应用和后台管理两部分。

前台应用：提供本系统重要功能，数据采集、数据可视化、提供密钥对数据进行初步保密。
后台管理：管理并存储从前台输入的数据信息，管理世界城市经纬度数据、采集的用户数据基本信息管理，以及djcelery定时任务的调度管理。

数据采集分析系统整体上分为用户端和服务器端，用户端（即浏览器），主要使用了CSS、HTML5、layer、echarts、jQuery等技术，服务器端，采用nginx、uwsgi作为服务器，后端框架采用了Django+Python3.6，使用了pymysql、redis、djcelery等组件、自定义spider_itchat模块以及定时任务脚本redis_to_mysql;数据库主要使用了Redis和MySQL

## 项目配置
测试环境：VM+CentOS7.3

开发环境：Pycharm pro

开发语言：python3.6

开发框架：Django2.1

数据库：MySQL5.7

redis3.2.12

前端控件：Echarts

## 项目结构：
```
Spider_Data: 存储Django框架的设置，url路由，以及wsgi通信接口。
static: 存储网站所有应用的静态文件，如图片，js文件，css文件。
templates: 存储所有应用的模板文件，主要内容为html文件
venv: 存储虚拟开发环境文件。
wechat: 微信数据采集与分析的应用目录，包含了路由、视图等应用逻辑文件。
manage.py: Django框架功能管理模块，用于框架功能性管理，比如启动内置服务器、数据迁移等等
nohup.out: 定时任务日志文件
public_function.log: 应用逻辑运行日志文件
requirements: 网站所需要的模块列表，方便部署使一键配置模块
uwsgi.log: uWSGI服务器日志文件
uwsgi.ini: uWSGI服务器启动配置，通过这个文件一键启动uWSGI服务器
uwsgi.pid: uWSGI服务器进程号，通过这个文件一次性杀死所有uWSGI服务进程

///////以下是网站外的程序/////
mysql:存放mysql的sql文件，便于构建数据库
visua_data:数据清理以及可视化脚本代码
//////////
```




## 用户操作流程：
	访问网址，网页出现一个选项，点击相应选项，跳转至基本信息录入，页面，按照提示填写表单，点击开始采集数据按钮，弹出二维码，扫码，数据开始采集，数据采集完成关闭二维码，跳转页面至成功界面。
## 用户个人数据可视化展示
提供查询密钥，保证数据的隐秘性，提供好友地区分布世界地图，提供好友性别比例饼图，提供好友签名词频统计词云及概况。

数据需求
学生：用户性别、专业、入学年份、系别、学校，老师：用户性别、系别、学校，全球城市地图经纬度数据，用户的好友数据：地区、性别、个性签名

## 页面介绍
### 首页面
首页面（da.html），继承于da_base.html，包含了两个公共模板（copyright_template.html、icp_beian_template.html），用于数据采集向导以及系统安全说明，主要功能为链接向导，根据页面提供的链接导向指定功能页面，主要使用CSS样式以及button控件实现界面效果。

### 数据填表页面
数据填表页面（studentinfo.html、teacherinfo.html），继承于info_base.html，包含了三个公共模板(copyright_template.html、info_ajax_template.js、info_qr_template.html),是数据采集核心页面，包含两种类型,分别采集学生数据和老师数据，主要使用表单页面样式、layer插件实现界面效果，使用Ajax、jQuery实现页面功能，其中，Ajax用于异步交互json数据，检查数据是否重复，随后页面无刷新弹出二维码，等待用户扫描；jQuery用于表单验证，去除不必要的数据，以及提交表单。

### 采集成功页面
采集成功页面（da_success.html），继承于da_base.html，包含了一个公共模板（copyright_template.html），用于展现采集成功信息，提供一键导向个人数据可视化页面，并提供查询密钥。

### 采集失败页面
采集失败页面（da_fail.html），继承于da_base.html，与采集成功页面功能类似，用于展现采集失败信息。

### 个人数据展现页面
个人数据展现页面（wechat_analysis.html），为单独的一个模板，是采集系统功能呈现页面，主要利用了Echarts完成数据可视化呈现，其中地图用了百度的bmap接口，词云利用了echatrs_wordcloud.js插件。前端所需的数据，由后端渲染模板时，直接传参。

### 数据查询页面
数据查询页面（da_search.html），继承于da_base.html，包含了一个公共模板（copyright_template.html），提供数据查询功能，用户可通过此页面对自己的数据进行精确查询。


## itchat源码修改（路径请各位看官根据自己项目修改）
### 一、

位置：

==/home/alex/.virtualenvs/bysj/lib/python3.6/site-packages/itchat/__init__.py==


操作：添加代码块

功能：根据sessid获取itchat实例实现多开

```
def new_instance_dict(sessid):
    newInstance = Core()
    instanceDict[sessid] = newInstance
    return newInstance


#按sessid取得instance

def restore_instance(sessid):
    return instanceDict[sessid]
```

### 二
位置：
/home/alex/.virtualenvs/bysj/lib/python3.6/site-packages/itchat/components/login.py

操作：注释==utils.print_qr(picDir)==

功能：不打印qrcode，直接生成后存在picDir

```
def get_QR(self, uuid=None, enableCmdQR=False, picDir=None, qrCallback=None):
    uuid = uuid or self.uuid
    picDir = picDir or config.DEFAULT_QR
    qrStorage = io.BytesIO()
    qrCode = QRCode('https://login.weixin.qq.com/l/' + uuid)
    qrCode.png(qrStorage, scale=10)
    if hasattr(qrCallback, '__call__'):
        qrCallback(uuid=uuid, status='0', qrcode=qrStorage.getvalue())
    else:
        if enableCmdQR:
            utils.print_cmd_qr(qrCode.text(1), enableCmdQR=enableCmdQR)
        else:
            with open(picDir, 'wb') as f:
                f.write(qrStorage.getvalue())
            # utils.print_qr(picDir)
    return qrStorage
```

### 三
位置：/home/alex/.virtualenvs/bysj/lib/python3.6/site-packages/itchat

操作：添加user_agent代理池

功能：实现user_agent随机，防止被微信查出来同一个机器
```
agent = [
'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1',
'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0',
'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16',
'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0',
'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)']
USER_AGENT = agent[random.randint(0,6)]
```

# 编辑于11/9/2019，项目创建于 2018年11月份
# 待续...