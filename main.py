#!/usr/bin/env python
# -*- coding: utf_8 -*- 

import argparse
from zipfile import ZipFile
from html import escape

import six
from google.cloud import translate_v2 as translate

translate_client = translate.Client()

parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
parser.add_argument("-c", "--columns", help="save text as parallel texts, with both languages side by side", action="store_true")
parser.add_argument("-s", "--sourcelang", dest="sourcelang", help="language of source epub file")
parser.add_argument("-t", "--targetlang", dest="targetlang", help="language to translate to")
parser.add_argument("-f", "--file", dest="filename", help="read epub from FILE", metavar="FILE")
parser.add_argument("-o", "--outfile", dest="out_filename", help="write translated epub to FILE", metavar="FILE")
parser.add_argument("-d", "--donotranslate", dest="donotranslate", help="test run, do not translate", action="store_true")

args = parser.parse_args()

sourcelang = "en"
targetlang = "es"
if args.sourcelang:
	sourcelang = args.sourcelang
if args.targetlang:
	targetlang = args.targetlang

filename = "test.epub"
out_filename = "out.epub"
if args.filename:
	filename = args.filename
if args.out_filename:
	out_filename = args.out_filename


def is_printable(s):
	return not any(repr(ch).startswith("'\\x") or repr(ch).startswith("'\\u") for ch in s)


def translatable (string):
	if (not string):
		return False
	# python string.isprintable() does NOT work with cyrillic script sentences
	if (not is_printable(string)):
		return False
	if (string.isspace()):
		return False
	if (not string.strip()):
		return False
	if (string == '\n'):
		return False
	return True


with ZipFile(filename, 'r') as zip:
	with ZipFile(out_filename, 'w') as zout:

		for info in zip.infolist():
			filedata = zip.read(info.filename)

			if (info.filename.endswith('html') or info.filename.endswith('ncx')):
				print(info.filename)
				originaldata = str(filedata.decode())
				if args.verbose:
					print("filedump:", originaldata)

				inside_tag = 0
				file_data = ""
				original_text = ""
				translated_text = ""
				tag = ""
				tagspace = False

				for char_index in range(len(originaldata)):
					if (originaldata[char_index] == "<"):
						inside_tag += 1
						# Check if translate
						if (translatable(original_text)):
							# Translate 
							if args.verbose:
								print("translatable:", original_text)
							# if tag in ["title", "style"]:
							# 	print("tag in:", tag)
							if args.donotranslate or tag in ["title", "style"]:
								translated_text = original_text
							else:
								translation = translate_client.translate(str(original_text), source_language=sourcelang, target_language=targetlang)
								translated_text = translation['translatedText']
							if args.verbose:
								print("translation:", translated_text)
							if args.columns:
								if tag in ["title", "style"]:
									file_data += original_text
								else:
									file_data += "<table style=\"width: 100%;\"><tbody><tr><td style=\"width: 50%; padding-right:6pt; vertical-align: top;\">"
									file_data += original_text
									file_data += "</td><td style=\"width: 50%; padding-left:6pt; vertical-align: top;\">"
									file_data += translated_text
									file_data += "</td></tr></tbody></table>"
							else:
								file_data += translated_text
						else:
							# Append to file_data
							if args.verbose:
								print("untranslatable:", original_text)
							file_data += original_text
						original_text = ""
						tag = ""
						tagspace = False
					if (inside_tag < 1):
						# print(originaldata[char_index], end='')
						original_text += originaldata[char_index]
					else:
						# print(originaldata[char_index], end='')
						file_data += originaldata[char_index]
						if originaldata[char_index] == ' ':
							tagspace = True
						if not tagspace and originaldata[char_index] not in ['<', '>']:
							tag += originaldata[char_index]
					if (originaldata[char_index] == ">"):
						inside_tag -= 1
						# print("tag", tag)

				zout.writestr(info.filename, file_data)

			else:
				zout.writestr(info.filename, filedata)

		print('Done!')
