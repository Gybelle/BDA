#!/usr/bin/python
import xml.sax


class ListOfAllTitles(xml.sax.ContentHandler):
    map = {}
    tag = ""

    def startElement(self, name, attrs):
        self.map[name] = ""
        self.tag = name

    def characters(self, content):
        self.map[self.tag] += content

    def endElement(self, name):
        if name == "title":
            f.write(self.map[name] + "\n")


class ListOfTitlesPerPublication(xml.sax.ContentHandler):
    map = {}
    tag = ""
    start_adding = False
    correctType = False

    def startElement(self, name, attrs):
        if name == "article" or name == "inproceedings":
            self.map["titlelist"] = "["
            self.correctType = True
        elif name == "title" and self.correctType:
            self.start_adding = True


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
        if name == "title" and self.correctType:
            self.map["titlelist"] += ","
            self.start_adding = False


# Parsing XML file
f = open("../Input/titles.txt", "w")
parser = xml.sax.make_parser()
parser.setContentHandler(ListOfTitlesPerPublication())
parser.parse(open("../Input/dblp50000.xml", "r", encoding="utf8"))
# parser.parse(open("../../dblp/dblp.xml", "r", encoding="utf8"))
f.close()
