#!/usr/bin/python
import xml.sax

conference = "PODS"
bigDataset = False

class ListOfAuthorsPerPublication(xml.sax.ContentHandler):
    authorList = ""
    author = ""
    booktitle = ""
    year = ""
    correctType = False
    isAuthor = False
    isBooktitle = False
    correctConference = False
    isYear = False

    def startElement(self, name, attrs):
        if name == "article" or name == "inproceedings":
            self.correctType = True
            self.authorList = "["
        elif self.correctType and name == "author":
            self.isAuthor = True
            self.author = ""
        elif self.correctType and name == "booktitle":
            self.isBooktitle = True
            self.booktitle = ""
        elif self.correctType and name == "year":
            self.isYear = True
            self.year = ""


    def characters(self, content):
        if self.isAuthor:
            self.author += content
        elif self.isBooktitle:
            self.booktitle += content
        elif self.isYear:
            self.year += content

    def endElement(self, name):
        if self.correctType and name == "article" or name == "inproceedings":
            self.correctType = False
            if self.correctConference and len(self.authorList) > len("["):
                self.authorList = self.authorList.strip().rstrip(',')
                self.authorList += "]\n"
                line = self.year + " " + self.authorList
                f.write(line)
        elif self.isAuthor and name == "author":
            self.isAuthor = False
            self.authorList += self.author + ","
        elif self.isBooktitle and name == "booktitle":
            self.isBooktitle = False
            self.correctConference = self.booktitle == conference
        elif self.isYear and name == "year":
            self.isYear = False

# Parsing XML file
if not bigDataset:
    f = open("../Input/pods.txt", "w", encoding="utf8")
else:
    f = open("../Input/podsBIG.txt", "w", encoding="utf8")
parser = xml.sax.make_parser()
parser.setContentHandler(ListOfAuthorsPerPublication())
if not bigDataset:
    parser.parse(open("../Input/dblp50000.xml", "r", encoding="utf8"))
else:
    parser.parse(open("../../dblp/dblp.xml", "r", encoding="utf8"))
f.close()
