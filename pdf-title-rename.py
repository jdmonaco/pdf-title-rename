#!/usr/bin/env python

"""
A script to batch rename PDF files based on metadata/XMP title and author

Requirements:
    - PDFMiner: https://github.com/euske/pdfminer/
    - xmp: lightweight XMP parser from
        http://blog.matt-swain.com/post/25650072381/
            a-lightweight-xmp-parser-for-extracting-pdf-metadata-in
"""



import os
import sys
import argparse
import subprocess

# PDF and metadata libraries
from pdfminer.pdfparser import PDFParser, PDFSyntaxError
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdftypes import resolve1
from xmp import xmp_to_dict


class RenamePDFsByTitle(object):

    """
    This class parses PDF files for title and author and then
    renames them.
    """

    def __init__(self, args):
        self.pdf_files = args.files
        self.dry_run = args.dry_run
        self.interactive = args.interactive
        self.destination = None
        if args.destination:
            if os.path.isdir(args.destination):
                self.destination = args.destination
            else:
                print('warning: destination is not a valid directory')

    def main(self):
        """Entry point for running the script."""
        for f in self.pdf_files:
            path, base = os.path.split(f)
            title, author = self._get_info(f)
            if title:
                g = os.path.join(path, self._new_filename(title, author))
                print('--> moving', '\"%s\"' % f, 'to', '\"%s\"' % g)
                if self.dry_run:
                    continue
                try:
                    os.rename(f, g)
                except OSError:
                    print('--> error renaming file, maybe it moved?')
                    continue
                if self.destination is not None:
                    ret = subprocess.call(['mv', g, self.destination])
                    if ret == 0:
                        print('--> filed to', self.destination)
                    else:
                        print('--> error moving file')
        return 0

    def _new_filename(self, title, author):
        n = self._sanitize(title)
        if author:
            n = '%s - %s' % (self._sanitize(author), n)
        n = '%s.pdf' % n[:250]  # limit filenames to ~255 chars
        return n

    def _sanitize(self, s):
        keep = [' ', '.', '_', '-', '\u2014']
        return "".join(c for c in s if c.isalnum() or c in keep).strip()

    def _get_info(self, filename):
        title = author = None
        with open(filename, 'rb') as pdf:
            info = self._get_metadata(pdf)
            if not info:
                return title, author
            if 'Title' in info and info['Title'].strip() != 'untitled':
                title = info['Title'].strip()
            if 'Author' in info and info['Author'].strip():
                author = self._au_last_name(info['Author'].strip())
            if 'Metadata' in self.doc.catalog:
                ti, au = self._get_xmp_metadata()
                if type(ti) is str and ti.strip().lower() != 'untitled':
                    title = ti
                if au:
                    author = au
        if self.interactive:
            title, author = self._interactive_info_query(filename, title, author)
        return title, author

    def _interactive_info_query(self, fn, t, a):
        print('-' * 60)
        print('Filename:'.ljust(20), fn)
        print(' * Found (t)itle:'.ljust(20), '\"%s\"' % str(t))
        print(' * Found (a)uthors:'.ljust(20), '\"%s\"' % str(a))
        ri = lambda p: input(p).lower().strip()
        ans = ri('Change (t/a) or open (o) or keep (k)? (t/a/o/k) ')
        while ans != 'k':
            if ans == 't':
                t = input('New title: ').strip()
            elif ans == 'a':
                a = input('New author string: ').strip()
            elif ans == 'o':
                subprocess.call(['open', fn])
            else:
                print('Bad option, please choose again:')
            ans = ri('(t/a/o/k) ')
        return t, a

    def _get_metadata(self, h):
        parser = PDFParser(h)
        try:
            doc = self.doc = PDFDocument(parser)
        except PDFSyntaxError:
            return {}
        parser.set_document(doc)
        return doc.info[0]

    def _get_xmp_metadata(self):
        t = a = None
        metadata = resolve1(self.doc.catalog['Metadata']).get_data()
        try:
            md = xmp_to_dict(metadata)
        except:
            return t, a
        try:
            t = md['dc']['title']['x-default']
        except KeyError:
            pass
        try:
            a = md['dc']['creator']
        except KeyError:
            pass
        else:
            if type(a) is str:
                a = [a]
            a = list(filter(bool, a))  # remove None, empty strings, ...
            if len(a) > 1:
                a = '%s %s' % (self._au_last_name(a[0]),
                        self._au_last_name(a[-1]))
            elif len(a) == 1:
                a = self._au_last_name(a[0])
            else:
                a = None
        return t, a

    def _au_last_name(self, name):
        return name.split()[-1]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PDF batch rename")
    parser.add_argument('files', nargs='+',
                        help='list of pdf files to rename')
    parser.add_argument('-n', dest='dry_run', action='store_true',
                        help='dry-run listing of filename changes')
    parser.add_argument('-i', dest='interactive', action='store_true',
                        help='interactive mode')
    parser.add_argument('-d', '--dest', dest='destination',
                        help='destination folder for renamed files')
    args = parser.parse_args()
    sys.exit(RenamePDFsByTitle(args).main())

