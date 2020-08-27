from fpdf import FPDF
from gtts import gTTS


class ExportFile:
    def __init__(self, data, file_path, format_type="plain_text", lang=None):
        self.data = data
        self.format = format_type
        self.file_path = file_path
        self.lang = lang

    def export(self):
        if self.format == "plain_text":
            file_obj = open(f'{self.file_path}.txt', "w")
            file_obj.writelines(self.data)
            file_obj.close()

        if self.format == "pdf":
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=15)
            line = 1
            for row in str(self.data).split("\n"):
                pdf.cell(200, 10, txt=row, ln=line, align='C')
                line += 1
            pdf.output(f'{self.file_path}.pdf')

        if self.format == "mp3" and self.lang:
            myobj = gTTS(text=self.data, lang=self.lang, slow=False)
            myobj.save(f'{self.file_path}.mp3')

        return True
