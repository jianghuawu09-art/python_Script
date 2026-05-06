
# 这个脚本要开启网络连接，VPN 或科学上网工具才能成功下载模型并运行。
from pathlib import Path

TARGET_AUDIO = Path(r"D:\python\music_downloads\勋章 Medals - 鹿晗.m4a")
OUTPUT_DIR = TARGET_AUDIO.parent / "transcripts"
SUPPORTED_SUFFIXES = {".mp3", ".wav", ".m4a", ".flac", ".aac", ".ogg"}
MODEL_SIZE = "medium"
MODEL_CACHE_DIR = Path(r"D:\python\whisper_models")
LANGUAGE = "zh"
INITIAL_PROMPT = "以下内容是中文歌曲歌词，请尽量完整输出，不要省略重复句。"


def load_model():
	try:
		from faster_whisper import WhisperModel
	except ImportError as exc:
		raise RuntimeError(
			"缺少 faster-whisper 依赖，请先执行: pip install faster-whisper"
		) from exc

	try:
		MODEL_CACHE_DIR.mkdir(parents=True, exist_ok=True)
		return WhisperModel(
			MODEL_SIZE,
			device="cpu",
			compute_type="int8",
			download_root=str(MODEL_CACHE_DIR),
		)
	except Exception as exc:
		raise RuntimeError(
			"Whisper 模型加载失败。\n"
			"通常是第一次运行时需要从 Hugging Face 下载模型，但当前网络无法连接或下载超时。\n"
			f"模型名称: {MODEL_SIZE}\n"
			f"模型缓存目录: {MODEL_CACHE_DIR}\n"
			"解决方法：\n"
			"1. 保证当前电脑可以访问 Hugging Face，然后重新运行脚本。\n"
			"2. 如果网络不通，可以先手动下载 faster-whisper 对应模型到上述缓存目录，再运行脚本。\n"
			"3. 如果你只是想先测试流程，可以把 MODEL_SIZE 改成 tiny，但首次仍然需要联网下载。\n"
			f"原始错误: {exc}"
		) from exc


def validate_target_file(file_path: Path):
	if not file_path.exists():
		raise FileNotFoundError(f"目标音频文件不存在: {file_path}")
	if file_path.suffix.lower() not in SUPPORTED_SUFFIXES:
		raise ValueError(f"不支持的音频格式: {file_path.suffix}")


def transcribe_file(model, file_path: Path):
	segments, info = model.transcribe(
		str(file_path),
		language=LANGUAGE,
		vad_filter=False,
		beam_size=5,
		best_of=5,
		temperature=0,
		initial_prompt=INITIAL_PROMPT,
		condition_on_previous_text=False,
	)
	lines = [segment.text.strip() for segment in segments if segment.text.strip()]
	return "\n".join(lines), info.language, info.duration


def save_text(file_path: Path, text: str, detected_language: str, duration: float):
	OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
	output_path = OUTPUT_DIR / f"{file_path.stem}.txt"
	output_text = (
		f"文件: {file_path.name}\n"
		f"识别语言: {detected_language}\n"
		f"音频时长: {duration:.2f} 秒\n\n"
		f"{text}\n"
	)
	output_path.write_text(output_text, encoding="utf-8")
	return output_path


def main():
	print(f"目标文件: {TARGET_AUDIO}")
	print(f"输出目录: {OUTPUT_DIR}")
	validate_target_file(TARGET_AUDIO)

	model = load_model()

	print(f"\n开始识别: {TARGET_AUDIO.name}")
	text, detected_language, duration = transcribe_file(model, TARGET_AUDIO)

	if not text:
		print("未识别到有效文字。")
		return

	output_path = save_text(TARGET_AUDIO, text, detected_language, duration)
	print("识别内容:")
	print(text)
	print(f"识别完成，已保存到: {output_path}")


if __name__ == "__main__":
	try:
		main()
	except Exception as exc:
		print(f"运行失败: {exc}")
