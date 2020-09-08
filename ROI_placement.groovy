double xCent = 28173.6    //x coordinate from python script
double yCent = 3830       //y coordinate from python script

import qupath.lib.objects.PathObjects
import qupath.lib.roi.ROIs
import qupath.lib.regions.ImagePlane

int z = 0
int t = 0
def plane = ImagePlane.getPlane(z, t)
def server = getCurrentServer()
def cal = server.getPixelCalibration()

// Scale the values
double pixelScale = 1/cal.getPixelWidthMicrons()
double xCorner = (xCent)*pixelScale-500*pixelScale
double yCorner = (yCent)*pixelScale-500*pixelScale
int width = 1000*pixelScale
int height = 1000*pixelScale

// Create the hot spot circle and display it
def roi = ROIs.createEllipseROI(xCorner, yCorner, width, height, plane)
def annotation = PathObjects.createAnnotationObject(roi)
addObject(annotation)