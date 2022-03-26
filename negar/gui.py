#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from pathlib import Path
from pyperclip import copy
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
sys.path.append(Path(__file__).parent.as_posix()) # https://stackoverflow.com/questions/16981921
from virastar import PersianEditor, UnTouchable

__version__ = "0.8.0"


class TableModel(QAbstractTableModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.ItemDataRole.TextAlignmentRole:
            return Qt.AlignmentFlag.AlignVCenter + Qt.AlignmentFlag.AlignRight
        if role == Qt.ItemDataRole.BackgroundRole:
            if index.row()%2:
                return QColor('gray')
        if role == Qt.ItemDataRole.DisplayRole:
            try:
                return self._data[index.row()][index.column()]
            except:
                return ''

    def rowCount(self, index):
        # The length of the outer list.
        return len(self._data)

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return len(self._data[0])

class Form(QMainWindow):
    def __init__(self, parent = None):
        super(Form, self).__init__(parent)
        self.option_list = []
        self.logo = (Path(__file__).parent.absolute()/"logo.png").as_posix()

        self.table = QTableView(layoutDirection=Qt.LayoutDirection.RightToLeft)
        data, col = sorted(list(UnTouchable().get())), 10
        data = [data[i*col:(i+1)*col] for i in range(int(len(data)//col)+1)]
        model = TableModel(data)
        self.table.setModel(model)

        self.setupUi()

    def setupUi(self):
        self.edit_btn = QPushButton(self.tr("&Edit"))
        self.edit_btn.setEnabled(False)
        reset_btn = QPushButton(self.tr("&Reset"))
        Quit_btn = QPushButton(self.tr("&Quit"))
        copy_btn = QPushButton(QIcon(), '\u2398',)
        self.autoedit_chkbox = QCheckBox(self.tr("&Automatic edit"))
        self.autoedit_chkbox.setChecked(True)
        self.font_slider = QSlider(orientation=Qt.Orientation.Horizontal,
            minimum=10, maximum=40, value=22)
        font_slider_label = QLabel(self.tr("&Font Size"))
        font_slider_label.setBuddy(self.font_slider)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.autoedit_chkbox)
        btn_layout.addStretch()
        btn_layout.addWidget(font_slider_label)
        btn_layout.addWidget(self.font_slider)
        btn_layout.addStretch()
        btn_layout.addWidget(self.edit_btn)
        btn_layout.addWidget(reset_btn)
        btn_layout.addWidget(Quit_btn)

        self.input_editor = QTextEdit()
        input_editor_label = QLabel(self.tr("&Input Box"))
        input_editor_label.setBuddy(self.input_editor)
        self.output_editor = QTextEdit()
        output_editor_label = QLabel(self.tr("&Output Box"))
        output_editor_label.setBuddy(self.output_editor)

        # Options:
        self.f_dashes = QCheckBox(self.tr("Fix &Dashes"))
        self.f_dashes.setChecked(True)
        self.f_three_dots = QCheckBox(self.tr("Fix &three dots"))
        self.f_three_dots.setChecked(True)
        self.f_english_quotes = QCheckBox(self.tr("Fix English &quotes"))
        self.f_english_quotes.setChecked(True)
        self.f_hamzeh = QCheckBox(self.tr("Fix &hamzeh"))
        self.f_hamzeh.setChecked(True)
        self.hamzeh_yeh = QCheckBox(self.tr("Use 'Persian &yeh' to show hamzeh"))
        self.hamzeh_yeh.setChecked(True)
        self.f_spacing_bq = QCheckBox(self.tr("Fix &spacing braces and qoutes"))
        self.f_spacing_bq.setChecked(True)
        self.f_arab_num = QCheckBox(self.tr("Fix Arabic &numbers"))
        self.f_arab_num.setChecked(True)
        self.f_eng_num = QCheckBox(self.tr("Fix &English numbers"))
        self.f_eng_num.setChecked(True)
        self.f_non_persian_ch = QCheckBox(self.tr("Fix non Persian &chars"))
        self.f_non_persian_ch.setChecked(True)
        self.f_p_spacing = QCheckBox(self.tr("Fix &prefix spacing"))
        self.f_p_spacing.setChecked(True)
        self.f_p_separate = QCheckBox(self.tr("Fix p&refix separating"))
        self.f_p_separate.setChecked(True)
        self.f_s_spacing = QCheckBox(self.tr("Fix su&ffix spacing"))
        self.f_s_spacing.setChecked(True)
        self.f_s_separate = QCheckBox(self.tr("Fix s&uffix separating"))
        self.f_s_separate.setChecked(True)
        self.aggresive = QCheckBox(self.tr("A&ggresive"))
        self.aggresive.setChecked(True)
        self.clnup_kashidas = QCheckBox(self.tr("Cleanup &kashidas"))
        self.clnup_kashidas.setChecked(True)
        self.clnup_ex_marks = QCheckBox(self.tr("Cleanup e&xtra marks"))
        self.clnup_ex_marks.setChecked(True)
        self.clnup_spacing = QCheckBox(self.tr("C&leanup spacing"))
        self.clnup_spacing.setChecked(True)

        # Add to untouchable list:
        self.untouch_word = QLineEdit()
        untouch_label = QLabel(self.tr("Add a &word to untouchable list"))
        untouch_label.setBuddy(self.untouch_word)
        self.untouch_button = QPushButton(self.tr("&Add"))
        self.untouch_button.setEnabled(False)
        untouch_box = QGroupBox(self.tr("Untouchable words"))
        untouch_layout = QGridLayout()
        untouch_layout.addWidget(untouch_label, 0, 0)
        untouch_layout.addWidget(self.untouch_word, 1, 0)
        untouch_layout.addWidget(self.untouch_button, 1, 1)
        untouch_layout.addWidget(self.table, 2,0,1,2)
        untouch_box.setLayout(untouch_layout)

        # Options Box:
        config_box = QGroupBox(self.tr("Options"))
        config_layout = QGridLayout()
        config_layout.addWidget(self.f_dashes, 0, 0)
        config_layout.addWidget(self.f_three_dots, 0, 1)
        config_layout.addWidget(self.f_english_quotes, 0, 2)
        config_layout.addWidget(self.f_hamzeh, 0, 3)
        config_layout.addWidget(self.hamzeh_yeh, 0, 4)
        config_layout.addWidget(self.f_spacing_bq, 0, 5)
        config_layout.addWidget(self.f_arab_num, 1, 0)
        config_layout.addWidget(self.f_eng_num, 1, 1)
        config_layout.addWidget(self.f_non_persian_ch, 1, 2)
        config_layout.addWidget(self.f_p_spacing, 1, 3)
        config_layout.addWidget(self.f_p_separate, 1, 4)
        config_layout.addWidget(self.f_s_spacing, 1, 5)
        config_layout.addWidget(self.f_s_separate, 2, 0)
        config_layout.addWidget(self.aggresive, 2, 1)
        config_layout.addWidget(self.clnup_kashidas, 2, 2)
        config_layout.addWidget(self.clnup_ex_marks, 2, 3)
        config_layout.addWidget(self.clnup_spacing, 2, 4)
        config_box.setLayout(config_layout)

        # Tab widgets initializing:
        tab_widget = QTabWidget()
        main_tab = QWidget()
        config_tab = QWidget()

        # Config tab widgets layout:
        ct_layout = QVBoxLayout(config_tab)
        ct_layout.addWidget(config_box)
        ct_layout.addWidget(untouch_box)
        # ct_layout.addStretch()

        # layout for output_label + copy button
        output_layout = QHBoxLayout()
        output_layout.addWidget(output_editor_label)
        output_layout.addStretch()
        output_layout.addWidget(copy_btn)

        # Main Tab widgets layouts:
        mt_layout = QGridLayout(main_tab)
        mt_layout.addWidget(input_editor_label, 0, 0)
        mt_layout.addWidget(self.input_editor, 1, 0)
        # mt_layout.addWidget(output_editor_label, 2, 0)
        mt_layout.addLayout(output_layout, 2,0)
        mt_layout.addWidget(self.output_editor, 3, 0)
        mt_layout.addLayout(btn_layout, 4, 0)

        # self.__valueChanged()

        # Main tab widget control:
        tab_widget.addTab(main_tab, self.tr("&Main"))
        tab_widget.addTab(config_tab, self.tr("&Config"))

        # Main window configs:
        self.setCentralWidget(tab_widget)
        self.resize(800, 600)
        self.setWindowIcon(QIcon(self.logo))
        self.setWindowTitle(self.tr(f"Negar {__version__}"))

        # Signal control:
        # first of all negar have to check the default state of automatic edit feature.
        self.autoedit_handler()
        Quit_btn.clicked.connect(QApplication.instance().quit)
        reset_btn.clicked.connect(self.text_box_reset)
        self.edit_btn.clicked.connect(self.edit_text)

        copy_btn.clicked.connect(self.save_to_clipboard)
        # if autoedit_chkboxs state's changed, then autoedit_handler have to call again.
        self.autoedit_chkbox.stateChanged.connect(self.autoedit_handler)

        self.font_slider.valueChanged.connect(self.__valueChanged)
        self.untouch_word.textChanged.connect(self.untouch_add_enabler)
        self.untouch_button.clicked.connect(self.untouch_add)

        # Option checkbox lists signal control
        self.f_dashes.stateChanged.connect(self.option_control)
        self.f_three_dots.stateChanged.connect(self.option_control)
        self.f_english_quotes.stateChanged.connect(self.option_control)
        self.f_hamzeh.stateChanged.connect(self.option_control)
        self.hamzeh_yeh.stateChanged.connect(self.option_control)
        self.f_spacing_bq.stateChanged.connect(self.option_control)
        self.f_arab_num.stateChanged.connect(self.option_control)
        self.f_eng_num.stateChanged.connect(self.option_control)
        self.f_non_persian_ch.stateChanged.connect(self.option_control)
        self.f_p_spacing.stateChanged.connect(self.option_control)
        self.f_p_separate.stateChanged.connect(self.option_control)
        self.f_s_spacing.stateChanged.connect(self.option_control)
        self.f_s_separate.stateChanged.connect(self.option_control)
        self.aggresive.stateChanged.connect(self.option_control)
        self.clnup_kashidas.stateChanged.connect(self.option_control)
        self.clnup_ex_marks.stateChanged.connect(self.option_control)
        self.clnup_spacing.stateChanged.connect(self.option_control)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.save_to_clipboard()
            self.close()
        elif event.key() == Qt.Key.Key_F1:
            info="""نگار قابلیت های زیر را داراست:
* خط تیره های پیاپی نظیر (--) و (---) را به معادل های استاندارد شان تبدیل می کند.
* سه نقطه ی پیاپی را (...) به کاراکتر استانداردش در زبان فارسی تبدیل می کند.
* علایمی نظیر کتیشن فارسی را 'نگار' به گیومه تبدیل می کند.
* کلماتی مانند 'همه ی ' که با 'ی' پسوند همراه هستند را به صورت درست می‌نویسد و در صورت انتخاب کاربر می‌تواند آن را با حمزه 'ء' جایگزین کند.
* فاصله گذاری نادرست پرانتز ها نظیر ( نگار ) یا دیگر علایم را به صورت صحیح تنظیم می کند.
* اعداد عربی مانند '١٢٣٤٥٦٧٨٩٠' و انگلیسی مانند '1234567890' را به معادل فارسی شان تبدیل می کند.
* کاراکتر های غیر فارسی را شامل ',;%يةك' به معادل های فارسی شان تبدیل می کند.
* کلماتی که با فاصله ی اشتباه به صورت ' می شود ' و یا ' کمک تان ' نوشته شده‌، به صورت درست فاصله گذاری میشوند.
* کلماتی که به اشتباه بدون فاصله به صورت ' میشود ' , یا ' کمکتان ' نوشته شده‌، به صورت درست فاصله گذاری میشوند.
* از استفاده ی بیش از یک علامت ؟؟؟؟ یا !!! جلوگیری می کند.
* کلماتی که به صورت کشیـــــــــده نوشته شده اند را به صورت درست می نویسد.
* از فاصله گذاری     بیش از حد    جلوگیری می کند.
            """
            self.input_editor.clear()
            self.input_editor.setText(info)
        else:
            super().keyPressEvent(event)

    def __valueChanged(self,):
        size = self.font_slider.value()
        self.input_editor.setFontPointSize(size)
        self.output_editor.setFontPointSize(size)
        lines = self.input_editor.toPlainText()
        self.input_editor.clear()
        self.input_editor.append(lines)
        self.edit_text()

    def untouch_add_enabler(self):
        """
        This function will check if just one word is in the untouch word, then enable the untouch button.
        otherwise it will be disabled.
        """
        word_list = self.untouch_word.text().split(" ")
        if len(word_list) == 1:
            self.untouch_button.setEnabled(True)
        else:
            self.untouch_button.setEnabled(False)

    def untouch_add(self):
        """
        This function will make a unicode string from the word in untouch_word and add it to the
        untouchabl data file.
        """
        word = [self.untouch_word.text()]
        UnTouchable.add(word)
        self.untouch_word.clear()
        self.edit_text() # in order to update untouchable list

    def autoedit_handler(self):
        """
        if autoedit checkbox is checked then negar have to edit input text automatically. otherwise
        user have to click on edit button. this buttons signal is configed to do same behavior after
        click.
        """
        if self.autoedit_chkbox.isChecked():
            self.edit_btn.setEnabled(False)
            self.input_editor.textChanged.connect(self.edit_text)
        else:
            self.edit_btn.setEnabled(True)
            # This line will disconnect autoedit signal and will disable autoamtic edit option
            self.input_editor.textChanged.disconnect(self.edit_text)
        self.__valueChanged()

    def text_box_reset(self):
        """
        This function will help to clear input/output editor boxes
        """
        self.input_editor.clear()
        self.output_editor.clear()

    def option_control(self):
        """
        This function will help to disable Virastar features with checkbox list.
        """
        # this line will clean the option list. this will help to do not have duplicated options.
        self.option_list = []
        if not self.f_dashes.isChecked():
            self.option_list.append("fix-dashes")
        if not self.f_three_dots.isChecked():
            self.option_list.append("fix-three-dots")
        if not self.f_english_quotes.isChecked():
            self.option_list.append("fix-english-quotes")
        if not self.f_hamzeh.isChecked():
            self.option_list.append("fix-hamzeh")
        if not self.hamzeh_yeh.isChecked():
            self.option_list.append("hamzeh-with-yeh")
        if not self.f_spacing_bq.isChecked():
            self.option_list.append("fix-spacing-bq")
        if not self.f_arab_num.isChecked():
            self.option_list.append("fix-arabic-num")
        if not self.f_eng_num.isChecked():
            self.option_list.append("fix-english-num")
        if not self.f_non_persian_ch.isChecked():
            self.option_list.append("fix-non-persian-chars")
        if not self.f_p_spacing.isChecked():
            self.option_list.append("fix-p-spacing")
        if not self.f_p_separate.isChecked():
            self.option_list.append("fix-p-separate")
        if not self.f_s_spacing.isChecked():
            self.option_list.append("fix-s-spacing")
        if not self.f_s_separate.isChecked():
            self.option_list.append("fix-s-separate")
        if not self.aggresive.isChecked():
            self.option_list.append("aggresive")
        if not self.clnup_kashidas.isChecked():
            self.option_list.append("cleanup-kashidas")
        if not self.clnup_ex_marks.isChecked():
            self.option_list.append("cleanup-ex-marks")
        if not self.clnup_spacing.isChecked():
            self.option_list.append("cleanup-spacing")

    def file_dialog(self):
        fname, _ = QtGui.QFileDialog.getOpenFileName(self, 'Open a plain text file')
        data  = open(fname, 'r')
        with data:
            text = data.read()
            self.input_box.setText(text)

    def edit_text(self):
        self.output_editor.clear()
        lines = self.input_editor.toPlainText().split('\n')
        for line in lines:
            run_PE = PersianEditor(line, *self.option_list)
            self.output_editor.append(run_PE.cleanup())

    def save_to_clipboard(self):
        sanitizedText = self.output_editor.toPlainText().strip()
        if sanitizedText:
            copy(sanitizedText)

def main():
    app = QApplication(sys.argv)
    run = Form()
    run.show()
    run.input_editor.setFocus() # set focus on input box
    sys.exit(app.exec())

if __name__ == "__main__":
    main()