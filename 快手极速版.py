import uiautomator2 as u2
from threading import Thread
from time import sleep, monotonic
import random


device_ids = [
    # "192.168.70.70:5555",
    "192.168.112.236:5556",
]


BASE_WIDTH = 1080
BASE_HEIGHT = 2400


def click_scaled(d, x, y, base_width=BASE_WIDTH, base_height=BASE_HEIGHT):
    width, height = d.window_size()
    target_x = int(x / base_width * width)
    target_y = int(y / base_height * height)
    d.click(target_x, target_y)
    return target_x, target_y


def start_app(device_id):
    try:
        d = u2.connect(device_id)
        print(f"设备 {device_id} 连接成功")
        d.app_start("com.kuaishou.nebula")
        print(f"设备 {device_id} 快手极速版应用启动成功！")
        sleep(15)  # 等待15秒，确保应用完全启动
        print(f"设备 {device_id} 已等待15秒，进入发现界面观看视频")
    except Exception as exc:
        print(f"设备 {device_id} 连接失败：{exc}")

def watch_video(device_id):
    try:
        d = u2.connect(device_id)
        if d.xpath('//*[@text="看视频赚金币"]   ').wait(timeout=10):
            d.xpath('//*[@text="看视频赚金币"]   ').click()
            print(f"设备 {device_id} 已点击 看视频赚金币 元素")
            sleep(2)

        if d(description="发现").wait(timeout=10):
            d(description="发现").click()
            print(f"设备 {device_id} 已点击 发现 元素")
        elif d.xpath('//*[@content-desc="发现"]').wait(timeout=10):
            d.xpath('//*[@content-desc="发现"]').click()
            print(f"设备 {device_id} 已点击 发现 元素")
        else:
            print(f"设备 {device_id} 未找到 发现 元素")
            return

        sleep(8)
        print(f"设备 {device_id} 已等待8秒，开始随机滑动视频")

        width, height = d.window_size()
        end_time = monotonic() + 600  # 刷视频10分钟，单位是秒
        
        while monotonic() < end_time:
            start_x = random.randint(int(width * 0.45), int(width * 0.55))
            start_y = random.randint(int(height * 0.72), int(height * 0.82))
            end_x = random.randint(int(width * 0.40), int(width * 0.60))
            end_y = random.randint(int(height * 0.20), int(height * 0.35))
            swipe_duration = random.uniform(0.15, 0.35)

            d.swipe(start_x, start_y, end_x, end_y, swipe_duration)

            watch_seconds = random.randint(15, 70)
            print(f"设备 {device_id} 本条视频观看 {watch_seconds} 秒")
            sleep(watch_seconds)

        print(f"设备 {device_id} 已完成10分钟随机刷视频")
    except Exception as exc:
        print(f"设备 {device_id} 连接失败：{exc}")

def claim_money(device_id):
    try:
        d = u2.connect(device_id)
        claim_target = d.xpath('//*[contains(@text,"待领") and contains(@text,"金币") and contains(@text,"立即领取")]')
        if claim_target.wait(timeout=10):
            claim_target.click()
            print(f"设备 {device_id} 已点击 待领金币立即领取 元素")
        else:
            print(f"设备 {device_id} 未找到 待领金币立即领取 元素")

    except Exception as exc:
        print(f"设备 {device_id} 连接失败：{exc}")


def go_make_money(device_id):
    try:
        d = u2.connect(device_id)
        if d(description="去赚钱").wait(timeout=10):
            d(description="去赚钱").click()
            print(f"设备 {device_id} 已点击 去赚钱 元素")
            sleep(30)  # 等待30秒，确保应用完全启动
            print(f"设备 {device_id} 已等待30秒，准备进入任务中心界面")
        else:
            print(f"设备 {device_id} 未找到 去赚钱 元素")
    except Exception as exc:
        print(f"设备 {device_id} 连接失败：{exc}")

