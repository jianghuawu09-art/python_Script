import uiautomator2 as u2
from threading import Thread

# 1. 连接多台手机，填写多个设备号或 IP 地址
#    如果用 USB 连接，设备号可通过 adb devices 获取
#    如果用 Wi-Fi 连接，设备号类似 192.168.1.100:5555

device_ids = [
    "192.168.70.70:5555",
    "192.168.70.236:5556",
]


def start_app(device_id):
    try:
        d = u2.connect(device_id)
        print(f"设备 {device_id} 连接成功")
        d.app_start("com.kuaishou.nebula")
        print(f"设备 {device_id} 快手应用启动成功！")
    except Exception as exc:
        print(f"设备 {device_id} 连接失败：{exc}")


def start_app2(device_id):
    try:
        d = u2.connect(device_id)
        print(f"设备 {device_id} 连接成功")
        d.app_start("com.ss.android.ugc.aweme")
        print(f"设备 {device_id} 抖音应用启动成功！")
    except Exception as exc:
        print(f"设备 {device_id} 连接失败：{exc}")


# 这里是任务列表，后面如果要加功能，可以继续增加函数并放到这个列表里
task_functions = [
    start_app,
    start_app2,
]


def run_tasks(functions, device_ids):
    threads = []
    for func in functions:
        for device_id in device_ids:
            t = Thread(target=func, args=(device_id,))
            t.start()
            threads.append(t)

    for t in threads:
        t.join()


if __name__ == "__main__":
    run_tasks(task_functions, device_ids)
    print("所有任务已完成。")
    print("如果要增加新功能，按类似方式再定义函数并加到 task_functions 列表里。")
