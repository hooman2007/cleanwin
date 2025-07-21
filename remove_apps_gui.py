import sys
import subprocess
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QTableWidget, QTableWidgetItem, QPushButton, QTextEdit,
    QDialog, QAction, QMessageBox, QDialogButtonBox, QLineEdit, QCheckBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QCursor

# استایل QSS برای تم روشن و جدولی
STYLESHEET = """
QMainWindow, QDialog {
    background-color: #f5f5f5;
    color: #333333;
}
QLabel {
    color: #333333;
    padding: 5px;
    font-size: 12px;
}
QTableWidget {
    background-color: #ffffff;
    color: #333333;
    border: 1px solid #e0e0e0;
    border-radius: 5px;
    gridline-color: #e0e0e0;
}
QTableWidget::item {
    padding: 6px;
    font-size: 11px;
}
QTableWidget::item:selected {
    background-color: #e6f0fa;
}
QPushButton {
    background-color: #4a90e2;
    color: #ffffff;
    border-radius: 5px;
    padding: 8px 14px;
    font-size: 12px;
    font-weight: 500;
}
QPushButton:hover {
    background-color: #357abd;
}
QPushButton:pressed {
    background-color: #2a6099;
}
QTextEdit {
    background-color: #ffffff;
    color: #333333;
    border: 1px solid #e0e0e0;
    border-radius: 5px;
    padding: 5px;
    font-size: 11px;
}
QLineEdit {
    background-color: #ffffff;
    color: #333333;
    border: 1px solid #e0e0e0;
    border-radius: 5px;
    padding: 5px;
    font-size: 11px;
}
QHeaderView::section {
    background-color: #f0f0f0;
    color: #333333;
    padding: 5px;
    border: 1px solid #e0e0e0;
}
QMenuBar {
    background-color: #f0f0f0;
    color: #333333;
}
QMenuBar::item:selected {
    background-color: #e6f0fa;
}
QCheckBox {
    color: #333333;
    padding: 5px;
}
"""

