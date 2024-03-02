from PyPDF2 import PdfReader, PdfWriter
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

reader = PdfReader("./data/București.pdf")
number_of_pages = len(reader.pages)
print("Page 0: ")
print(getText(reader, 0))
print("Page 1: ")
print(getText(reader, 0))


