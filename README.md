# 🧹 CleanWin

**CleanWin** is a modern, bilingual Windows utility that allows users to safely remove unwanted built-in apps (like Xbox, Cortana, and OneDrive) with a clean and intuitive interface.

> ✨ No coding required. Just launch, select, and clean your Windows system.

## 🚀 Features

- ✅ Remove pre-installed Windows apps (e.g., Xbox, Cortana, OneDrive)
- 🎨 3-column grid layout with 28 custom app icons (48x48 pixels)
- 🌐 Bilingual interface (English & Persian) with RTL support
- 🔍 Search functionality to filter apps
- ⚡ Lazy loading for faster UI performance
- 🔐 Requires admin privileges for app removal

## 📸 Screenshots

### Main Window (English)
![Main Window (English)](screenshots/main_window.png)

### About Dialog
![About Dialog](screenshots/about_dialog.png)

## 🖥️ Installation

### 🧰 Prerequisites

- Windows 10 or 11 (64-bit)
- For development: Python 3.13+ and PyQt5 (`pip install PyQt5==5.15.10`)

### 📦 Run from Source


git clone https://github.com/hooman2007/cleanwin.git

cd cleanwin

pip install PyQt5==5.15.10

python cleanwin.py

📁 Download
Download the standalone executable from the Releases page.

Run CleanWin_v1.0.1.exe⚠️ Requires admin privileges

🛠️ Building Executable
To build the EXE using PyInstaller:
pip install PyInstaller
pyinstaller --noconfirm --onefile --windowed ^
  --upx-dir "C:\Program Files\UPX" ^
  --upx-exclude "vcruntime140.dll" ^
  --icon="icons/default.png" ^
  --add-data "icons;icons" ^
  --version-file "version.txt" ^
  --name CleanWinApp cleanwin.py


💡 Replace C:\Program Files\UPX with the path to your UPX installation directory.

🧪 Usage

Select a language (English or Persian) at launch
Choose apps to remove by checking the boxes
Click "Remove Selected Apps" (requires admin privileges)
Restart your PC to apply changes

🤝 Contributing
Contributions are welcome! Feel free to open issues or submit pull requests on GitHub.

Fork the repository
Create a feature branch (git checkout -b feature/your-feature)
Commit your changes (git commit -m "Add your feature")
Push to the branch (git push origin feature/your-feature)
Open a pull request

📄 License
This project is licensed under the MIT License.
👨‍💻 Author
Hooman Moezzi Azimi
📧 moezzi.hooman@gmail.com
🌐 https://hoomanmoezzi.ir
© 2025 Hooman Moezzi Azimi

Enjoy a clean, fast, and bloat-free Windows experience with CleanWin!
