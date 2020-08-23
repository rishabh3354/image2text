import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PyQt5.QtGui import QPixmap
from helper import LANG
from mainwindow import Ui_MainWindow
import extract
import os
from googletrans import Translator

from utils import ExportFile


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.preview_button.setEnabled(False)
        self.ui.convert_button.setEnabled(False)
        self.ui.path_edit.textEdited.connect(self.enable_preview_button)
        self.ui.browse_button.clicked.connect(self.browse_button_clicked)
        self.ui.preview_button.clicked.connect(self.preview_button_clicked)
        self.ui.convert_button.clicked.connect(self.get_string)
        self.ui.export_plain_text.triggered.connect(lambda: self.export(format_type="plain_text"))
        self.ui.export_pdf.triggered.connect(lambda: self.export(format_type="pdf"))
        self.ui.textEdit.textChanged.connect(self.set_items_in_combobox)
        self.ui.translate_comboBox.currentTextChanged.connect(self.translate_data)

    # logic when browse button is clicked
    def browse_button_clicked(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, 'Select Image', "/home/", "Images (*.png *.jpeg *.jpg)", options=options)
        if fileName != "":
            self.ui.path_edit.setText(fileName)
            self.ui.preview_button.setEnabled(True)
        else:
            msg = QMessageBox()
            msg.about(self, 'Error', "File PATH can't be empty, Please select Image File")

    # logic when preview button clicked
    def preview_button_clicked(self):
        path = self.ui.path_edit.text()

        if os.path.isfile(path):
            # below line if file exist enable convert button
            self.ui.convert_button.setEnabled(True)

            self.ui.preview_label.setPixmap(QPixmap(path))
        else:
            msg = QMessageBox()
            msg.about(self, 'Error', "Invalid File, Please select Valid Image File")

    def enable_preview_button(self):
        if self.ui.path_edit.text() != "":
            self.ui.preview_button.setEnabled(True)
        else:
            self.ui.preview_button.setEnabled(False)

    def get_string(self):
        path = self.ui.path_edit.text()
        if os.path.isfile(path):
            self.ui.textEdit.setText(extract.return_string(path))

    def set_items_in_combobox(self):
        trans = Translator()
        current_lang = trans.detect(self.ui.textEdit.toPlainText()).lang

        lang_list = LANG.values()
        for x in lang_list:
            self.ui.translate_comboBox.addItem(x)
        self.ui.translate_comboBox.setCurrentText(LANG[current_lang])

        # translates mthe text into german language

    def translate_data(self):
        trans = Translator()
        current_lang = self.ui.translate_comboBox.currentText()
        raw_str = self.ui.textEdit.toPlainText()
        to_trans = list(LANG.keys())[list(LANG.values()).index(current_lang)]
        trans_text = trans.translate(raw_str, dest=to_trans)
        self.ui.textEdit.setText(str(trans_text))

    def export(self, format_type):
        types = {"pdf": "PDF files (*.pdf)", "plain_text": "Plain Text (*.txt)"}
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_path = QFileDialog.getSaveFileName(self, self.tr("Export document to PDF"),
                                               "/home/Documents/Imagetotext", self.tr(types[format_type]), options=options)[0]
        print(file_path)
        data = str(self.ui.textedit.toPlainText()).strip("\f")
        ExportFile(data, file_path, format_type=format_type).export()
        msg = QMessageBox()
        msg.about(self, 'Success', "Export Successfully!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
