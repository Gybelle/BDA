#!/usr/bin/python
import xml.sax

correctBookTitles = ["KDD", "PKDD", "ICDM", "SDM"]
bigDataset = True

class ListOfAllTitles(xml.sax.ContentHandler):
    map = {}
    title = ""
    booktitle = ""
    correctType = False
    isTitle = False
    isBookTitle = False
    correctBookTitle = False

    def startElement(self, name, attrs):
        if name == "article" or name == "inproceedings":
            self.correctType = True
        elif self.correctType and name == "title":
            self.title = ""
            self.isTitle = True
        elif self.correctType and name == "booktitle":
            self.booktitle = ""
            self.isBookTitle = True

    def characters(self, content):
        if self.isTitle:
            self.title += content
        elif self.isBookTitle:
            self.booktitle += content

    def endElement(self, name):
        if self.correctType and name == "article" or name == "inproceedings":
            self.correctType = False
        elif self.isTitle and name == "title":
            self.isTitle = False
        elif self.isBookTitle and name == "booktitle":
            self.isBookTitle = False
            if self.booktitle in correctBookTitles:
                f.write(self.title + "\n")
            self.title = ""
            self.booktitle = ""


class ListOfTitlesPerPublication(xml.sax.ContentHandler):
    map = {}
    tag = ""
    start_adding = False
    correctType = False
    correctBookTitle = False

    def startElement(self, name, attrs):
        if name == "article" or name == "inproceedings":
            self.map["titlelist"] = "["
            self.correctType = True
        elif self.correctType and name == "title":
            self.tag = name
            self.start_adding = True
        elif self.correctType and name == "booktitle":
            self.tag = name

    def characters(self, content):
        if self.start_adding and self.correctType:
            self.map["titlelist"] += content

    def endElement(self, name):
        if name == "article" or name == "inproceedings":
            self.correctType = False
            if len(self.map["titlelist"]) > 1:
                if self.map["titlelist"][-1] == ",":
                    f.write(self.map["titlelist"][:-1] + "]\n")
                else:
                    f.write(self.map["titlelist"] + "]\n")
        elif name == "title" and self.correctType:
            self.map["titlelist"] += ","
            self.start_adding = False
            self.tag = ""
        elif name == "booktitle":
            self.tag = ""


# Parsing XML file
if not bigDataset:
    f = open("../Input/titles.txt", "w", encoding="utf8")
else:
    f = open("../Input/titlesBIG.txt", "w", encoding="utf8")
parser = xml.sax.make_parser()
parser.setContentHandler(ListOfAllTitles())
if not bigDataset:
    parser.parse(open("../Input/dblp50000.xml", "r", encoding="utf8"))
else:
    parser.parse(open("../../dblp/dblp.xml", "r", encoding="utf8"))
f.close()
