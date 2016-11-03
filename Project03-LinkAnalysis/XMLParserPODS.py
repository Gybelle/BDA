#!/usr/bin/python
import xml.sax

conference = "PODS"
bigDataset = True

class ListOfAuthorsPerPublication(xml.sax.ContentHandler):
    authorList = ""
    author = ""
    booktitle = ""
    correctType = False
    isAuthor = False
    isBooktitle = False
    correctConference = False

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

    def characters(self, content):
        if self.isAuthor:
            self.author += content
        elif self.isBooktitle:
            self.booktitle += content

    def endElement(self, name):
        if self.correctType and name == "article" or name == "inproceedings":
            self.correctType = False
            if self.correctConference and len(self.authorList) > len("["):
                self.authorList = self.authorList.strip().rstrip(',')
                self.authorList += "]\n"
                f.write(self.authorList)
        elif self.isAuthor and name == "author":
            self.isAuthor = False
            self.authorList += self.author + ","
        elif self.isBooktitle and name == "booktitle":
            self.isBooktitle = False
            self.correctConference = self.booktitle == conference

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
