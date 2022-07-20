from fpdf import FPDF

PORTRAIT_FULL_WIDTH = 190
LANDSCAPE_FULL_WIDTH = 277
MAX_ROWS = 10
LEFT_MARGIN = 10.00125
pdf = None

def main():
    global pdf
    pdf = FPDF('P', 'mm', [200, 210])

    page1Title = 'Annual Exam Report Card'
    subjects = ['Urdu', 'English', 'Math', 'Social Studies', 'Science', 'Islamiat', 'Sindhi', 'Art Drawing']
    page1Columns = ['Subject', 'Total Marks', 'Marks Obtained', 'Passing Grade']
    marksObtained = [86, 89, 90, 12, 92, 93, 94, 95]
    passingMarks = [33, 34, 35, 36, 37, 38, 39, 40]
    totalMarks = [100, 100, 100, 100, 100, 100, 75, 25]

    # for i in range(len(subjects)): 
    #     page1Data.append(['Jack Smith', str(i*10)])

    init()
    grades(columnNamesArr=page1Columns, subjects=subjects, marksArr=marksObtained, passingArr=passingMarks, totalArr=totalMarks)
    details_hardcoded()
    sig()
    
    pdf.output('PDF Reports/test_report.pdf', 'F')



def grades(columnNamesArr, subjects, marksArr, passingArr, totalArr):
    global pdf
    justification = 'C'

    heading_index = 0
    sub_counter = 0
    data_counter = 0

    width = 47
    height = 10


    pdf.set_font('Arial', '', 12)
    pdf.ln(10)
    # Heading

    pdf.set_font_size(10)
    pdf.set_fill_color(100,100,100)
    pdf.set_text_color(255,255,255)
    cell_index = 0
    for columnName in columnNamesArr:
        pdf.cell(width, height, columnName, 1, 0, justification, True)
        cell_index += 1
    

    while sub_counter < len(subjects):

        pdf.ln()
        pdf.set_font_size(9)
        pdf.set_text_color(0,0,0)
        fillColor = [240, 240, 242] if heading_index%2 else [255, 255, 255]
        pdf.set_fill_color(fillColor[0], fillColor[1], fillColor[2])
        

        for i in range(4):

            if i == 0:

                pdf.cell(width, height, subjects[sub_counter], 1, 0, justification, True)
                sub_counter+=1

            elif i == 1:

                pdf.cell(width, height, str(totalArr[data_counter]), 1, 0, justification, True)

            elif i == 2:

                if int(marksArr[data_counter]) < int(passingArr[data_counter]):
                    pdf.set_text_color(255,0,0)
                else:
                    pdf.set_text_color(0,0,255)
                pdf.cell(width, height, str(marksArr[data_counter]), 1, 0, justification, True)
                pdf.set_text_color(0,0,0)

            elif i == 3:
                pdf.cell(width, height, str(passingArr[data_counter]), 1, 0, justification, True)

        data_counter += 1
        pdf.set_x(LEFT_MARGIN)

        heading_index += 1
    pdf.ln(7)

        
def init():
    global pdf
    pdf.add_page('L')
    # Add page title
    pdf.set_fill_color(255,255,255)
    pdf.set_text_color(0,0,0)
    pdf.set_font('Times', 'bu', 24)
    pdf.cell(PORTRAIT_FULL_WIDTH, 12, 'Report Card', 0, 1, 'C')

# def details_dynamic():

#     global pdf
#     pdf.set_font('Arial', '', 10)
#     width = 15
#     height = 5

#     for i in range(5):

#         dist = pdf.get_string_width('Name: ')
#         pdf.cell(dist, height, 'Name:', 0, 0, 'L')

#         pdf.set_font('Arial', 'U', 10)
#         dist1 = pdf.get_string_width('Jack Smith ')
#         pdf.cell(dist1, height, 'Jack Smith', 0, 1, 'L')
#         pdf.set_font('Arial', '', 10)

