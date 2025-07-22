   # CleanWin

   CleanWin is a powerful tool to effortlessly remove unwanted Windows apps, designed for simplicity and efficiency. It supports both English and Persian languages.

   ## Features
   - Remove pre-installed Windows apps (e.g., Xbox, Cortana, OneDrive).
   - User-friendly interface with a 3-column grid layout.
   - Supports 28 apps with custom icons (48x48 pixels).
   - Bilingual interface (English and Persian).
   - Requires admin privileges for app removal.

   ## Screenshots
   ![Main Window](screenshots/main_window.png)
   ![About Dialog](screenshots/about_dialog.png)

   ## Installation
   ### Prerequisites
   - Python 3.11+
   - PyQt5 (`pip install PyQt5`)

   ### Steps
   1. Clone the repository:
      ```bash
      git clone https://github.com/hooman2007/cleanwin.git
      cd cleanwin
      ```
   2. Install dependencies:
      ```bash
      pip install PyQt5
      ```
   3. Run the app:
      ```bash
      python cleanwin_gui.py
      ```

   ## Building Executable
   To create a standalone EXE:
   ```bash
   pip install PyInstaller
   pyinstaller --noconfirm --onefile --windowed --icon="icons/default.png" --add-data "icons;icons" --version-file "version.txt" cleanwin_gui.py

Usage

Select a language (English or Persian).
Choose apps to remove by checking the boxes.
Click "Remove Selected Apps" (requires admin privileges).
Restart your PC to apply changes.

License
MIT License
Author
Hooman Moezzi AzimiWebsite: https://www.hoomanmoezzi.ir Email: moezzi.hooman@gmail.com
© 2025 Hooman Moezzi Azimi

