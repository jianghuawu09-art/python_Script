import uiautomator2 as u2
from threading import Thread
import time
import random
from search_text import text

# 1. 连接多台手机，填写多个设备号或 IP 地址
#    如果用 USB 连接，设备号可通过 adb devices 获取
#    如果用 Wi-Fi 连接，设备号类似 192.168.1.100:5555

device_ids = [
    "192.168.122.32:5555",
    "192.168.122.236:5556",
]

def screen(device_id):
    try:
        d = u2.connect(device_id)
        d.screen_on()
        print(f"设备 {device_id} 已亮屏")
        time.sleep(5)

        width, height = d.window_size()
        start_x = width // 2
        start_y = int(height * 0.8)
        end_y = int(height * 0.2)
        d.swipe(start_x, start_y, start_x, end_y, 0.2)
        print(f"设备 {device_id} 已上滑尝试解锁")
        time.sleep(5)

    except Exception as exc:
        print(f"设备 {device_id} 连接失败：{exc}")

def start_app(device_id):
    try:
        d = u2.connect(device_id)
        print(f"设备 {device_id} 连接成功")
        d.app_start("com.kuaishou.nebula")
        print(f"设备 {device_id} 快手应用启动成功！")
        time.sleep(15)  # 等待应用完全启动
    except Exception as exc:
        print(f"设备 {device_id} 连接失败：{exc}")

def swipto(device_id,duration=0.7):
    try:
        d = u2.connect(device_id)
        print(f"设备 {device_id} 连接成功，开始随机滑动 30 分钟")

        width, height = d.window_size()
        end_time = time.monotonic() + 40 * 60
        like_target = d.xpath('//*[@resource-id="com.kuaishou.nebula:id/like_icon"]')

        while time.monotonic() < end_time:
            start_x = random.randint(int(width * 0.45), int(width * 0.55))
            start_y = random.randint(int(height * 0.52), int(height * 0.82))
            end_x = random.randint(int(width * 0.40), int(width * 0.60))
            end_y = random.randint(int(height * 0.20), int(height * 0.38))
            swipe_duration = random.uniform(max(0.1, duration - 0.08), duration + 0.15)
            d.swipe(start_x, start_y, end_x, end_y, swipe_duration)

            if random.random() < 0.1:  # 10% 的概率尝试点赞
                if like_target.exists:
                    like_target.click()
                    print(f"设备 {device_id} 已执行一次随机点赞")
                    time.sleep(random.uniform(0.5, 1.5))

            wait_seconds = random.randint(20, 240)
            print(
                f"设备 {device_id} 已随机滑动一次，滑动时长 {swipe_duration:.2f} 秒，"
                f"停留 {wait_seconds} 秒"
            )
            time.sleep(wait_seconds)

        print(f"设备 {device_id} 已完成 30 分钟随机滑动")
    except Exception as exc:
        print(f"设备 {device_id} 连接失败：{exc}")

def search(device_id):
    try:
        d = u2.connect(device_id)
        start_app(device_id)
        search_button = d.xpath('//*[@resource-id="com.kuaishou.nebula:id/thanos_home_top_search"]')
        if search_button.exists:
            search_button.click()
            time.sleep(5)
            print(f"设备 {device_id} 已点击搜索按钮")
            input_button = d.xpath('//*[@resource-id="com.kuaishou.nebula:id/editor"]')
            input_button.set_text(random.choice(text))  # 这里可以根据需要选择不同的搜索词
            time.sleep(5)
            search_result = d.xpath('//*[@resource-id="com.kuaishou.nebula:id/right_tv"]')
            search_result.click()
            print(f"设备 {device_id} 已搜索并点击结果")
            time.sleep(10)
            
            video_item2 = d.xpath('(//android.view.View)[3]')

            if video_item2.exists:
                video_item2.click()
                time.sleep(5)
                print(f"设备 {device_id} 已点击视频")
                time.sleep(10)
                video_play = d.xpath('(//*[@resource-id="com.kuaishou.nebula:id/cover_container"])[3]')
                video_play.click()
                time.sleep(5)
                print(f"设备 {device_id} 已选择视频播放")
                swipto(device_id)

        time.sleep(5)
    except Exception as exc:
        print(f"设备 {device_id} 连接失败：{exc}")

def home(device_id):
    try:
        d = u2.connect(device_id)
        d.press("recent")
        print(f"设备 {device_id} 已切换到后台任务列表")
        time.sleep(2)

        width, height = d.window_size()
        start_x = width // 2
        start_y = int(height * 0.78)
        end_y = int(height * 0.22)
        d.swipe(start_x, start_y, start_x, end_y, 0.25)
        print(f"设备 {device_id} 已在后台任务列表执行向上滑动")
        time.sleep(2)
        
    except Exception as exc:
        print(f"设备 {device_id} 连接失败：{exc}")

# 这里是任务列表，后面如果要加功能，可以继续增加函数并放到这个列表里
task_functions = [
    screen, # 先亮屏并尝试解锁
    start_app, # 启动快手应用
    swipto, # 随机滑动 40 分钟
    # search, # 搜索对应的视频并播放视频,这个有问题,暂时不执行了
    home, # 进入快手首页
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

