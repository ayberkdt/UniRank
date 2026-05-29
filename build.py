import os
import sys
import subprocess
from pathlib import Path

def build_executable():
    print("Building UniRank executable with PyInstaller...")
    
    # Proje dizini
    project_dir = Path(__file__).parent.resolve()
    
    # Gereksinimlerin yüklü olduğunu kontrol edelim
    try:
        import PyInstaller
    except ImportError:
        print("PyInstaller bulunamadı! 'pip install pyinstaller' ile yükleyin.")
        sys.exit(1)
        
    main_script = project_dir / "main.py"
    data_dir = project_dir / "data_base"
    
    # PyInstaller komutu
    # --noconfirm: overwrite existing build
    # --onedir: klasör olarak çıkarır (başlangıç daha hızlıdır)
    # --windowed: konsol penceresini gizler (sadece UI görünür)
    # --add-data: data_base klasörünü kopyalar
    cmd = [
        "pyinstaller",
        "--noconfirm",
        "--onedir",
        "--windowed",
        "--name", "UniRank",
        f"--add-data={data_dir}{os.pathsep}data_base",
        str(main_script)
    ]
    
    print(f"Running command: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=project_dir)
    
    if result.returncode == 0:
        print("\nBuild başarılı! 'dist/UniRank/UniRank.exe' yolunda bulabilirsiniz.")
    else:
        print("\nBuild sırasında hata oluştu.")
        sys.exit(result.returncode)

if __name__ == "__main__":
    build_executable()
