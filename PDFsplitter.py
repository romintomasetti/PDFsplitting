#!/usr/bin/env python
import copy, sys
from PyPDF2 import PdfFileWriter, PdfFileReader

"""
Split a PDF page in a iven number of subpages.
    1) filename      : file name of the PDF source file
    2) filenamemod   : file name of the modified PDF (destination)
    3) lines         : number of lines   in the grid
    4) colms         : number of columns in the grid
    5) orderSubPages : order of the subpages (see example below)
    
    Example:
    
        This is one PDF page, splitted into 4 subpages (lines = 2, colms = 2):
        
            *------------*------------*
            |  subpage 2 |  subpage 3 |
            |            |            |
            |            |            |
            *------------*------------*
            |  subpage 0 |  subpage 1 |
            |            |            |
            |            |            |
            *------------*------------*
            
        If you want the new PDF to be as follows:
        
            *------------*
            |  subpage 2 |
            |            |
            |            |
            *------------*
            *------------*
            |  subpage 3 |
            |            |
            |            |
            *------------*
            *------------*
            |  subpage 0 |
            |            |
            |            |
            *------------*
            *------------*
            |  subpage 1 |
            |            |
            |            |
            *------------*

        Then you need to set orderSubPages to [2,3,0,1].
"""

filename = "PoM Bus Strat.pdf"

filenamemod = "PoM Bus Strat_split.pdf"

lines = 2
colms = 2

orderSubPages = [2,3,0,1]

input = PdfFileReader(filename)
output = PdfFileWriter()

for p in [input.getPage(i) for i in range(0,input.getNumPages())]:

    (w, h) = p.mediaBox.upperRight
    
    subpages = []
    
    for i in range(lines):
        for j in range(colms):
            
            pp = copy.deepcopy(p)
        
            pp.mediaBox.lowerLeft  = ( j    * w / colms ,  i    * h / lines)
            pp.mediaBox.lowerRight = ((j+1) * w / colms ,  i    * h / colms)
            pp.mediaBox.upperLeft  = ( j    * w / colms , (i+1) * h / lines)
            pp.mediaBox.upperRight = ((j+1) * w / colms , (i+1) * h / lines)
    
            subpages.append(pp)
    
    for i in orderSubPages:
        output.addPage(subpages[i])


output.write(open(filenamemod,"wb+"))
