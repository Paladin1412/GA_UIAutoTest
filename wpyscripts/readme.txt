v 1.1.1 版本更新日志：
====================
-----------------------------------
device=manager.get_device():
*新增接口get_element_world_bound，能够获取到节点的世界坐标。该方法只支持wetest sdk 8版本及其以上
*新增接口get_registered_handlers，获取可用的自定义函数。该方法只支持wetest sdk 8版本及其以上
*新增接口call_registered_handler，调用在游戏中注册的自定义函数，并返回对应的值。该方法只支持wetest sdk 8版本及其以上
~修复:NGUI部分版本,调用Input会出错的

main.py:
*添加游戏包名后，运行main.py能够直接拉起游戏，并进行全逻辑的测试

trave.py
*增加自动化探索测试接口，即便不写代码也可以直接遍历游戏


v 1.2.1 版本更新日志
====================
-----------------------------------
engine=manager.get_engine():
*新增接口get_touchable_elements_bound，能够获取可点击节点及节点左上角坐标，节点长宽高
*新增接口get_element_text,获取GameObject文字信息，NGUI控件则获取UILable、UIInput、GUIText组件上的文字信息，UGUI控件则获取Text、GUIText组件上的问题信息
*新增接口get_element_image,获取GameObject图片名称,NGUI控件则获取UITexture、UISprite、SpriteRenderer组件上的图片名称,UGUI控件则获取Image、RawImage、SpriteRenderer组件上的图片名称

-----------------------------------
device=manager.get_device():
*get_display_size,云端获取失败后，直接通过uiautomator获取。本地直接通过Uiautomator获取
*get_rotation，云端从平台获取失败后，直接通过UIAutomator获取。本地直接通过UIAutomator获取
*get_top_package_activity,云端从平台获取失败后，直接通过UIAutomator获取。本地UIAutomator获取失败后，通过adb shell dumpsys获取
*back，本地方式修改为UIAutomator

-----------------------------------
登陆实现进行了修改
-----------------------------------
将uiautomator独立出来，以备后用
-----------------------------------
main.py修改，修改native的游戏拉起时机。先拉起游戏，再进行socket的初始化


v 2.0.0版本
====================
V2版本将不再兼容老版本的SDK，新的SDK也不能兼容老的脚本GAutomator框架。

V2版本主要对GAutomator的框架进行了改进，通信协议全部改为json，对python的版本也没有windows 32的要求。新架构将支持与SDK的重连，与标准控件的操作也更加稳定。
SDK的性能更加高效，自动化测试基本对FPS的影响基本可以忽略，CPU的影响一般在1%的左右。
-----------------------------------
engine=manager.get_engine():
*新增get_component_field,能够反射获取游戏中对象的属性值

v 2.1.0版本
====================
V2.1.0版本主要对框架的结构进行了调整

-----------------------------------
1、支持一台pc同时控制多台手机
2、将于对外接口无关的wpyscripts.wetest.tools移到wpyscripts.common.utils.py，wpyscripts.platform_helper.py移到wpyscripts.common.platform_helper.py
3、将logger_config.py移除，日志初始化放置到wpyscripts.__init__.py
3、get_touchable_elements_bound、get_touchable_element处理默认的compnent为可点击候选之外，可以增加自定义的UI可点击控件组件。如，lua脚本编写的内容

