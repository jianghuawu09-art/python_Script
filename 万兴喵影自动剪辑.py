import subprocess
import sys
from pathlib import Path
FILMORA_EXE = Path(
    r"C:\Users\janny\AppData\Local\Wondershare\万兴喵影\Wondershare Filmora Launcher.exe"
)


def main():
    if not FILMORA_EXE.is_file():
        print(f"启动失败，未找到程序: {FILMORA_EXE}")
        sys.exit(1)

    try:
        subprocess.Popen([str(FILMORA_EXE)])
        print("万兴喵影已启动。")
    except Exception as exc:
        print(f"启动失败: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()