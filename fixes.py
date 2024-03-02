import json
import os
from PyPDF2 import PdfReader, PdfWriter

judet = "București  "


def getText(reader, pageNumber):
    page = reader.pages[pageNumber]
    text = page.extract_text()
    if (pageNumber == 0):
        cybereduIndexes = [i for i in range(
            len(text)) if text.startswith("CyberEDU", i)][1]
        workingText = text[cybereduIndexes+8:]
        return workingText
    firstIndex = text.find("/")

    workingText = text[firstIndex+5:]
    return workingText


elevi = []
reader = PdfReader(f"./data/{judet}.pdf")
number_of_pages = len(reader.pages)
print("Opened " + judet + ".pdf with " + str(number_of_pages) + " pages.")
for i in range(number_of_pages):
    page = reader.pages[i]
    print("Opened page " + str(i) + " from " +
          judet + ".pdf. Extracting text...")
    workingText = getText(reader, i)

    separatorChars = ['IX', 'X', 'XI', 'XII']

    workingLength = len(workingText)

    # loop through the text

    def foundElev(judet, cls, currentString):
        currentElev = {
            "clasa": cls,
            "judet": judet,
            "rank": "",
            "id": "",
            "punctaj": "",
            "absent": False
        }
        if (cls == "Unknown"):
            return
        print("Clasa " + str(cls))

        isAbsent = currentString.find("absent") != -1
        currentElev["absent"] = isAbsent
        if (isAbsent):
            print("Elev absent")
            return
        separatedString = currentString.split(" ")
        rank = separatedString[0]
        print(separatedString)
        separatedString = list(filter(lambda a: a != '', separatedString))
        separatedString = list(
            filter(lambda a: a != '\nX', separatedString))
        if (len(separatedString) < 8):
            print(
                "Elevul " + separatedString[1] + " are " + str(len(separatedString)) + " elemente.")
            print(separatedString)
            return
        if (rank == ""):
            rank = "Unknown"
            separatedString.insert(0, rank)

        id = separatedString[1].replace(
            "\n", "") + separatedString[2].replace("\n", "")
        punctaj = separatedString[3]
        currentElev["rank"] = rank
        currentElev["id"] = id
        currentElev["punctaj"] = punctaj
        elevi.append(currentElev)
        print(f"Rank: {rank}\nID: {id}\nPunctaj: {punctaj}\n")

    currentString = ""
    cls = "Unknown"
    i = 0
    while i < workingLength:
        currentString += workingText[i]
        currentString.replace("\n", " ")
        currentChar = workingText[i]
        current2CharsWith2After = workingText[i:i+2]
        current3CharsWith3After = workingText[i:i+3]
        # check if the current char is a separator char

        if (currentChar in separatorChars) and (current2CharsWith2After not in separatorChars) and (current3CharsWith3After not in separatorChars):
            foundElev(judet, cls, currentString)
            currentString = ""
            i += 1
            cls = currentChar
            # clasa 10
            pass
        # print(current2CharsWith2After)
        if (current2CharsWith2After in separatorChars) and (current3CharsWith3After not in separatorChars):
            foundElev(judet, cls, currentString)
            currentString = ""
            i += 2
            cls = current2CharsWith2After
            # clasa 9, 11
            pass
        # print(current3CharsWith3After)
        if (current3CharsWith3After in separatorChars):
            foundElev(judet, cls, currentString)
            currentString = ""
            i += 3
            cls = current3CharsWith3After
            # clasa 12
            pass
        i += 1
    foundElev(judet, cls, currentString)
# print(elevi)
