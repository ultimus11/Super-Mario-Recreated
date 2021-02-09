import cv2
import numpy as np
import time

def overlay_transparent(background, overlay, x, y):
	# https://stackoverflow.com/a/54058766/11359097
	background_width = background.shape[1]
	background_height = background.shape[0]

	if x >= background_width or y >= background_height:
		return background

	h, w = overlay.shape[0], overlay.shape[1]

	if x + w > background_width:
		w = background_width - x
		overlay = overlay[:, :w]

	if y + h > background_height:
		h = background_height - y
		overlay = overlay[:h]

	if overlay.shape[2] < 4:
		overlay = np.concatenate(
					[
						overlay,
						np.ones((overlay.shape[0], overlay.shape[1], 1), dtype = overlay.dtype) * 255
						],
					axis = 2,
		)

	overlay_image = overlay[..., :3]
	mask = overlay[..., 3:] / 255.0

	background[y:y+h, x:x+w] = (1.0 - mask) * background[y:y+h, x:x+w] + mask * overlay_image

	return background

def animate_walking(board,name,x):
	im2 = cv2.imread("../images/{}.png".format(name), cv2.IMREAD_UNCHANGED)
	back = overlay_transparent(board, im2, x, 100)
	cv2.waitKey(140)
	return back


def show_frames():
	board = cv2.imread("../images/background.png", cv2.IMREAD_UNCHANGED)
	name = 1
	x=20
	back = animate_walking(board.copy(),name,x)
	while True:
		back = animate_walking(board.copy(),name,x)
		cv2.imshow(' Super Mario ', back)
		name+=1
		x+=10
		if cv2.waitKey(25)&0xFF==('q'):
			cv2.destroyAllWindows()
			break
		if x>=620:
			break
		elif name==8:
			name=1

show_frames()