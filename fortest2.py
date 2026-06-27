from pathlib import Path
from datetime import datetime, timedelta
import shutil

SOURCE_ROOT = Path(r"D:\유클리닝자료백업")
DEST_DIR = Path(r"C:\Users\WD\Desktop\backup")

def copy_recent_zip_files(days: int = 7):
    today = datetime.today().date()
    start_date = today - timedelta(days=days - 1)  # 최근 7일 포함

    DEST_DIR.mkdir(parents=True, exist_ok=True)

    copied = 0
    skipped = 0

    for i in range(days):
        target_date = today - timedelta(days=i)
        folder_name = f"UDB_{target_date.strftime('%Y%m%d')}"
        folder_path = SOURCE_ROOT / folder_name

        if not folder_path.exists() or not folder_path.is_dir():
            continue

        for zip_file in folder_path.glob("*.zip"):
            dest_file = DEST_DIR / zip_file.name

            # 같은 이름이 있으면 날짜 폴더명을 붙여서 덮어쓰기 방지
            if dest_file.exists():
                dest_file = DEST_DIR / f"{zip_file.stem}_{folder_name}{zip_file.suffix}"

            shutil.copy2(zip_file, dest_file)
            copied += 1
            print(f"복사됨: {zip_file} -> {dest_file}")

    print(f"\n완료: {copied}개 복사")

if __name__ == "__main__":
    copy_recent_zip_files(days=7)