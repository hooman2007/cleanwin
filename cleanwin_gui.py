import sys
import os
import subprocess
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QTextEdit, QDialog, QAction, QMessageBox,
    QDialogButtonBox, QLineEdit, QCheckBox, QScrollArea, QProgressBar, QGridLayout
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QCursor, QIcon, QPixmap

# Set up icons directory
if getattr(sys, 'frozen', False):
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ICONS_DIR = os.path.join(BASE_DIR, "icons")
print(f"ICONS_DIR set to: {ICONS_DIR}")

# QSS stylesheet
STYLESHEET = """
QMainWindow, QDialog {
    background-color: #f8f9fa;
    color: #212529;
}
QLabel {
    color: #212529;
    padding: 6px;
    font-size: 14px;
}
QWidget#card {
    background-color: #ffffff;
    border: 1px solid #dee2e6;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    margin: 8px;
    padding: 10px;
}
QWidget#card:hover {
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}
QPushButton {
    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #4a90e2, stop:1 #17c4b5);
    color: #ffffff;
    border-radius: 6px;
    padding: 10px 20px;
    font-size: 14px;
    font-weight: 600;
}
QPushButton:hover {
    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #357abd, stop:1 #0f9d8a);
}
QPushButton:pressed {
    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #2a6099, stop:1 #0b7a6b);
}
QTextEdit {
    background-color: #ffffff;
    color: #212529;
    border: 1px solid #dee2e6;
    border-radius: 6px;
    padding: 8px;
    font-size: 13px;
}
QLineEdit {
    background-color: #ffffff;
    color: #212529;
    border: 1px solid #dee2e6;
    border-radius: 6px;
    padding: 8px;
    font-size: 13px;
}
QScrollArea {
    background-color: #f8f9fa;
    border: none;
}
QProgressBar {
    border: 1px solid #dee2e6;
    border-radius: 5px;
    text-align: center;
    font-size: 12px;
}
QProgressBar::chunk {
    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #4a90e2, stop:1 #17c4b5);
    border-radius: 5px;
}
QCheckBox {
    color: #212529;
    padding: 8px;
    font-size: 13px;
}
QMenuBar {
    background-color: #f0f0f0;
    color: #212529;
}
QMenuBar::item:selected {
    background-color: #e6f0fa;
}
"""

