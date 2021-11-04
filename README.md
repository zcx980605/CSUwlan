# CSUwlan

CSUwlan是一个用于自动化登录数字中南电信网的Python程序，也附带有一些其他功能。

## 项目简介

作为CSU电信校园网用户，你是否已经厌倦了每次上网前要先打开浏览器并登录账号的一系列操作？CSUwlan即可代替你完成这些。它最初被设计于Windows环境中运行，现在已对Linux和Android（借助Termux）进行了适配，但受限于系统环境和作者的水平，此程序目前只能在Windows操作系统中**全自动的按需运行**。也就是说，在Windows中使用此程序，在连接到数字中南电信网无线网络后，你**无需任何操作**即可开始上网，而在其他操作系统中，你需要手动运行此程序以完成登录认证。

注：考虑到使用者的计算机可能并未安装Python解释器，故该项目中内置了可再发行的python_embed，且以Windows Shell Script编写了安装/卸载程序。另，该项目的编写者是由一位从未系统学习过编程的医学生，故代码质量可能不高。

## 运行依赖

+ Python依赖
    + Python解释器3.x 【已内置用于64位Windows系统的python_embed】
    + rsa模块（仅在配置登录密码，即直接运行config.py时依赖）【已内置于python_embed】
+ 运行于Windows时的依赖
    + Windows任务计划程序（用于在连接无线网络后自动启动CSUwlan程序）【Windows系统组件】
    + Windows Console Based Script Host（用于安装时解释vbs脚本以创建快捷方式）【Windows系统组件】
    + SCHTASKS、NETSH命令行工具（用于添加/删除任务计划，读取/控制WLAN连接）【Windows系统组件】
+ 运行于Linux时的依赖
    + ifconfig命令行工具（用于读取WLAN连接信息）<sup>[ 1](#脚注1)</sup>
+ 运行于Android时依赖
    + Termux应用
    + Termux-Api应用<sup>[ 1](#脚注1)</sup>
    + Termux中的python、termux-api<sup>[ 1 ](#脚注1)</sup>软件包
    
<a name="脚注1">1</a>: 可选，仅运行核心功能时无需

## 功能计划

+ [x] 登录数字中南电信网
+ [x] 登录信息历史记录
+ [x] 登出数字中南电信网<sup>[ 2](#脚注2)</sup>
+ [x] 回显WLAN接口信息并可按指定间隔刷新
+ [x] 通过Android Toast显示信息<sup>[ 3](#脚注3)</sup>
+ [x] 利用认证服务器的秘钥对密码进行RSA加密
+ [x] 独立的配置文件
+ [x] 包含安装程序
+ [x] 手动指定登录IP（可用于为其他设备登录）
+ [ ] 完善的安装/卸载程序

<a name="脚注2">2</a>: 仅在历史记录功能已启用（默认启用）时可用    
<a name="脚注3">3</a>: 依赖Termux-Api应用及软件包，且需同时传入`/print-to-android-toast`和`/nopause`两个命令行参数

## 安装及配置

### Windows

从[这个页面](https://github.com/zcx980605/CSUwlan/releases)下载带有Win64后缀的最新Release，解压到你希望的路径（不建议放置于“Program Files”目录<sup>[ 4](#脚注4)</sup>）后双击运行`.\CSUwlan\安装.bat`并按照提示完成安装。在安装过程中，你需要输入Windows当前用户的密码（如果没有则直接留空并按回车）用于添加任务计划，在最后一步，你需要输入数字中南电信网的账户名和密码（也就是之前从网页登录时要填的信息）。

如果你希望更改之前输入的数字中南电信网账户名或密码，请再次运行安装程序或直接运行`config.py`（推荐，如果可能），原有配置将备份为`config.py_bak.txt`。

### Linux

直接将此项目clone到本地，或从[这个页面](https://github.com/zcx980605/CSUwlan/releases)下载最新Release中的源代码并解压，后进入`./CSUwlan/app`目录，先执行`python3 config.py`来配置账户名和密码，完成即可后执行主程序`python3 AutoLogin.py`。示例：

```shell
git clone https://github.com/zcx980605/CSUwlan.git
cd CSUwlan/app
python3 config.py
python3 AutoLogin.py
```

如果你希望更改之前输入的数字中南电信网账户名或密码，请再次执行`python3 config.py`，原有配置将备份为`config.py_bak.txt`。

### Android

需要在Termux App中完成，具体操作与Linux终端相同。

### 详细配置（高级）

直接编辑安装程序生成的`config.py`（和`launcher_config.py`）可配置的参数有……

<a name="脚注4">4</a>: 登录历史记录数据库的默认位置位于安装目录，由于Windows系统的安全限制，程序只有取得管理员权限后才可对“Program Files”目录及子目录写入，此程序运行时不会请求管理员权限因而无法正常工作，除非您手动禁用历史记录或将历史记录数据库移动到其他位置（详见[详细配置](#详细配置)）。

## 如何使用

### 基本用法

+ 用于登录
    + 在Windows下，程序将于新连接到无线网络后自动运行，要手动运行，请直接双击桌面“登录数字中南”快捷方式图标，或不带参数的运行AutoLogin.py。
    + 在Linux下，你只能手动运行主程序来登录，即执行`python3 AutoLogin.py`。
    + 在Android下，建议安装Termux-Widget应用，以便启动器中添加指向脚本的图标来方便运行。你也可以直接Termux App中执行`python AutoLogin.py`来登录，具体操作与Linux终端相同。
+ 用于登出
    + 在Windows下，请直接双击桌面“登出数字中南”快捷方式图标，手动运行需向程序传入`/logout`参数，即`python AutoLogin.py /logout`。
    + 在Linux和Android下，请执行`python3 AutoLogin.py /logout`。

### 命令行参数详解

+ `/logout`：登出数字中南（使用历史记录数据库中最近的一条登录记录）
+ `/ip ip_addr`：指定登录IP（可用于为其他设备登录）。*ip_addr*为必选参数，有效值为“10.96.\[0-255\].\[0-255\]”。
+ `/sysinfo`：动态显示无线接口信息（默认刷新5次，间隔1.0秒）
    + 子开关`/r [[loops] [[interval]]]`：持续刷新，直到用户退出程序。可选指定循环次数和间隔，可单独指定循环次数，不可单独指定间隔。
+ `/print-to-android-toast`：将所有输出（包括标准输出、标准错误）重定向到Android Toast（仅在Android Termux环境下可用，且依赖Termux-Api应用及软件包）
+ `/nopause`：在本次运行时禁用类似“请按任意键继续”的提示，并在运行完成后直接退出，无论是否发生异常。
+ 内部参数`/location`：在Windows下，由`Launcher.py`传入，为用于获取登录Cookie的网址
+ 内部参数`/return`：在Windows下，由`Launcher.py`传入，指定成功登录并退出时返回的exitcode

## 如何卸载

卸载程序（脚本）还没有写😂，在Windows下，你需要手动删除名为“1_登录数字中南”的任务计划、手动删除桌面图标及手动删除程序所在的文件夹。

对于删除任务计划，你可以使用Windows管理工具中的任务计划程序（`taskschd.msc`），在GUI下删除“任务计划程序库”根目录的“1_登录数字中南”任务。也可以以管理员身份直接执行命令`schtasks /DELETE /TN "1_登录数字中南" /F`。

## 致谢

本项目引用了GitHub用户[@founddev](https://github.com/founddev)编写的[myrsa.py](https://github.com/founddev/everything/tree/master/rsa)。本项目的myrsa.py文件中亦标明了引用。

## 许可证

还没想好。。。目前NO LISENCE。
