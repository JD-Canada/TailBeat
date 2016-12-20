# import the necessary packages
import cv2 
import numpy as np

video='fftTest.avi'

camera = cv2.VideoCapture(video)

success, firstFrame = camera.read() #reads the first image of the video for calibration function

count = 0
xdist=[]
ydist=[]
ix,iy=-1,-1

# initialize the first frame in the video stream
firstFrame = None

#declare variables and lists
xcoord=[]
ycoord=[]
cx=0
cy=0
cx1=0
cy1=0
r=20
contourarea=[]

# make the background subtractor a variable
fgbg = cv2.BackgroundSubtractorMOG()

# loop over the frames of the video,when False (i.e. no more frames) the loop is done
while True:
    
    #if for some reason video doesn't load, break while loop
    (grabbed, frame) = camera.read()
    if not grabbed:
        break

    #some preprocessing
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (11, 11), 0)

    #stores first image (i.e. first instance of "gray") for absdiff 
    if firstFrame is None:
        firstFrame = gray
        continue

    fgmask = fgbg.apply(frame)      #applies background subtractor which turns the image into a binary image of black and white
    (cnts, _) = cv2.findContours(fgmask, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE) #finds contours (i.e. "fish" as white pixels)
    
    frameDelta = cv2.absdiff(firstFrame, gray)
    thresh = cv2.threshold(frameDelta, 30, 255, cv2.THRESH_BINARY)[1]

    #create a few dummy lists required to draw circles
    cntarea=[0]
    xcntcoord=[0]
    ycntcoord=[0]

    #loop through contours
    for c in cnts:
        
        #if statements checks if contours are big enough to meet the criteria of a fish (you can change the number)
        if cv2.contourArea(c) < 300:          #feel free to change this number to adjust for noise
            continue                          #skips the contour if it is too small (i.e. too small = noise)
        
        #if contour area is big enough, then this code runs
        cntarea.append(cv2.contourArea(c)) #adds contour area to list
        M = cv2.moments(c)                 #finds moments of contour
        cx = int(M['m10']/M['m00'])        #calculates x coordinate of contour (i.e. centroid fish)
        cy = int(M['m01']/M['m00'])        #calculates y coordinate of contour (i.e. centroid fish)
        xcntcoord.append(cx)
        ycntcoord.append(cy)

    biggestcontour=cntarea.index(max(cntarea)) #finds biggest contour, which is likely the fish
    xcoord.append(xcntcoord[biggestcontour])   #adds coordinates to xcoord, which is the master list of all x for trackign the biggest contour in the video
    ycoord.append(ycntcoord[biggestcontour])
    
    cv2.circle(frame, (xcntcoord[biggestcontour], ycntcoord[biggestcontour]),r,(0, 255, 0), 1) #draws circle with center fish centroid
    

    for i in range(len(xcoord)):
        cv2.circle(frame, (xcoord[i], ycoord[i]),2, (0, 0, 255),thickness=-1)
    cv2.imshow("Circle",frame)

    """
    Draw circle around fishs' body. Needs to be small enough to unambigously grab a good central portion of the body.
    It is important that the circle "cuts" out a central portion of the fish, so that you make an oreo cookie (black, white, black)
    """
    
    H, W = thresh.shape #takes the size of the frame
    x, y = np.meshgrid(np.arange(W), np.arange(H))                               #x and y coordinates of every pixel in the image
    d2 = (x - xcntcoord[biggestcontour])**2 + (y - ycntcoord[biggestcontour])**2 #Finds the hypoteneuse extending down from the top left corner to the center of the circle
    mask = d2 > r**2                                                             #mask is True outside of the circle. The choice of r is important.
    outside = np.ma.masked_where(mask, thresh)                                   #apply mask to thresh
    average_color =255                                                           #255 is the color white
    thresh[mask] = average_color #strange syntax, but colors everything outside of the circle white

    cv2.imshow("Frequency circle",thresh) #this is what makes the white video pop up
    (contours, _) = cv2.findContours(thresh.copy(), cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE) #finds black contours or the black parts of the oreo cookie
    
    """
    Noise may show up as contours less than a certain number of pixels (i.e. 75)
    When there are no black cookie tops to track, then the contour is the entire image area, so > 1000 gets rid of those
    These numbers might need to be modified depending on the size of fish.
    """
    
    for c in contours:
        # if the contour is too small or too large, ignore it
        if cv2.contourArea(c) < 75 or cv2.contourArea(c) > 1000:
            continue
        
        area=cv2.contourArea(c)
        M = cv2.moments(c)
        cx1 = int(M['m10']/M['m00'])
        cy1 = int(M['m01']/M['m00'])

    contourarea.append(cv2.contourArea(c))

    # if the `q` key is pressed, break from the loop
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break


coords=np.array((xcoord,ycoord),dtype=float) #create numpy array with xcoord and ycoord of fish centroid

np.savetxt("coords.txt",np.transpose(coords))
np.savetxt("contourarea.txt", contourarea)

#close the camera and close any open windows
camera.release()
cv2.destroyAllWindows()











