from fpdf import FPDF

PORTRAIT_FULL_WIDTH = 190
LANDSCAPE_FULL_WIDTH = 277
MAX_ROWS = 2
LEFT_MARGIN = 10.00125
pdf = None

def main():
    global pdf
    pdf = FPDF('P', 'mm', [297, 210])

    page1Title = 'Report Card'
    subjects = ['Math', 'History', 'Chemistry', 'Biology', 'Physics', 'English', 'Computer Science']
    page1Columns = ['Subject', 'Teacher Name', 'Grade']
    page1Data = []

    for i in range(len(subjects)): 
        page1Data.append(['Jack Smith', str(i*10)])

    init()
    details()
    grades(page1Title, page1Columns, page1Data, subjects)
    
    pdf.output('PDF Reports/test_report.pdf', 'F')

def grades(sheetTitle, columnNamesArr, dataArr, subjects):
    global pdf
    justification = 'C'

    heading_index = 0
    sub_counter = 0
    data_counter = 0

    # Add page title
    # pdf.set_fill_color(255,255,255)
    # pdf.set_text_color(0,0,0)
    # pdf.set_font('Times', 'bu', 24)
    # pdf.cell(PORTRAIT_FULL_WIDTH, 12, sheetTitle, 0, 1, 'C')

    pdf.set_font('Arial', '', 12)
    
    while sub_counter < len(subjects):
     
        if heading_index == MAX_ROWS:
            heading_index = 0
        pdf.ln()
        # Add table header
        if not heading_index:
            pdf.set_font_size(7)
            pdf.set_fill_color(100,100,100)
            pdf.set_text_color(255,255,255)
            cell_index = 0
            for columnName in columnNamesArr:
                cellWidth = 150 if not cell_index else 50
                pdf.cell(63, 4, columnName, 1, 0, justification, True)
                cell_index += 1
            
            pdf.set_x(LEFT_MARGIN)
        # Add table content
        if heading_index:
            pdf.set_font_size(7)
            pdf.set_text_color(0,0,0)
            fillColor = [240, 240, 242] if heading_index%2 else [255, 255, 255]
            pdf.set_fill_color(fillColor[0], fillColor[1], fillColor[2])
            cell_index = 0
            
            for i in range(len(dataArr[0])+1):
                if i == 0:
                    pdf.cell(63, 4, subjects[sub_counter], 1, 0, justification, True)
                    sub_counter+=1
                elif i == 2:
                    if int(dataArr[data_counter][1]) < 60:
                        pdf.set_text_color(255,0,0)
                    else:
                        pdf.set_text_color(0,0,255)
                    pdf.cell(63, 4, dataArr[data_counter][i-1], 1, 0, justification, True)
                    # pdf.set_text_color(0,0,0)
                else:
                    pdf.cell(63, 4, dataArr[data_counter][i-1], 1, 0, justification, True)
            data_counter += 1
            pdf.set_x(LEFT_MARGIN)
        heading_index += 1
        if not heading_index%2:
            pdf.ln(4)
        
def init():
    global pdf
    pdf.add_page('L')

def details():
    global pdf
    pdf.set_font('Arial', '', 10)
    width = 15
    height = 5

    # for i in range(5):

    #     dist = pdf.get_string_width('Name: ')
    #     pdf.cell(dist, height, 'Name:', 0, 0, 'L')

    #     pdf.set_font('Arial', 'U', 10)
    #     dist1 = pdf.get_string_width('Jack Smith ')
    #     pdf.cell(dist1, height, 'Jack Smith', 0, 1, 'L')
    #     pdf.set_font('Arial', '', 10)

    # We can manually set bounds for all fields, input should be in list form so it works for either probably
    dist = pdf.get_string_width('Name: ')
    pdf.cell(dist, height, 'Name:', 0, 0, 'L')

    pdf.set_font('Arial', 'U', 10)
    pdf.cell(width, height, 'Jack Smith', 0, 1, 'L')
    pdf.set_font('Arial', '', 10)

    dist = pdf.get_string_width('Age: ')
    pdf.cell(dist, height, 'Age:', 0, 0, 'L')

    pdf.set_font('Arial', 'U', 10)
    pdf.cell(width, height, '20', 0, 1, 'L')
    pdf.set_font('Arial', '', 10)

    dist = pdf.get_string_width('Address: ')
    pdf.cell(dist, height, 'Address:', 0, 0, 'L')

    pdf.set_font('Arial', 'U', 10)
    pdf.cell(width, height, '123 Main St', 0, 1, 'L')
    pdf.set_font('Arial', '', 10)

    dist = pdf.get_string_width('City: ')
    pdf.cell(dist, height, 'City:', 0, 0, 'L')

    pdf.set_font('Arial', 'U', 10)
    pdf.cell(width, height, 'New York', 0, 1, 'L')
    pdf.set_font('Arial', '', 10)

    dist = pdf.get_string_width('State: ')
    pdf.cell(dist, height, 'State:', 0, 0, 'L')
    
    pdf.set_font('Arial', 'U', 10)
    pdf.cell(width, height, 'NY', 0, 1, 'L')
    pdf.set_font('Arial', '', 10)

    dist = pdf.get_string_width('Zip: ')
    pdf.cell(dist, height, 'Zip:', 0, 0, 'L')
    
    pdf.set_font('Arial', 'U', 10)
    pdf.cell(width, height, '10001', 0, 1, 'L')
    pdf.set_font('Arial', '', 10)

    dist = pdf.get_string_width('Phone: ')
    pdf.cell(dist, height, 'Phone:', 0, 0, 'L')
    
    pdf.set_font('Arial', 'U', 10)
    pdf.cell(width, height, '123-456-7890', 0, 1, 'L')
    pdf.set_font('Arial', '', 10)


if __name__ == '__main__':
    main()