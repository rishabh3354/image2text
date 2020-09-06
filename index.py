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

        self.make_invisible()
        self.msg = QMessageBox()
        self.multiple_file_flag = False
        self.browse_button_flag = True
        self.click_counter = 1
        self.pdf_browse_file_flag = False
        self.cached_data_dict = dict()

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
        self.ui.play_pause_button.clicked.connect(self.play_pause_button_clicked)
        self.ui.speed_comboBox.currentIndexChanged.connect(self.set_playback_speed)
        self.ui.stop_button.clicked.connect(self.player.stop)
        self.ui.pushButton.clicked.connect(self.convert_audio)

    def make_invisible(self):
        self.ui.prev_button.setVisible(False)
        self.ui.next_button.setVisible(False)
        self.ui.page_no_label.setVisible(False)

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
            self.total_pages = self.get_pdf_total_pages(fileName[0])
            if self.total_pages > 1:
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
        if self.multiple_file_flag or self.pdf_browse_file_flag:
            self.enable_next_prev_button()
            if self.pdf_browse_file_flag:
                self.ui.page_no_label.setText(f"Page {self.click_counter} of {self.total_pages}")
            else:
                self.ui.page_no_label.setText(f"Page {self.click_counter} of {len(self.path_list)}")

        file_extension_list = [".jpg", ".png", ".jpeg", ".webp", ".tiff", ".bmp", ".svg", ".pdf"]
        self.file_name, self.file_extension = os.path.splitext(self.path)
        if self.file_extension in file_extension_list:
            if self.path.startswith("http://") or self.path.startswith("https://"):
                try:
                    self.path = urllib.request.urlretrieve(self.path, f"image{self.file_extension}")[0]
                    if self.path.endswith(".pdf"):
                        self.total_pages = self.get_pdf_total_pages(self.path)
                        if self.total_pages > 1:
                            self.pdf_browse_file_flag = True
                            self.ui.page_no_label.setText(f"Page {self.click_counter} of {self.total_pages}")
                            self.enable_next_prev_button()

                except Exception as error:
                    self.msg.about(self, 'Error', "Unable to fetch data, please check your url")
                    return False

            if os.path.isfile(self.path):
                # showing image in pixmap
                height, width = self.frame_width_height_detect(600, 600)
                if self.file_extension == ".pdf":
                    self.path_list = pdf_to_image(self.path)
                    pixmap = QPixmap(self.path_list[0])
                    self.cached_data_dict[self.click_counter] = {"path": self.path_list[0], "text_data": ""}
                else:
                    pixmap = QPixmap(self.path)
                pixmap4 = pixmap.scaled(height, width, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
                self.ui.preview_label.setPixmap(pixmap4)

                # extracting data from image
                if self.file_extension == ".pdf":
                    self.extracted_text = extract.return_string(self.path_list[0])
                    self.cached_data_dict[self.click_counter] = {"path": self.path_list[0], "text_data": self.extracted_text}
                else:
                    self.extracted_text = extract.return_string(self.path)
                    self.cached_data_dict[self.click_counter] = {"path": self.path, "text_data": self.extracted_text}

                if self.extracted_text != "":
                    self.set_items_in_combobox()
                    self.ui.textEdit.setText(self.extracted_text)
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
                self.path = self.ui.path_edit.text()
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
            self.get_cached_values() if self.check_cached_data() else self.preview_button_clicked()
            self.ui.page_no_label.setText(f"Page {self.click_counter} of {len(self.path_list)}")
            if self.click_counter == len(self.path_list):
                self.ui.next_button.setEnabled(False)


    def check_cached_data(self):
        return True if self.cached_data_dict.get(self.click_counter) else False

    def frame_width_height_detect(self, t_width, t_height):
        # width = self.frameGeometry().width()
        # height = self.frameGeometry().height()
        # if t_width < width and t_height < height:
        #     return height, width
        # else:
        return t_width, t_height

    def get_cached_values(self):
        cache_data = self.cached_data_dict[self.click_counter]
        path = cache_data["path"]
        text_data = cache_data["text_data"]
        # setting cached data

        height, width = 600, 600
        pixmap = QPixmap(path)
        pixmap4 = pixmap.scaled(height, width, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        self.ui.preview_label.setPixmap(pixmap4)

        # self.set_items_in_combobox()
        self.ui.textEdit.setText(text_data)
        self.resize(1300, 600)

    def enable_next_prev_button(self):
        self.ui.next_button.setVisible(True)
        self.ui.prev_button.setVisible(True)
        self.ui.next_button.setEnabled(True)
        self.ui.page_no_label.setVisible(True)

    def get_prev_button_clicked_action(self):
        if self.multiple_file_flag or self.pdf_browse_file_flag:
            self.path = self.path_list[:-self.click_counter+1][len(self.path_list[:-self.click_counter+1])-1]
            self.click_counter -= 1
            self.get_cached_values() if self.check_cached_data() else self.preview_button_clicked()
            self.ui.page_no_label.setText(f"Page {self.click_counter} of {len(self.path_list)}")
            if self.click_counter == 1:
                self.ui.prev_button.setEnabled(False)
                self.ui.next_button.setEnabled(True)

    def get_pdf_total_pages(self, path):
        from PyPDF2 import PdfFileReader
        pdf = PdfFileReader(open(path, 'rb'))
        return pdf.getNumPages()

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