def details_hardcoded():
    global pdf
    pdf.set_font('Arial', '', 10)
    pdf.ln(13)
    width = 15
    height = 5

    left = 15
    right = 110

    # We can manually set bounds for all fields, input should be in list form so it works for either probably
    pdf.set_x(left)
    dist = pdf.get_string_width('Name: ')
    pdf.cell(dist, height, 'Name:', 0, 0, 'L')
    x = pdf.get_x()
    pdf.cell(width, height, 'Jack Smith', 0, 0, 'L')
    pdf.line(x, pdf.get_y()+height, pdf.get_x()+50, pdf.get_y()+height)
 


    pdf.set_x(right)
    dist = pdf.get_string_width('Name: ')
    pdf.cell(dist, height, 'Name:', 0, 0, 'L')
    x = pdf.get_x()
    pdf.cell(width, height, 'Jack Smith', 0, 0, 'L')
    pdf.line(x, pdf.get_y()+height, pdf.get_x()+50, pdf.get_y()+height)
    pdf.ln()


    pdf.set_x(left)
    dist = pdf.get_string_width('Name: ')
    pdf.cell(dist, height, 'Name:', 0, 0, 'L')
    x = pdf.get_x()
    pdf.cell(width, height, 'Jack Smith', 0, 0, 'L')
    pdf.line(x, pdf.get_y()+height, pdf.get_x()+50, pdf.get_y()+height)
 

    pdf.set_x(right)
    dist = pdf.get_string_width('Name: ')
    pdf.cell(dist, height, 'Name:', 0, 0, 'L')
    x = pdf.get_x()
    pdf.cell(width, height, 'Jack Smith', 0, 0, 'L')
    pdf.line(x, pdf.get_y()+height, pdf.get_x()+50, pdf.get_y()+height)
    pdf.ln()

    pdf.set_x(left)
    dist = pdf.get_string_width('Name: ')
    pdf.cell(dist, height, 'Name:', 0, 0, 'L')
    x = pdf.get_x()
    pdf.cell(width, height, 'Jack Smith', 0, 0, 'L')
    pdf.line(x, pdf.get_y()+height, pdf.get_x()+50, pdf.get_y()+height)


    pdf.set_x(right)
    dist = pdf.get_string_width('Name: ')
    pdf.cell(dist, height, 'Name:', 0, 0, 'L')
    x = pdf.get_x()
    pdf.cell(width, height, 'Jack Smith', 0, 0, 'L')
    pdf.line(x, pdf.get_y()+height, pdf.get_x()+50, pdf.get_y()+height)
    pdf.ln()




def sig():

    pdf.ln(10)
    pdf.set_text_color(0,0,0)

    pdf.set_x(50)
    pdf.image("C://Users//akeel//Desktop//Taleem Gah//Taleem-Gah-School-Website//Code//sig.jpeg", pdf.get_x()+1, pdf.get_y()-5, 25, 0, 'JPEG')
    pdf.set_x(90)
    pdf.image("C://Users//akeel//Desktop//Taleem Gah//Taleem-Gah-School-Website//Code//sig.jpeg", pdf.get_x()+1, pdf.get_y()-5, 25, 0, 'JPEG')
    pdf.set_x(130)
    pdf.image("C://Users//akeel//Desktop//Taleem Gah//Taleem-Gah-School-Website//Code//sig.jpeg", pdf.get_x()+1, pdf.get_y()-5, 25, 0, 'JPEG')
    pdf.ln(5)

    pdf.set_x(50)
    dist = pdf.get_string_width('Teacher Signature')
    pdf.line(pdf.get_x(), pdf.get_y(), pdf.get_x()+dist, pdf.get_y())
    pdf.cell(dist, 5, 'Teacher Signature', 0, 0, 'L')

    pdf.set_x(90)
    dist = pdf.get_string_width('Parents Signature')
    pdf.line(pdf.get_x(), pdf.get_y(), pdf.get_x()+dist, pdf.get_y())
    pdf.cell(dist, 5, 'Parents Signature', 0, 0, 'L')

    pdf.set_x(130)
    dist = pdf.get_string_width('Head Mistress Signature')
    pdf.line(pdf.get_x(), pdf.get_y(), pdf.get_x()+dist, pdf.get_y())
    pdf.cell(dist, 5, 'Head Mistress Signature', 0, 0, 'L')
    # add your own path here

if __name__ == '__main__':
    main()