import os
import shutil

# Generate the output file based on the template chosen
def generateOutputFile(template, output):
    # Get the current directory
    currentDir = os.getcwd()

    try:
        # Get the source template
        sourceFile = os.path.join(currentDir, "templates" , template)

        # Combine the current directory and the new file name to get the full path of the output file
        outputFile = os.path.join(currentDir, output)

        # Copy the file to the current directory and rename it
        shutil.copy2(sourceFile, outputFile)
    except IOError:
        print("(generateOutputFile) Unable to open file.")

    return outputFile

# Insert element into output file based on source file path
def insertElement(sourceFilePath, outputFilePath, elementToInsert, beforeElement):
    try:
        # Open source file to extract element and all its containing data
        with open(sourceFilePath, 'r', encoding='utf-8') as sourceFile:
            sourceHtml = sourceFile.read()

            # Get the start and end index of the element
            startIndex = sourceHtml.index(f'<{elementToInsert}>')
            endIndex = sourceHtml.index(f'</{elementToInsert}>', startIndex) + len(f'</{elementToInsert}>')

            # Extract the element from the source HTML
            elementHtml = sourceHtml[startIndex:endIndex]+"\n"
            sourceFile.close()

        # Open output file to insert element
        with open(outputFilePath, 'r+', encoding='utf-8') as outputFile:
            # Read the contents of the output file
            outputHtml = outputFile.read()

            # Find the index of the element that is after what is meant to be inserted
            startIndex = outputHtml.index(f'<{beforeElement}>')

            # Insert the data before the element
            outputHtml = outputHtml[:startIndex] + elementHtml + outputHtml[startIndex:]

            # Write the modified HTML to the output file
            outputFile.seek(0) 
            outputFile.write(outputHtml)
            outputFile.truncate()  # Remove any remaining content after the new data

            print(f"Element '{elementToInsert}' added to '{outputFilePath}'")
            outputFile.close()

    except IOError:
        print("(insertElement) Unable to open file.")

# To insert data into an HTML element in a file.
def insertDataIntoElement(element, dataInsert, filePath):
    # Flag to track if the element is found in the input file
    lineFound = False
    try:
        # Open the input file and read all lines into a list
        with open(filePath, 'r+', encoding='utf-8') as file:
            lines = file.readlines()

            # Look for the specified element in the lines and add the data to it
            for i in range(len(lines)):
                if element.lower() in lines[i].lower():
                    print(f"Adding line {dataInsert} to file after element {element}")
                    lines[i] = lines[i].replace(f"<{element}>", f"<{element}>{dataInsert}")
                    lineFound = True
                    break
            
            # If the specified element was found in the input file, write the modified lines to the output file
            if lineFound:
                file.seek(0)
                file.writelines(lines)
            # If the specified element was not found in the input file, print an error message
            else:
                print(f"Element '{element}' not found in file {filePath}")
            file.close()
                
    # If there was an error opening the input file, print an error message
    except IOError:
        print("(insertDataIntoElement) Unable to open file.")

if __name__ == '__main__':
    template = "AdminLoginPageTemplate.html"
    sourceFilePath = "source.html"
    # Generate output file first based on template file
    outputfile = generateOutputFile(template, "output.html")

    # Add head to output file, placed before <body>
    insertElement(sourceFilePath,outputfile,"head","body")

    # Add header to output file, placed before <main>
    insertElement(sourceFilePath,outputfile,"header","main")


    # Add footer to output file, placed before </body>
    insertElement(sourceFilePath,outputfile,"footer","/body")

    print (f"Output file generated. File name: {outputfile}")