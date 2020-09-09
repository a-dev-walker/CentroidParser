# CentroidParser
Scripts for analyzing Phox2B positivity

These files are used in the following paper:


Python code was written in python 3.7 and using dependencies found within the base installation of anaconda
https://www.python.org/downloads/release/python-370/

https://docs.anaconda.com/anaconda/install/

Groovy code was written and executable in the editor of Qupath0.2.0-m12

https://github.com/qupath/qupath/releases



Instructions for use:

1. Import digital slide images into Qupath
2. Use "Phox2BPosCellDetectionTest.groovy" to determine positive cells on current slide

        2.1 Before running script, make sure to change output directory (line 9) to desired directory on user's file system
3. Convert resulting .txt file to .csv using excel
4. Run "Centroid_Parser_Publish.py" with the .csv as input
5. Using the output of Centroid_Parser replace the first two lines of"ROI_placement.groovy" as indicated by comments
6. Select newly created circle annotation and observe %pos in bottom left of application
