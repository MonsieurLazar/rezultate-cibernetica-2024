from PyPDF2 import PdfReader, PdfWriter


# reader = PdfReader("rezultate.pdf")
# number_of_pages = len(reader.pages)
# print(number_of_pages)

# writer = None

# for i in range(number_of_pages):
#     page = reader.pages[i]
#     text = page.extract_text()
#     judetIndex = text.find("Județul")
#     if(judetIndex != -1):
#         if writer is not None:
#             with open(f"./data/{judetName}.pdf", "wb") as output_pdf:
#                 writer.write(output_pdf)
                
#         judetName = text[judetIndex+8:judetIndex+8+text[judetIndex+8:].find(" ")]
#         print(judetName)
        
#         writer = PdfWriter()
        
#     if writer is not None:
#         writer.add_page(page)

# for i in range(number_of_pages):
#     page = reader.pages[i]
#     text = page.extract_text()
#     judetIndex = text.find("Municipiul")
#     if(judetIndex != -1):
#         if writer is not None:
#             with open(f"./data/{judetName}.pdf", "wb") as output_pdf:
#                 writer.write(output_pdf)
                
#         judetName = text[judetIndex+11:judetIndex+11+text[judetIndex+11:].find(" ")]
#         print(judetName)
        
#         writer = PdfWriter()
        
#     if writer is not None:
#         writer.add_page(page)

# if writer is not None:
#     with open(f"./data/{judetName}.pdf", "wb") as output_pdf:
#         writer.write(output_pdf)

# import os
# os.remove("data/.pdf")


# reader = PdfReader("./data/Alba.pdf")
# number_of_pages = len(reader.pages)
# print(number_of_pages)

# page = reader.pages[0]
# text = page.extract_text()
# cybereduIndexes = [i for i in range(len(text)) if text.startswith("CyberEDU", i)][1]
# print(cybereduIndexes)
# workingText = text[cybereduIndexes+8:]
# workingText = workingText.split()
# workingText = [workingText[i:i+10] for i in range(0, len(workingText), 10)]
# print(workingText)



reader = PdfReader("./data/București.pdf")
number_of_pages = len(reader.pages)

page = reader.pages[3]
text = page.extract_text()
# print(text)

# find first instance of /

firstIndex = text.find("/")
# print other text

workingText = text[firstIndex+5:]
print(workingText)
# write it to a file
with open("output.txt", "w") as file:
    file.write(workingText)
# split it by the separator chars and print it
# separatorChars = ['IX', 'X', 'XI', 'XII']
# import re

# # Constructing the regular expression pattern
# pattern = '|'.join(separatorChars)

# # Splitting the data using the pattern
# sections = re.split(pattern, workingText)

# # Cleaning up the sections
# sections = [section.strip() for section in sections if section.strip()]

# # Printing the separated sections
# for i, section in enumerate(sections, 1):
#     # remove break lines
#     section = section.replace("\n", " ")
#     isAbsent = section.find("absent") != -1
#     # separate it by spaces
#     section = section.split(" ")
#     # REMOVE EMPTY STRINGS
#     section = list(filter(lambda a: a != '', section))

#     # if(len(section) == 9):

        



#     # if(len(section) != 9 and not isAbsent):
#     print(f"Section {i}:\n{section}\n")

separatorChars = ['IX', 'X', 'XI', 'XII']

workingLength = len(workingText)

# loop through the text

def foundElev(cls, currentString):
    print("Clasa " + str(cls))
    isAbsent = currentString.find("absent") != -1
    if(isAbsent):
        print("Elev absent")
        return
    separatedString = currentString.split(" ")
    separatedString = list(filter(lambda a: a != '', separatedString))
    separatedString = list(filter(lambda a: a != '\nX', separatedString))
    if(len(separatedString) != 8):
        return
    rank = separatedString[0]
    id = separatedString[1].replace("\n", "") + separatedString[2].replace("\n", "")
    punctaj = separatedString[3]
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
        foundElev(cls, currentString)
        currentString = ""
        i += 1
        cls = currentChar
        # clasa 10
        pass
    # print(current2CharsWith2After)
    if (current2CharsWith2After in separatorChars) and (current3CharsWith3After not in separatorChars):
        foundElev(cls, currentString)
        currentString = ""
        i += 2
        cls = current2CharsWith2After
        # clasa 9, 11
        pass
    # print(current3CharsWith3After)
    if (current3CharsWith3After in separatorChars):
        foundElev(cls, currentString)
        currentString = ""
        i += 3
        cls = current3CharsWith3After
        # clasa 12
        pass
    i += 1
foundElev(cls, currentString)