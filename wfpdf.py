#!/usr/bin/env python
# -*- coding: utf8 -*-

"""convenience wrapper for fpdf with unicode support
install_requires = ['fpdf'] ; + unicode fonts from pyfpdf.googlecode.com/files/fpdf_unicode_font_pack.zip in fpdf/font/

Usage:
  from wfpdf import PDF
  with PDF('output.pdf') as pdf:          # or ..PDF('output.pdf', ffamily [, fstyle, fsize, ffname])..
      pdf.write(8, u"unicode text")       #   ffname: name of .ttf file, it is recommended save fonts into fpdf/font/
                        #   you can download unicode fonts from pyfpdf.googlecode.com/files/fpdf_unicode_font_pack.zip

This was designed with fpdf 1.7.2 and it could be useful:
    for the calling with with.. syntax,
    for help with installation of unicode fonts as long as these fonts aren't included directly inside the fpdf module

In addition you can use some helpers from Utils class (pdf.utils). See Utils doc.
"""

from fpdf import FPDF

FONT_ERROR = ("Font not found. Hint: To output unicode characters copy unicode fonts "
            "from pyfpdf.googlecode.com/files/fpdf_unicode_font_pack.zip into fpdf/font/ "
            "(or to the location defined in SYSTEM_TTFONTS or FPDF_FONTPATH, "
            "or instantiate as PDF(filename, explicit_unicode_font, ffname=<path>/<fontfilename>)")


class PDF():
    """Basic export class. See Usage in module doc.
    """
    def __init__(self, fname, ffamily=None, fstyle='', fsize=0, ffname=None, fonts=None):
        """fname - name of the output pdf file
        you can initialize fonts in more ways, explicit (applies .add_font of fpdf) or explicit:
         - explicit with fonts= (see the implicit code bellow with DejaVu fonts where font styles B,I,BI are supported)
         - explicit with ffamily where just one font will be added
         - implicit DejaVu, if unicode fonts are installed for the fpdf package (in its font/ directory and so on)
         - implicit Arial, if fpdf cannot find unicode fonts
        """
        self.w_fname = fname
        self.w_pdf = FPDF()
        self.w_pdf.utils = Utils(self.w_pdf)
        self.w_pdf.add_page()
        explicit = ffamily or fonts
        if explicit:
            if not fonts:
                fonts = [(ffamily, '', ffname)] if ffname else []
        else:
            # try Unicode fonts from fpdf/font (or location defined by SYSTEM_TTFONTS or FPDF_FONTPATH) first
            fonts = [
                ('DejaVu', '', 'DejaVuSansCondensed.ttf'),
                ('DejaVu', 'B', 'DejaVuSansCondensed-Bold.ttf'),
                ('DejaVu', 'I', 'DejaVuSansCondensed-Oblique.ttf'),
                ('DejaVu', 'BI', 'DejaVuSansCondensed-BoldOblique.ttf'),
            ]
        try:
            for font in fonts:
                self.w_pdf.add_font(font[0], font[1], font[2], uni=True)
            self.w_pdf.set_font(fonts[0][0] if fonts else ffamily)
        except RuntimeError:
            if not explicit:    # fallback from unicode to latin-1
                self.w_pdf.set_font('Arial')
            else:
                raise RuntimeError(FONT_ERROR)

    def __enter__(self):
        return self.w_pdf

    def __exit__(self, *args):
        self.w_pdf.utils = None
        self.w_pdf.output(self.w_fname, 'F')


class Utils(object):
    """Print helper.
    Usage (example):
        # pdf.utils = Utils()           # this happens in PDF().__init__
        pdf.set_xy(x1, y1)
        pdf.utils.header("Name", 75, "Quantity", 100, "Unit")
        pdf.set_xy(x2, y2)
        pdf.utils.num(300.0, to_x=30)   # will format number using format parameter and force align='R'
        pdf.utils.txt("left aligned text", at_x=36)
        pdf.utils.down(10)              # move down from current position
        pdf.utils.txt("right aligned text", to_x=200)
    """
    height = 7      # default height for txt() and num() calls without h param,
    #               #   set this before txt()/num() calls or use explicit param ..(h=..)
    max_width = 26  # maximum width for all numeric (int/float) values printed with num()

    def __init__(self, pdf):
        self.oPdf = pdf

    def txt(self, txt, h=None, at_x=None, to_x=None, change_style=None, change_size=None):
        """print string to defined (at_x) position
        to_x can apply only if at_x is None and if used then forces align='R'
        """
        h = h or self.height
        self._change_props(change_style, change_size)
        align = 'L'
        w = None
        if at_x is None:
            if to_x is not None:
                align = 'R'
                self.oPdf.set_x(0)
                w = to_x
        else:
            self.oPdf.set_x(at_x)
        if w is None:
            w = self.oPdf.get_string_width(txt)
        self.oPdf.cell(w, h=h, txt=txt, align=align)

    def num(self, num, h=None, to_x=None, format="%.2f", change_style=None, change_size=None):
        """print number (int/float) right aligned before defined (to_x) position
        """
        self.txt(format % num, h=h, to_x=to_x, change_style=change_style, change_size=change_size)

    def header(self, item0, *items):
        """print string item0 to the current position and next strings to defined positions
        example: .header("Name", 75, "Quantity", 100, "Unit")
        """
        self.txt(item0)
        at_x = None
        for item in items:
            if at_x is None:
                at_x = item
            else:
                self.txt(item, at_x=at_x)
                at_x = None

    def down(self, h, cr=True):
        """moves current vertical position h mm down
        cr True will navigate to the left margin
        """
        if cr:
            self.oPdf.ln(h=0)
        self.oPdf.set_y(self.oPdf.get_y() + h)

    def _change_props(self, change_style, change_size):
        if change_style is not None:
            self.oPdf.set_font('', style=change_style)
        if change_size is not None:
            self.oPdf.set_font_size(change_size)


if __name__ == '__main__':
    # test the unicode support
    with PDF('test_unicode.pdf') as pdf:
        try:
            pdf.write(8, u"kůň úpěl ódy dobrý češtin")
        except UnicodeEncodeError:
            raise RuntimeError(FONT_ERROR)
    with PDF('test_ascii.pdf', 'Arial') as pdf:
        pdf.write("nice horses songs")
