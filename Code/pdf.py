from fpdf import FPDF
from numpy import mean

class my_pdf:

    pdf = FPDF('P', 'mm', [220, 210])

    def __init__(self, subjects=None, marksObtained=None, passingMarks=None, totalMarks=None, name=None, path1=None, path2=None, path3=None, output_path=None):

        # subjects = ['Urdu', 'English', 'Math', 'Social Studies', 'Science', 'Islamiat', 'Sindhi', 'Art Drawing', 'Total Marks']
        # marksObtained = [11, 89, 9, 12, 92, 93, 5, 75]
        # passingMarks = [33, 34, 35, 36, 37, 38, 39, 40]
        # totalMarks = [100, 100, 100, 100, 100, 100, 75, 75]
    
        self.name = name

        page1Columns = ['Subject', 'Total Marks', 'Marks Obtained', 'Passing Grade']
        passingMarks.append(str(round(mean(marksObtained), 1))+"%")
        marksObtained.append(sum(marksObtained))
        totalMarks.append(sum(totalMarks))

        self.initialize_pdf()
        self.grades(columnNamesArr=page1Columns, subjects=subjects, marksArr=marksObtained, passingArr=passingMarks, totalArr=totalMarks)
        self.details()
        self.sig(path1, path2, path3)
        
        self.pdf.output(output_path, 'F')

    def initialize_pdf(self):
        self.pdf.add_page('L')
        # Add page title
        self.pdf.set_fill_color(255,255,255)
        self.pdf.set_text_color(0,0,0)
        self.pdf.set_font('Times', 'bu', 24)
        self.pdf.cell(190, 12, 'Report Card', 0, 1, 'C')


    def grades(self, columnNamesArr, subjects, marksArr, passingArr, totalArr):
        justification = 'C'

        heading_index = 0
        sub_counter = 0
        data_counter = 0

        width = 47.5
        height = 10


        self.pdf.set_font('Arial', '', 12)
        self.pdf.ln(10)
        # Heading

        self.pdf.set_font_size(10)
        self.pdf.set_fill_color(100,100,100)
        self.pdf.set_text_color(255,255,255)
        cell_index = 0
        for columnName in columnNamesArr:
            self.pdf.cell(width, height, columnName, 1, 0, justification, True)
            cell_index += 1
        

        while sub_counter < len(subjects):

            self.pdf.ln()
            self.pdf.set_font_size(9)
            self.pdf.set_text_color(0,0,0)
            fillColor = [240, 240, 242] if heading_index%2 else [255, 255, 255]
            self.pdf.set_fill_color(fillColor[0], fillColor[1], fillColor[2])
            
            if isinstance(passingArr[data_counter], str):
                self.pdf.ln()


            for i in range(4):

                if i == 0:

                    self.pdf.cell(width, height, subjects[sub_counter], 1, 0, justification, True)
                    sub_counter+=1

                elif i == 1:

                    self.pdf.cell(width, height, str(totalArr[data_counter]), 1, 0, justification, True)

                elif i == 2:
                    
                    if isinstance(passingArr[data_counter], str):
                        
                        self.pdf.cell(width, height, str(marksArr[data_counter]), 1, 0, justification, True)
                        continue                                                                                                
                        
                    if int(marksArr[data_counter]) < int(passingArr[data_counter]):
                        self.pdf.set_text_color(255,0,0)
                    else:
                        self.pdf.set_text_color(0,0,255)
                    self.pdf.cell(width, height, str(marksArr[data_counter]), 1, 0, justification, True)
                    self.pdf.set_text_color(0,0,0)

                elif i == 3:
                    self.pdf.cell(width, height, str(passingArr[data_counter]), 1, 0, justification, True)

            data_counter += 1
            self.pdf.set_x(10)

            heading_index += 1
        self.pdf.ln(7)

    def details(self):
       
        self.pdf.set_font('Arial', '', 10)
        self.pdf.ln(20)
        width = 15
        height = 5

        left = 15
        right = 110

        self.pdf.set_x(left)
        dist = self.pdf.get_string_width('Name: ')
        self.pdf.cell(dist, height, 'Name: ', 0, 0, 'L')
        x = self.pdf.get_x()
        self.pdf.cell(width, height, self.name, 0, 0, 'L')
        self.pdf.line(x, self.pdf.get_y()+height, right-10, self.pdf.get_y()+height)
    


        self.pdf.set_x(right)
        dist = self.pdf.get_string_width('Result: ')
        self.pdf.cell(dist, height, 'Result: ', 0, 0, 'L')
        x = self.pdf.get_x()
        self.pdf.cell(width, height, '2nd Position', 0, 0, 'L')
        self.pdf.line(x, self.pdf.get_y()+height, 195, self.pdf.get_y()+height)
        self.pdf.ln()


        self.pdf.set_x(left)
        dist = self.pdf.get_string_width('Attendance: ')
        self.pdf.cell(dist, height, 'Attendance: ', 0, 0, 'L')
        x = self.pdf.get_x()
        self.pdf.cell(width, height, '85', 0, 0, 'L')
        self.pdf.line(x, self.pdf.get_y()+height, right-10, self.pdf.get_y()+height)
    

        self.pdf.set_x(right)
        dist = self.pdf.get_string_width('Working Days: ')
        self.pdf.cell(dist, height, 'Working Days:', 0, 0, 'L')
        x = self.pdf.get_x()
        self.pdf.cell(width, height, '90', 0, 0, 'L')
        self.pdf.line(x, self.pdf.get_y()+height, 195, self.pdf.get_y()+height)
        self.pdf.ln()

        self.pdf.set_x(left)
        dist = self.pdf.get_string_width('Student Condition: ')
        self.pdf.cell(dist, height, 'Student Condition:', 0, 0, 'L')
        x = self.pdf.get_x()
        self.pdf.cell(width, height, 'Horrendous', 0, 0, 'L')
        self.pdf.line(x, self.pdf.get_y()+height, right-10, self.pdf.get_y()+height)


        self.pdf.set_x(right)
        dist = self.pdf.get_string_width('Student ID: ')
        self.pdf.cell(dist, height, 'Student ID:', 0, 0, 'L')
        x = self.pdf.get_x()
        self.pdf.cell(width, height, '123456', 0, 0, 'L')
        self.pdf.line(x, self.pdf.get_y()+height, 195, self.pdf.get_y()+height)
        self.pdf.ln()




    def sig(self, teacher_path, parent_path, hm_path):

        self.pdf.ln(15)
        self.pdf.set_text_color(0,0,0)

        self.pdf.set_x(50)
        self.pdf.image(teacher_path, self.pdf.get_x()+1, self.pdf.get_y()-5, 25, 0, 'JPEG')
        self.pdf.set_x(90)
        self.pdf.image(parent_path, self.pdf.get_x()+1, self.pdf.get_y()-5, 25, 0, 'JPEG')
        self.pdf.set_x(130)
        self.pdf.image(hm_path, self.pdf.get_x()+1, self.pdf.get_y()-5, 25, 0, 'JPEG')
        self.pdf.ln(5)

        self.pdf.set_x(50)
        dist = self.pdf.get_string_width('Teacher Signature')
        self.pdf.line(self.pdf.get_x(), self.pdf.get_y(), self.pdf.get_x()+dist, self.pdf.get_y())
        self.pdf.cell(dist, 5, 'Teacher Signature', 0, 0, 'L')

        self.pdf.set_x(90)
        dist = self.pdf.get_string_width('Parents Signature')
        self.pdf.line(self.pdf.get_x(), self.pdf.get_y(), self.pdf.get_x()+dist, self.pdf.get_y())
        self.pdf.cell(dist, 5, 'Parents Signature', 0, 0, 'L')

        self.pdf.set_x(130)
        dist = self.pdf.get_string_width('Head Mistress Signature')
        self.pdf.line(self.pdf.get_x(), self.pdf.get_y(), self.pdf.get_x()+dist, self.pdf.get_y())
        self.pdf.cell(dist, 5, 'Head Mistress Signature', 0, 0, 'L')
        # add your own path here


def main():

    my_pdf(subjects=None, marksObtained=None, passingMarks=None, totalMarks=None, path1="C://Users//akeel//Desktop//Taleem Gah//Taleem-Gah-School-Website//Code//sig.jpeg",
    path2="C://Users//akeel//Desktop//Taleem Gah//Taleem-Gah-School-Website//Code//sig.jpeg",
    path3="C://Users//akeel//Desktop//Taleem Gah//Taleem-Gah-School-Website//Code//sig.jpeg")

if __name__ == '__main__':
    main()