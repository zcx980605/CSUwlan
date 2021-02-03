# CSUwlan

CSUwlan是一个用于自动化登录数字中南电信网的Python程序，也附带有一些其他功能。

## 项目简介

作为CSU电信校园网用户，你是否已经厌倦了每次上网前要先打开浏览器并登录账号的一系列操作？CSUwlan即可代替你完成这些。它最初被设计于Windows环境中运行，现在已对Linux和Android（借助Termux）进行了适配，但受限于系统环境和作者的水平，此程序目前只能在Windows操作系统中**全自动的按需运行**。也就是说，在Windows中使用此程序，在连接到数字中南电信网无线网络后，你**无需任何操作**即可开始上网，而在其他操作系统中，你需要手动运行此程序以完成登录认证。

注：考虑到使用者的计算机可能并未安装Python解释器，故该项目中内置了可再发行的python_embed，且以Windows Shell Script编写了安装/卸载程序。另，该项目的编写者是由一位从未系统学习过编程的医学生，故代码质量可能不高。

## 运行依赖

+ Python依赖
    + Python解释器3.x 【已内置用于64位Windows系统的python_embed】
    + rsa模块（仅在配置登录密码，即直接运行config.py时依赖）【已内置于python_embed】
+ Windows依赖
    + Windows任务计划程序（用于在连接无线网络后自动启动CSUwlan程序）【Windows系统组件】
    + Windows Console Based Script Host（用于安装时解释vbs脚本以创建快捷方式）【Windows系统组件】
    + SCHTASKS、NETSH命令行工具（用于添加/删除任务计划，读取/控制WLAN连接）【Windows系统组件】
+ Linux依赖
    + ifconfig命令行工具（用于读取WLAN连接信息）[^\*]
+ Android依赖
    + Termux应用
    + Termux-Api应用[^\*]
    + Termux中的python、termux-api[^\*]软件包
    [^\*]: 可选，仅运行核心功能时无需

