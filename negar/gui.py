#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
try:
    from virastar import PersianEditor, add_to_untouchable
except:
    from .virastar import PersianEditor, add_to_untouchable

__version__ = "0.6.7"

class Form(QMainWindow):
    def __init__(self, parent = None):
        super(Form, self).__init__(parent)
        self.option_list = []
        self.setupUi()

    def setupUi(self):
        self.edit_btn = QPushButton(self.tr("&Edit"))
        self.edit_btn.setEnabled(False)
        reset_btn = QPushButton(self.tr("&Reset"))
        Quit_btn = QPushButton(self.tr("&Quit"))
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
        self.f_dashes = QCheckBox(self.tr("&Fix Dashes"))
        self.f_dashes.setChecked(True)
        self.f_three_dots = QCheckBox(self.tr("&Fix three dots"))
        self.f_three_dots.setChecked(True)
        self.f_english_quotes = QCheckBox(self.tr("&Fix English quotes"))
        self.f_english_quotes.setChecked(True)
        self.f_hamzeh = QCheckBox(self.tr("&Fix hamzeh"))
        self.f_hamzeh.setChecked(True)
        self.hamzeh_yeh = QCheckBox(self.tr("&Use 'Persian yeh' to show hamzeh"))
        self.hamzeh_yeh.setChecked(True)
        self.f_spacing_bq = QCheckBox(self.tr("&Fix spacing braces and qoutes"))
        self.f_spacing_bq.setChecked(True)
        self.f_arab_num = QCheckBox(self.tr("&Fix Arabic numbers"))
        self.f_arab_num.setChecked(True)
        self.f_eng_num = QCheckBox(self.tr("&Fix English numbers"))
        self.f_eng_num.setChecked(True)
        self.f_non_persian_ch = QCheckBox(self.tr("&Fix non Persian chars"))
        self.f_non_persian_ch.setChecked(True)
        self.f_p_spacing = QCheckBox(self.tr("&Fix perfix spacing"))
        self.f_p_spacing.setChecked(True)
        self.f_p_separate = QCheckBox(self.tr("&Fix perfix separating"))
        self.f_p_separate.setChecked(True)
        self.f_s_spacing = QCheckBox(self.tr("&Fix suffix spacing"))
        self.f_s_spacing.setChecked(True)
        self.f_s_separate = QCheckBox(self.tr("&Fix suffix separating"))
        self.f_s_separate.setChecked(True)
        self.aggresive = QCheckBox(self.tr("&Aggresive"))
        self.aggresive.setChecked(True)
        self.clnup_kashidas = QCheckBox(self.tr("&Cleanup kashidas"))
        self.clnup_kashidas.setChecked(True)
        self.clnup_ex_marks = QCheckBox(self.tr("&Cleanup extra marks"))
        self.clnup_ex_marks.setChecked(True)
        self.clnup_spacing = QCheckBox(self.tr("&Cleanup spacing"))
        self.clnup_spacing.setChecked(True)

        # Add to untouchable list:
        self.untouch_word = QLineEdit()
        untouch_label = QLabel(self.tr("&Add a word to untouchable list"))
        untouch_label.setBuddy(self.untouch_word)
        self.untouch_button = QPushButton(self.tr("&Add"))
        self.untouch_button.setEnabled(False)
        untouch_box = QGroupBox(self.tr("Untouchable words"))
        untouch_layout = QGridLayout()
        untouch_layout.addWidget(untouch_label, 0, 0)
        untouch_layout.addWidget(self.untouch_word, 1, 0)
        untouch_layout.addWidget(self.untouch_button, 1, 1)
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
        ct_layout.addStretch()
        # Main Tab widgets layouts:
        mt_layout = QGridLayout(main_tab)

        mt_layout.addWidget(input_editor_label, 0, 0)
        mt_layout.addWidget(self.input_editor, 1, 0)
        mt_layout.addWidget(output_editor_label, 2, 0)
        mt_layout.addWidget(self.output_editor, 3, 0)
        mt_layout.addLayout(btn_layout, 4, 0)

        # self.__valueChanged()

        # Main tab widget control:
        tab_widget.addTab(main_tab, self.tr("&Main"))
        tab_widget.addTab(config_tab, self.tr("&Config"))

        # Main window configs:
        self.setCentralWidget(tab_widget)
        self.resize(800, 600)
        this_dir, _ = os.path.split(__file__)
        logo = os.path.join(this_dir, "logo.png")
        self.setWindowIcon(QIcon(logo))
        self.setWindowTitle(self.tr(f"Negar {__version__}"))

        # Signal control:
        # first of all negar have to check the default state of automatic edit feature.
        self.autoedit_handler()
        Quit_btn.clicked.connect(QApplication.instance().quit)
        reset_btn.clicked.connect(self.text_box_reset)
        self.edit_btn.clicked.connect(self.edit_text)
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
        add_to_untouchable(word)
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

def main():
    app = QApplication(sys.argv)
    run = Form()
    run.show()
    run.input_editor.setFocus() # set focus on input box
    sys.exit(app.exec())

if __name__ == "__main__":
    main()