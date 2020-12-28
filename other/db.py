# Python-Sqlite cemetery database.
# this file will provide all backend functionalities for the databse-editing gui.
# table requirements: cemetery name (filename), headstone id (count or rng), row, col, headstone bbox-global coord (four-corners), headstone centroid.

import sqlite3
import re
import json
import pandas as pd
from csv import reader, writer

# change database name here, to apply functions to a different database.
cemetery = "cemetery.db"

# validate cemetery name before inserting into table.
def isValidCemetery(cemetery_name: str) -> bool:
    pattern = re.compile('^[a-zA-Z ]+$')
    if cemetery_name and re.match(pattern, cemetery_name):
        return True
    print("Cemetery name may only contain alphabetical characters or spaces.")
    return False

# validate headstone id before inserting into table.
def isValidID(id: str) -> bool:
    pattern = re.compile('^[0-9]+$')
    if id and re.match(pattern, id):
        return True
    print("Headstone ID may only consist of integers.")
    return False

# validate headstone row's and col's before inserting into table.
def isValidOrder(rc: str) -> bool:
    pattern = re.compile('^[0-9a-zA-Z -]+$')
    if rc and re.match(pattern, rc):
        return True
    print("Row's and Col's may only consist of integers or letters.")
    return False 

# validate headstone coordinates and centroid before inserting into table.
def isValidCoord(coord: str) -> bool:
    pattern = re.compile('^[+-]*[0-9]*[.][0-9]+$')
    if coord and re.match(pattern, coord):
        return True
    print("Coordinate may only consist of a proper floating point number.")
    return False

# validate whether input is a valid feature in table.
def isValidFeature(feature: str) -> bool:
    features = set(['id', 'row', 'col', 'toplx', 'toply', 'toprx', 'topry', 'botlx', 'botly', 'botrx', 'botry', 'centroidx', 'centroidy']) 
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

# NOTE: (not in use) get cemetery name, from yolo file or any other source.
def getCemeteryName(name: str) -> str:
    return name

# NOTE: (not in use) get table name, table name can be cemetery name.
def getTableName(name: str) -> str:
    return name

# NOTE: (input parameters might need changing) MAIN METHOD- populate table based on cemetery (enter filename and tablename, one-click create).
def populateTable(tablename: str, container: str) -> None:
    conn = sqlite3.connect(cemetery)
    c = conn.cursor()
    try:
        create = f'''CREATE TABLE IF NOT EXISTS {tablename} 
            (id INTEGER UNIQUE, row INTEGER, col INTEGER, 
            toplx FLOAT, toply FLOAT, toprx FLOAT, topry FLOAT, 
            botlx FLOAT, botly FLOAT, botrx FLOAT, botry FLOAT,
            centroidx FLOAT, centroidy FLOAT);'''
        c.execute(create)
    except conn.Error as e:
        conn.commit()
        conn.close()
        print(e)
        return
    except:
        conn.commit()
        conn.close()
        print("Unknown Error Occured")
        return
    for row in container:
        insert = f"INSERT OR REPLACE INTO {tablename} VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?);"
        c.execute(insert, row)
    conn.commit()
    conn.close()

# create a table, (enter table name, one-click add).
def createTable(tablename: str) -> None:
    conn = sqlite3.connect(cemetery)
    c = conn.cursor()
    try:
        create = f'''CREATE TABLE IF NOT EXISTS {tablename} 
            (id INTEGER UNIQUE, row INTEGER, col INTEGER, 
            toplx FLOAT, toply FLOAT, toprx FLOAT, topry FLOAT, 
            botlx FLOAT, botly FLOAT, botrx FLOAT, botry FLOAT,
            centroidx FLOAT, centroidy FLOAT);'''
        c.execute(create)
    except conn.Error as e:
        conn.commit()
        conn.close()
        print(e)
        return
    except:
        conn.commit()
        conn.close()
        print("Unknown Error Occured")
        return
    conn.commit()
    conn.close()

# delete an enitre table (enter table name, verify action, one-click delete).
def deleteTable(tablename: str) -> None:
    conn = sqlite3.connect(cemetery)
    c = conn.cursor()
    try:
        delete = f"DROP TABLE IF EXISTS {tablename};"
        c.execute(delete)
    except conn.Error as e:
        conn.commit()
        conn.close()
        print(e)
        return
    except:
        conn.commit()
        conn.close()
        print("Unknown Error Occured")
        return
    conn.commit()
    conn.close()