# لیست برنامه‌های پیش‌فرض ویندوز
PROGRAMS = [
    {"name": "OneDrive", "desc_en": "Microsoft cloud storage", "desc_fa": "ذخیره‌سازی ابری مایکروسافت", "powershell_name": "OneDrive"},
    {"name": "Cortana", "desc_en": "Microsoft assistant", "desc_fa": "دستیار مایکروسافت", "powershell_name": "Cortana"},
    {"name": "Xbox", "desc_en": "Microsoft gaming app", "desc_fa": "برنامه بازی‌های مایکروسافت", "powershell_name": "Xbox"},
    {"name": "Paint 3D", "desc_en": "3D modeling app", "desc_fa": "برنامه مدل‌سازی سه‌بعدی", "powershell_name": "Paint3D"},
    {"name": "Mixed Reality Portal", "desc_en": "VR/AR portal", "desc_fa": "درگاه واقعیت مجازی/افزوده", "powershell_name": "MixedRealityPortal"},
    {"name": "Skype", "desc_en": "Microsoft chat app", "desc_fa": "برنامه چت مایکروسافت", "powershell_name": "Skype"},
    {"name": "Office 365 Trial", "desc_en": "Microsoft Office trial version", "desc_fa": "نسخه آزمایشی آفیس ۳۶۵", "powershell_name": "Office"},
    {"name": "Your Phone", "desc_en": "Phone integration app", "desc_fa": "برنامه اتصال تلفن", "powershell_name": "YourPhone"},
    {"name": "Groove Music", "desc_en": "Music player app", "desc_fa": "پخش‌کننده موسیقی", "powershell_name": "ZuneMusic"},
    {"name": "Movies & TV", "desc_en": "Media player app", "desc_fa": "پخش‌کننده ویدئو", "powershell_name": "ZuneVideo"},
    {"name": "3D Viewer", "desc_en": "3D model viewer", "desc_fa": "نمایشگر مدل سه‌بعدی", "powershell_name": "3DViewer"},
    {"name": "Alarm and Clock", "desc_en": "Alarm and timer app", "desc_fa": "برنامه ساعت و هشدار", "powershell_name": "WindowsAlarms"},
    {"name": "Weather", "desc_en": "Weather forecasting app", "desc_fa": "برنامه هواشناسی", "powershell_name": "BingWeather"},
    {"name": "Feedback Hub", "desc_en": "Windows feedback app", "desc_fa": "برنامه ارسال بازخورد ویندوز", "powershell_name": "WindowsFeedbackHub"},
    {"name": "Snip & Sketch", "desc_en": "Screenshot and editing app", "desc_fa": "برنامه عکس‌برداری و ویرایش", "powershell_name": "ScreenSketch"},
    {"name": "Sticky Notes", "desc_en": "Note taking app", "desc_fa": "یادداشت چسبان", "powershell_name": "MicrosoftNotes"},
    {"name": "Maps", "desc_en": "Map and navigation app", "desc_fa": "برنامه نقشه", "powershell_name": "WindowsMaps"},
    {"name": "Mail", "desc_en": "Email client app", "desc_fa": "برنامه ایمیل", "powershell_name": "WindowsCommunicationsApps"},
    {"name": "News", "desc_en": "News app", "desc_fa": "برنامه اخبار", "powershell_name": "BingNews"},
    {"name": "Voice Recorder", "desc_en": "Audio recording app", "desc_fa": "برنامه ضبط صدا", "powershell_name": "WindowsSoundRecorder"},
    {"name": "People", "desc_en": "Contacts app", "desc_fa": "برنامه مخاطبین", "powershell_name": "People"},
    {"name": "Xbox Game Bar", "desc_en": "Gaming overlay", "desc_fa": "نوار بازی ایکس‌باکس", "powershell_name": "XboxGameOverlay"},
    {"name": "Photos", "desc_en": "Photo viewer and editor", "desc_fa": "نمایشگر و ویرایشگر عکس", "powershell_name": "Photos"},
    {"name": "Solitaire Collection", "desc_en": "Microsoft game collection", "desc_fa": "مجموعه بازی‌های مایکروسافت", "powershell_name": "MicrosoftSolitaireCollection"},
    {"name": "Get Help", "desc_en": "Windows support app", "desc_fa": "برنامه پشتیبانی ویندوز", "powershell_name": "ContactSupport"},
    {"name": "Microsoft Teams", "desc_en": "Collaboration platform", "desc_fa": "پلتفرم همکاری تیمی", "powershell_name": "Teams"},
    {"name": "Skype for Business", "desc_en": "Business communication app", "desc_fa": "برنامه ارتباط تجاری", "powershell_name": "SkypeBusiness"}
]

class LanguageDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.lang = None
        self.setWindowTitle("Select Language / انتخاب زبان")
        self.setMinimumSize(300, 100)
        layout = QVBoxLayout()
        layout.setSpacing(8)
        layout.setContentsMargins(8, 8, 8, 8)
        label = QLabel("Please select language / لطفاً زبان را انتخاب کنید:")
        label.setWordWrap(True)
        label.setFont(QFont("Segoe UI", 11))
        layout.addWidget(label)

        btn_layout = QHBoxLayout()
        btn_en = QPushButton("English")
        btn_fa = QPushButton("فارسی")
        btn_en.clicked.connect(lambda: self.choose_lang("en"))
        btn_fa.clicked.connect(lambda: self.choose_lang("fa"))
        btn_en.setCursor(QCursor(Qt.PointingHandCursor))
        btn_fa.setCursor(QCursor(Qt.PointingHandCursor))
        btn_layout.addWidget(btn_en)
        btn_layout.addWidget(btn_fa)
        layout.addLayout(btn_layout)
        self.setLayout(layout)
        self.setStyleSheet(STYLESHEET)

    def choose_lang(self, lang):
        self.lang = lang
        self.accept()

