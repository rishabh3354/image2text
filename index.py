import re
import sys
import urllib.request


from PyQt5 import QtCore
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
        self.setWindowTitle("Image2Text")
        self.ui.path_edit.textEdited.connect(self.enable_preview_button)
        self.ui.browse_button.clicked.connect(self.browse_button_clicked)
        self.ui.preview_button.clicked.connect(lambda: self.preview_button_clicked())
        self.ui.convert_button.clicked.connect(self.convert_button_clicked)
        self.ui.export_txt.triggered.connect(lambda: self.export(format_type="plain_text"))
        self.ui.export_pdf.triggered.connect(lambda: self.export(format_type="pdf"))
        self.ui.export_mp3.triggered.connect(lambda: self.export(format_type="mp3"))
        self.ui.translate_comboBox.currentTextChanged.connect(self.translate_data)

        self.msg = QMessageBox()

    # logic when browse button is clicked
    def browse_button_clicked(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, 'Select Image', "/home/", "Images (*.png *.jpeg *.jpg)",
                                                  options=options)
        if fileName != "":
            self.ui.path_edit.setText(fileName)
            self.ui.preview_button.setEnabled(True)
        else:
            self.msg.about(self, 'Error', "File PATH can't be empty, Please select Image File")

    # logic when preview button clicked
    def preview_button_clicked(self):
        self.path = self.ui.path_edit.text()
        if self.path.startswith("http://") or self.path.startswith("https://"):
            file_extension_list = [".jpg", ".png", ".jpeg", ".webp", ".tiff", ".bmp", ".svg"]
            file_name, file_extension = os.path.splitext(self.path)
            if file_extension in file_extension_list or (
                    self.path.startswith("http://") or self.path.startswith("https://")):
                if file_extension in file_extension_list:
                    try:
                        self.path = urllib.request.urlretrieve(self.path, f"image{file_extension}")[0]
                    except Exception as error:
                        self.msg.about(self, 'Error', "Invalid URL, Please select Valid Image URL")
                        return False
                else:
                    self.msg.about(self, 'Error', "Invalid URL, Please select Valid Image URL")
                    return False



        if os.path.isfile(self.path):
            self.ui.convert_button.setEnabled(True)
            pixmap = QPixmap(self.path)
            pixmap4 = pixmap.scaled(700, 700, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
            self.ui.preview_label.setPixmap(pixmap4)
        else:
            self.msg.about(self, 'Error', "Invalid File, Please select Valid Image File")

    def enable_preview_button(self):
        if self.ui.path_edit.text() != "":
            self.ui.preview_button.setEnabled(True)
        else:
            self.ui.preview_button.setEnabled(False)

    def convert_button_clicked(self):
        if self.ui.to_comboBox.currentText() == "Plain Text":
            if os.path.isfile(self.path):
                extracted_text = extract.return_string(self.path)
                if extracted_text != "":
                    self.set_items_in_combobox()
                    self.ui.textEdit.setText(extract.return_string(self.path))
                else:
                    self.msg.about(self, 'Error', "File PATH can't be empty, Please select Image File")

                self.resize(1300, 500)

    def set_items_in_combobox(self):
        self.ui.translate_comboBox.setEnabled(True)
        lang_list = LANG.values()
        self.ui.translate_comboBox.addItems(lang_list)
        trans = Translator()
        current_lang = trans.detect(self.ui.textEdit.toPlainText()).lang
        self.ui.translate_comboBox.setCurrentText(LANG[str(current_lang).lower()])

    def translate_data(self):
        self.ui.export_txt.setEnabled(True)
        self.ui.export_pdf.setEnabled(True)
        self.ui.export_mp3.setEnabled(True)

        trans = Translator()
        current_lang = self.ui.translate_comboBox.currentText()
        raw_str = self.ui.textEdit.toPlainText()
        self.to_trans = list(LANG.keys())[list(LANG.values()).index(current_lang)]
        trans_text = trans.translate(raw_str, dest=self.to_trans).text
        self.ui.textEdit.setText(str(trans_text))
        self.ui.translate_comboBox.setCurrentText(self.to_trans)

    def export(self, format_type):
        types = {"pdf": "PDF files (*.pdf)", "plain_text": "Plain Text (*.txt)", "mp3": "Mp3 (*.mp3)"}
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_path = QFileDialog.getSaveFileName(self, self.tr("Export document to PDF"),
                                                "/home/Documents/Imagetotext",
                                                self.tr(types[format_type]), options=options)[0]
        data = str(self.ui.textEdit.toPlainText()).strip("\f")
        self.msg = QMessageBox()

        if data and data != "":
            ExportFile(data, file_path, format_type=format_type, lang=self.to_trans).export()
            self.msg.about(self, 'Success', "Export Successfully!")
        else:
            self.msg.warning(self, "Failed", "Nothing to export!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
