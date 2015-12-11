#!/usr/bin/env python
# -*- coding: utf8 -*-

"""convenience wrapper for fpdf with unicode support
Usage:
  form wfpdf import PDF
  with PDF('output.pdf') as pdf:          # or ..PDF('output.pdf', ffamily [, fstyle, fsize, ffname])..
      pdf.write(8, u"unicode text")       #   ffname: name of .ttf file, it is recommended save fonts into fpdf/font/
                        #   you can download unicode fonts from pyfpdf.googlecode.com/files/fpdf_unicode_font_pack.zip

This was designed with fpdf 1.7.2 and it could be useful:
    for the calling with with.. syntax,
    for help with installation of unicode fonts as long as these fonts aren't included directly inside the fpdf module
"""

from fpdf import FPDF

FONT_ERROR = ("Font not found. Hint: To output unicode characters copy unicode fonts "
            "from pyfpdf.googlecode.com/files/fpdf_unicode_font_pack.zip into fpdf/font/ "
            "(or to the location defined in SYSTEM_TTFONTS or FPDF_FONTPATH, "
            "or instantiate as PDF(filename, explicit_unicode_font, ffname=<path>/<fontfilename>)")

class PDF():
    def __init__(self, fname, ffamily=None, fstyle='', fsize=0, ffname=None):
        self.w_fname = fname
        self.w_pdf = FPDF()
        self.w_pdf.add_page()
        explicit = ffamily
        if not explicit:
            # try Unicode fonts from fpdf/font (or location defined by SYSTEM_TTFONTS or FPDF_FONTPATH) first
            ffamily = 'DejaVu'
            ffname = 'DejaVuSansCondensed.ttf'
        try:
            if ffname:
                self.w_pdf.add_font(ffamily, '', ffname, uni=True)
            self.w_pdf.set_font(ffamily)
        except RuntimeError:
            if not explicit:    # fallback from unicode to latin-1
                self.w_pdf.set_font('Arial')
            else:
                raise RuntimeError(FONT_ERROR)

    def __enter__(self):
        return self.w_pdf

    def __exit__(self, *args):
        self.w_pdf.output(self.w_fname, 'F')


if __name__ == '__main__':
    # test the unicode support
    with PDF('test_unicode.pdf') as pdf:
        try:
            pdf.write(8, u"kůň úpěl ódy dobrý češtin")
        except UnicodeEncodeError:
            raise RuntimeError(FONT_ERROR)
    with PDF('test_unicode.pdf', 'Arial') as pdf:
        pdf.write("nice horses songs")
