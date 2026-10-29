MaceInstaller One-Click GitHub Publisher

1. Extract the entire ZIP.
2. Put your current data.bin beside the BAT file.
3. Put icon.ico beside it if you want a custom icon (optional).
4. Check launcher_version in installer_config.ini (default 1.0.8).
5. Double-click Publish_MaceInstaller_GitHub.bat.

Requires Python, Git for Windows, Git LFS, and GitHub authentication for https://github.com/Kwvanty/Mace-Launcher.git.

Builds MaceInstaller.exe, copies it and the support files into the repository's Mace Installer folder, then commits and pushes. It does not delete unrelated existing files.
