# LegacyNet
Cemetery Drone Image Analysis (UCF Award Best In Show)

Sponsored under the U.S. Department of Veteran Affairs, by the National Cemetery Administration.

LegacyNet is a program, written in Python3, that takes an aerial image of a cemetery (tif file with global coordinates)
and uses machine learning to detect all gravestones in the image. Once the gravestones are detected,
the program automatically calculates the coordinates of each gravestone and writes all the information
to a database (SQLite3). The program also allows for the information in the database to be exported to a 
GeoJSON file for other uses.
All these features and functinoalities are used through a GUI, created using PyQt5. The GUI displays the 
cemetery image and allows the user to run an inference on the image using a machine learning model. Once all 
the gravestones are detected, the user can then add, delete, edit, rotate, and select each detection as they please.
The user can then export the gravestones to the database, and from database export to GeoJSON.

This program does in seconds what use to take a person weeks to complete. This process required manually creating 
polygons for each individual gravestone (hundreds to thousands per image), then manually calculating the coordinates
for each corner of each polygon. The task of populating a database has also been automated.
