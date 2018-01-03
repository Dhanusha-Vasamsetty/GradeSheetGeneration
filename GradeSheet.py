# IMPORT STATEMENTS DO NOT MODIFY

from PyPDF2 import PdfFileReader, PdfFileWriter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4
import csv

''' 
WARNING: DO NOT FIELDS OTHER THAN MENTIONED IN THE EDIT SECTION. EDITING ANY OTHER SECTION MAY RESULT IN FAILURE 
OF THE PROJECT. 

CODE WRITTEN BY ANIRUDH SAI MERGU ON 18TH SEPTEMBER 2017.

READ COMMENTS BEFORE MODIFYING.
'''

''' START EDIT SECTION

REGISTER FONTS HERE
PASTE THE '.ttf' FILES IN THE PROJECT FOLDER BEFORE REGISTERING THE FONT AND DO NOT GIVE DUPLICATE FILE NAMES
REGISTER USING THE FORMAT 

pdfmetrics.registerFont(TTFont('FontName', 'Font.ttf'))

                               FONT NAME    FONT PATH

'''

# START -- FONT REGISTRATION

pdfmetrics.registerFont(TTFont('Aileron', 'Fonts/Aileron-Light.ttf'))

# SAMPLE --- REMOVE THE COMMENTS BEFORE USING
pdfmetrics.registerFont(TTFont('AileronBold', 'Fonts/Aileron-Bold.ttf'))
pdfmetrics.registerFont(TTFont('AileronSemiBold', 'Fonts/Aileron-SemiBold.ttf'))

# END -- FONT REGISTRATION

# START -- DOCUMENT SIZE SECTION

'''
    BOTTOMUP = 0 --> CO-ORDINATES FROM TOP TO BOTTOM
    CHANGE PAGESIZE IF YOU ARE USING ANY OTHER FORMAT OTHER THAN A4
    IMPORT SIZES USING

    from reportlab.lib.pagesizes import 'PAGETYPE'

                                            ^- A4, LEGAL, LETTER ETC.,
'''

line_no = 0
main_details = []
subjects = []
subject_names = []
credits_array = []
total_credits = 0
serial_number = 1

for line in open("CSE.csv"):

    line_no += 1

    if line_no <= 4:
        print("Acquiring Metadata\n")
    else:
        print("Generating certificate of %d" % (line_no - 4));

    var = line.split(',')

    if line_no == 1:
        for x in range(3):
            main_details.append(var[x])
        continue

    if line_no == 2:
        for x in range(4, len(var)):
            if var[x] != '':
                subjects.append(var[x])

        noOfSubjects = len(subjects)

        continue

    if line_no == 3:
        for x in range(4, 4 + noOfSubjects):
            subject_names.append(var[x])
        continue

    if line_no == 4:
        for x in range(4, 4 + noOfSubjects):
            if var[x] != '':
                credits_array.append(var[x])
                total_credits += int(var[x])
        continue

    c = canvas.Canvas("GradeSheetTemp.pdf", bottomup=0, pagesize=A4)

    # END -- DOCUMENT SIZE SECTION

    # START -- TYPOGRAPHY SECTION

    # SET FONT AND SIZE
    c.setFont('AileronSemiBold', 9)

    # SET FONT COLOR 000 FOR WHITE, 111 FOR BLACK
    c.setFillColorRGB(0, 0, 0)

    # END -- TYPOGRAPHY SECTION

    # MAIN CODE STARTS

    serial_number += 1
    branch = main_details[0]
    examination = main_details[1]
    month = main_details[2]
    name = var[2+noOfSubjects+1]
    father_name = var[2+noOfSubjects+2]
    mother_name = var[2+noOfSubjects+3]

    c.drawString(83, 133.67, str(serial_number))
    c.drawString(110, 154, examination)
    c.drawString(110, 170, branch)
    c.drawString(110, 186, name)
    c.drawString(110, 202, father_name)
    c.drawString(110, 218, mother_name)
    c.drawString(487.29, 218, month)

    rollno = var[0]
    credit = var[1]
    sgpa = var[2]
    cgpa = var[3]

    c.drawString(487.29, 154, rollno)

    absent = 0
    failed = 0

    for subject in range(noOfSubjects - 1):
        c.drawCentredString(61, 265.5 + x * subject, str(subject + 1))
        c.drawCentredString(118.28, 265.5 + x * subject, subjects[subject])
        c.drawString(188, 265.5 + x * subject, subject_names[subject])
        c.drawString(467, 265.5 + x * subject, var[4 + subject])
        if var[4 + subject] == 'Ab':
            absent += 1
        elif var[4 + subject] == 'F':
            failed += 1
        c.drawString(522, 265.5 + x * subject, credits_array[subject])

    c.drawCentredString(522, 594, str(sgpa))
    c.drawCentredString(522, 610, str(cgpa))

    c.drawCentredString(522, 578, str(credit))
    c.drawString(147.68, 578, str(noOfSubjects - 1))
    c.drawString(262, 578, str(noOfSubjects - absent - 1))
    c.drawString(368.5, 578, str(noOfSubjects - failed - absent - 1))

    c.showPage()
    c.save()

    c2 = canvas.Canvas('Image.pdf', pagesize=A4)

    c2.drawImage('Photographs/' + rollno + '.jpg', 488, 632, 51, 53, mask='auto')
    c2.showPage()
    c2.save()

    background = PdfFileReader(open('Background.pdf', 'rb'))
    foreground = PdfFileReader(open('GradeSheetTemp.pdf', 'rb'))
    image = PdfFileReader(open('Image.pdf', 'rb'))

    print("Line number %s parse successful!" % (line_no - 4))

    output = PdfFileWriter()

    page = background.getPage(0)
    page.mergePage(foreground.getPage(0))
    page.mergePage(image.getPage(0))

    output.addPage(page)

    print("Generating PDF")

    outputStream = open("Outputs/cse/" + rollno + ".pdf", "wb")

    output.write(outputStream)

    outputStream.close()

    print("Successfully generated to /Outputs/" + rollno + ".pdf\n")
