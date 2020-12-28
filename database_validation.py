import re


def validate_cemetery_name(cemetery_name: str) -> bool:
    pattern = re.compile('^[a-zA-Z ]+$')
    if cemetery_name and re.match(pattern, cemetery_name):
        return True
    print("Cemetery name may only contain alphabetical characters or spaces.")
    return False


def isValidCemetery(cemetery_name: str) -> bool:
    pattern = re.compile('^[a-zA-Z ]+$')
    if cemetery_name and re.match(pattern, cemetery_name):
        return True
    print("Cemetery name may only contain alphabetical characters or spaces.")
    return False


# validate headstone id before inserting into table.
def isValidID(id: int) -> bool:
    pattern = re.compile('^[0-9]+$')
    return True
    if id and re.match(pattern, str(id)):
        return True
    print("Headstone ID may only consist of integers.")
    return False


# validate headstone row's and col's before inserting into table.
def isValidOrder(rc: int) -> bool:
    return True
    pattern = re.compile('^[0-9a-zA-Z -]+$')
    if rc and re.match(pattern, str(rc)):
        return True
    print("Row's and Col's may only consist of integers or letters.")
    return False


# validate headstone coordinates and centroid before inserting into table.
def isValidCoord(coord: float) -> bool:
    pattern = re.compile('^[+-]*[0-9]*[.][0-9]+$')
    if coord and re.match(pattern, str(coord)):
        return True
    print("Coordinate may only consist of a proper floating point number.")
    return False


# validate whether input is a valid feature in table.
def isValidFeature(feature: str) -> bool:
    features = {'id', 'row', 'col', 'toplx', 'toply', 'toprx', 'topry', 'botlx', 'botly', 'botrx', 'botry', 'centroidx',
                'centroidy'}
    if feature and feature in features:
        return True
    print("Feature is not a valid feature in table.")
    return False


# validate whether input is a valid geojson file type.
def isValidGeoJSON(filename: str) -> bool:
    pattern = re.compile('^[a-zA-Z0-9 -_]+.geojson$')
    if filename and re.match(pattern, filename):
        return True
    print("File name format is incorrect.")
    return False


# NOTE: (might not need when deployed) validate csv file.
def isValidCSV(filename: str) -> bool:
    pattern = re.compile('^[a-zA-Z0-9 -_]+.csv$')
    if filename and re.match(pattern, filename):
        return True
    print("File is not a CSV file.")
    return False


# NOTE: (might not need when deployed) validate yolo txt file.
def isValidTXT(filename: str) -> bool:
    pattern = re.compile('^[a-zA-Z0-9 -_]+.txt$')
    if filename and re.match(pattern, filename):
        return True
    print("File is not a TXT file.")
    return False
