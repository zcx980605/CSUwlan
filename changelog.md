# 更新日志

First Version 0.9.0 @ 2019/05/01
  + 完成了核心功能

Version 0.9.1 @ 2019/05/04
  + 输出、错误处理

Version 0.9.2 @ 2019/05/11
  + 历史记录，超时硬限制

Version 0.10.0 @ 2019/08/25
  + 无需操作时不弹出窗口(构建了启动器Launcher.pyw)

Version 0.11.0 @ 2019/08/26
  + step3超时重试，命令行参数，模块化重构
  + 启动器调用主程序时利用命令行传参

Version 0.11.1 @ 2019/08/27
  + 登出功能

Version 0.11.2 @ 2019/09/01
  + 显示系统无线接口信息，重构主函数
  + 启动器中可指定python解释器路径、检测无线网络连接状态

Version 0.11.3 @ 2019/09/02
  + “账号已在线”错误时尝试注销并重试，启动器更新

Version 0.12.0 @ 2019/09/04
  + 独立的配置信息文件

Version 0.12.1 @ 2019/09/14
  + 启动器更新：阻止系统自动从无网络访问的WLAN断开(issue of Win10 1903)

Version 0.12.2 @ 2019/09/20
  + 配置文件支持直接运行以修改账号密码

Version 0.12.3 @ 2019/09/22
  + 启动器更新：无网络连接时在限定时间内重试

Version 0.12.4 @ 2019/09/28
  + 修改exitcode，使之符合Linux规范
  + 启动器更新：修改exitcode，线程同步(issue 20190926)

Version 0.12.5 @ 2019/10/20
  + 启动器更新：转义处理网址中的特殊含义字符以安全地回显消息(issue 20191011)

Version 0.13.0 @ 2020/01/10
  + 可利用termux-api输出到安卓Toast
  + 启动器更新：开始登陆同时即监测WLAN并阻止系统自动切换到其他网络而致step3、4失败(issue 20191026)

Version - @ 2021/11/15
  + 构建了安装脚本setup.py

Version 0.14.0 @ 2021/11/04
  + 可手动指定登录IP（用于为其他设备登录）
  + 其他修正

Version 0.14.1 @ 2021/11/05
  + 修正一处错误：（0.14.0中）传入location参数时未分析ip

- TODO issue 20200101 登陆成功后服务器未返回剩余流量等信息导致程序于存储历史记录前终止
