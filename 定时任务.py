import os  # 用于处理文件路径
import sys  # 用于获取当前 Python 可执行文件路径
import subprocess  # 用于运行外部命令


def create_task(name, script_name, start_time):
    script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), script_name))
    command = f'"{sys.executable}" "{script_path}"'
    print(f"创建任务 {name}：每天 {start_time} 运行 {script_name}")
    subprocess.run([
        'schtasks',
        '/Create',
        '/SC',
        'DAILY',
        '/TN',
        name,
        '/TR',
        command,
        '/ST',
        start_time,
        '/F',
    ], check=True)


create_task('RunTest', '快手极速版养号.py', '08:00')
create_task('RunTest2', '快手极速版养号.py', '12:20')
create_task('RunTest3', '快手极速版养号.py', '18:20')


print('定时任务已创建：')
print('  - RunTest  -> 每天 08:00 运行 快手极速版养号.py')
print('  - RunTest2 -> 每天 12:20 运行 快手极速版养号.py')
print('  - RunTest3 -> 每天 18:20 运行 快手极速版养号.py')
print('如何查看任务，点击开始菜单，搜索“任务计划程序”，打开后在“任务计划程序库”中可以看到创建的任务。')
# print('删除任务命令：schtasks /Delete /TN RunTest /F')  # RunTest是任务名称，/F表示强制删除，无需确认

