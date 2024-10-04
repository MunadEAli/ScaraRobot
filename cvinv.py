import numpy as np
import cv2
import matplotlib.pyplot as plt
import sys

sys.path.append('C:/Users/ADMIN/OneDrive/Desktop/ScaraKinematics/pycvscara')  # Add path to CoppeliaSim Python files
import sim  # Import the CoppeliaSim remote API module

def detect_shapes(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150)
    contours, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    shapes = {"triangles": [], "squares": [], "circles": []}

    for contour in contours:
        peri = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.04 * peri, True)
        M = cv2.moments(contour)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
        else:
            cX, cY = 0, 0

        if len(approx) == 3:
            shape_name = "triangles"
        elif len(approx) == 4:
            x, y, w, h = cv2.boundingRect(approx)
            aspect_ratio = float(w) / h
            if 0.95 <= aspect_ratio <= 1.05:
                shape_name = "squares"
        else:
            shape_name = "circles"

        size = cv2.arcLength(contour, True) if shape_name != "circles" else cv2.minEnclosingCircle(contour)[1] * 2
        x_mapped = np.interp(cX, [0, resolution[0]], [0.778, -0.427])
        y_mapped = np.interp(cY, [0, resolution[1]], [-0.594, 0.596])
        shapes[shape_name].append((size, contour, (x_mapped, y_mapped)))

    for shape_type, shape_list in shapes.items():
        shapes[shape_type] = sorted(shape_list, key=lambda x: x[0], reverse=True)

    return contours, shapes

sim.simxFinish(-1)
clientID = sim.simxStart('127.0.0.1', 19994, True, True, 5000, 5)

if clientID != -1:
    print('Connection successful.')
else:
    print('Failed connecting to remote API server')
    sys.exit()

err, camhandle = sim.simxGetObjectHandle(clientID, 'Vision_sensor', sim.simx_opmode_oneshot_wait)
err, resolution, raw_image = sim.simxGetVisionSensorImage(clientID, camhandle, 0, sim.simx_opmode_streaming)

while err != sim.simx_return_ok:
    err, resolution, raw_image = sim.simxGetVisionSensorImage(clientID, camhandle, 0, sim.simx_opmode_buffer)

img = np.array(raw_image, dtype=np.uint8)
img.resize([resolution[1], resolution[0], 3])
img = cv2.flip(img, 0)

contours, shapes = detect_shapes(img)

i = 1
for shape_type, shape_list in shapes.items():
    for size, contour, (x_mapped, y_mapped) in shape_list:
        signal_name_x = f"{shape_type}{i}_x"
        signal_name_y = f"{shape_type}{i}_y"
        sim.simxSetFloatSignal(clientID, signal_name_x, float(x_mapped), sim.simx_opmode_oneshot)
        sim.simxSetFloatSignal(clientID, signal_name_y, float(y_mapped), sim.simx_opmode_oneshot)
        i += 1

i = 1
for shape_type, shape_list in shapes.items():
    for size, contour, (x_mapped, y_mapped) in shape_list:
        print(f"{shape_type.capitalize()} {i}: Diameter/Length - {size}, Mapped Coordinates - ({x_mapped:.2f}, {y_mapped:.2f})")
        i += 1

cv2.imshow('Detected Shapes', img)
cv2.waitKey(0)
cv2.destroyAllWindows()

sim.simxFinish(clientID)
