# LegacyNet User Interface

This project was created by UCF CS Senior Design Group 6 during the Fall 2020 Semester.
It was designed to automate the tedious process of mapping headstone locations by hand.
This program uses machine learning to detect visible headstones in a TIFF image,
and calculates the latitude and logitude of each headstone automatically based on the associated world file.
The user can then export this data to GeoJSON format and into a SQLite database.

This project won Best in Show in the Fall 2020 UCF Senior Design Showcase.

Created by:
Alec Kerrigan, Nick Evans, Maleah Jamieson, Grant Mullinax, Nicolas Soto

Sponsored by: Dr. Amy Giroux

## Installation

The `environment.yml` file is the exported conda environment that we used to run the application. To install:

```shell
conda env create --file LegacyNet.yml
```
This will create a new environment named LegacyNet, and will begin installing all the required dependencies.

## Usage

### To run the program:

```shell
conda activate LegacyNet
cd [path_to_LegacyNet_folder]
python main.py
```

### Application Shortcuts

Line Select: `SHIFT` + `LEFT MOUSE CLICK/DRAG`

With multiple headstones selected, you can update row, col, and rotation of all the selected headstones.

### Steps to Use Application:
1. Click Load Image to select TIFF image (with associated world file in the same folder).

2. If you have an already existing database, open it now using Open Database.

3. If you selected an existing database, you can select a table from which to import headstone markings
(when marking an image you have already worked on).

4. If you did not have an existing database, or if this is a new image,
press Detect in the bottom left to start the headstone detection process.

5. Create Box to mark any headstones missed during detection.

6. Make any changes to existing boxes by left clicking on them and moving the vertices.

7. Update row and column by selecting headstones, changing the values in the top right, and clicking Update.

8. Update rotation by pressing the rotation button and inputting the degrees to rotate.

9. Export Table will save your changes in the SQLite database. If you did not open a database, it will prompt
to create a new one along with the table to populate.

10. Export Geojson will export your work to `.geojson` format.

## Making Changes

### Headstone Detection

If the headstone detection is not up to par, within `config.ini` you can change a few model parameters.

The confidence threshold (how confident the model is that what it marked is a headstone) default we set is 
`confidence_threshold = 0.45`. Higher numbers will decrease the number of false positives but also may decrease the
number of actual headstones marked depending on how well the model worked for a particular image.

The intersection over union threshold was our solution to the situation where bounding boxes overlap each other
(where the model would detect the same headstone as multiple headstones). The default we set for this is
`iou_threshold = 0.15`. Higher numbers mean boxes need to overlap more to be discarded.

If you choose to train a different model, you can change which exported model is used by editing
`saved_model_path = ml/final_trained_model/saved_model`.The final trained model is our version of the model
trained on an Azure box, which allows for a larger batch size and better optimization for the model detections.

### Coordinate Calculation

This can be found in `coordmap.py`.

The formulas come from this site: http://webhelp.esri.com/arcims/9.3/General/topics/author_world_files.htm

The `pixel_map` function uses the information from the world file and the coordinates 
to determine the pixel location of the object.

The `coordinate_map` function uses the information from the world file and pixel location
to determine the coordinates of an object.
