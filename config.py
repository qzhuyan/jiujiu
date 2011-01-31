#!/usr/bin/env python
from xlrd import open_workbook
import xlrd
wb = open_workbook('config.xls')
ConfigSheet = wb.sheet_by_name('config')
for row in range(ConfigSheet.nrows):
    print ConfigSheet.row(row)
    

    

