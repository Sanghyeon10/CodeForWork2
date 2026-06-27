import os
import sys

# 1. 방금까지 작성하신 백업 파이썬 코드의 실제 위치를 적어주세요.
# (예: 바탕화면에 backup_code.py 라고 저장하셨다면 아래 경로를 그대로 쓰시면 됩니다)
python_script_path = r"C:\Users\WD\PycharmProjects\pythonProject\GoogleBackup.py"


# 2. 만들어질 .bat 파일의 위치와 이름입니다.
bat_file_path = r"C:\Users\WD\Desktop\run_backup.bat"

# 3. 작업 스케줄러 환경에서도 완벽하게 작동하도록 현재 파이썬 실행기 경로를 가져옵니다.
python_exe = sys.executable

# 4. .bat 파일 안에 들어갈 명령어 내용 (한글 깨짐 방지 및 자동 종료 포함)
bat_content = f"""@echo off
chcp 65001 > nul
echo 🚀 백업 자동화 스크립트를 시작합니다...
echo.

"{python_exe}" "{python_script_path}"

echo.
echo 백업 작업이 완료되었습니다! 5초 뒤 창이 자동으로 닫힙니다.
timeout /t 5 > nul
"""

# 5. .bat 파일 생성 (쓰기 모드)
with open(bat_file_path, "w", encoding="utf-8") as f:
    f.write(bat_content)

print(f"✅ [ {os.path.basename(bat_file_path)} ] 파일이 성공적으로 생성되었습니다!")
print(f"저장된 위치: {bat_file_path}")