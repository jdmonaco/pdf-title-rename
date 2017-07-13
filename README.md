pdf-title-rename
----------------

A batch-renaming script for PDF files based on the Title and Author information in the metadata and XMP. The XMP metadata, if available, supersedes the standard PDF metadata. The output format is currently:

    [FirstAuthorLastName [LastAuthorLastName ]- ][SanitizedTitleText].pdf

Only the article title is used if no author information is found. First and last author surnames are used if the `creator` field in the XMP is a list of more than one author. 

To use the script, simply pass in a list or glob of PDF filenames. If you want to see what it would do without changing anything, do a dry run with `-n`. There is also an interactive mode with `-i` that will let you open the files and manually enter titles and author strings if you have problematic PDFs without proper metadata.

    usage: pdf-title-rename [-h] [-n] [-i] [-d DESTINATION] files [files ...]

    PDF batch rename

    positional arguments:
      files                 list of pdf files to rename

    optional arguments:
      -h, --help            show this help message and exit
      -n                    dry-run listing of filename changes
      -i                    interactive mode
      -d DESTINATION, --dest DESTINATION
                            destination folder for renamed files

This script is intended as a first pass in an academic PDF workflow to get browsable filenames for a pile of articles that have been downloaded but not yet filed away.

## Requirements

The PDF parsing uses [PDFMiner](https://github.com/euske/pdfminer/). The XMP parsing uses [this xmp module](http://blog.matt-swain.com/post/25650072381/a-lightweight-xmp-parser-for-extracting-pdf-metadata-in). Important: For XMP parsing to work, you will need to copy the code from that link to an `xmp.py` file and put it on your `PYTHONPATH`. (Note, I've now included `xmp.py` in the repo in case that link goes away; you still have to put it on your path.)

 * [PDFMiner](https://github.com/euske/pdfminer/)
 * [xmp](http://blog.matt-swain.com/post/25650072381/a-lightweight-xmp-parser-for-extracting-pdf-metadata-in)
