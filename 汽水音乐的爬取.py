import json
import os
import re
import sys
import urllib.parse
import urllib.request


SEARCH_API = "https://itunes.apple.com/search"
DOWNLOAD_DIR = os.path.join(os.path.dirname(__file__), "music_downloads")


def search_music(keyword, limit=10):
	params = {
		"term": keyword,
		"media": "music",
		"entity": "song",
		"limit": limit,
		"country": "CN",
	}
	url = f"{SEARCH_API}?{urllib.parse.urlencode(params)}"

	request = urllib.request.Request(
		url,
		headers={
			"User-Agent": "Mozilla/5.0",
			"Accept": "application/json",
		},
	)

	with urllib.request.urlopen(request, timeout=15) as response:
		return json.loads(response.read().decode("utf-8"))


def print_results(data):
	results = data.get("results", [])
	if not results:
		print("没有找到相关歌曲。")
		return results

	for index, item in enumerate(results, start=1):
		track_name = item.get("trackName", "未知歌曲")
		artist_name = item.get("artistName", "未知歌手")
		album_name = item.get("collectionName", "未知专辑")
		preview_url = item.get("previewUrl", "无")
		track_url = item.get("trackViewUrl", "无")

		print(f"\n结果 {index}")
		print(f"歌曲: {track_name}")
		print(f"歌手: {artist_name}")
		print(f"专辑: {album_name}")
		print(f"试听: {preview_url}")
		print(f"详情: {track_url}")

	return results


def sanitize_filename(value):
	cleaned = re.sub(r'[\\/:*?"<>|]', "_", value)
	return cleaned.strip().strip(".") or "unknown"


def get_download_path(item):
	track_name = sanitize_filename(item.get("trackName", "未知歌曲"))
	artist_name = sanitize_filename(item.get("artistName", "未知歌手"))
	preview_url = item.get("previewUrl", "")
	extension = os.path.splitext(urllib.parse.urlparse(preview_url).path)[1] or ".m4a"
	filename = f"{track_name} - {artist_name}{extension}"
	return os.path.join(DOWNLOAD_DIR, filename)


def download_preview(item):
	preview_url = item.get("previewUrl")
	if not preview_url:
		raise ValueError("当前结果没有可下载的试听链接")

	os.makedirs(DOWNLOAD_DIR, exist_ok=True)
	file_path = get_download_path(item)

	request = urllib.request.Request(
		preview_url,
		headers={
			"User-Agent": "Mozilla/5.0",
		},
	)

	with urllib.request.urlopen(request, timeout=30) as response, open(file_path, "wb") as output:
		output.write(response.read())

	return file_path


def prompt_download(results):
	if not results:
		return

	selection = input("请输入要下载的序号，直接回车跳过: ").strip()
	if not selection:
		return

	if not selection.isdigit():
		print("输入无效，请输入数字序号。")
		return

	index = int(selection)
	if index < 1 or index > len(results):
		print("序号超出范围。")
		return

	selected_item = results[index - 1]
	try:
		file_path = download_preview(selected_item)
	except Exception as exc:
		print(f"下载失败: {exc}")
		return

	print(f"已下载试听音频到: {file_path}")


def main():
	print("输入歌曲名称即可搜索音乐信息；输入 exit 退出。")
	print(f"下载目录: {DOWNLOAD_DIR}")

	while True:
		keyword = input("请输入歌曲名称: ").strip()

		if not keyword:
			print("歌曲名称不能为空。")
			continue

		if keyword.lower() in {"exit", "quit"}:
			print("程序已退出。")
			return

		try:
			data = search_music(keyword)
		except Exception as exc:
			print(f"查询失败: {exc}")
			continue

		results = print_results(data)
		prompt_download(results)


if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		print("\n程序已中断。")
		sys.exit(0)
