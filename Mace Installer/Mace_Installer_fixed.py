import os
import sys
import time
import zipfile
import subprocess
import tkinter as tk
from tkinter import filedialog

if sys.platform == "win32":
    os.system("")

def get_base_dir():
    if getattr(sys, "frozen", False):
        return getattr(sys, "_MEIPASS", os.path.dirname(sys.executable))
    return os.path.dirname(os.path.abspath(__file__))

BASE_DIR = get_base_dir()
DATA_BIN_FILE = os.path.join(BASE_DIR, "data.bin")
DEFAULT_PATH = os.path.join(
    os.environ.get("ProgramFiles", r"C:\Program Files"),
    "Mace Launcher"
)

def select_directory_dialog(initial_dir):
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    selected_path = filedialog.askdirectory(
        title="Select Installation Directory",
        initialdir=initial_dir
    )
    root.destroy()

    if selected_path:
        if os.path.basename(os.path.normpath(selected_path)).lower() != "mace launcher":
            selected_path = os.path.join(selected_path, "Mace Launcher")
    return selected_path

def get_desktop_path():
    try:
        import ctypes
        from ctypes import wintypes
        CSIDL_DESKTOPDIRECTORY = 0x0010
        path = ctypes.create_unicode_buffer(wintypes.MAX_PATH)
        result = ctypes.windll.shell32.SHGetFolderPathW(
            None, CSIDL_DESKTOPDIRECTORY, None, 0, path
        )
        if result == 0 and path.value and os.path.isdir(path.value):
            return path.value
    except Exception:
        pass

    candidates = [
        os.path.join(os.environ.get("USERPROFILE", ""), "Desktop"),
        os.path.join(os.environ.get("USERPROFILE", ""), "OneDrive", "Desktop"),
    ]
    for candidate in candidates:
        if os.path.isdir(candidate):
            return candidate
    return candidates[0]

def create_shortcut(target_exe, shortcut_name="Mace Launcher V 1.0.5"):
    try:
        desktop = get_desktop_path()
        if not os.path.isdir(desktop):
            os.makedirs(desktop, exist_ok=True)

        shortcut_path = os.path.join(desktop, shortcut_name + ".lnk")
        target_exe = os.path.abspath(target_exe)
        working_dir = os.path.dirname(target_exe)

        def vbs_escape(value):
            return value.replace('"', '""')

        vbs_script = (
            'Set WshShell = WScript.CreateObject("WScript.Shell")\n'
            f'Set shortcut = WshShell.CreateShortcut("{vbs_escape(shortcut_path)}")\n'
            f'shortcut.TargetPath = "{vbs_escape(target_exe)}"\n'
            f'shortcut.WorkingDirectory = "{vbs_escape(working_dir)}"\n'
            f'shortcut.IconLocation = "{vbs_escape(target_exe)}, 0"\n'
            'shortcut.Save\n'
        )

        vbs_file = os.path.join(
            os.environ.get("TEMP", os.getcwd()),
            "mace_create_shortcut.vbs"
        )

        with open(vbs_file, "w", encoding="utf-8") as f:
            f.write(vbs_script)

        result = subprocess.run(
            ["cscript.exe", "//Nologo", vbs_file],
            capture_output=True,
            text=True,
            shell=False
        )

        try:
            os.remove(vbs_file)
        except OSError:
            pass

        if result.returncode != 0:
            print("\033[31m[!] Shortcut creation failed:\033[0m")
            if result.stderr:
                print(result.stderr.strip())
            return False

        if os.path.exists(shortcut_path):
            return True

        print("\033[31m[!] Shortcut was not created.\033[0m")
        return False

    except Exception as e:
        print(f"\033[31m[!] Failed to create shortcut: {e}\033[0m")
        return False

def find_exe_file(target_path):
    possible_names = ["run.exe", "Mace Launcher.exe", "MaceLauncher.exe"]
    for root, dirs, files in os.walk(target_path):
        for file in files:
            if file in possible_names:
                return os.path.join(root, file)
    return None

def get_color(percent):
    if percent < 35:
        return "\033[31m"
    elif percent < 70:
        return "\033[33m"
    return "\033[32m"

