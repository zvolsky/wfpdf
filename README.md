# wfpdf
convenience wrapper for fpdf with unicode support

## Usage:
```
form wfpdf import PDF
with PDF('output.pdf') as pdf:          # or ..PDF('output.pdf', ffamily [, fstyle, fsize, ffname])..
pdf.write(8, u"unicode text")           #   ffname: name of .ttf file, it is recommended save fonts into fpdf/font/
                #   you can download unicode fonts from pyfpdf.googlecode.com/files/fpdf_unicode_font_pack.zip
```

This was designed with fpdf 1.7.2 and it could be useful:
    for the calling with with.. syntax,
    for help with installation of unicode fonts as long as these fonts aren't included directly inside the fpdf module
"""
