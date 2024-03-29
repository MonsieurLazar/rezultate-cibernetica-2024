import json
import os
from PyPDF2 import PdfReader, PdfWriter


# create the data folder
if not os.path.exists("./data"):
    os.makedirs("./data")
# create output folder
if not os.path.exists("./output"):
    os.makedirs("./output")

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
    if judetIndex == -1:
        judetIndex = text.find("Municipiul")
        if judetIndex != -1:
            isMunicipiu = True

    if judetIndex != -1:
        judetName = text[judetIndex+8:text.find("\n", judetIndex)]
        judetName = judetName.replace(" ", "")
        judetName = judetName.replace("  ", "")

        if isMunicipiu:
            judetName = text[judetIndex+11:text.find("\n", judetIndex)]
        if judetName != "":
            judete.append(judetName)
            writer = PdfWriter()
            writer.add_page(page)
            with open(f"./data/{judetName}.pdf", "wb") as output_pdf:
                writer.write(output_pdf)
        else:
            if writer is not None:
                writer.add_page(page)
                with open(f"./data/{judetName}.pdf", "wb") as output_pdf:
                    writer.write(output_pdf)

    else:
        if writer is not None:
            writer.add_page(page)
            with open(f"./data/{judetName}.pdf", "wb") as output_pdf:
                writer.write(output_pdf)

print(judete)
elevi = []


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


for judet in judete:
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

# sort elevi by punctaj
elevi = sorted(elevi, key=lambda elev: elev["punctaj"], reverse=True)
# names
# loop thorugh elevi and fix unicode caracters in judet like  'ă', 'â', 'ș', 'ț'
for elev in elevi:
    judet = elev["judet"]
    judet = judet.replace("ă", "a")
    judet = judet.replace("â", "a")
    judet = judet.replace("ș", "s")
    judet = judet.replace("ț", "t")
    elev["judet"] = judet


def getName(id):
    import requests
    url = "https://api.cyber-edu.co/v1/user/" + id
    response = requests.get(url)
    print(response.text)
    return response.json()["name"]


# get the names of the students
maxElevi = len(elevi)
currentIndex = 0
for elev in elevi:
    currentIndex += 1
    print("Getting name for " + elev['id'] + "...")
    elev["nume"] = getName(elev["id"])
    print(f"Got name for {elev['id']} as {
          elev['nume']}. {currentIndex}/{maxElevi}")


# write the elevi to a file
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
    if (elev["clasa"] in clase):
        clase[elev["clasa"]].append(elev)
    else:
        print("Elevul " + elev["id"] + " nu are clasa.")

# loop through classes key
for clasa in clase:
    with open(f"./output/{clasa}.json", "w") as f:
        json.dump(clase[clasa], f)
    clasaData = clase[clasa]
    clasaData = list(filter(lambda elev: float(
        elev["punctaj"]) >= 40.0, clasaData))
    clasaData = sorted(
        clasaData, key=lambda elev: elev["punctaj"], reverse=True)
    number_of_elevi = len(clasaData)
    print(f"Clasa {clasa} has {
          number_of_elevi} / {len(clase[clasa])} students.")
    with open(f"./output/{clasa}_40.json", "w") as f:
        json.dump(clasaData, f)


def getJudetName(judet):
    judet = judet.replace("ă", "a")
    judet = judet.replace("â", "a")
    judet = judet.replace("ș", "s")
    judet = judet.replace("ț", "t")
    return judet


for judet in judete:
    claseJud = {
        "IX": [],
        "X": [],
        "XI": [],
        "XII": []
    }
    totiElevii = []
    for elev in elevi:
        if (getJudetName(elev["judet"]) == getJudetName(judet)):
            totiElevii.append(elev)
            if (elev["clasa"] in claseJud):
                claseJud[elev["clasa"]].append(elev)
            else:
                print("Elevul " + elev["id"] + " nu are clasa.")
    with open(f"./data/{judet}.json", "w") as f:
        json.dump(totiElevii, f)
    for clasa in claseJud:
        with open(f"./data/{judet}_{clasa}.json", "w") as f:
            json.dump(claseJud[clasa], f)
        clasaData = claseJud[clasa]
        clasaData = list(filter(lambda elev: float(
            elev["punctaj"]) >= 40.0, clasaData))
        clasaData = sorted(
            clasaData, key=lambda elev: elev["punctaj"], reverse=True)
        number_of_elevi = len(clasaData)
        print(f"Clasa {clasa} from {judet} has {
              number_of_elevi} / {len(claseJud[clasa])} students.")
        with open(f"./data/{judet}_{clasa}_40.json", "w") as f:
            json.dump(clasaData, f)
