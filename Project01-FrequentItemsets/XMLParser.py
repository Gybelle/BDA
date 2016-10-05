#!/usr/bin/python
import xml.sax


class ListOfAllAuthors(xml.sax.ContentHandler):
    map = {}
    tag = ""

    def startElement(self, name, attrs):
        self.map[name] = ""
        self.tag = name

    def characters(self, content):
        self.map[self.tag] += content

    def endElement(self, name):
        if name == "author":
            f.write(self.map[name] + "\n")


class ListOfAuthorsPerPublication(xml.sax.ContentHandler):
    map = {}
    tag = ""
    start_adding = False
    correctType = False

    def startElement(self, name, attrs):
        if name == "article" or name == "inproceedings":
            self.map["authorlist"] = "["
            self.correctType = True
        elif name == "author" and self.correctType:
            self.start_adding = True


    def characters(self, content):
        if self.start_adding and self.correctType:
            self.map["authorlist"] += content

    def endElement(self, name):
        if name == "article" or name == "inproceedings":
            self.correctType = False
            if len(self.map["authorlist"]) > 1:
                if self.map["authorlist"][-1] == ",":
                    f.write(self.map["authorlist"][:-1] + "]\n")
                else:
                    f.write(self.map["authorlist"] + "]\n")
        if name == "author" and self.correctType:
            self.map["authorlist"] += ","
            self.start_adding = False


# Parsing XML file
f = open("../Input/authorsperpublication.txt", "w")
parser = xml.sax.make_parser()
parser.setContentHandler(ListOfAuthorsPerPublication())
parser.parse(open("../Input/dblp50000.xml", "r", encoding="utf8"))
# parser.parse(open("../../dblp/dblp.xml", "r", encoding="utf8"))
f.close()