def pop_up(device_id):
    try:
        d = u2.connect(device_id)
        wait_seconds = random.randint(30, 60)
        deadline = monotonic() + wait_seconds

        while monotonic() < deadline:
            if d.xpath('//*[@text="翻倍任务开启"]').exists:
                target_x, target_y = click_scaled(d, 991, 510)
                print(f"设备 {device_id} 识别到广告弹窗，已点击关闭弹窗位置: ({target_x}, {target_y})")
                sleep(5)
                return
            if d.xpath('//*[@text="去微信邀请好友"]').exists:
                target_x, target_y = click_scaled(d, 991, 454)
                print(f"设备 {device_id} 识别到 去微信邀请好友 广告，已点击关闭弹窗位置: ({target_x}, {target_y})")
                sleep(5)
                return
            sleep(7)

        print(f"设备 {device_id} 在 {wait_seconds} 秒内未找到广告弹窗，继续执行其他任务")
    except Exception as exc:
        print(f"设备 {device_id} 连接失败：{exc}")

def task_centre(device_id):
    try:
        d = u2.connect(device_id)
        if d.xpath('//*[@text="瓜分百亿"]').wait(timeout=10):
            print(f"设备 {device_id} 已成功进入任务中心")
            
        else:
            print(f"设备 {device_id} 未检测到 瓜分百亿，重新执行一遍任务流程")
    except Exception as exc:
        print(f"设备 {device_id} 连接失败：{exc}")

def sign_in(device_id):
    try:
        d = u2.connect(device_id)
        if d.xpath('//*[@text="立即签到"]').wait(timeout=10):
            d.xpath('//*[@text="立即签到"]').click()
            print(f"设备 {device_id} 已点击 立即签到 元素")
        elif d.xpath('//android.widget.Button[@text="立即签到"]').wait(timeout=10):
            d.xpath('//android.widget.Button[@text="立即签到"]').click()
            print(f"设备 {device_id} 已点击 立即签到 按钮")
            sleep(5)  # 等待5秒，确保签到操作完成
            target_x, target_y = click_scaled(d, 1002, 373)
            print(f"设备 {device_id} 已点击签到后的确认位置: ({target_x}, {target_y})")
        else:
            print(f"设备 {device_id} 未找到 签到 元素")
    except Exception as exc:
        print(f"设备 {device_id} 连接失败：{exc}")


def back(device_id):
    try:
        d = u2.connect(device_id)
        d.press("back")
        print(f"设备 {device_id} 已执行返回操作")
    except Exception as exc:
        print(f"设备 {device_id} 返回失败：{exc}")


