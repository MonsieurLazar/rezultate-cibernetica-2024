from PyPDF2 import PdfReader, PdfWriter


reader = PdfReader("rezultate.pdf")
number_of_pages = len(reader.pages)

number_of_pages = number_of_pages - 1

writer = None
judete = []
for i in range(number_of_pages):
    page = reader.pages[i]
    text = page.extract_text()
    judetIndex = text.find("Județul")
    isMunicipiu = False
    if(judetIndex == -1):
        judetIndex = text.find("Municipiul")
        if(judetIndex != -1):
            isMunicipiu = True

    if(judetIndex != -1):
        if writer is not None:
            with open(f"./data/{judetName}.pdf", "wb") as output_pdf:
                writer.write(output_pdf)
                
        judetName = text[judetIndex+8:judetIndex+8+text[judetIndex+8:].find(" ")]
        if(isMunicipiu):
            judetName = text[judetIndex+11:judetIndex+11+text[judetIndex+11:].find(" ")]
        if(judetName != ""):
            judete.append(judetName)
           
        
        writer = PdfWriter()
        
    if writer is not None:
        writer.add_page(page)

if writer is not None:
    with open(f"./data/{judetName}.pdf", "wb") as output_pdf:
        writer.write(output_pdf)

import os
os.remove("data/.pdf")

print(judete)
elevi = []
def getText(reader, pageNumber):
    page = reader.pages[pageNumber]
    text = page.extract_text()
    if(pageNumber == 0):
        cybereduIndexes = [i for i in range(len(text)) if text.startswith("CyberEDU", i)][1]
        workingText = text[cybereduIndexes+8:]
        return workingText
    firstIndex = text.find("/")

    workingText = text[firstIndex+5:]
    return workingText

for judet in judete:
    reader = PdfReader(f"./data/{judet}.pdf")
    number_of_pages = len(reader.pages)
    print("Opened " + judet + ".pdf with " + str(number_of_pages) + " pages.")
    for i in range(number_of_pages):
        page = reader.pages[i]
        print("Opened page " + str(i) + " from " + judet + ".pdf. Extracting text...")
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
            if(cls == "Unknown"): return
            print("Clasa " + str(cls))
            isAbsent = currentString.find("absent") != -1
            currentElev["absent"] = isAbsent
            if(isAbsent):
                print("Elev absent")
                return
            separatedString = currentString.split(" ")
            separatedString = list(filter(lambda a: a != '', separatedString))
            separatedString = list(filter(lambda a: a != '\nX', separatedString))
            if(len(separatedString) < 8):
                print("Elevul " + separatedString[1] + " are " + str(len(separatedString)) + " elemente.")
                print(separatedString)
                return
            rank = separatedString[0]
            id = separatedString[1].replace("\n", "") + separatedString[2].replace("\n", "")
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
    
    
# write the elevi to a file
import json
with open("./output/elevi.json", "w") as f:
    json.dump(elevi, f)

# sort elevi into separated classes and write them to a file
clase = {
    "IX": [],
    "X": [],
    "XI": [],
    "XII": []
}
for elev in elevi:
    if(elev["clasa"] in clase):
        clase[elev["clasa"]].append(elev)
    else:
        print("Elevul " + elev["id"] + " nu are clasa.")

# loop through classes key
for clasa in clase:
    with open(f"./output/{clasa}.json", "w") as f:
        json.dump(clase[clasa], f)
    clasaData = clase[clasa]
    clasaData = list(filter(lambda elev: float(elev["punctaj"]) >= 40.0, clasaData))
    clasaData = sorted(clasaData, key=lambda elev: elev["punctaj"], reverse=True)
    number_of_elevi = len(clasaData)
    print(f"Clasa {clasa} has {number_of_elevi} students.")
    with open(f"./output/{clasa}_40.json", "w") as f:
        json.dump(clasaData, f)