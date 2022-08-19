# epub-translate
Script to automatically translate an ePub using Google API. It can output parallel text in columns.

After translation, use Calibre editor to fix any errors before opening the resulting ePub file.

Requirements:

Depending on the engine used, you will need Google, AWS, or DeepL credentials.
See the corresponding translation provider documentation for more information.

Usage:


    python main.py -h
    usage: main.py [-h] [-v] [-c] [-s SOURCELANG] [-t TARGETLANG] [-f FILE] [-o FILE] [-e ENGINE]
    
    optional arguments:
      -h, --help            show this help message and exit
      -v, --verbose         increase output verbosity
      -c, --columns         save text as parallel texts, with both languages side by side
      -s SOURCELANG, --sourcelang SOURCELANG
                            language of source epub file
      -t TARGETLANG, --targetlang TARGETLANG
                        language to translate to
      -f FILE, --file FILE  read epub from FILE
      -o FILE, --outfile FILE
                            write translated epub to FILE
      -e ENGINE, --engine ENGINE
                            valid options are: google, aws, deepl. Default is google.
                        