class AboutDialog(QDialog):
    def __init__(self, lang):
        super().__init__()
        self.lang = lang
        self.setWindowTitle("About CleanWin / درباره کلین‌وین")
        self.setMinimumSize(350, 150)
        layout = QVBoxLayout()
        layout.setSpacing(8)
        layout.setContentsMargins(10, 10, 10, 10)

        title = QLabel("<b>CleanWin</b>")
        title.setFont(QFont("Segoe UI", 14, QFont.Bold))
        desc = QLabel(
            "A simple tool to remove unwanted Windows apps quickly and easily." if lang == "en" else
            "ابزاری ساده برای حذف سریع و آسان برنامه‌های ناخواسته ویندوز."
        )
        desc.setWordWrap(True)
        desc.setFont(QFont("Segoe UI", 11))
        website = QLabel('<a href="https://hoomanmoezzi.ir" target="_blank">hoomanmoezzi.ir</a>')
        website.setOpenExternalLinks(True)
        website.setFont(QFont("Segoe UI", 11))
        website.setTextFormat(Qt.RichText)

        layout.addWidget(title)
        layout.addWidget(desc)
        layout.addWidget(website)
        layout.addStretch()

        btn_box = QDialogButtonBox(QDialogButtonBox.Close)
        btn_box.rejected.connect(self.close)
        layout.addWidget(btn_box)
        self.setLayout(layout)
        self.setStyleSheet(STYLESHEET)

