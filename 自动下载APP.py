import uiautomator2 as u2
from threading import Thread
from pathlib import Path
import subprocess

# 1. 连接多台手机，填写多个设备号或 IP 地址
#    如果用 USB 连接，设备号可通过 adb devices 获取
#    如果用 Wi-Fi 连接，设备号类似 192.168.1.100:5555

device_ids = [
    "192.168.122.162:5557"
]

APK_SOURCE_FILE = Path(r"D:\快手APK\快手极速版.apk")
REMOTE_APK_DIR = "/sdcard/Download"

def download_app(device_id):
    try:
        u2.connect(device_id)
        print(f"设备 {device_id} 连接成功，开始推送并安装 APK")

        if not APK_SOURCE_FILE.exists() or not APK_SOURCE_FILE.is_file():
            print(f"本地 APK 文件不存在：{APK_SOURCE_FILE}")
            return

        remote_path = f"{REMOTE_APK_DIR}/{APK_SOURCE_FILE.name}"

        subprocess.run(
            ["adb", "-s", device_id, "shell", "mkdir", "-p", REMOTE_APK_DIR],
            check=True,
            capture_output=True,
            text=True,
        )

        subprocess.run(
            ["adb", "-s", device_id, "push", str(APK_SOURCE_FILE), remote_path],
            check=True,
            capture_output=True,
            text=True,
        )
        print(f"设备 {device_id} 已推送 {APK_SOURCE_FILE.name} 到 {remote_path}")

        install_result = subprocess.run(
            ["adb", "-s", device_id, "shell", "pm", "install", "-r", remote_path],
            check=True,
            capture_output=True,
            text=True,
        )
        install_output = install_result.stdout.strip() or "安装命令已执行"
        print(f"设备 {device_id} 已安装 {APK_SOURCE_FILE.name}：{install_output}")

        print(f"设备 {device_id} 已完成 APK 推送和安装")
    except FileNotFoundError:
        print("未找到 adb 命令，请先确认 adb 已安装并加入 PATH")
    except subprocess.CalledProcessError as exc:
        error_message = exc.stderr.strip() if exc.stderr else str(exc)
        print(f"设备 {device_id} 推送 APK 失败：{error_message}")

    except Exception as exc:
        print(f"设备 {device_id} 连接失败：{exc}")

task_functions = [
    download_app, # 下载快手极速版应用
]


def run_one_device(device_id, functions):
    for func in functions:
        func(device_id)


def run_tasks(functions, device_ids):
    threads = []
    for device_id in device_ids:
        t = Thread(target=run_one_device, args=(device_id, functions))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()


if __name__ == "__main__":
    run_tasks(task_functions, device_ids)
    print("所有任务已完成。")
