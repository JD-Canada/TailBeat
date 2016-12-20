# import the necessary packages
import cv2 #this needs to installed 
import numpy as np

video='fftTest.avi'

camera = cv2.VideoCapture(video)
totalnbrframes=camera.get(7)
#print totalnbrframes
success, firstFrame = camera.read() #reads the first image of the video for calibration function
#print success
count = 0
xdist=[]
ydist=[]
ix,iy=-1,-1

# make the background subtractor a variable
fgbg = cv2.BackgroundSubtractorMOG()

# initialize the first frame in the video stream
firstFrame = None

coordlist=np.zeros((totalnbrframes,5))
coordlistavg=np.zeros((totalnbrframes,5))
counter=0
xcoord=[]
ycoord=[]
framerate=500
dt=0.002
averagex=0
averagey=0#why dont I have a comment here?
cx=0
cy=0
cx1=0
cy1=0
r=20
contourarea=[]
# loop over the frames of the video
while True:
	
	(grabbed, frame) = camera.read()
	if not grabbed:
		break

	frame2 = fgbg.apply(frame)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (11, 11), 0)

	if firstFrame is None:
		firstFrame = gray
		continue

	fgmask = fgbg.apply(frame)#applies the background subtractor
	frameDelta = cv2.absdiff(firstFrame, gray)
	thresh = cv2.threshold(frameDelta, 30, 255, cv2.THRESH_BINARY)[1]
	(cnts, _) = cv2.findContours(fgmask, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

	#create a few dummy list required to draw circles
	cntarea=[0]
	xcntcoord=[0]
	ycntcoord=[0]
 
	for c in cnts:
		if cv2.contourArea(c) < 300:# if the contour is too small, ignore it
			continue
		cntarea.append(cv2.contourArea(c))
		(x, y, w, h) = cv2.boundingRect(c)
		M = cv2.moments(c)
		cx = int(M['m10']/M['m00'])
		cy = int(M['m01']/M['m00'])
		xcntcoord.append(cx)
		ycntcoord.append(cy)

	biggestcontour=cntarea.index(max(cntarea))
	xcoord.append(xcntcoord[biggestcontour])
	ycoord.append(ycntcoord[biggestcontour])
	cv2.circle(frame, (xcntcoord[biggestcontour], ycntcoord[biggestcontour]),r,(0, 255, 0), 1)
	fishcoords=np.array((xcoord,ycoord),dtype=float)
	for i in range(len(xcoord)):
		cv2.circle(frame, (xcoord[i], ycoord[i]),2, (0, 0, 255),thickness=-1)
	cv2.imshow("Circle",frame)

	"""
	Draw circle around fish body. Needs to be small enough to unambigously grab a good central portion of the body.
	"""
	# size the image
	H, W = thresh.shape
	x, y = np.meshgrid(np.arange(W), np.arange(H))                               # x and y coordinates per every pixel of the image
	d2 = (x - xcntcoord[biggestcontour])**2 + (y - ycntcoord[biggestcontour])**2 #Finds the hypoteneuse extending down from the top left corner to the center of the circle
	mask = d2 > r**2                                                             # mask is True outside of the circle. The choice of r is important.
	outside = np.ma.masked_where(mask, thresh)                                   #apply mask to fgmask
	average_color =255
	thresh[mask] = average_color #strange syntax, but colors everything outside of the circle white

	cv2.imshow("fgmask",thresh)
	(contours, _) = cv2.findContours(thresh.copy(), cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE) #finds black contours
	
	for c in contours:
		# if the contour is too small, ignore it
		if cv2.contourArea(c) < 75 or cv2.contourArea(c) > 1000:
			continue
		area=cv2.contourArea(c)
		(x1, y1, w1, h1) = cv2.boundingRect(c)
		M = cv2.moments(c)
		cx1 = int(M['m10']/M['m00'])
		cy1 = int(M['m01']/M['m00'])
	
	cv2.circle(thresh, (cx1, cy1),r,(0, 255, 0), 1)

	
	if cv2.contourArea(c) > 50 or cv2.contourArea(c) < 1000:
		contourarea.append(cv2.contourArea(c))

	# if the `q` key is pressed, break from the loop
	key = cv2.waitKey(1) & 0xFF
	if key == ord("q"):
		break
	counter += 1

# cleanup the camera and close any open windows
np.savetxt("fishcoords.txt",np.transpose(fishcoords))
np.savetxt("contourarea.txt", contourarea)
np.savetxt("coords.txt", coordlist, delimiter="\t",fmt='%.2f') #save coordinates to file
np.savetxt("avrgcoords.txt", coordlistavg, delimiter="\t",fmt='%.2f') #save coordinates to file
camera.release()
cv2.destroyAllWindows()











