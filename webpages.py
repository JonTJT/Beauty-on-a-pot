import os
import shutil
from bs4 import BeautifulSoup


def generateOutputFile(template, output, sourceFile=None):
    try:
        if sourceFile:
            shutil.copy2(sourceFile, output)
        else:
            shutil.copy2(template, output)

    except IOError:
        print("(generateOutputFile) Unable to open file.")
        return None

    return output


def extractElement(htmlFilePath, element):
    try:
        with open(htmlFilePath, 'r', encoding='utf-8') as htmlFile:
            soup = BeautifulSoup(htmlFile.read(), 'html.parser')
            mainElement = soup.find(element)
            if mainElement:
                return str(mainElement)

    except IOError:
        print(f"Unable to open file {htmlFilePath}.")
    
    return None


def insertOrReplaceElement(outputFilePath, elementToInsertTag, afterElementTag, elementData):
    try:
        # Decode the element data
        elementData = BeautifulSoup(elementData, 'html.parser')

        # Open output file to insert element
        with open(outputFilePath, 'r+', encoding='utf-8') as outputFile:
            # Read the contents of the output file
            outputHtml = outputFile.read()

            # Create a BeautifulSoup object
            soup = BeautifulSoup(outputHtml, 'html.parser')

            # Find the element to insert after
            afterElement = soup.find(afterElementTag)

            # Find the element that to be inserted
            insertElement = soup.find(elementToInsertTag)

            # If the element to insert is not found, insert the new element after the "afterElement"
            if (not insertElement) and afterElement:
                afterElement.insert_after(elementData)
                print("Element inserted after header.")
            # If element to insert is not found and no "afterelement", insert into the body.
            elif not insertElement:
                soup.find('body').insert_after(elementData)
                print("Element inserted after body.")
            # If the element is found, replace the new element at the end of the body
            else:
                insertElement.replace_with(elementData)
                print("Element replaced.")
                
            # Write the modified HTML to the output file
            outputFile.seek(0)
            outputFile.write(str(soup))
            outputFile.truncate()

            print(f"Element '{elementToInsertTag}' added to '{outputFilePath}'")
            
    except IOError:
        print("(insertElement) Unable to open file.")


def generateHoneypotPage(template, sourceFilePath, outputFile):
    try:
        # Get the current directory
        currentDir = os.getcwd()

        # Get the source template
        templateFile = os.path.join(currentDir, "templates", template)

        # Combine the current directory and the new file name to get the full path of the output file
        outputFile = os.path.join(currentDir, outputFile)

        # Generate output file first based on template file
        outputfile = generateOutputFile(templateFile, outputFile, sourceFilePath)

        # Extract the main element from the template file
        templatemain = extractElement(templateFile, 'main')

        # Add main to output file, placed before footer if main is not present.
        insertOrReplaceElement(outputfile, "main", "header", templatemain)
    
    except IOError:
        print("IO Exception: Unable to generate output file.")

if __name__ == '__main__':
    template = "SecretSearchPage.html"
    sourceFilePath = "source.html"
    outputFile = "output.html"

    generateHoneypotPage(template, sourceFilePath, outputFile)