# List of programs to remove
PROGRAMS = [
    {"name": "OneDrive", "desc_en": "Microsoft cloud storage", "desc_fa": "ذخیره‌سازی ابری مایکروسافت", "powershell_name": "OneDrive", "icon": "onedrive.png"},
    {"name": "Cortana", "desc_en": "Microsoft assistant", "desc_fa": "دستیار مایکروسافت", "powershell_name": "Cortana", "icon": "cortana.png"},
    {"name": "Xbox", "desc_en": "Microsoft gaming app", "desc_fa": "برنامه بازی‌های مایکروسافت", "powershell_name": "Microsoft.Xbox.App", "icon": "xbox.png"},
    {"name": "Paint 3D", "desc_en": "3D modeling app", "desc_fa": "برنامه مدل‌سازی سه‌بعدی", "powershell_name": "Paint3D", "icon": "paint3d.png"},
    {"name": "Mixed Reality Portal", "desc_en": "VR/AR portal", "desc_fa": "درگاه واقعیت مجازی/افزوده", "powershell_name": "MixedRealityPortal", "icon": "mixedreality.png"},
    {"name": "Skype", "desc_en": "Microsoft chat app", "desc_fa": "برنامه چت مایکروسافت", "powershell_name": "Skype", "icon": "skype.png"},
    {"name": "Office 365 Trial", "desc_en": "Microsoft Office trial version", "desc_fa": "نسخه آزمایشی آفیس ۳۶۵", "powershell_name": "Office", "icon": "office.png"},
    {"name": "Your Phone", "desc_en": "Phone integration app", "desc_fa": "برنامه اتصال تلفن", "powershell_name": "YourPhone", "icon": "yourphone.png"},
    {"name": "Groove Music", "desc_en": "Music player app", "desc_fa": "پخش‌کننده موسیقی", "powershell_name": "ZuneMusic", "icon": "groovemusic.png"},
    {"name": "Movies & TV", "desc_en": "Media player app", "desc_fa": "پخش‌کننده ویدئو", "powershell_name": "ZuneVideo", "icon": "movies.png"},
    {"name": "3D Viewer", "desc_en": "3D model viewer", "desc_fa": "نمایشگر مدل سه‌بعدی", "powershell_name": "3DViewer", "icon": "3dviewer.png"},
    {"name": "Alarm and Clock", "desc_en": "Alarm and timer app", "desc_fa": "برنامه ساعت و هشدار", "powershell_name": "WindowsAlarms", "icon": "alarms.png"},
    {"name": "Weather", "desc_en": "Weather forecasting app", "desc_fa": "برنامه هواشناسی", "powershell_name": "BingWeather", "icon": "weather.png"},
    {"name": "Feedback Hub", "desc_en": "Windows feedback app", "desc_fa": "برنامه ارسال بازخورد ویندوز", "powershell_name": "WindowsFeedbackHub", "icon": "feedback.png"},
    {"name": "Snip & Sketch", "desc_en": "Screenshot and editing app", "desc_fa": "برنامه عکس‌برداری و ویرایش", "powershell_name": "ScreenSketch", "icon": "snip.png"},
    {"name": "Sticky Notes", "desc_en": "Note taking app", "desc_fa": "یادداشت چسبان", "powershell_name": "MicrosoftNotes", "icon": "stickynotes.png"},
    {"name": "Maps", "desc_en": "Map and navigation app", "desc_fa": "برنامه نقشه", "powershell_name": "WindowsMaps", "icon": "maps.png"},
    {"name": "Mail", "desc_en": "Email client app", "desc_fa": "برنامه ایمیل", "powershell_name": "WindowsCommunicationsApps", "icon": "mail.png"},
    {"name": "News", "desc_en": "News app", "desc_fa": "برنامه اخبار", "powershell_name": "BingNews", "icon": "news.png"},
    {"name": "Voice Recorder", "desc_en": "Audio recording app", "desc_fa": "برنامه ضبط صدا", "powershell_name": "WindowsSoundRecorder", "icon": "voicerecorder.png"},
    {"name": "People", "desc_en": "Contacts app", "desc_fa": "برنامه مخاطبین", "powershell_name": "People", "icon": "people.png"},
    {"name": "Xbox Game Bar", "desc_en": "Gaming overlay", "desc_fa": "نوار بازی ایکس‌باکس", "powershell_name": "XboxGameOverlay", "icon": "xboxgamebar.png"},
    {"name": "Photos", "desc_en": "Photo viewer and editor", "desc_fa": "نمایشگر و ویرایشگر عکس", "powershell_name": "Photos", "icon": "photos.png"},
    {"name": "Solitaire Collection", "desc_en": "Microsoft game collection", "desc_fa": "مجموعه بازی‌های مایکروسافت", "powershell_name": "MicrosoftSolitaireCollection", "icon": "solitaire.png"},
    {"name": "Get Help", "desc_en": "Windows support app", "desc_fa": "برنامه پشتیبانی ویندوز", "powershell_name": "ContactSupport", "icon": "gethelp.png"},
    {"name": "Microsoft Teams", "desc_en": "Collaboration platform", "desc_fa": "پلتفرم همکاری تیمی", "powershell_name": "Teams", "icon": "teams.png"},
    {"name": "Paint", "desc_en": "Classic Microsoft Paint app", "desc_fa": "برنامه نقاشی کلاسیک مایکروسافت", "powershell_name": "MicrosoftPaint", "icon": "paint.png"},
    {"name": "Camera", "desc_en": "Windows Camera app", "desc_fa": "برنامه دوربین ویندوز", "powershell_name": "WindowsCamera", "icon": "camera.png"}
]

class LanguageDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.lang = None
        self.setWindowTitle("Select Language / انتخاب زبان")
        self.setMinimumSize(350, 150)
        default_icon_path = os.path.join(ICONS_DIR, "default.png")
        print(f"Checking LanguageDialog icon: {default_icon_path}")
        if os.path.exists(default_icon_path):
            self.setWindowIcon(QIcon(default_icon_path))
            print(f"Loaded LanguageDialog icon: {default_icon_path}")
        else:
            print(f"Error: LanguageDialog icon not found at {default_icon_path}")
        self.setStyleSheet(STYLESHEET)
        layout = QVBoxLayout()
        layout.setSpacing(8)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Language selection label
        label = QLabel("Please select language / لطفاً زبان را انتخاب کنید:")
        label.setWordWrap(True)
        label.setFont(QFont("Segoe UI", 14))
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        # Language buttons
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

    def choose_lang(self, lang):
        self.lang = lang
        self.accept()

class AboutDialog(QDialog):
    def __init__(self, lang):
        super().__init__()
        self.lang = lang
        self.setWindowTitle("About CleanWin")
        self.setMinimumSize(550, 350)
        default_icon_path = os.path.join(ICONS_DIR, "default.png")
        print(f"Checking AboutDialog window icon: {default_icon_path}")
        if os.path.exists(default_icon_path):
            self.setWindowIcon(QIcon(default_icon_path))
            print(f"Loaded AboutDialog window icon: {default_icon_path}")
        else:
            print(f"Error: AboutDialog window icon not found at {default_icon_path}")
        if lang == "fa":
            self.setLayoutDirection(Qt.RightToLeft)
        self.setStyleSheet(STYLESHEET)
        layout = QVBoxLayout()
        layout.setSpacing(8)
        layout.setContentsMargins(15, 15, 15, 15)

        # Header
        header = QWidget()
        header.setFixedHeight(80)
        header.setStyleSheet("background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #4a90e2, stop:1 #17c4b5); border-radius: 8px;")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(10, 5, 10, 5)
        title_icon = QLabel()
        title_icon_path = os.path.join(ICONS_DIR, "default.png")
        print(f"Checking AboutDialog header icon: {title_icon_path}")
        if os.path.exists(title_icon_path):
            title_icon.setPixmap(QPixmap(title_icon_path).scaled(48, 48, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            print(f"Loaded AboutDialog header icon: {title_icon_path}")
        else:
            print(f"Error: AboutDialog header icon not found at {title_icon_path}")
        title_label = QLabel("<b>CleanWin v1.0.1</b>")
        title_label.setFont(QFont("Segoe UI", 20, QFont.Bold))
        title_label.setStyleSheet("color: #ffffff; padding: 8px;")
        if lang == "fa":
            title_label.setAlignment(Qt.AlignRight)
        header_layout.addWidget(title_icon)
        header_layout.addWidget(title_label)
        header_layout.addStretch()

        # Description
        desc_layout = QHBoxLayout()
        desc_layout.setSpacing(5)
        desc_icon = QLabel()
        desc_icon_path = os.path.join(ICONS_DIR, "about_icon.png")
        print(f"Checking AboutDialog description icon: {desc_icon_path}")
        if os.path.exists(desc_icon_path):
            desc_icon.setPixmap(QPixmap(desc_icon_path).scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            print(f"Loaded AboutDialog description icon: {desc_icon_path}")
        else:
            default_icon_path = os.path.join(ICONS_DIR, "default.png")
            if os.path.exists(default_icon_path):
                desc_icon.setPixmap(QPixmap(default_icon_path).scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                print(f"Warning: Used default icon for description, {desc_icon_path} not found")
            else:
                print(f"Error: AboutDialog description icon and default icon not found: {desc_icon_path}, {default_icon_path}")
        desc = QLabel(
            "CleanWin: A powerful tool to effortlessly remove unwanted Windows apps, designed for simplicity and efficiency." if lang == "en" else
            "کلین‌وین: ابزاری قدرتمند برای حذف آسان و سریع برنامه‌های ناخواسته ویندوز، طراحی‌شده با سادگی و کارایی."
        )
        desc.setWordWrap(True)
        desc.setFont(QFont("Segoe UI", 16))
        desc.setFixedWidth(400)
        if lang == "fa":
            desc.setAlignment(Qt.AlignRight)
        else:
            desc.setAlignment(Qt.AlignLeft)
        desc_layout.addWidget(desc_icon)
        desc_layout.addWidget(desc)
        desc_layout.addStretch()

        # Developer
        dev_layout = QHBoxLayout()
        dev_layout.setSpacing(5)
        dev_icon = QLabel()
        dev_icon_path = os.path.join(ICONS_DIR, "developer_icon.png")
        print(f"Checking AboutDialog developer icon: {dev_icon_path}")
        if os.path.exists(dev_icon_path):
            dev_icon.setPixmap(QPixmap(dev_icon_path).scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            print(f"Loaded AboutDialog developer icon: {dev_icon_path}")
        else:
            default_icon_path = os.path.join(ICONS_DIR, "default.png")
            if os.path.exists(default_icon_path):
                dev_icon.setPixmap(QPixmap(default_icon_path).scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                print(f"Warning: Used default icon for developer, {dev_icon_path} not found")
            else:
                print(f"Error: AboutDialog developer icon and default icon not found: {dev_icon_path}, {default_icon_path}")
        dev = QLabel("Developer: Hooman Moezzi Azimi")
        dev.setFont(QFont("Segoe UI", 14))
        dev.setFixedWidth(400)
        if lang == "fa":
            dev.setAlignment(Qt.AlignRight)
        else:
            dev.setAlignment(Qt.AlignLeft)
        dev_layout.addWidget(dev_icon)
        dev_layout.addWidget(dev)
        dev_layout.addStretch()

        # Website
        website_layout = QHBoxLayout()
        website_layout.setSpacing(5)
        website_icon = QLabel()
        website_icon_path = os.path.join(ICONS_DIR, "website_icon.png")
        print(f"Checking AboutDialog website icon: {website_icon_path}")
        if os.path.exists(website_icon_path):
            website_icon.setPixmap(QPixmap(website_icon_path).scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            print(f"Loaded AboutDialog website icon: {website_icon_path}")
        else:
            default_icon_path = os.path.join(ICONS_DIR, "default.png")
            if os.path.exists(default_icon_path):
                website_icon.setPixmap(QPixmap(default_icon_path).scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                print(f"Warning: Used default icon for website, {website_icon_path} not found")
            else:
                print(f"Error: AboutDialog website icon and default icon not found: {website_icon_path}, {default_icon_path}")
        website = QLabel('<a href="https://hoomanmoezzi.ir">https://hoomanmoezzi.ir</a>')
        website.setOpenExternalLinks(True)
        website.setFont(QFont("Segoe UI", 14))
        website.setTextFormat(Qt.RichText)
        website.setFixedWidth(400)
        if lang == "fa":
            website.setAlignment(Qt.AlignRight)
        else:
            website.setAlignment(Qt.AlignLeft)
        website_layout.addWidget(website_icon)
        website_layout.addWidget(website)
        website_layout.addStretch()

        # Email
        email_layout = QHBoxLayout()
        email_layout.setSpacing(5)
        email_icon = QLabel()
        email_icon_path = os.path.join(ICONS_DIR, "email_icon.png")
        print(f"Checking AboutDialog email icon: {email_icon_path}")
        if os.path.exists(email_icon_path):
            email_icon.setPixmap(QPixmap(email_icon_path).scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            print(f"Loaded AboutDialog email icon: {email_icon_path}")
        else:
            default_icon_path = os.path.join(ICONS_DIR, "default.png")
            if os.path.exists(default_icon_path):
                email_icon.setPixmap(QPixmap(default_icon_path).scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                print(f"Warning: Used default icon for email, {email_icon_path} not found")
            else:
                print(f"Error: AboutDialog email icon and default icon not found: {email_icon_path}, {default_icon_path}")
        email = QLabel('<a href="mailto:moezzi.hooman@gmail.com">moezzi.hooman@gmail.com</a>')
        email.setOpenExternalLinks(True)
        email.setFont(QFont("Segoe UI", 14))
        email.setTextFormat(Qt.RichText)
        email.setFixedWidth(400)
        if lang == "fa":
            email.setAlignment(Qt.AlignRight)
        else:
            email.setAlignment(Qt.AlignLeft)
        email_layout.addWidget(email_icon)
        email_layout.addWidget(email)
        email_layout.addStretch()

        layout.addWidget(header)
        layout.addLayout(desc_layout)
        layout.addLayout(dev_layout)
        layout.addLayout(website_layout)
        layout.addLayout(email_layout)
        layout.addStretch()

        # Close button
        btn_box = QDialogButtonBox(QDialogButtonBox.Close)
        btn_box.rejected.connect(self.reject)
        btn_box.button(QDialogButtonBox.Close).setText("Close" if lang == "en" else "بستن")
        layout.addWidget(btn_box)
        self.setLayout(layout)

class MainWindow(QMainWindow):
    def __init__(self, lang):
        super().__init__()
        self.lang = lang
        self.setWindowTitle("CleanWin v1.0.1")
        self.setMinimumSize(1200, 900)
        default_icon_path = os.path.join(ICONS_DIR, "default.png")
        print(f"Checking MainWindow icon: {default_icon_path}")
        if os.path.exists(default_icon_path):
            self.setWindowIcon(QIcon(default_icon_path))
            print(f"Loaded MainWindow icon: {default_icon_path}")
        else:
            print(f"Error: MainWindow icon not found at {default_icon_path}")
        if lang == "fa":
            self.setLayoutDirection(Qt.RightToLeft)
        self.setStyleSheet(STYLESHEET)
        self.init_ui()

    def init_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout()
        main_layout.setSpacing(12)
        main_layout.setContentsMargins(15, 15, 15, 15)
        central.setLayout(main_layout)

        # Header
        header = QWidget()
        header.setFixedHeight(80)
        header.setStyleSheet("background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #4a90e2, stop:1 #17c4b5); border-radius: 8px;")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(10, 5, 10, 5)
        title_icon = QLabel()
        title_icon_path = os.path.join(ICONS_DIR, "default.png")
        print(f"Checking MainWindow header icon: {title_icon_path}")
        if os.path.exists(title_icon_path):
            title_icon.setPixmap(QPixmap(title_icon_path).scaled(48, 48, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            print(f"Loaded MainWindow header icon: {title_icon_path}")
        else:
            print(f"Error: MainWindow header icon not found at {title_icon_path}")
        title_label = QLabel("CleanWin v1.0.1" if self.lang == "en" else "کلین‌وین نسخه ۱.۰.۱")
        title_label.setFont(QFont("Segoe UI", 20, QFont.Bold))
        title_label.setStyleSheet("color: #ffffff; padding: 8px;")
        if self.lang == "fa":
            title_label.setAlignment(Qt.AlignRight)
        header_layout.addWidget(title_icon)
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        main_layout.addWidget(header)

        # Search bar
        search_layout = QHBoxLayout()
        search_layout.setSpacing(8)
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search apps..." if self.lang == "en" else "جستجوی برنامه‌ها...")
        self.search_input.textChanged.connect(self.filter_apps)
        if self.lang == "fa":
            self.search_input.setAlignment(Qt.AlignRight)
        search_layout.addWidget(self.search_input)

        select_all_btn = QPushButton("Select All" if self.lang == "en" else "انتخاب همه")
        select_all_btn.clicked.connect(self.select_all)
        select_all_btn.setCursor(QCursor(Qt.PointingHandCursor))
        search_layout.addWidget(select_all_btn)
        main_layout.addLayout(search_layout)

        # Apps label
        label_text = "Select programs to remove:" if self.lang == "en" else "برنامه‌های مورد نظر برای حذف را انتخاب کنید:"
        label = QLabel(label_text)
        label.setFont(QFont("Segoe UI", 16, QFont.Bold))
        if self.lang == "fa":
            label.setAlignment(Qt.AlignRight)
        main_layout.addWidget(label)

        # Scroll area for app cards
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(12)
        self.grid_layout.setContentsMargins(10, 10, 10, 10)
        self.scroll_content.setLayout(self.grid_layout)
        self.scroll.setWidget(self.scroll_content)
        main_layout.addWidget(self.scroll)

        self.cards = []
        self.populate_cards()

        # Remove button
        self.remove_btn = QPushButton("Remove Selected Apps" if self.lang == "en" else "حذف برنامه‌های انتخاب شده")
        self.remove_btn.setFont(QFont("Segoe UI", 14, QFont.Bold))
        self.remove_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.remove_btn.clicked.connect(self.remove_apps)
        main_layout.addWidget(self.remove_btn)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(False)
        main_layout.addWidget(self.progress_bar)

        # Output console
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.output.setFont(QFont("Segoe UI", 13))
        self.output.setFixedHeight(120)
        if self.lang == "fa":
            self.output.setAlignment(Qt.AlignRight)
        main_layout.addWidget(self.output)

        # Help menu
        menubar = self.menuBar()
        help_menu = menubar.addMenu("Help" if self.lang == "en" else "راهنما")
        about_action = QAction("About" if self.lang == "en" else "درباره", self)
        about_action.triggered.connect(self.show_about)
        guide_action = QAction("Usage Guide" if self.lang == "en" else "راهنمای استفاده", self)
        guide_action.triggered.connect(self.show_guide)
        help_menu.addAction(about_action)
        help_menu.addAction(guide_action)

    def populate_cards(self):
        # Clear existing cards
        for widget in self.scroll_content.findChildren(QWidget):
            widget.deleteLater()
        self.cards.clear()

        # Filter and populate app cards
        search_text = self.search_input.text().lower()
        for i, program in enumerate(PROGRAMS):
            if search_text and search_text not in program["name"].lower():
                continue
            card = QWidget()
            card.setObjectName("card")
            card_layout = QHBoxLayout(card)
            card_layout.setContentsMargins(8, 8, 8, 8)
            card_layout.setSpacing(8)

            # Program icon
            icon_path = os.path.join(ICONS_DIR, program["icon"])
            print(f"Checking program icon: {icon_path}")
            icon = QLabel()
            if os.path.exists(icon_path):
                icon.setPixmap(QPixmap(icon_path).scaled(48, 48, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                print(f"Loaded program icon: {icon_path}")
            else:
                default_icon_path = os.path.join(ICONS_DIR, "default.png")
                if os.path.exists(default_icon_path):
                    icon.setPixmap(QPixmap(default_icon_path).scaled(48, 48, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                    print(f"Warning: Used default icon for {program['name']}, {icon_path} not found")
                else:
                    print(f"Error: Program icon and default icon not found: {icon_path}, {default_icon_path}")
            card_layout.addWidget(icon)

            # Program name and description
            text_layout = QVBoxLayout()
            name_label = QLabel(program["name"])
            name_label.setFont(QFont("Segoe UI", 14, QFont.Bold))
            desc_label = QLabel(program["desc_en"] if self.lang == "en" else program["desc_fa"])
            desc_label.setFont(QFont("Segoe UI", 12))
            desc_label.setWordWrap(True)
            if self.lang == "fa":
                name_label.setAlignment(Qt.AlignRight)
                desc_label.setAlignment(Qt.AlignRight)
            text_layout.addWidget(name_label)
            text_layout.addWidget(desc_label)
            card_layout.addLayout(text_layout)

            # Checkbox
            checkbox = QCheckBox()
            checkbox.setProperty("powershell_name", program["powershell_name"])
            checkbox.setCursor(QCursor(Qt.PointingHandCursor))
            card_layout.addWidget(checkbox, alignment=Qt.AlignRight)

            # Add card to grid layout (3 columns)
            row = i // 3
            col = i % 3
            self.grid_layout.addWidget(card, row, col)
            self.cards.append(checkbox)

        self.grid_layout.setRowStretch(self.grid_layout.rowCount(), 1)

    def filter_apps(self):
        self.populate_cards()

    def select_all(self):
        state = not all(cb.isChecked() for cb in self.cards)
        for cb in self.cards:
            cb.setChecked(state)

    def remove_apps(self):
        # Get selected apps
        selected = [cb.property("powershell_name") for cb in self.cards if cb.isChecked()]
        if not selected:
            msg = "Please select at least one app." if self.lang == "en" else "لطفاً حداقل یک برنامه را انتخاب کنید."
            QMessageBox.warning(self, "Warning" if self.lang == "en" else "هشدار", msg)
            return

        # Check for admin privileges
        try:
            subprocess.check_call(['net', 'session'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except subprocess.CalledProcessError:
            msg = "This action requires admin privileges. Please run the program as administrator." if self.lang == "en" else "این عملیات نیاز به دسترسی ادمین دارد. لطفاً برنامه را با دسترسی ادمین اجرا کنید."
            QMessageBox.critical(self, "Error" if self.lang == "en" else "خطا", msg)
            return

        self.progress_bar.setVisible(True)
        self.progress_bar.setMaximum(len(selected))
        output = []

        # Remove apps using PowerShell
        for i, app in enumerate(selected):
            # Remove installed package
            cmd = f'Get-AppxPackage -AllUsers *{app}* | Remove-AppxPackage -ErrorAction SilentlyContinue'
            try:
                result = subprocess.run(
                    ['powershell', '-Command', cmd],
                    check=True,
                    capture_output=True,
                    text=True,
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
                output.append(f"<span style='color: #2e7d32'>{app}: Removed successfully</span>" if self.lang == "en" else
                              f"<span style='color: #2e7d32'>{app}: با موفقیت حذف شد</span>")
            except subprocess.CalledProcessError as e:
                error_msg = e.stderr.strip() or "Unknown error"
                output.append(f"<span style='color: #d32f2f'>{app}: Failed to remove - {error_msg}</span>" if self.lang == "en" else
                              f"<span style='color: #d32f2f'>{app}: خطا در حذف - {error_msg}</span>")
            
            # Remove provisioned package
            cmd_provisioned = f'Get-AppxProvisionedPackage -Online | Where-Object {{$_.PackageName -like "*{app}*"}} | Remove-AppxProvisionedPackage -Online -ErrorAction SilentlyContinue'
            try:
                result = subprocess.run(
                    ['powershell', '-Command', cmd_provisioned],
                    check=True,
                    capture_output=True,
                    text=True,
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
                output.append(f"<span style='color: #2e7d32'>{app}: Provisioned package removed</span>" if self.lang == "en" else
                              f"<span style='color: #2e7d32'>{app}: پکیج پروویژن‌شده حذف شد</span>")
            except subprocess.CalledProcessError as e:
                error_msg = e.stderr.strip() or "Unknown error"
                output.append(f"<span style='color: #d32f2f'>{app}: Failed to remove provisioned package - {error_msg}</span>" if self.lang == "en" else
                              f"<span style='color: #d32f2f'>{app}: خطا در حذف پکیج پروویژن‌شده - {error_msg}</span>")
            
            self.progress_bar.setValue(i + 1)
            QApplication.processEvents()

        self.output.setHtml("<br>".join(output))
        self.progress_bar.setVisible(False)

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
        dlg.setMinimumSize(450, 300)
        default_icon_path = os.path.join(ICONS_DIR, "default.png")
        print(f"Checking GuideDialog icon: {default_icon_path}")
        if os.path.exists(default_icon_path):
            dlg.setWindowIcon(QIcon(default_icon_path))
            print(f"Loaded GuideDialog icon: {default_icon_path}")
        else:
            print(f"Error: GuideDialog icon not found at {default_icon_path}")
        if self.lang == "fa":
            dlg.setLayoutDirection(Qt.RightToLeft)
        dlg.setStyleSheet(STYLESHEET)
        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(15, 15, 15, 15)
        label = QLabel(guide_text)
        label.setFont(QFont("Segoe UI", 14))
        label.setWordWrap(True)
        if self.lang == "fa":
            label.setAlignment(Qt.AlignRight)
        layout.addWidget(label)
        btn = QPushButton("Close" if self.lang == "en" else "بستن")
        btn.clicked.connect(dlg.reject)
        btn.setCursor(QCursor(Qt.PointingHandCursor))
        layout.addWidget(btn, alignment=Qt.AlignCenter)
        dlg.setLayout(layout)
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