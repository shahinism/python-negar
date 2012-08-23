#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from   PySide   import QtGui, QtCore
from   Virastar import PersianEditor

class NegarGui(QtGui.QMainWindow):
    """
    This class will make a GUI for negar
    """
    def __init__(self):
        super(NegarGui, self).__init__()
        self.initUi()

    def initUi(self):
        self.setLocale(QtCore.QLocale(QtCore.QLocale.Persian, QtCore.QLocale.Iran))
        self.setLayoutDirection(QtCore.Qt.RightToLeft)
        open_action = QtGui.QAction('Open File', self)
        open_action.setShortcut('Ctrl+O')
        open_action.setStatusTip('Open a file and edit it')
        open_action.triggered.connect(self.file_dialog)

        self.statusBar()
        
        menubar   = self.menuBar()
        file_menu = menubar.addMenu('&File')
        file_menu.addAction(open_action)
        
        main_widget  = QtGui.QWidget(self)
        input_label  = QtGui.QLabel(u'متن‌تان را این‌جا وارد کنید:')
        output_label = QtGui.QLabel('Output Box:')
        close_button = QtGui.QPushButton(self.tr('Close'))
        self.input_box  = QtGui.QTextEdit()
        self.Output_box = QtGui.QTextEdit()
        self.input_box.zoomIn(2)
        self.Output_box.zoomIn(2)

        self.input_box.textChanged.connect(self.edit_text)
        close_button.clicked.connect(QtGui.qApp.quit)
        
        hbox = QtGui.QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(close_button)
        
        grid = QtGui.QGridLayout(self)
        grid.setSpacing(10)
        grid.addWidget(input_label, 1, 0)
        grid.addWidget(self.input_box, 2, 0)
        grid.addWidget(output_label, 6, 0)
        grid.addWidget(self.Output_box, 7, 0)
        grid.addLayout(hbox, 8, 0)
        main_widget.setLayout(grid)

        self.setCentralWidget(main_widget)

        
        self.resize(600, 500)
        self.setWindowTitle('Negar')
        self.show()

    def file_dialog(self):
        fname, _ = QtGui.QFileDialog.getOpenFileName(self, 'Open a plain text file')
        data  = open(fname, 'r')
        with data:
            text = unicode(data.read(), encoding="utf-8")
            self.input_box.setText(text)

        
    def edit_text(self):
        self.Output_box.clear()
        lines = unicode(self.input_box.toPlainText()).split('\n')
        for line in lines:
            run_PE = PersianEditor(line)
            self.Output_box.append(run_PE.cleanup())

        
def main():
    translator = QtCore.QTranslator()
    translator.load('fa_ir','i18n/fa_ir')
    app = QtGui.QApplication(sys.argv)
    app.installTranslator(translator)
    
    run = NegarGui()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()