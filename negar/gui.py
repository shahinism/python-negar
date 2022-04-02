#!/usr/bin/env python

import sys
import icu
from pathlib import Path
from pyperclip import copy
from PyQt6.QtGui import QIcon, QColor
from PyQt6.QtCore import Qt, QAbstractTableModel, QSize
from PyQt6.QtWidgets import (QApplication, QMainWindow, QPushButton, QTableView, QHeaderView, QCheckBox,
                            QSlider, QLabel, QTextEdit, QLineEdit, QGroupBox, QGridLayout, QTabWidget,
                            QWidget, QHBoxLayout, QVBoxLayout, QFileDialog)
sys.path.append(Path(__file__).parent.as_posix()) # https://stackoverflow.com/questions/16981921
from virastar import PersianEditor, UnTouchable
from constants import __version__, INFO, LOGO

collator = icu.Collator.createInstance(icu.Locale('fa_IR.UTF-8'))

class TableModel(QAbstractTableModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.ItemDataRole.TextAlignmentRole:
            return Qt.AlignmentFlag.AlignVCenter
        if role == Qt.ItemDataRole.BackgroundRole:
            if index.row()%2:
                return QColor('gray')
        if role == Qt.ItemDataRole.ForegroundRole:
            if index.row()%2:
                return QColor('white')
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

    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return ''
            if orientation == Qt.Orientation.Vertical:
                return str(section+1)

class Form(QMainWindow):
    def __init__(self, parent = None):
        super(Form, self).__init__(parent)
        self.editing_options = []

        self.table = QTableView(layoutDirection=Qt.LayoutDirection.RightToLeft,)
        self.setup_table()

        self.setupUi()

    def setup_table(self, col=8):
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        data = sorted(list(UnTouchable().get()), key=collator.getSortKey)
        data = [data[i*col:(i+1)*col] for i in range(int(len(data)//col)+1)]
        model = TableModel(data)
        self.table.setModel(model)

    def setupUi(self):
        self.edit_btn = QPushButton(self.tr("&Edit"))
        self.edit_btn.setEnabled(False)
        reset_btn = QPushButton(self.tr("&Reset"))
        quit_btn = QPushButton(self.tr("&Quit"))
        import_btn = QPushButton(self.tr('Im&port'),)
        copy_btn = QPushButton(QIcon(LOGO), '',)
        copy_btn.setIconSize(QSize(24,24))
        copy_btn.setToolTip(self.tr("Click to Copy Sanitized Output"))
        copy_btn.setStyleSheet("QPushButton {border-style: outset; border-width: 0px;}")
        self.autoedit_chkbox = QCheckBox(self.tr("&Automatic edit"))
        self.autoedit_chkbox.setChecked(True)
        self.font_slider = QSlider(orientation=Qt.Orientation.Horizontal,
            minimum=10, maximum=40, value=18)
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
        btn_layout.addWidget(quit_btn)

        self.input_editor = QTextEdit()
        input_editor_label = QLabel(self.tr("&Input Box"))
        input_editor_label.setBuddy(self.input_editor)
        self.output_editor = QTextEdit()
        output_editor_label = QLabel(self.tr("&Output Box"))
        output_editor_label.setBuddy(self.output_editor)

        # Options:
        self.f_dashes = QCheckBox(self.tr("Fix &Dashes"), checked=True)
        self.f_three_dots = QCheckBox(self.tr("Fix &three dots"), checked=True)
        self.f_english_quotes = QCheckBox(self.tr("Fix English &quotes"), checked=True)
        self.f_hamzeh = QCheckBox(self.tr("Fix &hamzeh"), checked=True)
        self.hamzeh_yeh = QCheckBox(self.tr("Use 'Persian &yeh' to show hamzeh"), checked=True)
        self.f_spacing_bq = QCheckBox(self.tr("Fix &spacing braces and qoutes"), checked=True)
        self.f_arab_num = QCheckBox(self.tr("Fix Arabic &numbers"), checked=True)
        self.f_eng_num = QCheckBox(self.tr("Fix &English numbers"), checked=True)
        self.f_non_persian_ch = QCheckBox(self.tr("Fix non Persian &chars"), checked=True)
        self.f_p_spacing = QCheckBox(self.tr("Fix &prefix spacing"), checked=True)
        self.f_p_separate = QCheckBox(self.tr("Fix p&refix separating"), checked=True)
        self.f_s_spacing = QCheckBox(self.tr("Fix su&ffix spacing"), checked=True)
        self.f_s_separate = QCheckBox(self.tr("Fix s&uffix separating"), checked=True)
        self.aggressive = QCheckBox(self.tr("Fix a&ggressive punctuation"), checked=True)
        self.clnup_kashidas = QCheckBox(self.tr("Cleanup &kashidas"), checked=True)
        self.clnup_ex_marks = QCheckBox(self.tr("Cleanup e&xtra marks"), checked=True)
        self.clnup_spacing = QCheckBox(self.tr("C&leanup spacing"), checked=True)
        self.trim_lt_whitespaces = QCheckBox(self.tr("Tr&im Leading/Trailing Whitespaces"), checked=True)

        # Add to untouchable list:
        self.untouch_word = QLineEdit()
        untouch_label = QLabel(self.tr("Add a &word to untouchable list"))
        untouch_label.setBuddy(self.untouch_word)
        self.untouch_button = QPushButton(self.tr("&Add"), enabled=False)
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
        config_layout.addWidget(self.f_three_dots, 1, 0)
        config_layout.addWidget(self.f_english_quotes, 0, 2)
        config_layout.addWidget(self.f_arab_num, 0, 1)
        config_layout.addWidget(self.f_eng_num, 1, 1)
        config_layout.addWidget(self.f_non_persian_ch, 1, 2)
        config_layout.addWidget(self.f_hamzeh, 2, 0)
        config_layout.addWidget(self.f_p_separate, 2, 1)
        config_layout.addWidget(self.f_s_separate, 2, 2)
        config_layout.addWidget(self.f_s_spacing, 3, 1)
        config_layout.addWidget(self.f_p_spacing, 3, 2)
        config_layout.addWidget(self.aggressive, 3, 3)
        config_layout.addWidget(self.f_spacing_bq, 0, 3, 1, 2)
        config_layout.addWidget(self.hamzeh_yeh, 1, 3, 1, 2)
        config_layout.addWidget(self.trim_lt_whitespaces, 2, 3, 1, 2)
        config_layout.addWidget(self.clnup_spacing, 0, 5)
        config_layout.addWidget(self.clnup_ex_marks, 1, 5)
        config_layout.addWidget(self.clnup_kashidas, 2, 5)
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

        # layout for input_label + import button
        input_layout = QHBoxLayout()
        input_layout.addWidget(input_editor_label)
        input_layout.addStretch()
        input_layout.addWidget(import_btn)

        # layout for output_label + copy button
        output_layout = QHBoxLayout()
        output_layout.addWidget(output_editor_label)
        output_layout.addStretch()
        output_layout.addWidget(copy_btn)

        # Main Tab widgets layouts:
        mt_layout = QGridLayout(main_tab)
        mt_layout.addLayout(input_layout, 0, 0)
        mt_layout.addWidget(self.input_editor, 1, 0)
        mt_layout.addLayout(output_layout, 2,0)
        mt_layout.addWidget(self.output_editor, 3, 0)
        mt_layout.addLayout(btn_layout, 4, 0)

        # Main tab widget control:
        tab_widget.addTab(main_tab, self.tr("&Main"))
        tab_widget.addTab(config_tab, self.tr("&Config"))

        # Main window configs:
        self.setCentralWidget(tab_widget)
        self.resize(800, 600)
        self.setWindowIcon(QIcon(LOGO))
        self.setWindowTitle(self.tr(f"Negar {__version__}"))

        # Signal control:
        # first of all negar have to check the default state of automatic edit feature.
        self.autoedit_handler()
        quit_btn.clicked.connect(QApplication.instance().quit)
        reset_btn.clicked.connect(self.text_box_reset)
        self.edit_btn.clicked.connect(self.edit_text)

        import_btn.clicked.connect(self.file_dialog)
        copy_btn.clicked.connect(self.save_to_clipboard)
        # if autoedit_chkboxs state's changed, then autoedit_handler have to call again.
        self.autoedit_chkbox.stateChanged.connect(self.autoedit_handler)

        self.font_slider.valueChanged.connect(self._set_font_size)
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
        self.aggressive.stateChanged.connect(self.option_control)
        self.clnup_kashidas.stateChanged.connect(self.option_control)
        self.clnup_ex_marks.stateChanged.connect(self.option_control)
        self.clnup_spacing.stateChanged.connect(self.option_control)
        self.trim_lt_whitespaces.stateChanged.connect(self.option_control)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.save_to_clipboard()
            self.close()
        elif event.key() == Qt.Key.Key_F1:
            self.input_editor.clear()
            self.input_editor.setText(INFO)
        else:
            super().keyPressEvent(event)

    def _set_font_size(self,):
        size = self.font_slider.value()
        self.input_editor.setFontPointSize(size)
        self.output_editor.setFontPointSize(size)
        lines = self.input_editor.toPlainText()
        self.input_editor.clear()
        self.input_editor.append(lines)
        self.edit_text()

    def untouch_add_enabler(self):
        """Checks untouchable word text input to enable the `Add` button if just one word is typed."""
        word_list = self.untouch_word.text().split(" ")
        if len(word_list) == 1:
            self.untouch_button.setEnabled(True)
        else:
            self.untouch_button.setEnabled(False)

    def untouch_add(self):
        """Adds a new word into untouchable words"""
        word = [self.untouch_word.text()]
        UnTouchable.add(word)
        self.untouch_word.clear()
        self.edit_text()  # retouches the input text
        self.setup_table() # updates untouchable list

    def autoedit_handler(self):
        """Edits the input text automatically if `autoedit` is checked."""
        if self.autoedit_chkbox.isChecked():
            self.edit_btn.setEnabled(False)
            self.input_editor.textChanged.connect(self.edit_text)
        else:
            self.edit_btn.setEnabled(True)
            # This line will disconnect autoedit signal and will disable autoamtic edit option
            self.input_editor.textChanged.disconnect(self.edit_text)
        self._set_font_size()

    def text_box_reset(self):
        """Clears input/output editor boxes"""
        self.input_editor.clear()
        self.output_editor.clear()

    def option_control(self):
        """Enable/Disable Editing features"""
        if not self.f_dashes.isChecked():
            self.editing_options.append("fix-dashes")
        if not self.f_three_dots.isChecked():
            self.editing_options.append("fix-three-dots")
        if not self.f_english_quotes.isChecked():
            self.editing_options.append("fix-english-quotes")
        if not self.f_hamzeh.isChecked():
            self.editing_options.append("fix-hamzeh")
        if not self.hamzeh_yeh.isChecked():
            self.editing_options.append("hamzeh-with-yeh")
        if not self.f_spacing_bq.isChecked():
            self.editing_options.append("fix-spacing-bq")
        if not self.f_arab_num.isChecked():
            self.editing_options.append("fix-arabic-num")
        if not self.f_eng_num.isChecked():
            self.editing_options.append("fix-english-num")
        if not self.f_non_persian_ch.isChecked():
            self.editing_options.append("fix-non-persian-chars")
        if not self.f_p_spacing.isChecked():
            self.editing_options.append("fix-p-spacing")
        if not self.f_p_separate.isChecked():
            self.editing_options.append("fix-p-separate")
        if not self.f_s_spacing.isChecked():
            self.editing_options.append("fix-s-spacing")
        if not self.f_s_separate.isChecked():
            self.editing_options.append("fix-s-separate")
        if not self.aggressive.isChecked():
            self.editing_options.append("aggressive")
        if not self.clnup_kashidas.isChecked():
            self.editing_options.append("cleanup-kashidas")
        if not self.clnup_ex_marks.isChecked():
            self.editing_options.append("cleanup-ex-marks")
        if not self.clnup_spacing.isChecked():
            self.editing_options.append("cleanup-spacing")
        if not self.trim_lt_whitespaces.isChecked():
            self.editing_options.append("trim-leading-trailing-whitespaces")

    def file_dialog(self):
        fname, _ = QFileDialog.getOpenFileName(self, 'Open File - A Plain Text')
        try:
            with open(fname, 'r') as f:
                self.input_editor.setText(f.read())
        except:
            pass

    def edit_text(self):
        self.output_editor.clear()
        run_PE = PersianEditor(self.input_editor.toPlainText(), *self.editing_options)
        self.output_editor.append(run_PE.cleanup())

    def save_to_clipboard(self):
        sanitizedText = self.output_editor.toPlainText()
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
