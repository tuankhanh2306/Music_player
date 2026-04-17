"""
File: src/audio_processing/whisper_service.py
Chức năng: Chuyển đổi file audio thành lời bài hát đồng bộ (Synchronized Lyrics).
Pipeline: File MP3 → Whisper (Speech-to-Text) → Chuỗi LRC chuẩn
"""
import logging
import os

logger = logging.getLogger(__name__)

# --- HỖ TRỢ WINDOWS: Thêm PATH cho ffmpeg từ WinGet nếu chưa có ---
def _ensure_ffmpeg_in_path():
    import shutil
    if shutil.which("ffmpeg"):
        return

    # Đường dẫn mặc định của WinGet FFmpeg
    winget_ffmpeg_path = r'C:\Users\ASUS\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1-full_build\bin'
    if os.path.exists(winget_ffmpeg_path):
        os.environ["PATH"] = winget_ffmpeg_path + os.pathsep + os.environ["PATH"]
        logger.info(f"Đã thêm ffmpeg vào PATH: {winget_ffmpeg_path}")

_ensure_ffmpeg_in_path()

# Cache model toàn cục để tránh load lại mỗi lần gọi (tốn ~3-5s mỗi lần load)
_whisper_model = None
_whisper_model_size = "base"


def _get_model():
    """Lazy-load Whisper model (chỉ load 1 lần, tái dùng cho các cuộc gọi sau)."""
    global _whisper_model
    if _whisper_model is None:
        try:
            import whisper
            logger.info(f"Đang tải Whisper model '{_whisper_model_size}'... (chỉ lần đầu)")
            _whisper_model = whisper.load_model(_whisper_model_size)
            logger.info("Whisper model đã sẵn sàng.")
        except ImportError:
            logger.error("Thư viện 'openai-whisper' chưa được cài đặt. Chạy: pip install openai-whisper")
            raise
        except Exception as e:
            logger.error(f"Lỗi khi load Whisper model: {e}")
            raise
    return _whisper_model


def _seconds_to_lrc_timestamp(seconds: float) -> str:
    """
    Chuyển đổi giây (float) sang định dạng LRC timestamp [mm:ss.xx].
    Ví dụ: 75.83 → [01:15.83]
    """
    minutes = int(seconds // 60)
    secs = seconds % 60
    return f"[{minutes:02d}:{secs:05.2f}]"


def transcribe_to_lrc(file_path: str) -> str | None:
    """
    Dùng Whisper để nhận diện lời bài hát từ file audio và format thành chuẩn LRC.

    Args:
        file_path: Đường dẫn tuyệt đối tới file audio (.mp3, .wav, ...)

    Returns:
        Chuỗi LRC format đầy đủ, ví dụ:
            [00:12.34] Lời câu đầu tiên
            [00:15.80] Câu tiếp theo...
        Trả về None nếu có lỗi xảy ra.
    """
    if not os.path.exists(file_path):
        logger.error(f"File không tồn tại: {file_path}")
        return None

    try:
        model = _get_model()

        logger.info(f"Bắt đầu Whisper transcription: {os.path.basename(file_path)}")

        # word_timestamps=False để lấy theo segment (câu), không theo từng chữ
        # verbose=False để không in log thừa ra console
        result = model.transcribe(
            file_path,
            word_timestamps=False,
            verbose=False,
            task="transcribe",
            # Thử tiếng Việt trước, Whisper sẽ tự detect nếu sai
            language=None,
        )

        segments = result.get("segments", [])

        if not segments:
            logger.warning(f"Whisper không nhận diện được lời trong file: {file_path}")
            # Trả về LRC rỗng hợp lệ thay vì None để phân biệt với lỗi
            return "[00:00.00] ♪"

        lrc_lines = []
        for seg in segments:
            start = seg.get("start", 0.0)
            text = seg.get("text", "").strip()
            if text:  # Bỏ qua segment rỗng
                timestamp = _seconds_to_lrc_timestamp(start)
                lrc_lines.append(f"{timestamp} {text}")

        lrc_content = "\n".join(lrc_lines)

        logger.info(
            f"Hoàn tất transcription: {len(lrc_lines)} dòng lời, "
            f"ngôn ngữ phát hiện: {result.get('language', 'unknown')}"
        )

        return lrc_content

    except ImportError:
        logger.error("openai-whisper chưa được cài. Bỏ qua transcription.")
        return None
    except Exception as e:
        logger.error(f"Lỗi Whisper transcription cho '{file_path}': {e}", exc_info=True)
        return None
