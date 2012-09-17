# -*- coding: utf-8 -*-
from JiuJiuException import ErrorToUser



def print_barcode_str(Barcode,Str,Config):  
  FileName = gen_pic(Barcode,Str,Config)
  printer_print_file(FileName)

def gen_pic(Barcode,Str,Config):  #StrSize,BCSize):
  import ImageFont, ImageDraw, Image
  from string import lower, upper

  #Get config data
  StrSize=int(Config.get_GLCvalue('SizeOfString'))
  BCSize = int(Config.get_GLCvalue('SizeOfBarcode'))
  StrLeftMargin = int(Config.get_GLCvalue('StringLeftMargin'))
  BCLeftMargin = int(Config.get_GLCvalue('BarcodeLeftMargin'))
  EndMargin = int(Config.get_GLCvalue('EndMargin'))
  EndSepreater = Config.get_GLCvalue('StringEndSepreater').encode('cp936')
  IsPrintBC = int(Config.get_GLCvalue('IsPrintBC'))
  ImgW = int(Config.get_GLCvalue('PageWidth'))
  ImgH = int(Config.get_GLCvalue('PageHight'))


  #Turn Barcode to string
  if type(Barcode) == type(1):
    Barcode = str(Barcode)
  #split lines
  Lines = Str.split("\n")
    


  extension="JPEG"

  printstring = Str

  TextFontName = Config.get_GLCvalue('TextTTF').encode('cp936')

  position = 8
  image = Image.new("1",(ImgW+position,ImgH))
  # Create drawer
  draw = ImageDraw.Draw(image)

  # use a truetype font

  try:
    barcodefont = ImageFont.truetype("c39hrp36dltt.ttf", BCSize)
    textfont = ImageFont.truetype(TextFontName, StrSize)
  except IOError as ErrIO :
    raise ErrorToUser(TextFontName+" not found!")

  
  draw.rectangle(((0,0),(image.size[0],image.size[1])),fill=256)

  #Draw strings
  #draw.text((10, 25), unicode(printstring,'UTF-8'), font=textfont)
  (X,Y) = draw_lines(draw,Lines,(StrLeftMargin,25),textfont)

  #Draw barcodes
  (X2,Y2) = (0,0)
  if IsPrintBC == 0:
    BCStr =  "*"+Barcode+"*" #format barcode
    draw.text((BCLeftMargin, 25+Y),BCStr, font=barcodefont)
    (X2,Y2)=draw.textsize(BCStr,font=barcodefont)

  #Draw some empty area at the end of page.
  draw.text((BCLeftMargin, Y+Y2+25+EndMargin), EndSepreater, font=textfont)


  FileName = "printtmpfile"+"."+lower(extension)

  image.save(FileName,upper(extension))
  return FileName

def printer_print_file(FileName):
  import win32print
  import win32ui
  from PIL import Image, ImageWin
  file_name = FileName
  #
  # Constants for GetDeviceCaps
  #
  #
  # HORZRES / VERTRES = printable area
  #
  HORZRES = 8
  VERTRES = 10
  #
  # LOGPIXELS = dots per inch
  #
  LOGPIXELSX = 300
  LOGPIXELSY = 300
  #
  # PHYSICALWIDTH/HEIGHT = total area
  #
  PHYSICALWIDTH = 110
  PHYSICALHEIGHT = 111
  #
  # PHYSICALOFFSETX/Y = left / top margin
  #
  PHYSICALOFFSETX = 112
  PHYSICALOFFSETY = 113

  printer_name = win32print.GetDefaultPrinter ()
  #   file_name = "test.jpg"

  #
  # You can only write a Device-independent bitmap
  #  directly to a Windows device context; therefore
  #  we need (for ease) to use the Python Imaging
  #  Library to manipulate the image.
  #
  # Create a device context from a named printer
  #  and assess the printable size of the paper.
  #
  hDC = win32ui.CreateDC ()
  hDC.CreatePrinterDC (printer_name)
  printable_area = hDC.GetDeviceCaps (HORZRES), hDC.GetDeviceCaps (VERTRES)
  printer_size = hDC.GetDeviceCaps (PHYSICALWIDTH), hDC.GetDeviceCaps (PHYSICALHEIGHT)
  printer_margins = hDC.GetDeviceCaps (PHYSICALOFFSETX), hDC.GetDeviceCaps (PHYSICALOFFSETY)

  #
  # Open the image, rotate it if it's wider than
  #  it is high, and work out how much to multiply
  #  each pixel by to get it as big as possible on
  #  the page without distorting.
  #
  bmp = Image.open (file_name)
  if bmp.size[0] > bmp.size[1]:
    bmp = bmp.rotate (180)

  ratios = [1.0 * printable_area[0] / bmp.size[0], 1.0 * printable_area[1] / bmp.size[1]]
  scale = min (ratios)

  #
  # Start the print job, and draw the bitmap to
  #  the printer device at the scaled size.
  #
  hDC.StartDoc (file_name)
  hDC.StartPage ()

  dib = ImageWin.Dib (bmp)
  scaled_width, scaled_height = [int (scale * i) for i in bmp.size]
  x1 = int ((printer_size[0] - scaled_width) /2)
  y1 = int ((printer_size[1] - scaled_height) /2)
  x2 = x1 + scaled_width
  y2 = y1 + scaled_height
  dib.draw (hDC.GetHandleOutput (), (x1, y1, x2, y2))

  hDC.EndPage ()
  hDC.EndDoc ()
  hDC.DeleteDC ()


def draw_lines(draw,Lines,pos,font):
  (x,y) = pos
  for Line in Lines:
      draw.text((x, y), unicode(Line,'cp936'), font=font)
      (newX,newY) = draw.textsize(Line,font=font)
      y=y+newY
  return (x,y)

if __name__ == '__main__':
  #print_barcode_str(123456,"This is a test string\n hahah\nsafk\n")
  gen_pic(123456,"测试打印")
  
