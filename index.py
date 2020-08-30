import sys
import urllib.request

import PyPDF2
import requests
from PyQt5 import QtCore
from PyQt5.QtCore import QUrl, QFileInfo, QFile
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QStyle
from PyQt5.QtGui import QPixmap, QGuiApplication
from gtts import gTTS

from helper import LANG
from mainwindow import Ui_MainWindow
import extract
import os
from googletrans import Translator

from pdftoimagetotext import pdf_to_image
from utils import ExportFile
QT_DEBUG_PLUGINS = 1


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Image2Text")

        self.msg = QMessageBox()
        self.multiple_file_flag = False
        self.browse_button_flag = True
        self.click_counter = 1
        self.pdf_browse_file_flag = False

        self.ui.path_edit.textChanged.connect(self.enable_preview_button)
        self.ui.browse_button.clicked.connect(self.browse_button_clicked)
        self.ui.preview_button.clicked.connect(self.preview_button_clicked)
        self.ui.translate_comboBox.currentTextChanged.connect(self.translate_data)
        self.ui.paste_button.clicked.connect(self.paste_button_clicked)

        self.ui.export_txt.triggered.connect(lambda: self.export(format_type="plain_text"))
        self.ui.export_pdf.triggered.connect(lambda: self.export(format_type="pdf"))
        self.ui.export_mp3.triggered.connect(lambda: self.export(format_type="mp3"))
        self.ui.next_button.clicked.connect(self.get_next_button_clicked_action)
        self.ui.prev_button.clicked.connect(self.get_prev_button_clicked_action)


        # media player
        self.player = QMediaPlayer(self)
        self.player.setVolume(60)
        self.ui.volume_slider.setValue(60)
        self.player.positionChanged.connect(self.media_position_changed)
        self.player.stateChanged.connect(self.mediastate_changed)
        self.player.durationChanged.connect(self.update_duration)
        self.ui.volume_slider.valueChanged.connect(self.player.setVolume)
        self.ui.radio_seek_slider.valueChanged.connect(self.player.setPosition)
        # self.player.setMedia(QMediaContent(QUrl.fromLocalFile("/home/sherlock/bellaciao.mp3"))) #path of the extracted file
        self.ui.play_pause_button.clicked.connect(self.play_pause_button_clicked)
        self.ui.speed_comboBox.currentIndexChanged.connect(self.set_playback_speed)
        self.ui.stop_button.clicked.connect(self.player.stop)
        self.ui.pushButton.clicked.connect(self.convert_audio)

    # logic when browse button is clicked
    def browse_button_clicked(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileNames(self, 'Select Image', "/home/", "Images (*.png *.jpeg *.jpg *.pdf)",
                                                  options=options)
        if len(fileName) == 0:
            self.msg.about(self, 'Error', "File PATH can't be empty, Please select Image File")
            return False
        if len(fileName) >= 2:
            self.multiple_file_flag = True
        if str(fileName[0]).endswith(".pdf"):
            total_pages = self.get_pdf_total_pages(fileName[0])
            if total_pages > 1:
                self.pdf_browse_file_flag = True

        self.path = fileName[0]
        self.path_list = fileName
        self.ui.path_edit.setText(','.join([str(elem) for elem in fileName]))
        self.ui.preview_button.setEnabled(True)
        return True

    def paste_button_clicked(self):
        clipboard_text = QGuiApplication.clipboard().text()
        if clipboard_text != "":
            self.ui.path_edit.setText(clipboard_text)

    # logic when preview button clicked
    def preview_button_clicked(self):
        if not MainWindow.check_internet_connection():
            self.msg.about(self, 'No internet connection', "Please check your internet connection!")
            return False
        if not self.browse_button_flag:
            self.path = self.ui.path_edit.text()
        if self.multiple_file_flag or self.pdf_browse_file_flag:
            self.ui.next_button.setEnabled(True)

        file_extension_list = [".jpg", ".png", ".jpeg", ".webp", ".tiff", ".bmp", ".svg", ".pdf"]
        self.file_name, self.file_extension = os.path.splitext(self.path)
        if self.file_extension in file_extension_list:
            if self.path.startswith("http://") or self.path.startswith("https://"):
                try:
                    self.path = urllib.request.urlretrieve(self.path, f"image{self.file_extension}")[0]
                except Exception as error:
                    self.msg.about(self, 'Error', "Unable to fetch data, please check your url")
                    return False

            if os.path.isfile(self.path):
                height, width = 600, 600
                if self.file_extension == ".pdf":
                    self.path_list = pdf_to_image(self.path)
                    pixmap = QPixmap(self.path_list[0])
                else:
                    pixmap = QPixmap(self.path)
                pixmap4 = pixmap.scaled(height, width, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
                self.ui.preview_label.setPixmap(pixmap4)

                if self.file_extension == ".pdf":
                    extracted_text = extract.return_string(self.path_list[0])
                else:
                    extracted_text = extract.return_string(self.path)
                if extracted_text != "":
                    self.set_items_in_combobox()
                    self.ui.textEdit.setText(extracted_text)
                    self.resize(1300, 500)
            else:
                self.msg.about(self, 'Error', "Invalid File, Please select Valid Image File")
        else:
            self.msg.about(self, 'Error', "Invalid File, Please select Valid Image File")

    def enable_preview_button(self):
        str_data = self.ui.path_edit.text()
        if str_data != "":
            self.ui.preview_button.setEnabled(True)
            if str_data.startswith("http://") or str_data.startswith("https://"):
                self.browse_button_flag = False
        else:
            self.ui.preview_button.setEnabled(False)

    @staticmethod
    def check_internet_connection():
        try:
            requests.get("http://www.google.com", timeout=5)
            return True
        except (requests.ConnectionError, requests.Timeout):
            return False

    def get_next_button_clicked_action(self):
        if self.multiple_file_flag or self.pdf_browse_file_flag:
            self.ui.prev_button.setEnabled(True)
            self.path = self.path_list[self.click_counter:][0]
            self.click_counter += 1
            self.preview_button_clicked()
            if self.click_counter == len(self.path_list):
                self.ui.next_button.setEnabled(False)

    def get_prev_button_clicked_action(self):
        if self.multiple_file_flag or self.pdf_browse_file_flag:
            self.path = self.path_list[:-self.click_counter+1][len(self.path_list[:-self.click_counter+1])-1]
            self.click_counter -= 1
            self.preview_button_clicked()
            if self.click_counter == 1:
                self.ui.prev_button.setEnabled(False)


    def get_pdf_total_pages(self, path):
        from PyPDF2 import PdfFileReader
        pdf = PdfFileReader(open(path, 'rb'))
        return pdf.getNumPages()



        data_by_pages = ""
        with open(self.path, mode='rb') as f:
            reader = PyPDF2.PdfFileReader(f)
            for count, page in enumerate(reader.pages, 1):
                data_by_pages += f"Page{count}:\n\n{page.extractText()}\n\n"
        return str(data_by_pages)

    def set_items_in_combobox(self):
        self.ui.translate_comboBox.setEnabled(True)
        lang_list = LANG.values()
        self.ui.translate_comboBox.addItems(lang_list)
        trans = Translator()
        self.current_lang = trans.detect(self.ui.textEdit.toPlainText()).lang
        self.ui.translate_comboBox.setCurrentText(LANG[str(self.current_lang).lower()])

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
        if data and data != "":
            ExportFile(data, file_path, format_type=format_type, lang=self.to_trans).export()
            self.msg.about(self, 'Success', "Export Successfully!")
        else:
            self.msg.warning(self, "Failed", "Nothing to export!")

    def convert_audio(self):
        self.txt = self.ui.textEdit.toPlainText()
        if os.path.isfile("audio/tmp.mp3"):
            os.remove("audio/tmp.mp3")
        if self.txt != "":
            myob = gTTS(text=self.txt, lang=self.current_lang, slow=False)
            myob.save('audio/tmp.mp3')
            print("done")

    def play_pause_button_clicked(self):
        self.audio_path = QFileInfo("audio/tmp.mp3").canonicalFilePath()
        if os.path.isfile(self.audio_path):
            self.player.setMedia(QMediaContent(QUrl.fromLocalFile(self.audio_path)))  # path of the extracted file

            if self.player.state() == 1:
                self.player.pause()
            else:
                self.player.play()
        print(self.player.bufferStatus())

    def media_position_changed(self, position):
        self.ui.position.setText(self.hhmmss(position))
        self.ui.radio_seek_slider.setValue(position)

    def mediastate_changed(self, state):
        if self.player.state() == self.player.PlayingState:
            self.ui.play_pause_button.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPause)

            )

        else:
            self.ui.play_pause_button.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPlay)

            )

    def update_duration(self, duration):
        self.ui.radio_seek_slider.setMaximum(duration)

        if duration >= 0:
            self.ui.duration.setText(self.hhmmss(duration))

    def set_playback_speed(self):
        rate = float((self.ui.speed_comboBox.currentText()).split('x')[0])
        self.player.setPlaybackRate(rate)

    def hhmmss(self, ms):
        # s = 1000
        # m = 60000
        # h = 3600000
        s = round(ms / 1000)
        m, s = divmod(s, 60)
        h, m = divmod(m, 60)
        return ("%d:%02d:%02d" % (h, m, s)) if h else ("%d:%02d" % (m, s))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