def print_progress_bar(iteration, total, prefix="", length=40):
    percent = int(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    color = get_color(percent)
    reset = "\033[0m"
    bar = "▰" * filled_length + "-" * (length - filled_length)
    sys.stdout.write(f"\r{prefix} [{color}{bar}{reset}] {percent}%")
    sys.stdout.flush()

def launch_exe(exe_path, text_locale):
    try:
        exe_path = os.path.abspath(exe_path)
        working_dir = os.path.dirname(exe_path)
        print("\033[36m[+] Launching Mace Launcher...\033[0m")
        print(f"    EXE: {exe_path}")
        process = subprocess.Popen([exe_path], cwd=working_dir)
        print(f"\033[32m[+] Mace Launcher started successfully (PID {process.pid}).\033[0m")
        return True
    except Exception as e:
        print("\033[31m[!] Failed to launch Mace Launcher:\033[0m")
        print(f"    {type(e).__name__}: {e}")
        input(f"\n{text_locale['press_enter']}")
        return False

def install(target_path, text_locale):
    print(f"\n[+] Target directory: {target_path}")

    if not os.path.exists(DATA_BIN_FILE):
        print(f"\n\033[31m[!] {text_locale['err_not_found']}\033[0m")
        input(f"\n{text_locale['press_enter']}")
        return False

    try:
        os.makedirs(target_path, exist_ok=True)
    except Exception as e:
        print(f"\n\033[31m[!] {text_locale['err_access']}: {e}\033[0m")
        input(f"\n{text_locale['press_enter']}")
        return False

    try:
        with zipfile.ZipFile(DATA_BIN_FILE, "r") as archive:
            file_list = archive.infolist()
            total_files = len(file_list)

            if total_files == 0:
                print(f"\n\033[31m[!] {text_locale['err_corrupt']}\033[0m")
                input(f"\n{text_locale['press_enter']}")
                return False

            print("\nStarting installation process...\n")
            for index, item in enumerate(file_list, start=1):
                archive.extract(item, target_path)
                print_progress_bar(index, total_files, prefix="Extracting:", length=40)
                time.sleep(0.01)
            print("\033[0m\n")

    except zipfile.BadZipFile:
        print(f"\n\033[31m[!] {text_locale['err_corrupt']}\033[0m")
        input(f"\n{text_locale['press_enter']}")
        return False
    except Exception as e:
        print(f"\n\033[31m[!] {text_locale['err_generic']}: {e}\033[0m")
        input(f"\n{text_locale['press_enter']}")
        return False

    exe_path = find_exe_file(target_path)

    if not exe_path:
        print(f"\033[31m[!] {text_locale['err_exe_not_found']}\033[0m")
        input(f"\n{text_locale['press_enter']}")
        return False

    shortcut_choice = input(f"{text_locale['shortcut_prompt']}").strip().upper()
    if shortcut_choice in ["Y", "YES", "Д", "ДА", "ТАК"]:
        if create_shortcut(exe_path):
            print("\033[32m[+] Desktop shortcut created successfully.\033[0m")
        else:
            print("\033[33m[!] Installation completed, but the Desktop shortcut could not be created.\033[0m")

    print("\n\033[32m=== Installation completed successfully! ===\033[0m")
    user_input = input(f"\n{text_locale['finish_prompt']}")

    if user_input == "":
        launch_exe(exe_path, text_locale)

    return True

print("\033[36m===| Welcome to the Mace Launcher 1.0.5 Setup |===\033[0m")
language = input("Please, select the installer language (EN/RU/UK): ").strip().upper()

LOCALES = {
    "EN": {
        "selected": "\nYou have selected English.",
        "prompt": "Do you want to select a custom installation path? (Y/N): ",
        "shortcut_prompt": "Do you want to create a Desktop shortcut? (Y/N): ",
        "dialog": "Opening directory selection window...",
        "canceled": "No path selected. Using default path: ",
        "default_msg": "Using default path: ",
        "err_not_found": "Error: Data package 'data.bin' inside installer is missing!",
        "err_corrupt": "Error: Package 'data.bin' is corrupted! Installation aborted.",
        "err_access": "Access error",
        "err_generic": "Extraction failed",
        "press_enter": "Press Enter to exit...",
        "finish_prompt": "Press Enter to launch Mace Launcher (or enter any text to exit): ",
        "err_exe_not_found": "Error: Mace Launcher executable not found!"
    },
    "RU": {
        "selected": "\nВы выбрали русский язык.",
        "prompt": "Хотите выбрать папку для установки? (Y/N): ",
        "shortcut_prompt": "Создать ярлык на рабочем столе? (Y/N): ",
        "dialog": "Открытие диалогового окна выбора папки...",
        "canceled": "Папка не выбрана. Используется путь по умолчанию: ",
        "default_msg": "Используется путь по умолчанию: ",
        "err_not_found": "Ошибка: Внутренний пакет 'data.bin' не найден!",
        "err_corrupt": "Ошибка: Файл 'data.bin' поврежден! Пожалуйста, скачайте инсталлятор заново.",
        "err_access": "Ошибка доступа",
        "err_generic": "Сбой при распаковке",
        "press_enter": "Нажмите Enter для выхода...",
        "finish_prompt": "Нажмите Enter для запуска Mace Launcher (или введите любой символ для выхода): ",
        "err_exe_not_found": "Ошибка: Исполняемый файл Mace Launcher не найден!"
    },
    "UK": {
        "selected": "\nВи обрали українську мову.",
        "prompt": "Бажаєте обрати шлях встановлення? (Y/N): ",
        "shortcut_prompt": "Створити ярлик на робочому столі? (Y/N): ",
        "dialog": "Відкриття діалогового вікна обрання папки...",
        "canceled": "Шлях не обрано. Використовується шлях за замовчуванням: ",
        "default_msg": "Використовується шлях за замовчуванням: ",
        "err_not_found": "Помилка: Внутрішній пакет 'data.bin' не знайдено!",
        "err_corrupt": "Помилка: Файл 'data.bin' пошкоджено! Будь ласка, завантажте інсталятор наново.",
        "err_access": "Помилка доступу",
        "err_generic": "Збій під час розпакування",
        "press_enter": "Натисніть Enter, щоб вийти...",
        "finish_prompt": "Натисніть Enter, щоб запустити Mace Launcher (або введіть будь-який символ, щоб вийти): ",
        "err_exe_not_found": "Помилка: Виконуваний файл Mace Launcher не знайдено!"
    }
}

if language not in LOCALES:
    language = "EN"

text = LOCALES[language]
print(text["selected"])

choice = input(f"{text['prompt']}").strip().upper()

if choice == "Y":
    print(text["dialog"])
    chosen_path = select_directory_dialog(DEFAULT_PATH)
    if chosen_path:
        install_path = chosen_path
    else:
        print(f"{text['canceled']} {DEFAULT_PATH}")
        install_path = DEFAULT_PATH
else:
    install_path = DEFAULT_PATH
    print(f"{text['default_msg']} {install_path}")

install(install_path, text)