def novel_task(device_id):
    try:
        d = u2.connect(device_id)
        width, height = d.window_size()
        target = d.xpath('//*[@text="看小说领金币"]')

        for _ in range(8):
            if target.exists:
                target.click()
                print(f"设备 {device_id} 已点击 看小说领金币 元素")
                sleep(7)  # 等待7秒，确保点击操作完成

                next_target = d.xpath('//*[@resource-id="com.kuaishou.nebula.growth_novel_plugin:id/task_sub_title_wrapper"]')
                if next_target.wait(timeout=10):
                    next_target.click()
                    sleep(5)  # 等待5秒，确保点击操作完成
                    print(f"设备 {device_id} 已点击 小说任务子标题元素")
                else:
                    print(f"设备 {device_id} 未找到 小说任务子标题元素")
                    return

                claim_now = d.xpath('(//*[@text="立即领取"])[2]')
                if claim_now.exists:
                    claim_now.click()
                    sleep(5)  # 等待5秒，确保点击操作完成
                    print(f"设备 {device_id} 已点击 立即领取 按钮")
                else:
                    print(f"设备 {device_id} 未找到 立即领取 按钮")

                reading = d.xpath('(//*[@text="去阅读"])[3]')
                reading2 = d.xpath('(//*[@text="立即领取"])[2]')
                reading3 = d.xpath('//*[@text="去阅读"]')
                if reading.exists:
                    reading.click()
                    sleep(5)  # 等待5秒，确保点击操作完成
                    print(f"设备 {device_id} 已点击 去阅读 按钮")
                elif reading2.exists:
                    reading2.click()
                    sleep(5)  # 等待5秒，确保点击操作完成
                    print(f"设备 {device_id}识别到去阅读变成了立即领取按钮，已点击立即领取按钮")
                elif reading3.exists:
                    reading3.click()
                    sleep(5)  # 等待5秒，确保点击操作完成
                    print(f"设备 {device_id} 已点击 去阅读 按钮")
                else:
                    print(f"设备 {device_id} 未找到 去阅读 按钮")
                    return

                one_book = d.xpath('//*[@resource-id="com.kuaishou.nebula.growth_novel_plugin:id/book_cover"]')
                if one_book.exists:
                    one_book.click()
                    sleep(5)  # 等待5秒，确保点击操作完成
                    print(f"设备 {device_id} 已点击 小说封面元素")
                    # 这里是进入小说后随机滑动阅读的代码，模拟用户阅读小说的行为，持续40分钟
                    read_deadline = monotonic() + 40 * 60
                    while monotonic() < read_deadline:
                        width, height = d.window_size()
                        # 尽量在靠下的安全区域翻页，避开中间插屏广告和底部广告
                        swipe_y = random.randint(int(height * 0.82), int(height * 0.87))
                        start_x = random.randint(int(width * 0.78), int(width * 0.88))
                        end_x = random.randint(int(width * 0.18), int(width * 0.28))
                        d.swipe(start_x, swipe_y, end_x, swipe_y, random.uniform(0.12, 0.22))

                        read_seconds = random.randint(5, 21)
                        print(f"设备 {device_id} 正在阅读小说，在安全区域翻页，{read_seconds} 秒后翻到下一页")
                        sleep(read_seconds)

                    print(f"设备 {device_id} 已完成40分钟小说阅读")
                else:
                    print(f"设备 {device_id} 未找到 小说封面元素")
                    return
                
                back(device_id)
                sleep(5)  # 等待5秒，确保返回操作完成
                print(f"设备 {device_id} 已返回小说任务主界面,,,,向上滑动两次")
                width, height = d.window_size()
                for _ in range(2):
                    d.swipe(
                        int(width * 0.5),
                        int(height * 0.78),
                        int(width * 0.5),
                        int(height * 0.38),
                        0.2,
                    )
                    sleep(2)
                print(f"设备 {device_id} 已向上滑动两次")
                # 这里是返回，然后点击立即领取奖励按钮的代码
                task_item_button = d.xpath('//*[@resource-id="com.kuaishou.nebula.growth_novel_plugin:id/task_item_button"]')
                if task_item_button.wait(timeout=10):
                    click_count = 0
                    for _ in range(5):
                        if not task_item_button.exists:
                            break

                        task_item_button.click()
                        click_count += 1
                        print(f"设备 {device_id} 已点击 立即领取奖励 按钮，第 {click_count} 次")
                        sleep(3)

                    if click_count == 0:
                        print(f"设备 {device_id} 未成功点击 立即领取奖励 按钮")
                    else:
                        print(f"设备 {device_id} 已完成 {click_count} 次 立即领取奖励 按钮点击")
                else:
                    print(f"设备 {device_id} 未找到 立即领取奖励 按钮，进行返回操作")
                    back(device_id)
                    sleep(5)
                
                return

            d.swipe(
                int(width * 0.5),
                int(height * 0.78),
                int(width * 0.5),
                int(height * 0.38),
                0.2,
            )
            sleep(2)

        print(f"设备 {device_id} 多次下滑后仍未找到 看小说领金币 元素")
        return
    except Exception as exc:
        print(f"设备 {device_id} 连接失败：{exc}")



# 这里是任务列表，后面如果要加功能，可以继续增加函数并放到这个列表里
task_functions = [
    start_app, # 启动应用
    go_make_money, # 去赚钱
    task_centre, # 进入任务中心
    pop_up, # 识别广告弹窗并关闭
    sign_in, # 签到
    watch_video, # 刷视频，10分钟
    go_make_money, # 去赚钱
    task_centre, # 进入任务中心
    pop_up, # 识别广告弹窗并关闭
    claim_money, # 领取奖励
    novel_task, # 小说任务

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
