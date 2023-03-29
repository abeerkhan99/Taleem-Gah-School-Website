from fpdf import FPDF
from numpy import mean
from flask import send_file

class my_pdf:

    pdf = FPDF('P', 'mm', [220, 210])

    def __init__(self, subjects, marksObtained, passingMarks, totalMarks, student_name, student_attendance, working_days, class_name, semester_name, path_name, overall_percentage):
    
        self.name = student_name

        page1Columns = ['Subject', 'Total Marks', 'Marks Obtained', 'Passing Grade']
        
        if overall_percentage >= 90 and overall_percentage <= 100:
            overall_grade = "A"
        elif overall_percentage >= 80 and overall_percentage < 90:
            overall_grade = "B"
        elif overall_percentage >= 70 and overall_percentage < 80:
            overall_grade = "C"
        elif overall_percentage >= 60 and overall_percentage < 70:
            overall_grade = "D"
        elif overall_percentage >= 50 and overall_percentage < 60:
            overall_grade = "E"
        else:
            overall_grade = "F"

        self.initialize_pdf()
        self.grades(columnNamesArr=page1Columns, subjects=subjects, marksArr=marksObtained, passingArr=passingMarks, totalArr=totalMarks)
        self.details(student_name, class_name, semester_name, student_attendance, working_days, overall_grade)
        self.sig()
        
        self.pdf.output(path_name, 'F')
        return send_file(path_name, as_attachment=True)

    def initialize_pdf(self):
        self.pdf.add_page('L')
        # Add page title
        self.pdf.set_fill_color(255,255,255)
        self.pdf.set_text_color(0,0,0)
        self.pdf.set_font('Times', 'bu', 24)
        self.pdf.cell(190, 12, 'Report Card', 0, 1, 'C')
        # self.pdf.image('taleem-gah logo.png', 10, 5, 33)
        return


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
        return

    def details(self, student_name, class_name, semester_name, student_attendance, working_days, overall_grade):
       
        self.pdf.set_font('Arial', '', 10)
        self.pdf.ln(10)
        width = 15
        height = 5

        left = 15
        right = 110

        self.pdf.set_x(left)
        dist = self.pdf.get_string_width('Name: ')
        self.pdf.cell(dist, height, 'Name: ', 0, 0, 'L')
        x = self.pdf.get_x()
        self.pdf.cell(width, height, student_name, 0, 0, 'L')
        self.pdf.line(x, self.pdf.get_y()+height, right-10, self.pdf.get_y()+height)

        self.pdf.set_x(right)
        dist = self.pdf.get_string_width('')
        self.pdf.cell(dist, height, '', 0, 0, 'L')
        x = self.pdf.get_x()
        self.pdf.cell(width, height, '', 0, 0, 'L')
        # self.pdf.line(x, self.pdf.get_y()+height, 195, self.pdf.get_y()+height)
        self.pdf.ln()    


        self.pdf.set_x(left)
        dist = self.pdf.get_string_width('Class: ')
        self.pdf.cell(dist, height, 'Class: ', 0, 0, 'L')
        x = self.pdf.get_x()
        self.pdf.cell(width, height, class_name, 0, 0, 'L')
        self.pdf.line(x, self.pdf.get_y()+height, right-10, self.pdf.get_y()+height) 

        self.pdf.set_x(right)
        dist = self.pdf.get_string_width('Semester: ')
        self.pdf.cell(dist, height, 'Semester: ', 0, 0, 'L')
        x = self.pdf.get_x()
        self.pdf.cell(width, height, semester_name, 0, 0, 'L')
        self.pdf.line(x, self.pdf.get_y()+height, 195, self.pdf.get_y()+height)
        self.pdf.ln()  

        
        self.pdf.set_x(left)
        dist = self.pdf.get_string_width('Attendance: ')
        self.pdf.cell(dist, height, 'Attendance: ', 0, 0, 'L')
        x = self.pdf.get_x()
        self.pdf.cell(width, height, student_attendance, 0, 0, 'L')
        self.pdf.line(x, self.pdf.get_y()+height, right-10, self.pdf.get_y()+height)

        self.pdf.set_x(right)
        dist = self.pdf.get_string_width('Working Days: ')
        self.pdf.cell(dist, height, 'Working Days: ', 0, 0, 'L')
        x = self.pdf.get_x()
        self.pdf.cell(width, height, working_days, 0, 0, 'L')
        self.pdf.line(x, self.pdf.get_y()+height, 195, self.pdf.get_y()+height)
        self.pdf.ln()  

        self.pdf.set_x(left)
        dist = self.pdf.get_string_width('Result: ')
        self.pdf.cell(dist, height, 'Result:', 0, 0, 'L')
        x = self.pdf.get_x()
        self.pdf.cell(width, height, overall_grade, 0, 0, 'L')
        self.pdf.line(x, self.pdf.get_y()+height, right-10, self.pdf.get_y()+height)
    
    def sig(self):

        self.pdf.ln(50)
        self.pdf.set_text_color(0,0,0)

        # self.pdf.set_x(50)
        # self.pdf.image(teacher_path, self.pdf.get_x()+1, self.pdf.get_y()-5, 25, 0, 'JPEG')
        # self.pdf.set_x(90)
        # self.pdf.image(parent_path, self.pdf.get_x()+1, self.pdf.get_y()-5, 25, 0, 'JPEG')
        # self.pdf.set_x(130)
        # self.pdf.image(hm_path, self.pdf.get_x()+1, self.pdf.get_y()-5, 25, 0, 'JPEG')
        # self.pdf.ln(5)

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