# add a table entry (enter tablename and all values in csv format).
def addEntry(tablename: str, id: int, row: int, col: int, toplx: float, toply: float, toprx: float, topry: float, botlx: float, botly: float, botrx: float, botry: float, centroidx: float, centroidy: float) -> None:
    #id, row, col, toplx, toply, toprx, topry, botlx, botly, botrx, botry, centroidx, centroidy = values.split(',')
    if not isValidID(id):
        return
    if not isValidOrder(row) or not isValidOrder(col):
        return 
    if not isValidCoord(toplx) or not isValidCoord(toply) or not isValidCoord(toprx) or not isValidCoord(topry) or not isValidCoord(botlx) or not isValidCoord(botly) or not isValidCoord(botrx) or not isValidCoord(botry) or not isValidCoord(centroidx) or not isValidCoord(centroidy):
        return
    conn = sqlite3.connect(cemetery)
    c = conn.cursor()
    try:
        add = f"INSERT OR REPLACE INTO {tablename} VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?);"
        c.execute(add, (id, row, col, toplx, toply, toprx, topry, botlx, botly, botrx, botry, centroidx, centroidy))
    except conn.Error as e:
        conn.commit()
        conn.close()
        print(e)
        return
    except:
        conn.commit()
        conn.close()
        print("Unknown Error Occured")
        return
    conn.commit()
    conn.close()

# edit a table entry based on headstone id (enter table name, headstone ID, and updated features (csv format), one-click edit).
def editEntry(tablename: str, id: int, row: int, col: int, toplx: float, toply: float, toprx: float, topry: float, botlx: float, botly: float, botrx: float, botry: float, centroidx: float, centroidy: float) -> None:
    #row, col, toplx, toply, toprx, topry, botlx, botly, botrx, botry, centroidx, centroidy = values.split(',')
    if not isValidID(id):
        return 
    if not isValidOrder(row) or not isValidOrder(col):
        return 
    if not isValidCoord(toplx) or not isValidCoord(toply) or not isValidCoord(toprx) or not isValidCoord(topry) or not isValidCoord(botlx) or not isValidCoord(botly) or not isValidCoord(botrx) or not isValidCoord(botry) or not isValidCoord(centroidx) or not isValidCoord(centroidy):
        return
    conn = sqlite3.connect(cemetery)
    c = conn.cursor()
    try:
        edit = f"UPDATE {tablename} SET row = ?, col = ?, toplx = ?, toply = ?, toprx = ?, topry = ?, botlx = ?, botly = ?, botrx = ?, botry = ?, centroidx = ?, centroidy = ? WHERE id = ?" 
        c.execute(edit, (row, col, toplx, toply, toprx, topry, botlx, botly, botrx, botry, centroidx, centroidy, id))
    except conn.Error as e:
        conn.commit()
        conn.close()
        print(e)
        return
    except:
        conn.commit()
        conn.close()
        print("Unknown Error Occured")
        return
    conn.commit()
    conn.close()

# delete a table entry based on headstone id (enter headstone id, verify action, one-click delete).
def deleteEntry(tablename: str, id: int) -> None:
    if not isValidID(id):
        return 
    conn = sqlite3.connect(cemetery)
    c = conn.cursor()
    try:
        delete = f"DELETE FROM {tablename} WHERE id = ?;" 
        c.execute(delete, (id,))
    except conn.Error as e:
        conn.commit()
        conn.close()
        print(e)
        return
    except:
        conn.commit()
        conn.close()
        print("Unknown Error Occured")
        return
    conn.commit()
    conn.close()

# search table entries by ID (enter ID range, provide a list of all results).
def searchTable(tablename: str, start_id: str, finish_id) -> list:
    if not isValidID(start_id) or not isValidID(finish_id):
        return
    conn = sqlite3.connect(cemetery)
    c = conn.cursor()
    try:
        search = f"SELECT * FROM {tablename} WHERE id BETWEEN ? AND ?;"
        c.execute(search, (start_id, finish_id))
    except conn.Error as e:
        conn.commit()
        conn.close()
        print(e)
        return
    except:
        conn.commit()
        conn.close()
        print("Unknown Error Occured")
        return
    entries = c.fetchall()
    result = []
    for entry in entries:
        result.append(entry)
    conn.commit()
    conn.close()
    return result

