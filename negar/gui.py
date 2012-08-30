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
        
        # File menu actions:
        # This is open action wich help user to open a file
        open_action = QtGui.QAction(self)
        open_action.setText(self.tr('&Open'))
        open_action.setShortcut('Ctrl+O')
        open_action.setStatusTip(self.tr('Open a file and edit it'))
        open_action.triggered.connect(self.file_dialog)
        exit_action = QtGui.QAction(self)
        exit_action.setText(self.tr('&Close'))
        exit_action.setStatusTip(self.tr('Close the program'))
        exit_action.triggered.connect(QtGui.qApp.quit)
        
        # Turn main windows status bar on
        self.statusBar()


        # Make a menubar and adding objects to it
        menubar   = self.menuBar()
        # adding file menu actions
        file_menu = menubar.addMenu(self.tr('&File'))
        file_menu.addAction(open_action)
        file_menu.addAction(exit_action)
        
        # Make a widget with QtGui.QWidget and giving it a grid layout
        # it will capable me to add a grid layout in main windows central
        # widge.
        main_widget  = QtGui.QWidget(self)
        input_label  = QtGui.QLabel()
        input_label.setText(self.tr('Input Box'))
        output_label = QtGui.QLabel()
        output_label.setText(self.tr('Output Box'))
        close_button = QtGui.QPushButton()
        close_button.setText(self.tr('Close'))
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
        self.setWindowTitle(self.tr('Negar'))
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
    app = QtGui.QApplication(sys.argv)
    local = u"fa_IR"
    qtTranslator = QtCore.QTranslator()
    if qtTranslator.load(local, "i18n/"):
        print 'yes'
        app.installTranslator(qtTranslator)
    run = NegarGui()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()