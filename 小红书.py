import uiautomator2 as u2

# 1. 连接手机（替换成你的设备号）
device_id = "192.168.70.236:5556"

try:
    d = u2.connect(device_id)
    print("设备信息：", d.device_info)
    print("连接成功！")
    d.app_start("com.xingin.xhs")
    print("小红书应用启动成功！")
except Exception as exc:
    print(f"连接失败：{exc}")
    print("请确认设备号是否正确，且手机已通过 USB 或 Wi-Fi 连接。")
