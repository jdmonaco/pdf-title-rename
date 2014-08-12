pdf-title-rename
----------------

A simple batch-renaming script for PDF files based on the Title and Author information in the metadata and XMP. The XMP metadata, if available, supersedes the standard metadata. The output format is currently fixed to this:

    [FirstAuthorLastName [LastAuthorLastName ]- ][SanitizedTitleText].pdf

Only the title text is used if no author information is found. Both first and last author surnames are used if the `creator` field in the XMP is a list of more than one author. 

Usage is very basic right now. Pass in a glob of pdfs, and do a dry run with `-n`.

    usage: pdf-title-rename [-h] [-n] files [files ...]

    PDF batch rename

    positional arguments:
      files       list of pdf files to rename

    optional arguments:
        -h, --help  show this help message and exit
        -n          dry-run listing of filename changes

This script is intended as a first-pass in an academic PDF workflow, just to get browsable filenames when looking through a huge pile of articles that have been downloaded but not yet filed away in a proper bibliographic database.

## Requirements

As noted in the script's docstring, all the PDF parsing is based on [PDFMiner](https://github.com/euske/pdfminer/). The XMP parsing requires [this xmp module](http://blog.matt-swain.com/post/25650072381/a-lightweight-xmp-parser-for-extracting-pdf-metadata-in), which will require copying from that page into a new `xmp.py` module somewhere on your `PYTHONPATH`.

 * [PDFMiner](https://github.com/euske/pdfminer/)
 * [xmp](http://blog.matt-swain.com/post/25650072381/a-lightweight-xmp-parser-for-extracting-pdf-metadata-in)
