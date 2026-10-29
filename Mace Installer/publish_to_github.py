#!/usr/bin/env python3
"""Build MaceInstaller, replace files in the GitHub repo's 'Mace Installer' folder, commit and push."""
from __future__ import annotations
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO_URL = "https://github.com/Kwvanty/Mace-Launcher.git"
REPO_DIR = ROOT / "_Mace-Launcher_repo"
TARGET_REL = Path("Mace Installer")

# Files from the builder folder that should be published alongside the EXE.
PUBLISH_FILES = [
    "Mace_Installer_fixed.py",
    "build_installer.py",
    "publish_to_github.py",
    "installer_config.ini",
    "README.txt",
    "data.bin",
    "icon.ico",
]

def run(args, cwd=None):
    print("\n> " + " ".join(str(x) for x in args), flush=True)
    subprocess.run([str(x) for x in args], cwd=cwd, check=True)

def main():
    try:
        # Build first so a failed build never replaces the published EXE.
        run([sys.executable, ROOT / "build_installer.py"], cwd=ROOT)
        cfg_text = (ROOT / "installer_config.ini").read_text(encoding="utf-8")
        exe_name = "MaceInstaller"
        for line in cfg_text.splitlines():
            if line.strip().lower().startswith("output_exe") and "=" in line:
                exe_name = line.split("=", 1)[1].strip() or exe_name
                break
        built_exe = ROOT / "dist" / f"{exe_name}.exe"
        if not built_exe.is_file():
            raise FileNotFoundError(f"Сборка не найдена: {built_exe}")

        if not (REPO_DIR / ".git").exists():
            if REPO_DIR.exists():
                shutil.rmtree(REPO_DIR)
            run(["git", "clone", REPO_URL, REPO_DIR])
        else:
            run(["git", "pull", "--rebase"], cwd=REPO_DIR)

        target = REPO_DIR / TARGET_REL
        target.mkdir(parents=True, exist_ok=True)
        shutil.copy2(built_exe, target / "MaceInstaller.exe")
        copied = ["MaceInstaller.exe"]
        for filename in PUBLISH_FILES:
            src = ROOT / filename
            if src.is_file():
                shutil.copy2(src, target / filename)
                copied.append(filename)

        # Ensure Git LFS is active for the installer executable, matching the repo's LFS setup.
        try:
            run(["git", "lfs", "install"], cwd=REPO_DIR)
            run(["git", "lfs", "track", "Mace Installer/MaceInstaller.exe"], cwd=REPO_DIR)
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("[!] Git LFS не найден. Если репозиторий хранит EXE через LFS, установи Git LFS и повтори запуск.")
            raise RuntimeError("Git LFS обязателен для безопасной публикации MaceInstaller.exe в этом репозитории.")

        run(["git", "add", "--", "Mace Installer"], cwd=REPO_DIR)
        status = subprocess.run(["git", "status", "--porcelain", "--", "Mace Installer"], cwd=REPO_DIR, text=True, capture_output=True, check=True).stdout.strip()
        if not status:
            print("\n[OK] Изменений для публикации нет — GitHub уже содержит эти файлы.")
            return

        run(["git", "commit", "-m", f"Update Mace Installer ({exe_name})"], cwd=REPO_DIR)
        # Push to the current branch's upstream; fallback to main if upstream is unset.
        # Push the checked-out branch; if no upstream exists, use origin and current branch name.
        push = subprocess.run(["git", "push"], cwd=REPO_DIR)
        if push.returncode != 0:
            branch = subprocess.run(["git", "branch", "--show-current"], cwd=REPO_DIR, text=True, capture_output=True, check=True).stdout.strip()
            if not branch:
                raise RuntimeError("Не удалось определить текущую ветку Git для push.")
            run(["git", "push", "-u", "origin", branch], cwd=REPO_DIR)

        print("\n[OK] Файлы опубликованы в GitHub:", REPO_URL)
        print("Папка: Mace Installer")
        print("Заменены/добавлены:", ", ".join(copied))
        print("Если GitHub запросит авторизацию, войди через настроенный Git Credential Manager.")
    except subprocess.CalledProcessError as e:
        print(f"\n[ERROR] Команда завершилась с кодом {e.returncode}.")
        print("Проверь Git, Git LFS, доступ к репозиторию и авторизацию GitHub.")
        sys.exit(e.returncode or 1)
    except Exception as e:
        print(f"\n[ERROR] {type(e).__name__}: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
