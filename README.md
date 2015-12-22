# wfpdf
convenience wrapper for fpdf with unicode support

## Requires
fpdf

## Status: Beta
0.9.1 improved initialization of fpdf fonts; Utils class added
0.9.0 published

## Usage:
```
from wfpdf import PDF
with PDF('output.pdf') as pdf:          # or ..PDF('output.pdf', ffamily [, fstyle, fsize, ffname])..
    pdf.write(8, u"unicode text")       #   ffname: name of .ttf file, it is recommended save fonts into fpdf/font/
                # you can download unicode fonts from pyfpdf.googlecode.com/files/fpdf_unicode_font_pack.zip
                #   or from backup in this package in fpdf/font/
```

This was designed with fpdf 1.7.2 and it could be useful:
   - for the calling with with.. syntax,
   - for help with installation of unicode fonts as long as these fonts aren't included directly inside the fpdf module

In addition you can use some helpers from Utils class (pdf.utils). See Utils doc.
