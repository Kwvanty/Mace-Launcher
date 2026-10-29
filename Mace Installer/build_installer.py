#!/usr/bin/env python3
from __future__ import annotations
import configparser, os, re, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def yes_no(v,name):
    v=v.strip().lower()
    if v in {"1","true","yes","y","да","так"}: return True
    if v in {"0","false","no","n","нет","ні"}: return False
    raise ValueError(f"{name}: ожидается true/false, получено {v!r}")

def load_config():
    cp=configparser.ConfigParser(interpolation=None)
    cp.read(ROOT/"installer_config.ini",encoding="utf-8")
    if "installer" not in cp: raise ValueError("В config отсутствует секция [installer]")
    s=cp["installer"]
    defaults={"launcher_version":"1.0.8","installer_version":"1.0.1","product_name":"Mace Launcher","output_exe":"MaceInstaller","source_file":"Mace_Installer_fixed.py","data_file":"data.bin","icon_file":"icon.ico","language_mode":"ask","language_default":"EN","shortcut_mode":"ask","launch_after_install":"ask","ask_custom_path":"true","onefile":"true","console":"true","clean":"true"}
    c={k:s.get(k,v).strip() for k,v in defaults.items()}
    c["language_mode"]=c["language_mode"].lower(); c["language_default"]=c["language_default"].upper()
    if c["language_mode"] not in {"ask","fixed"}: raise ValueError("language_mode должен быть ask или fixed")
    if c["language_default"] not in {"EN","RU","UK","UA"}: raise ValueError("language_default должен быть EN, RU, UK или UA")
    for k in ("shortcut_mode","launch_after_install"):
        c[k]=c[k].lower()
        if c[k] not in {"ask","yes","no"}: raise ValueError(f"{k} должен быть ask, yes или no")
    for k in ("ask_custom_path","onefile","console","clean"): c[k]=yes_no(c[k],k)
    if not re.fullmatch(r"[A-Za-z0-9_. -]+",c["output_exe"]): raise ValueError("Некорректное имя output_exe")
    return c

def make_configured_source(source,c):
    # Version text and shortcut version are updated even if the old source has another version.
    source,n=re.subn(r'(?m)^(\s*print\(.*?Welcome to the )Mace Launcher [0-9.]+( Setup.*)$',lambda m:m.group(1)+c["product_name"]+" "+c["launcher_version"]+m.group(2),source,count=1)
    if not n:
        source,n=re.subn(r'(?m)^(\s*print\(.*?Welcome to the )([^\n]*?)( Setup.*)$',lambda m:m.group(1)+c["product_name"]+" "+c["launcher_version"]+m.group(3),source,count=1)
    source=re.sub(r'(def create_shortcut\(target_exe,\s*shortcut_name=)["\'][^"\']*["\'](\):)',lambda m:m.group(1)+repr(c["product_name"]+" V "+c["launcher_version"])+m.group(2),source,count=1)
    source=source.replace('"Mace Launcher"',repr(c["product_name"]))
    if c["language_mode"]=="fixed":
        fixed=c["language_default"]
        if fixed in {"UK","UA"} and re.search(r"['\"]UА['\"]\s*:",source): fixed="UА"
        source,n=re.subn(r'(?m)^(\s*)language\s*=\s*input\([^\n]*$',lambda m:m.group(1)+"language = "+repr(fixed),source,count=1)
        if not n: raise ValueError("Не найдена строка language = input(...) в исходнике")
    if not c["ask_custom_path"]:
        source,n=re.subn(r'(?m)^(\s*)choice\s*=\s*input\([^\n]*$',r'\1choice = "N"',source,count=1)
        if not n: raise ValueError("Не найдена строка choice = input(...) для выбора пути")
    if c["shortcut_mode"] in {"yes","no"}:
        val="Y" if c["shortcut_mode"]=="yes" else "N"
        source,n=re.subn(r'(?m)^(\s*)shortcut_choice\s*=\s*input\([^\n]*$',lambda m:m.group(1)+"shortcut_choice = "+repr(val),source,count=1)
        if not n: raise ValueError("Не найдена строка shortcut_choice = input(...) в исходнике")
    if c["launch_after_install"] in {"yes","no"}:
        val="" if c["launch_after_install"]=="yes" else "exit"
        source,n=re.subn(r'(?m)^(\s*)user_input\s*=\s*input\([^\n]*$',lambda m:m.group(1)+"user_input = "+repr(val),source,count=1)
        if not n: raise ValueError("Не найдена строка user_input = input(...) в исходнике")
    return source

def main():
    try:
        c=load_config(); src=ROOT/c["source_file"]; data=ROOT/c["data_file"]; icon=ROOT/c["icon_file"]
        if not src.is_file(): raise FileNotFoundError(f"Не найден исходник: {src}")
        if not data.is_file(): raise FileNotFoundError(f"Не найден пакет {data}; положи data.bin рядом со сборщиком")
        icon_path=icon if c["icon_file"] and icon.is_file() else None
        if c["icon_file"] and icon_path is None: print(f"[!] Иконка не найдена: {icon}; сборка продолжится без неё.")
        configured=make_configured_source(src.read_text(encoding="utf-8-sig"),c)
        compile(configured,str(src),"exec")
        generated=ROOT/"_build_MaceInstaller.py"; generated.write_text(configured,encoding="utf-8")
        dist=ROOT/"dist"; work=ROOT/"build"; spec=ROOT/"spec"
        cmd=[sys.executable,"-m","PyInstaller","--name",c["output_exe"],"--distpath",str(dist),"--workpath",str(work),"--specpath",str(spec),"--onefile" if c["onefile"] else "--onedir","--console" if c["console"] else "--windowed"]
        if c["clean"]: cmd.append("--clean")
        if icon_path: cmd += ["--icon",str(icon_path)]
        cmd += ["--add-data",f"{data}{';' if os.name=='nt' else ':'}{data.name}",str(generated)]
        print("=== MaceInstaller Builder ===",flush=True); print("Версия лаунчера:",c["launcher_version"],flush=True)
        subprocess.run(cmd,cwd=ROOT,check=True)
        print(f"\n[OK] Сборка готова: {dist/(c['output_exe']+'.exe')}",flush=True)
    except subprocess.CalledProcessError as e:
        print(f"\n[ERROR] PyInstaller завершился с кодом {e.returncode}"); sys.exit(e.returncode or 1)
    except Exception as e:
        print(f"\n[ERROR] {type(e).__name__}: {e}"); sys.exit(1)
if __name__=="__main__": main()