class MainWindow(QMainWindow):
    def __init__(self, lang):
        super().__init__()
        self.lang = lang
        self.setWindowTitle("CleanWin" if lang == "en" else "کلین‌وین")
        self.setMinimumSize(800, 600)
        self.init_ui()

    def init_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout()
        main_layout.setSpacing(8)
        main_layout.setContentsMargins(10, 10, 10, 10)
        central.setLayout(main_layout)

        # جستجو
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search apps..." if self.lang == "en" else "جستجوی برنامه‌ها...")
        self.search_input.textChanged.connect(self.filter_apps)
        search_layout.addWidget(self.search_input)

        select_all_btn = QPushButton("Select All" if self.lang == "en" else "انتخاب همه")
        select_all_btn.clicked.connect(self.select_all)
        select_all_btn.setCursor(QCursor(Qt.PointingHandCursor))
        search_layout.addWidget(select_all_btn)
        main_layout.addLayout(search_layout)

        label_text = "Select programs to remove:" if self.lang == "en" else "برنامه‌های مورد نظر برای حذف را انتخاب کنید:"
        label = QLabel(label_text)
        label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        main_layout.addWidget(label)

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Select", "Name", "Description"] if self.lang == "en" else ["انتخاب", "نام", "توضیحات"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setSelectionMode(QTableWidget.NoSelection)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        main_layout.addWidget(self.table)

        self.populate_table()

        self.remove_btn = QPushButton("Remove Selected Apps" if self.lang == "en" else "حذف برنامه‌های انتخاب شده")
        self.remove_btn.setFont(QFont("Segoe UI", 12, QFont.Bold))
        self.remove_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.remove_btn.clicked.connect(self.remove_apps)
        main_layout.addWidget(self.remove_btn)

        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.output.setFont(QFont("Segoe UI", 11))
        self.output.setFixedHeight(80)
        main_layout.addWidget(self.output)

        menubar = self.menuBar()
        help_menu = menubar.addMenu("Help" if self.lang == "en" else "راهنما")
        about_action = QAction("About" if self.lang == "en" else "درباره", self)
        about_action.triggered.connect(self.show_about)
        guide_action = QAction("Usage Guide" if self.lang == "en" else "راهنمای استفاده", self)
        guide_action.triggered.connect(self.show_guide)
        help_menu.addAction(about_action)
        help_menu.addAction(guide_action)

        self.setStyleSheet(STYLESHEET)

    def populate_table(self):
        self.table.setRowCount(0)
        search_text = self.search_input.text().lower()
        for program in PROGRAMS:
            if search_text and search_text not in program["name"].lower():
                continue
            row = self.table.rowCount()
            self.table.insertRow(row)

            # چک‌باکس
            checkbox = QCheckBox()
            checkbox.setProperty("powershell_name", program["powershell_name"])
            checkbox.setCursor(QCursor(Qt.PointingHandCursor))
            checkbox_widget = QWidget()
            checkbox_layout = QHBoxLayout(checkbox_widget)
            checkbox_layout.addWidget(checkbox)
            checkbox_layout.setAlignment(Qt.AlignCenter)
            checkbox_layout.setContentsMargins(0, 0, 0, 0)
            self.table.setCellWidget(row, 0, checkbox_widget)

            # نام برنامه
            name_item = QTableWidgetItem(program["name"])
            name_item.setFont(QFont("Segoe UI", 11))
            self.table.setItem(row, 1, name_item)

            # توضیحات
            desc_item = QTableWidgetItem(program["desc_en"] if self.lang == "en" else program["desc_fa"])
            desc_item.setFont(QFont("Segoe UI", 11))
            self.table.setItem(row, 2, desc_item)

        self.table.resizeColumnsToContents()

    def filter_apps(self):
        self.populate_table()

    def select_all(self):
        state = not all(self.table.cellWidget(row, 0).findChild(QCheckBox).isChecked() for row in range(self.table.rowCount()))
        for row in range(self.table.rowCount()):
            self.table.cellWidget(row, 0).findChild(QCheckBox).setChecked(state)

    def remove_apps(self):
        selected = [self.table.cellWidget(row, 0).findChild(QCheckBox).property("powershell_name")
                    for row in range(self.table.rowCount()) if self.table.cellWidget(row, 0).findChild(QCheckBox).isChecked()]
        if not selected:
            msg = "Please select at least one app." if self.lang == "en" else "لطفاً حداقل یک برنامه را انتخاب کنید."
            QMessageBox.warning(self, "Warning" if self.lang == "en" else "هشدار", msg)
            return

        try:
            subprocess.check_call(['net', 'session'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except subprocess.CalledProcessError:
            msg = "This action requires admin privileges." if self.lang == "en" else "این عملیات نیاز به دسترسی ادمین دارد."
            QMessageBox.critical(self, "Error" if self.lang == "en" else "خطا", msg)
            return

        output = []
        for app in selected:
            try:
                cmd = f'Get-AppxPackage *"{app}"* | Remove-AppxPackage'
                subprocess.run(['powershell', '-Command', cmd], check=True, capture_output=True, text=True)
                output.append(f"<span style='color: #2e7d32'>{app}: Removed successfully</span>" if self.lang == "en" else f"<span style='color: #2e7d32'>{app}: با موفقیت حذف شد</span>")
            except subprocess.CalledProcessError as e:
                output.append(f"<span style='color: #d32f2f'>{app}: Failed to remove - {e.stderr}</span>" if self.lang == "en" else f"<span style='color: #d32f2f'>{app}: خطا در حذف - {e.stderr}</span>")
        
        self.output.setHtml("<br>".join(output))

    def show_about(self):
        AboutDialog(self.lang).exec()

    def show_guide(self):
        guide_text = (
            "1. Select apps to remove by checking the boxes.\n"
            "2. Click 'Remove Selected Apps' button.\n"
            "3. The app will be removed (requires admin privileges).\n"
            "4. Restart your PC after removal for changes to take effect."
        ) if self.lang == "en" else (
            "۱. برنامه‌های مورد نظر برای حذف را انتخاب کنید.\n"
            "۲. دکمه «حذف برنامه‌های انتخاب شده» را بزنید.\n"
            "۳. برنامه حذف خواهد شد (نیاز به دسترسی ادمین).\n"
            "۴. برای اعمال تغییرات، کامپیوتر را ری‌استارت کنید."
        )
        dlg = QDialog(self)
        dlg.setWindowTitle("Usage Guide" if self.lang == "en" else "راهنمای استفاده")
        dlg.setMinimumSize(400, 250)
        layout = QVBoxLayout()
        layout.setSpacing(8)
        layout.setContentsMargins(10, 10, 10, 10)
        label = QLabel(guide_text)
        label.setFont(QFont("Segoe UI", 11))
        label.setWordWrap(True)
        layout.addWidget(label)
        btn = QPushButton("Close" if self.lang == "en" else "بستن")
        btn.setCursor(QCursor(Qt.PointingHandCursor))
        layout.addWidget(btn, alignment=Qt.AlignCenter)
        dlg.setLayout(layout)
        dlg.setStyleSheet(STYLESHEET)
        dlg.exec()

def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    lang_dlg = LanguageDialog()
    if lang_dlg.exec() == QDialog.Accepted:
        lang = lang_dlg.lang
        win = MainWindow(lang)
        win.show()
        sys.exit(app.exec())

if __name__ == "__main__":
    main()