import logging
import os
from logging.handlers import RotatingFileHandler

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "app.log")

# Tạo thư mục logs/ nếu chưa tồn tại
os.makedirs(LOG_DIR, exist_ok=True)

# Format chuẩn: timestamp - level - module - message
LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

def setup_logging(level: int = logging.INFO) -> None:
    """
    Khởi tạo cấu hình logging cho toàn bộ ứng dụng.
    Gọi hàm này một lần duy nhất trong main.py khi khởi động server.
    Output: console + file logs/app.log (tự xoay vòng khi đạt 5MB, giữ 3 bản backup).
    """
    formatter = logging.Formatter(fmt=LOG_FORMAT, datefmt=DATE_FORMAT)

    # --- Console Handler ---
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(level)

    # --- File Handler (RotatingFileHandler: tối đa 5MB, giữ 3 file backup) ---
    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=5 * 1024 * 1024,  # 5 MB
        backupCount=3,
        encoding="utf-8"
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(level)

    # --- Root Logger ---
    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    # Tránh thêm handler trùng lặp nếu setup_logging bị gọi nhiều lần
    if not root_logger.handlers:
        root_logger.addHandler(console_handler)
        root_logger.addHandler(file_handler)

    # Tắt bớt log ồn ào từ các thư viện bên thứ 3
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
