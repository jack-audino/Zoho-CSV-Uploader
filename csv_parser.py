import csv

# list of keywords used to identify titles in a csv file
KEYWORDS = [
    'first name',
    'last name',
    'email',
    'company',
    'phone',
    'mobile',
    'cell',
    'fax',
    'position',
    'title',
    'street',
    'state',
    'country',
    'city',
    'zip code',
    'website',
    'description'
]

class CSVParser():
    __slots__ = ['__filename', '__parsed', '__titleLineNum']

    def __init__(self, filename):
        self.__filename = filename
        self.__parsed = list() # this will end up looking like the record_list example in insert_lead.py

        # create a new reader and find the line of the first matching keyword, i.e. the title line
        with open(self.__filename) as f:
            titleLineFinder = csv.reader(f)

            for row in titleLineFinder:
                if row[0].lower() in KEYWORDS:
                    self.__titleLineNum = titleLineFinder.line_num
                    break

    # helper function used to skip a set amount of rows with a given reader, since line_num in the csv class is read-only
    def row_skipper(self, reader: csv.reader, numOfRows):
        for i in range(numOfRows):
            next(reader)    

    # finds each title, then adds it to a dict which will be returned as a template that populate_dict() will add each row to
    def find_all_titles(self):
        foundTitlesList = list()

        with open(self.__filename) as f:
            titleFinder = csv.reader(f)

            # skip to the title line so the whitespace at the top isn't added, the title line is not needed now, hence the - 1
            self.row_skipper(titleFinder, (self.__titleLineNum - 1))

            for row in titleFinder:
                for word in row:
                    col = row.index(word) # this is set equal to col for reading and understanding's sake, it's just the current column of the title line
                    title = row[col] # this is the current cell
                    lowerCaseTitle = title.lower()
                    lowerCaseTitleArray = lowerCaseTitle.split(' ')

                    if lowerCaseTitle in KEYWORDS:
                        foundTitlesList.append(title.replace(' ', '_')) # can't use lowerCaseTitle since it will add improperly-formatted data which will stop the upload from occurring

                    else:
                        for i in range(len(lowerCaseTitleArray)):
                            if lowerCaseTitleArray[i] in KEYWORDS: # if the lowercase-converted title is in the KEYWORDS list (every item in KEYWORDS should be all lowercase), then add it
                                # check for specific words so that they are properly added to the list, otherwise, just replace the space in the phrase with an underscore
                                # also check if a word has been added to foundTitlesList to stop repeats
                                if ('email') in lowerCaseTitleArray[i]:
                                    foundTitlesList.append('Email')
                                    break

                                elif ('phone') in lowerCaseTitleArray[i]:
                                    foundTitlesList.append('Phone')
                                    break
                                
                                elif ('fax') in lowerCaseTitleArray[i]:
                                    foundTitlesList.append('Fax')
                                    break
                                
                                elif ('mobile') in lowerCaseTitleArray[i] or ('cell') in lowerCaseTitleArray[i]: 
                                    foundTitlesList.append('Mobile')
                                    break

                                elif ('position') in lowerCaseTitleArray[i] or ('title') in lowerCaseTitleArray[i]:
                                    foundTitlesList.append('Designation') # this is 'Title' when looking at individual lead pages in Zoho, but for the API, it needs to be changed to 'Designation' (this is unfortunately not easy to find in the documentation)
                                    break                               

                break # have to add this break here otherwise it will continue to go through every row in the csv, only the title row is needed
        
        return foundTitlesList

    # return columns as lists for find_nonempty_cols() to check
    def read_col(self, columnNumber):
        colAsList = list()

        with open(self.__filename) as f:
            colReader = csv.reader(f)

            # skip to the title line so the whitespace at the top isn't checked, only the title line is needed since the title that each column belongs to needs to be determined in find_nonempty_cols()
            self.row_skipper(colReader, self.__titleLineNum - 1)

            for row in colReader:
                for cell in row:
                    colAsList.append(row[columnNumber])
                    break

        return colAsList

    # reads through each column list from find_all_titles() using read_col()
    def find_nonempty_cols(self, titleTemplate: list):
        listOfCols = list()
        titlesRemoved = 0

        with open(self.__filename) as f:
            emptyColFinder = csv.reader(f)
            # skip the whitespace at the top, only the title line is needed because if it's skipped, then it causes titles to become duplicated when parsing improperly-formatted csv files
            self.row_skipper(emptyColFinder, self.__titleLineNum - 1)

            for row in emptyColFinder:
                for cell in row:
                    currentCol = self.read_col(row.index(cell)) # read the current column, where row.index(cell) is the current column number, starting at 0

                    emptyCellCount = 0
                    for i in range(len(currentCol)): # count the number of empty cells in the column
                        if currentCol[i] == '':
                            emptyCellCount += 1
                    
                    if emptyCellCount == len(currentCol): # if the column is completely empty, skip it
                        continue
                    if emptyCellCount == (len(currentCol) - 1) and currentCol[0] in titleTemplate: # if the column is completely empty except for the title, then it should be skipped, and the title should be removed from titleTemplate
                        titleTemplate.pop(row.index(cell) - titlesRemoved) # have to use row.index(cell) as the index to pop from since it is being called from within the 'for cell in row' loop
                        titlesRemoved += 1
                        continue
                    else: # if it's not completely empty and not just a title, add it to the list of cols
                        listOfCols.append(currentCol[1:len(currentCol)]) # add everything except the title to the list of columns
                break # only one copy of each column is needed, so it should break out of the loop after one iteration
            
        return listOfCols, titleTemplate

    # use the list from find_all_titles() and the list from find_nonempty_cols() to add each column list to each title key 
    def populate_dict(self, colList: list, titleTemplate: list):
        # make a base dictionary from titleTemplate to be used each for each iteration
        baseDict = dict()
        for i in range(len(titleTemplate)):
            baseDict.update({titleTemplate[i]: None})
        
        # populate each baseDict iteration, add it to "__parsed", clear it, and continue
        for i in range(len(colList[0])): # iterate through every value in the list of names (the first list in the list of columns), since it is extremely unlikely for a lead to not have a first name
            dictCopy = baseDict.copy() # create a new dict copy for every iteration (update(), setdefault(), and clear() work strangely with for loops, so a new dict is needed for every iteration unfortunately)
            for j in range(len(dictCopy)): # iterate through the title template and add it, along with each value in the colList, to the dictCopy
                if colList[j][i] == '': # if the current value is empty, then don't add it and remove the title from the dictCopy (i.e. it would remove a dict value like Email: '')
                    dictCopy.pop(titleTemplate[j])
                    continue
                else:
                    dictCopy.update({titleTemplate[j]: colList[j][i]})
            self.__parsed.append(dictCopy) # once the temporary dictionary is complete, add it to the "__parsed" list

    # similar to a main function, by calling this, everything needed in the CSVParser class is called, and it will return a list of all of the leads
    def parse(self):
        columnList, titleTemplate = self.find_nonempty_cols(self.find_all_titles())
        self.populate_dict(columnList, titleTemplate)

    # a simple get method in case the parsed information is needed later
    def get_parsed(self):
        return self.__parsed