# view/order table with specified feature (enter feature to view specific entries, order view by specified feature)
def orderTable(tablename: str, feature: str, sort: str) -> list:
    if sort.lower() == "asc" or sort.lower() == "desc":
        pass
    else:
        print("Please enter 'asc' or 'desc' for order.")
        return
    if not isValidFeature(feature):
        return
    conn = sqlite3.connect(cemetery)
    c = conn.cursor()
    try:
        order = f"SELECT * FROM {tablename} ORDER BY {feature} {sort};"
        c.execute(order)
    except conn.Error as e:
        conn.commit()
        conn.close()
        print(e)
        return
    except:
        conn.commit()
        conn.close()
        print("Unknown Error Occured")
        return
    entries = c.fetchall()
    result = []
    for entry in entries:
        result.append(entry)
    conn.commit()
    conn.close()
    return result

# NOTE: (to be removed) csv and yolo txt file should have the same name, diff extension.
# edit yolo text file to update bboxes (as table is edited (time-consuming) or after editing (more efficient, one-click update)) (enter table corresponding to yolo text file).
def updateLabels(tablename: str, yolofile: str, csvfile: str) -> None:
    # To update the yolo files bboxes, we need to reverse the coordinates to pixel coordinates.
    return

# convert a pandas dataframe into gejson format.
def df_to_geojson(df, properties, toplx = 'toplx', toply = 'toply', toprx = 'toprx', topry = 'topry', botlx = 'botlx', botly = 'botly', botrx = 'botrx', botry = 'botry', centroidx = 'centroidx', centroidy = 'centroidy') -> dict:
    geojson = {'type':'FeatureCollection', 'name': getCemeteryName("Arlington"), 'features':[]}
    for _, row in df.iterrows():
        feature = {'type':'Feature', 'properties':{}, 'geometry':{'type':'MultiPolygon', 'coordinates':[]}}
        feature['geometry']['coordinates'] = [[[row[toplx], row[toply]],[row[toprx], row[topry]], [row[botlx], row[botly]], [row[botrx], row[botry]], [row[toplx], row[toply]]]]
        for prop in properties:
            if prop == 'id' or prop == 'row' or prop == 'col':
                feature['properties'][prop] = int(row[prop])
            elif prop == 'centroid':
                feature['properties'][prop] = [row[centroidx], row[centroidy]]
            else:
                feature['properties'][prop] = row[prop]
        geojson['features'].append(feature)
    return geojson

# (complete) store entries in a pandas dataframe, export table to geojson file (one-click export).
def exportTable(tablename: str) -> None:
    output_filename = tablename + '.geojson'
    conn = sqlite3.connect(cemetery)
    try:
        df = pd.read_sql_query(f"SELECT * FROM {tablename}", conn)
    except conn.Error as e:
        conn.commit()
        conn.close()
        print(e)
        return
    except:
        conn.commit()
        conn.close()
        print("Unknown Error Occured")
        return
    conn.commit()
    conn.close()
    properties = ['id', 'row', 'col', 'centroid']
    geojson = df_to_geojson(df, properties)
    with open(output_filename, 'w') as output_file:
        json.dump(geojson, output_file, indent = 2)

# test functions.
# print(isValidCemetery("ce"))
# print(isValidID("0099887"))
# print(isValidOrder("1000"))
# print(isValidCoord("-000006.7"))
# print(createTable("test"))
# print(populateTable("test.csv", "test"))
# print(addEntry("test", "119887,17,23,+11.1999000456789,-10.1123123123123,-23.2000111111111,+32.21112229907,-03.3333333333333,+3.3333333333333,-41.477777777777790,-4.47777777779990,50.660606060606060,5.660606060606060"))
# print(addEntry("test", "5,17,23,+11.1999000456789,-10.1123123123123,-23.2000111111111,+32.21112229907,-03.3333333333333,+3.3333333333333,-41.477777777777790,-4.47777777779990,50.660606060606060,5.660606060606060"))
# print(addEntry("test", "105,17,23,+11.1999000456789,-10.1123123123123,-23.2000111111111,+32.21112229907,-03.3333333333333,+3.3333333333333,-41.477777777777790,-4.47777777779990,50.660606060606060,5.660606060606060"))
# print(editEntry("test", "0099887", "16,22,+11.1999000456789,-10.1123123123123,-23.2000111111111,+32.21112229907,-03.3333333333333,+3.3333333333333,-41.477777777777790,-4.47777777779990,50.660606060606060,5.660606060606060"))
# print(deleteEntry("test", "1111111"))
# print(searchTable("test", "1", "10"))
# print(orderTable("test", "id", "DESC"))
# print(orderTable("test", "id", "ASC"))
# print(exportTable("test"))
