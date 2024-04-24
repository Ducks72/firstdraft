import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog

def dot_counter(image, smallarea, largearea):
    num_dots = 0 
    path = image #defining the file that is to be used
    gray_image = cv2.imread(path, 0) #conversion of image to grey scale 

    th, threshed = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY_INV|cv2.THRESH_OTSU)

    cnts = cv2.findContours(threshed, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[-2]

    #filtering by area 
    s1 = smallarea
    s2 = largearea
    xcnts = []
    for cnt in cnts:
        if s1< cv2.contourArea(cnt) <s2:
            xcnts.append(cnt)
    print("\nDots number: {}.".format(len(xcnts)))
    num_dots = len(xcnts)
    return num_dots
        

# Function to draw the circle on the image
def draw_circle(event, x, y, flags, param):
    global center, radius, drawing, image
    
    if event == cv2.EVENT_LBUTTONDOWN:
        center = (x, y)
        drawing = True
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            distance = np.sqrt((x - center[0])**2 + (y - center[1])**2)
            radius = max(int(distance), 1)  # Ensure radius is at least 10
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False

    # Draw the circle on the image
    if drawing or (not drawing and radius > 0):  # Draw the circle even if not dragging
        img_copy = image.copy()
        cv2.circle(img_copy, center, radius, (0, 255, 0), 2)  # Green color for circle
        text = "Highlight the smallest particle, Press Enter to Continue"
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.7
        thickness = 2
        (text_width, text_height), baseline = cv2.getTextSize(text, font, font_scale, thickness)
        cv2.rectangle(img_copy, (50, 30 - text_height), (50 + text_width, 30 + baseline), (0, 0, 0), -1)  # Black background
        cv2.putText(img_copy, text, (50, 30), font, font_scale, (255, 255, 255), thickness, cv2.LINE_AA)  # White text
        cv2.imshow('Image', img_copy)

# Function to draw the circle on the second image
def draw_circle2(event, x, y, flags, param):
    global center2, radius2, drawing2, image2
    
    if event == cv2.EVENT_LBUTTONDOWN:
        center2 = (x, y)
        drawing2 = True
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing2:
            distance = np.sqrt((x - center2[0])**2 + (y - center2[1])**2)
            radius2 = max(int(distance), 1)  # Ensure radius is at least 10
    elif event == cv2.EVENT_LBUTTONUP:
        drawing2 = False

    # Draw the circle on the image
    if drawing2 or (not drawing2 and radius2 > 0):  # Draw the circle even if not dragging
        img_copy = image2.copy()
        cv2.circle(img_copy, center2, radius2, (0, 0, 255), 2)  # Red color for circle
        text = "Highlight the largest particle, Press N to continue"
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.7
        thickness = 2
        (text_width, text_height), baseline = cv2.getTextSize(text, font, font_scale, thickness)
        cv2.rectangle(img_copy, (50, 30 - text_height), (50 + text_width, 30 + baseline), (0, 0, 0), -1)  # Black background
        cv2.putText(img_copy, text, (50, 30), font, font_scale, (255, 255, 255), thickness, cv2.LINE_AA)  # White text
        cv2.imshow('Image', img_copy)

# Function to display welcome page
def welcome_page():
    cv2.namedWindow('Welcome', cv2.WINDOW_NORMAL)  # Create a resizable window
    cv2.resizeWindow('Welcome', 1000, 800)  # Set initial dimensions
    welcome_img = np.zeros((800, 1000, 3), np.uint8)  # Set image dimensions to match window
    cv2.putText(welcome_img, "Welcome to Particle Counting!", (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.putText(welcome_img, "Press 's' to select an image.", (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    cv2.imshow('Welcome', welcome_img)

# Function to select image
def select_image():
    global image
    global image_path
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    image_path = filedialog.askopenfilename()  # Open file dialog to select image
    if image_path:
        image = cv2.imread(image_path)
        cv2.namedWindow('Image')
        cv2.setMouseCallback('Image', draw_circle)
        # Display the text "Highlight the smallest circle"
        img_copy = image.copy()
        text = "Highlight the smallest particle, Press Enter to Continue"
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.7
        thickness = 2
        (text_width, text_height), baseline = cv2.getTextSize(text, font, font_scale, thickness)
        cv2.rectangle(img_copy, (50, 30 - text_height), (50 + text_width, 30 + baseline), (0, 0, 0), -1)  # Black background
        cv2.putText(img_copy, text, (50, 30), font, font_scale, (255, 255, 255), thickness, cv2.LINE_AA)  # White text
        cv2.imshow('Image', img_copy)
        root.destroy()  # Close the root window
    else:
        root.destroy()  # Close the root window if canceled

# Initialize global variables
center = (0, 0)
radius = 50
drawing = False
center2 = (0, 0)  # Add center2 initialization
radius2 = 50  # Add radius2 initialization
drawing2 = False  # Add drawing2 initialization
image = None

# Display welcome page and select image
welcome_page()
select_image()

if image is not None:
    while True:
        # Wait for the user to press ESC key to exit
        key = cv2.waitKey(1) & 0xFF
        if key == 13:  # Enter key
            saved_radius = radius
            print("Radius saved:", saved_radius)
            cv2.destroyAllWindows()  # Close the current image window
            # Reopen the image and reset drawing parameters
            image2 = image.copy()  # Create a copy of the original image
            cv2.namedWindow('Image')  # Create a new window for the second image
            cv2.setMouseCallback('Image', draw_circle2)  # Set mouse callback for the second image
            img_copy = image2.copy()  # Create a copy of the second image
            draw_circle2(None, 0, 0, 0, None)  # Call draw_circle2 function to display the circle
            text = "Highlight the largest particle, Press N to Continue"  # Text for the second image
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 0.7
            thickness = 2
            (text_width, text_height), baseline = cv2.getTextSize(text, font, font_scale, thickness)
            cv2.rectangle(img_copy, (50, 30 - text_height), (50 + text_width, 30 + baseline), (0, 0, 0), -1)  # Black background
            cv2.putText(img_copy, text, (50, 30), font, font_scale, (255, 255, 255), thickness, cv2.LINE_AA)  # White text
            cv2.imshow('Image', img_copy)  # Show the second image
            while True:
                key_largest_circle = cv2.waitKey(1) & 0xFF
                if key_largest_circle == 13:  # Enter key
                    break  # Exit the loop to ensure the program continues
                elif key_largest_circle == ord('n'):  # 'n' key
                    large_radius = radius2
                    print("Large Radius saved:", large_radius)
                    cv2.destroyAllWindows()  # Close the current image window
                    # Create a new black image with white text
                    new_page = np.zeros((800, 1000, 3), np.uint8)
                    print(saved_radius)
                    print(large_radius)
                    smallest_area = round(((saved_radius)*(saved_radius)*3.14),4)
                    largest_area = round(((large_radius)*(large_radius)*3.14),4)
                    print(smallest_area)
                    print(largest_area)
                    num_dots = dot_counter(image_path, smallest_area, largest_area)
                    print(num_dots)
                    cv2.putText(new_page, "Number: " + str(num_dots), (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                    cv2.imshow('New Page', new_page)
                    while True:
                        key_new_page = cv2.waitKey(1) & 0xFF
                        if key_new_page == 27:  # Esc key
                            cv2.destroyWindow('New Page')  # Close the new page window
                            break
                    break  # Exit the loop to ensure the program continues
                elif key_largest_circle == 27:  # Esc key
                    break

        elif key == 27:  # Esc key
            break

# Close all OpenCV windows
cv2.destroyAllWindows()
