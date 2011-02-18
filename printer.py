# coding=utf-8
# type/draw a text string to the default printer
# needs the win32 extensions package
# from: http://starship.python.net/crew/mhammond/win32/Downloads.html

import win32ui
import win32print
import win32con
import calendar as cd
def print_in_paper(str1):
    # set monthly calendar so it will start with a Saturday
    cd.setfirstweekday(cd.SATURDAY)
    try:
        hDC = win32ui.CreateDC()
        print win32print.GetDefaultPrinter()  # test
        hDC.CreatePrinterDC(win32print.GetDefaultPrinter())
        hDC.StartDoc("Test doc")
        hDC.StartPage()
        hDC.SetMapMode(win32con.MM_TWIPS)

        # draws text within a box (assume about 1400 dots per inch for typical HP printer)
        ulc_x = 20    # give a left margin
        ulc_y = -20   # give a top margin
        lrc_x = 21500   # width of text area-margin, close to right edge of page
        lrc_y = -25000  # height of text area-margin, close to bottom of the page
        hDC.DrawText(str1, (ulc_x, ulc_y, lrc_x, lrc_y), win32con.DT_LEFT)

        hDC.EndPage()
        hDC.EndDoc()
    except:
        print "Printer not online"  # does not work!


if __name__ == '__main__':
    #str1 = u"ÄãºÃ"
    # put a year's monthly calendars into a string
    str1 = cd.calendar(2008)
    #str1 = "Hello William!\n"
    raw_input('make sure printer is ready then hit enter key ... ')
    print_in_paper("XXXXXXXXXXXXXXXXXXXXXXXXXX")
