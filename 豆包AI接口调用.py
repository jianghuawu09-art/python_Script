import os

from volcenginesdkarkruntime import Ark
from volcenginesdkarkruntime._exceptions import ArkAPIError

BASE_URL = "https://ark.cn-beijing.volces.com/api/v3"
API_KEY = os.getenv("ARK_API_KEY")
MODEL = os.getenv("ARK_MODEL", "doubao-seed-2-0-pro-260215")

if not API_KEY:
    raise RuntimeError("未设置 ARK_API_KEY 环境变量")

client = Ark(
    base_url=BASE_URL,
    api_key=API_KEY,
)


def chat_once(messages):
    return client.chat.completions.create(
        model=MODEL,
        messages=messages,
        thinking={"type": "enabled"},
    )


def main():
    messages = []

    print(f"当前模型: {MODEL}")
    print("输入内容后回车即可继续追问；输入 exit 退出，输入 clear 清空上下文。")

    while True:
        user_input = input("你: ").strip()

        if not user_input:
            continue

        if user_input.lower() in {"exit", "quit"}:
            print("对话已结束。")
            break

        if user_input.lower() == "clear":
            messages.clear()
            print("上下文已清空。")
            continue

        messages.append({"role": "user", "content": user_input})

        try:
            resp = chat_once(messages)
        except ArkAPIError as exc:
            print("调用失败。")
            print(f"当前使用模型: {MODEL}")
            print(f"请求地址: {BASE_URL}/chat/completions")
            print(f"错误信息: {exc}")
            messages.pop()
            continue

        message = resp.choices[0].message
        assistant_text = message.content

        # if hasattr(message, "reasoning_content") and message.reasoning_content:
        #     print("思考:")
        #     print(message.reasoning_content)

        print("助手:")
        print(assistant_text)

        messages.append({"role": "assistant", "content": assistant_text})


if __name__ == "__main__":
    main()