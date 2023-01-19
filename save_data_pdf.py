from fpdf import FPDF

class SaveDataPdf:

    def __init__(self, name, surname, cheat_list):
        self.name = name
        self.surname = surname
        self.cheat_list = cheat_list

    def save_data(self):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Name: " + self.name, ln=1, align="L")
        pdf.cell(200, 10, txt="Surname: " + self.surname, ln=1, align="L")

        
        for cheat in self.cheat_list:
            pdf.cell(200, 10, txt="Cheating detected: " + cheat, ln=1, align="L")
        pdf.output("data.pdf")