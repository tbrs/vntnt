#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Simple .vnt into text converter.

This script converts .vnt files used to store notes on Samsung devices
into plain text.

Usage:
    $ python vntnt.py <input directory> <output directory>

For each .vnt file in input directory (non-recursive) it creates a .txt
file in output folder with the original body stored as plain text.
"""

import codecs
import os
import quopri
import sys

from datetime import datetime


class VntFile:
    program = ""
    version = ""
    charset = ""
    encoding = ""
    body = ""
    bodyDecoded = ""
    created = datetime.today()
    modified = datetime.today()

    def read(self, filename):
        """Read .vnt file contents into class' fields."""
        with open(filename, "r") as file:
            for line in file:
                if (line.startswith("BEGIN:")):
                    self.program = line[6:].strip()
                    continue
                if (line.startswith("VERSION:")):
                    self.version = line[8:].strip()
                    continue
                if (line.startswith("BODY;")):
                    parts = line.strip().rsplit(";")
                    self.charset = parts[1][8:]
                    parts = parts[2].rsplit(":")
                    self.encoding = parts[0][9:]
                    self.body = parts[1]
                    if (self.encoding == "QUOTED-PRINTABLE"):
                        self.bodyDecoded = quopri.decodestring(
                            self.body).decode(self.charset)
                    continue
                if (line.startswith("DCREATED:")):
                    self.created = datetime.strptime(
                        line[9:].strip(), "%Y%m%dT%H%M%S")
                    continue
                if (line.startswith("LAST-MODIFIED:")):
                    self.modified = datetime.strptime(
                        line[14:].strip(), "%Y%m%dT%H%M%S")

    def write(self, filename):
        """Save decoded body as plain text with UTF-8 encoding."""
        file = codecs.open(filename, "w", "utf-8")
        file.write(self.bodyDecoded)
        file.close()


def convertNote(filename, outputDir):
    note = VntFile()
    note.read(filename)
    outFilename = os.path.join(outputDir, note.modified.isoformat() + ".txt")
    note.write(outFilename)
    return outFilename

if (len(sys.argv) < 3):
    print "Usage:"
    print " $ python vntnt.py <input directory> <output directory>."
    exit()

inputDir = sys.argv[1]
outputDir = sys.argv[2]

if not os.path.exists(inputDir):
    print "Input directory " + inputDir + " does not exist."
    exit()

if not os.path.exists(outputDir):
    os.makedirs(outputDir)

noteCount = 0
for dirname, dirnames, filenames in os.walk(inputDir):
    for filename in filenames:
        fullFileName = os.path.join(dirname, filename)
        if (fullFileName.endswith(".vnt")):
            convertNote(fullFileName, outputDir)
            noteCount += 1

print "Usless counting resulted in discovering the fact that there are", noteCount, "note(s) in there."
