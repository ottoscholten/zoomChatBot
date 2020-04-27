# Import libraries
import os
from time import sleep
# Control mouse and keyboard
import pyautogui
# Character recognition from images
import pytesseract
from pytesseract import Output
# Manipulating images
from PIL import ImageGrab, ImageOps, Image
# Used to take screenshots
import mss
import mss.tools
# Computer vision (the eyes)
import cv2
# For arrays/ scientific computing
import numpy as np


# Commands to control the bot
class Commands:
    botKeyWord = "/pp"
    forceStopBot = "fstop"
    createBreakout = "create-breakout"
    resetBreakout = "reset-breakout"


class UserPresets:
    computerUsername = "ottoscholten"
    loopDelay = 5  # Seconds
    amountOfBreakOutRooms = 40
    mouseSensitivity = "slow-medium"


class Presets:
    mouseSensitivityMode = {
        'slow': 1.5,
        'slow-medium': 1.25,
        'medium': 1,
        'medium-fast': 0.75,
        "fast": 0.5
    }
    brRoomsListWindowSize = {
        "width": 318,
        "height": 485
    }
    brRoomsUsers = {}
    brUsersAdded = []
    brRoomsListWindowCoordinates = ()
    brRoomsListWords = {}
    brAssignListWindowCoordinates = ()
    brAssignListWords = {}
    brRoomsListOpenCoordinates = {}


# Images (used for recognition)
class Images:
    zoomApp = "zoomApp.png"
    desktopWindow = "desktopWindow.png"
    breakoutRoomsButton = "breakoutRoomsButton.png"
    shareScreenButton = "shareScreenButton.png"
    brAmountArrows = "brAmountArrows.png"
    brManuallyButton = "brManuallyButton.png"
    brCreateButton = "brCreateButton.png"
    brRoomsListOpen = "brRoomsListOpen.png"
    brRoomsListWindow = "brRoomsListWindow.png"
    brAssignListWindow = "brAssignListWindow.png"
    brOpenAllRoomsButton = "brOpenAllRoomsButton.png"
    brRecreateButton = "brRecreateButton.png"
    brRecreateAllRoomsButton = "brRecreateAllRoomsButton.png"
    brRoomsListNotStartedText = "brRoomsListNotStartedText.png" # Window is selected
    brRoomsListNotStartedClosedText = "brRoomsListNotStartedClosedText.png" # Window is not selected


class Files:
    meetingSavedChat = "meeting_saved_chat.txt"


class Directories:
    zoomDirectory = "/Users/" + UserPresets.computerUsername + "/Documents/Zoom"


# All sub directories of a folder
def all_sub_directories_of(b='.'):
    result = []
    for d in os.listdir(b):
        bd = os.path.join(b, d)
        if os.path.isdir(bd):
            result.append(bd)
    return result


# Latest folder in directory
def latest_sub_directory(all_directories):
    latest_directory = max(all_directories, key=os.path.getmtime)
    return latest_directory


def get_meeting_chat():
    # Get zoom folder
    zoom_directory = all_sub_directories_of(Directories.zoomDirectory)
    # Get latest zoom chat file
    latest_zoom_meeting_directory = latest_sub_directory(zoom_directory)
    # Grab chat messages
    chat_messages = open(latest_zoom_meeting_directory + "/" + Files.meetingSavedChat, "r")
    return chat_messages.readlines()


# Shortcuts
def click(coordinates):
    pyautogui.click(coordinates)


def press(key):
    pyautogui.press(key)


def move_to(x, y):
    pyautogui.moveTo(x, y)


def scroll(amount):
    pyautogui.scroll(amount)


def move_and_scroll(amount, x, y):
    pyautogui.scroll(amount, x, y)


def drag_to(x, y):
    coordinates = x, y
    pyautogui.dragTo(coordinates)

def write(text, interval=0):
    pyautogui.typewrite(text, interval=interval)


def write_int(text, interval=0):
    pyautogui.typewrite(str(text), interval=interval)


def hotkey2(key1, key2):
    pyautogui.hotkey(key1, key2)


# Full/desktop screenshot
def full_screenshot():
    # Take a full screen shot.
    with mss.mss() as sct:
        screenshot = sct.shot(output="images/" + Images.desktopWindow)


# Screenshot of certain region.
def create_screenshot(name, offset_left, offset_up, width, height):
    with mss.mss() as sct:
        # The screen part to capture
        region = {'top': offset_up, 'left': offset_left, 'width': width, 'height': height}
        # Grab the data
        img = sct.grab(region)
        # Save to the picture file
        mss.tools.to_png(img.rgb, img.size, output='images/' + name)


# Check for pixel offset
def offset(v, d, min_or_plus):
    difference = 0
    for x in range(0, 5):
        if min_or_plus == "plus":
            if v + x in d:
                difference = x
                break
        elif min_or_plus == "minus":
            if v - x in d:
                difference = x
                break
    return difference


# Find certain icon/button on screen
def find_image_coordinates(img_name, left=0, up=0, right=0, down=0, type_of_conversion="center"):  # Move coords 10 pixels left. (Not the usual left,top,right,down)
    # Take screenshot
    full_screenshot()
    # Icon/Image you want to find (the needle)
    needle_img = os.path.abspath("images/" + img_name)
    # Search desktop for a match (the haystack)
    haystack_img = os.path.abspath("images/" + Images.desktopWindow)
    # Locate image on desktop
    img_coordinates = pyautogui.locate(needle_img, haystack_img, grayscale=False)
    if img_coordinates is not None:
        if type_of_conversion is "center":
            # Locate image
            # If image found, get coordinates.
            img_coordinates_x, img_coordinates_y = pyautogui.center(img_coordinates)
            # See if we need to move right or left of the image center
            img_coordinates_x = img_coordinates_x / 2  # divide by half because mac retina screens are 2x resolution
            img_coordinates_y = img_coordinates_y / 2
            if left != 0:
                img_coordinates_x = img_coordinates_x - left
            if up != 0:
                img_coordinates_y = img_coordinates_y + up
            if right != 0:
                img_coordinates_x = img_coordinates_x + right
            if down != 0:
                img_coordinates_y = img_coordinates_y - down
            return img_coordinates_x, img_coordinates_y
        elif type_of_conversion is "dimensionsConverted":
            img_coordinates_x, img_coordinates_y, width, height = img_coordinates
            return img_coordinates_x / 2, img_coordinates_y / 2, width / 2, height / 2
        elif type_of_conversion is "dimensionsOriginal":
            return img_coordinates
    else:
        print("Image not found: " + img_name)
        return None


# Find value of type of image.
def get_coordinates_of_img_text(img_file_name):
    # Grab image
    img_name = "images/" + img_file_name
    img = cv2.imread(img_name)
    # Image Data
    d = pytesseract.image_to_data(img, output_type=Output.DICT)
    # Number of boxes
    n_boxes = len(d['level'])
    # Loop through words and get coordinates.
    list_of_words = []
    for i in range(n_boxes):
        (left, top, width, height) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
        if d['text'][i] != 0 and len(d['text'][i]) != 0:
            # Retina screens, 2x resolution
            text = d["text"][i]
            coordinates = {"x": round(left / 2 + width / 4), "y": round(top / 2 + height / 4)}
            # Append data to array
            list_of_words.append({"text": text, "coordinates": coordinates})
    return list_of_words


# Remove command line
def delete_command_line():
    hotkey2('command', 'a')
    press("backspace")


# Find and click image
def click_image(param):
    image = find_image_coordinates(param)
    click(image)


def open_zoom_app():
    zoom_app = find_image_coordinates(Images.zoomApp)
    click(zoom_app)
    sleep(.5)


def open_breakout_app():
    print("Opening breakout")
    click_image(Images.breakoutRoomsButton)


def set_amount_of_breakout_rooms():
    print("Setting amount of breakout rooms")
    br_arrows = find_image_coordinates(Images.brAmountArrows, 22)
    click(br_arrows)
    delete_command_line()  # Remove existing numbers
    write_int(UserPresets.amountOfBreakOutRooms)  # Write numbers


# Set to "manually" assign
def click_manually_btn():
    print("Setting assign to 'manually'")
    click_image(Images.brManuallyButton)


def click_create_breakout_btn():
    click_image(Images.brCreateButton)


def click_re_create_breakout_btn():
    click_image(Images.brRecreateAllRoomsButton)


def click_open_all_rooms_btn():
    click_image(Images.brOpenAllRoomsButton)


def move_mouse_out_the_way_during_assigns():
    parent_window_x, parent_window_y, parent_window_w, parent_window_h = Presets.brRoomsListWindowCoordinates
    move_to(parent_window_x - 50, parent_window_y)


def move_mouse_out_the_way():
    move_to(0, 400)


def move_breakout_rooms_list_window_to_center():
    # Move mouse to rooms list "not started" text
    x_not_started_text = ""
    y_not_started_text = ""
    room_not_started_text = find_image_coordinates(Images.brRoomsListNotStartedText)
    if room_not_started_text is None:
        room_not_started_closed_text = find_image_coordinates(Images.brRoomsListNotStartedClosedText)
        if room_not_started_closed_text is not None:
            x_not_started_text, y_not_started_text = room_not_started_closed_text
    else:
        x_not_started_text, y_not_started_text = room_not_started_text
    if x_not_started_text != "" and y_not_started_text != "":
        move_to(x_not_started_text, y_not_started_text)
        # Drag window to center of zoom (center of zoom is share btn)
        x_share_screen_btn, y_share_screen_btn = find_image_coordinates(Images.shareScreenButton)
        drag_to(x_share_screen_btn, y_not_started_text)
    else:
        print("Can't find breakout rooms list window")


# Convert to breakout room words
def convert_text_to_breakout_rooms_list(param):
    # Create Rows
    rows = {}
    # Banned Words
    banned_words = ["room", "x", "vy", "y", "", "v", "l", "e@", ">]", "to", " "]
    # Check all words
    for index, word in enumerate(param):
        # Remove characters we don't want
        if not word["text"].lower() in banned_words:
            # Check if row already exists. (and pixels close to it)
            y_coord = word["coordinates"]["y"]
            # Check for pixel offset (words that are nearly on the same y/height)
            y_plus_offset = offset(y_coord, rows, "plus")
            y_minus_offset = offset(y_coord, rows, "minus")
            # Check if row exists
            row_exists = (y_coord in rows) or y_plus_offset > 0 or y_minus_offset > 0
            # Need next index, to remove (7 int, that is the pen icon)
            next_index = index + 1
            amount_of_words = len(param)
            if row_exists:
                # If this word is same as previous, add it to the same group
                if next_index < amount_of_words:
                    # Check if next word is not Rename, and current word isn't a digit (to remove pen icon)
                    if not param[next_index]["text"] == "Rename" and word["text"].isdigit:
                        # Check for offset
                        if y_plus_offset != 0:
                            rows[y_coord + y_plus_offset].append(word)
                        elif y_minus_offset != 0:
                            rows[y_coord - y_minus_offset].append(word)
                        else:
                            rows[y_coord].append(word)
            else:
                rows[y_coord] = [word]
    # Now order and sort rows by breakout number
    rows_sorted = {}
    # Access each row
    for key in rows:
        # Check the text
        for word in rows[key]:
            # If a digit (so the number of the room)
            if word["text"].isdigit():
                # Add it to sorted list with name of room
                rows_sorted[word["text"]] = rows[key]

    # "Assign" --> Last item is list always seems to miss "assign" button, add it.
    last_row = int(max(rows_sorted, key=int))
    assign_in_last_row_found = False
    assign_y_coord = 0
    assign_x_coord = 0
    # Check if last row is missing "assign" (reverse, usually its in the back)
    for row in reversed(rows_sorted[str(last_row)]):
        if row["text"] is "Assign":
            assign_in_last_row_found = True
        elif assign_y_coord is 0:
            # If not found, set "assign" y.
            assign_y_coord = row["coordinates"]["y"]
    # If no assign found
    if not assign_in_last_row_found:
        # Loop through previous breakout room, to use their assigns (loop from the back)
        for row in reversed(rows_sorted[str(last_row - 1)]):
            if assign_x_coord is 0:
                if row["text"] == "Assign":
                    # Grab assign x coordinates from previous row
                    assign_x_coord = row["coordinates"]["x"]
        # Assemble assign word
        assign_word = {
            "text": "Assign",
            "coordinates": {
                "x": assign_x_coord,
                "y": assign_y_coord
            }
        }
        # Append word to last row
        rows_sorted[str(last_row)].append(assign_word)

    # Set breakout list window words
    Presets.brRoomsListWords = rows_sorted


# Convert to breakout assign list
def convert_text_to_breakout_assign_list(param):
    # Create Rows
    rows = {}
    # Banned Words
    banned_words = ["Breakout", "Others", "Rooms"]
    for index, word in enumerate(param):
        # Remove characters we don't want (no lowercase, since its super specific)
        if not word["text"] in banned_words:
            # Check if row already exists. (and pixels close to it)
            y_coord = word["coordinates"]["y"]
            # Check for pixel offset (words that are nearly on the same y/height)
            y_plus_offset = offset(y_coord, rows, "plus")
            y_minus_offset = offset(y_coord, rows, "minus")
            # Check if row exists
            row_exists = (y_coord in rows) or y_plus_offset > 0 or y_minus_offset > 0
            # Need next index, to remove (7 int, that is the pen icon)
            next_index = index + 1
            amount_of_words = len(param)
            if row_exists:
                # If this word is same as previous, add it to the same group
                if next_index < amount_of_words:
                    # Check for offset
                    if y_plus_offset != 0:
                        rows[y_coord + y_plus_offset].append(word)
                    elif y_minus_offset != 0:
                        rows[y_coord - y_minus_offset].append(word)
                    else:
                        rows[y_coord].append(word)
            else:
                rows[y_coord] = [word]
    # Set list

    # Now order and sort rows by usernames
    rows_sorted = {}
    # Access each row
    for key in rows:
        # Combine text to create multi word username
        username = ""
        x_coordinate = 0
        y_coordinate = 0
        for word in rows[key]:
            # Create username
            if username != "":
                username = username + " " + word["text"]
            else:
                username = word["text"]
            # Create coordinates
            if x_coordinate != 0 and y_coordinate != 0:
                x_coordinate = (word["coordinates"]["x"] + x_coordinate) / 2
                y_coordinate = (word["coordinates"]["y"] + y_coordinate) / 2
            else:
                x_coordinate = word["coordinates"]["x"]
                y_coordinate = word["coordinates"]["y"]
        # Add it to sorted list with name of room
        rows_sorted[username] = {"text": username, "coordinates": {"x": x_coordinate, "y": y_coordinate}}
    Presets.brAssignListWords = rows_sorted


# Grab coordinates of a word from a row
def find_coordinates_of_word_in_row(rows, number, text):
    try:
        for word in rows[str(number)]:
            if word["text"].lower() == text.lower():
                return word["coordinates"]["x"], word["coordinates"]["y"]
    except KeyError:
        return "Not within window"


def get_coordinates_br_room_list_window():
    if Presets.brRoomsListOpenCoordinates is not None:
        img_x, img_y, img_w, img_h = Presets.brRoomsListOpenCoordinates
        # Adjust coordinates to capture entire window.
        img_x = img_x - 14
        img_y = img_y - 7
        img_w = img_w + Presets.brRoomsListWindowSize["width"]
        img_h = img_h + Presets.brRoomsListWindowSize["height"]
        # Take picture of entire room list window
        create_screenshot(Images.brRoomsListWindow, img_x, img_y, img_w, img_h)
        Presets.brRoomsListWindowCoordinates = (img_x, img_y, img_w, img_h)


def get_coordinates_br_room_list_open():
    Presets.brRoomsListOpenCoordinates = find_image_coordinates(Images.brRoomsListOpen, type_of_conversion="dimensionsConverted")


def get_coordinates_br_assign_list_window(coordinates_assign_button):
    # Find coordinates relative to rooms list window
    assign_btn_x, assign_btn_y = coordinates_assign_button
    # Move right pixels
    img_x = assign_btn_x + 37
    # Move up pixels
    img_y = 25  # 25 pixels is mac navigation
    img_w = 231
    img_h = 770  # Is where zoom navigation starts
    # Take a screenshot of assign window
    create_screenshot(Images.brAssignListWindow, img_x, img_y, img_w, img_h)
    Presets.brAssignListWindowCoordinates = img_x, img_y, img_w, img_h


def get_relative_coordinates(child_image_x, child_image_y, parent_coordinates):
    parent_window_x, parent_window_y, parent_window_w, parent_window_h = parent_coordinates
    relative_coordinates = child_image_x + parent_window_x, child_image_y + parent_window_y
    return relative_coordinates


def assign_all_users_to_room(room_number):
    # Only assign for rooms that aren't empty
    if len(Presets.brRoomsUsers[room_number]) != 0:
        # Fetch coordinates of assign button
        coordinates_of_assign = find_coordinates_of_word_in_row(Presets.brRoomsListWords, room_number, "assign")
        # If assign button found
        if coordinates_of_assign is not None and coordinates_of_assign != "Not within window":
            print("\nAssign found for room " + str(room_number))
            # Split up assign coordinates
            assign_btn_x, assign_btn_y = coordinates_of_assign
            # Get coordinates relative to entire screen (by checking difference of assign window
            assign_btn_coordinates = get_relative_coordinates(assign_btn_x, assign_btn_y, Presets.brRoomsListWindowCoordinates)
            # Click to open assign window
            click(assign_btn_coordinates)
            # Delay before taking screenshot
            sleep(.5)
            print("Opened assign window")
            # Get assigns window coordinates, and screenshot coordinates
            get_coordinates_br_assign_list_window(assign_btn_coordinates)
            print("Found assign list in window")
            # Delay, give it time to take screenshot
            sleep(1)
            # Get list of words in that image
            br_assign_window_all_text = get_coordinates_of_img_text(Images.brAssignListWindow)
            print("Fetched all words from assign list window")
            # Convert words to usernames
            convert_text_to_breakout_assign_list(br_assign_window_all_text)
            # Loop through users in this room
            users_in_room_stayed_in_meeting = 0
            for username in Presets.brRoomsUsers[room_number]:
                # If username is in the "added" list
                user_found_in_added_list = any(username in s for s in Presets.brUsersAdded)
                # Check if user exists in assign window list
                user_found_in_assign_list = any(username in s for s in Presets.brAssignListWords)

                # Matching system
                # Look if single words match the found usernames.
                username_split_by_words = username.split(" ")
                username_amount_of_words = len(username_split_by_words)
                username_without_spaces = ""
                for word in username_split_by_words: # todo Add a way to check if current matched word, is unique and not a username.
                    match_word = [s for s in Presets.brAssignListWords if username in s]
                    if match_word != "":
                        print("fuck yeah a single word matches")
                    username_without_spaces = username_without_spaces + word

                match_username_without_spaces = [s for s in Presets.brAssignListWords if username_without_spaces in s] # array
                # If more than 1 user match, then its not a match
                if len(match_username_without_spaces) == 1:
                    if username != match_username_without_spaces[0]:
                        username = match_username_without_spaces[0]

                # If list of assign words contains username
                if (user_found_in_added_list and user_found_in_assign_list) or len(match_username_without_spaces) == 1:
                    print("  Match found for: " + username)
                    # Split up coordinates
                    username_x = Presets.brAssignListWords[username]["coordinates"]["x"]
                    username_y = Presets.brAssignListWords[username]["coordinates"]["y"]
                    # Make coordinates relative to entire screen
                    # Our username coordinates are on an [] image that is only a portion of the screen
                    username_coordinates = get_relative_coordinates(username_x, username_y, Presets.brAssignListWindowCoordinates)
                    # Click username
                    click(username_coordinates)
                    users_in_room_stayed_in_meeting = users_in_room_stayed_in_meeting + 1
                    print("  Assigned user " + username + " to room " + str(room_number))
                else:
                    print("  User " + username + " not found, maybe they have left the meeting" + "\n")
                    print("Trying to find user one more time")
                    # if failed, screenshot assigns window and try again.
                    # But only try for the username that wasn't found? todo THIS??
                    # What happens when list is too long? Search functionality?
                    # assign_all_users_to_room(room_number)

            # Close breakout room window if a user was assigned
            if users_in_room_stayed_in_meeting > 0:
                # Get coordinates of text
                coordinates_of_breakout_text = find_coordinates_of_word_in_row(Presets.brRoomsListWords, room_number, "breakout")
                # Get coordinates relative to desktop
                breakout_text_x, breakout_text_y = coordinates_of_breakout_text
                assign_btn_coordinates = get_relative_coordinates(breakout_text_x, breakout_text_y, Presets.brRoomsListWindowCoordinates)
                # Add delay between each assigns list
                sleep(1)
                click(assign_btn_coordinates)
            else:
                # Otherwise move the mouse out of the way
                move_mouse_out_the_way_during_assigns()
        else:
            # If room not found in within current window
            if coordinates_of_assign == "Not within window":
                print("Coordinates of Assigns Button not found within the current List Window")
                parent_window_x, parent_window_y, parent_window_w, parent_window_h = Presets.brRoomsListWindowCoordinates
                sleep(.5)
                # Scroll down room window list
                middle_of_parent_window_x = (parent_window_x / 2) * 3
                middle_of_parent_window_y = (parent_window_y / 2) * 3
                # negative distance, to move down
                scroll_distance = -Presets.mouseSensitivityMode[UserPresets.mouseSensitivity] * 10
                move_and_scroll(scroll_distance, middle_of_parent_window_x, middle_of_parent_window_y)
                # Move mouse out of the way
                move_mouse_out_the_way_during_assigns()
                print("Scrolling down rooms window list")
                sleep(1)
                # Try finding the room again, and assigning the user
                get_coordinates_br_room_list_window()
                if Presets.brRoomsListWindowCoordinates is not None:
                    # Get list of words in that image
                    br_rooms_list_window_all_text = get_coordinates_of_img_text(Images.brRoomsListWindow)
                    print("Fetched all words from window")
                    # Convert words into breakout rows/groups
                    convert_text_to_breakout_rooms_list(br_rooms_list_window_all_text)
                    print("Converted text to relevant words")
                    assign_all_users_to_room(room_number)
                else:
                    print("Could not find Breakout List Window")


def assign_users_to_breakout():
    # Check if breakout rooms window is open, and fetch coordinates. Also takes screenshot (of default window size)
    get_coordinates_br_room_list_open()
    get_coordinates_br_room_list_window()

    # Check if coordinates were found
    if Presets.brRoomsListWindowCoordinates is not None:
        print("\nFound rooms list window")

        # Get list of words in that image
        br_rooms_list_window_all_text = get_coordinates_of_img_text(Images.brRoomsListWindow)
        print("Fetched all words from window")

        # Convert words into breakout rows/groups
        convert_text_to_breakout_rooms_list(br_rooms_list_window_all_text)
        print("Converted text to relevant words")

        # Assign users to rooms
        for roomNumber in Presets.brRoomsUsers:
            assign_all_users_to_room(roomNumber)

        print("Breakout rooms have been created")
        move_mouse_out_the_way()
    else:
        print("Could not find Breakout List Window")


# Generate amount of breakout rooms we want
def generate_breakout_rooms():
    for roomNumber in range(1, UserPresets.amountOfBreakOutRooms + 1):
        Presets.brRoomsUsers[roomNumber] = []


def add_chat_user_to_breakout_list(chat_username, chat_number):
    if UserPresets.amountOfBreakOutRooms >= int(chat_number):
        # Check if user exists in sign up list
        if chat_username in Presets.brUsersAdded:
            # Check Rooms
            for room_number in Presets.brRoomsUsers:
                # If username is in room
                if chat_username in Presets.brRoomsUsers[room_number]:
                    print("Removed user from breakout room " + str(room_number))
                    Presets.brRoomsUsers[room_number].remove(chat_username)
        else:
            # Add user to assigned list
            Presets.brUsersAdded.append(chat_username)
        # Add user to breakout room
        Presets.brRoomsUsers[int(chat_number)].append(chat_username)
        print('Added user to breakout room ' + chat_number)
    else:
        print("Breakout room " + chat_number + " doesn't exist")


def create_breakout():
    print("Creating breakout rooms")
    open_breakout_app()
    sleep(.5)
    # Check if we need to recreate room, or this is first time creating rooms
    recreate_image_coordinates = find_image_coordinates(Images.brRecreateButton)
    if recreate_image_coordinates is not None:
        click(recreate_image_coordinates)
        sleep(.5)
    set_amount_of_breakout_rooms()
    click_manually_btn()
    # if recreate, button is different.
    if recreate_image_coordinates is not None:
        click_re_create_breakout_btn()
    else:
        click_create_breakout_btn()

    # Move breakout rooms list window, to center of zoom (to avoid it reading other words from chat etc)
    move_breakout_rooms_list_window_to_center()
    assign_users_to_breakout()


def reset_breakout():
    print("Resetting breakout")
    # Reset users in rooms
    Presets.brRoomsUsers = {}
    # Reset users on added list
    Presets.brUsersAdded = []
    # Reset coordinates of windows and words
    Presets.brRoomsListWindowCoordinates = ()
    Presets.brRoomsListWords = {}
    Presets.brAssignListWindowCoordinates = ()
    Presets.brAssignListWords = {}
    Presets.brRoomsListOpenCoordinates = {}
    # Generate new breakout rooms
    print("Generating breakout rooms structure")
    generate_breakout_rooms()


# Start the chat bot
def start_chatbot():
    # State of bot.
    stop_chatbot = False

    # Last message date (ignore any before this date)
    latest_message_date = ''
    latest_message_text = ''
    latest_message_username = ''

    # Generate breakout rooms data structure
    print("Generating breakout rooms structure")
    generate_breakout_rooms()

    print("Starting Chat Bot")
    # Loop bot, till told to stop
    while not stop_chatbot:
        # Get lines from file
        lines = get_meeting_chat()

        # Loop through lines
        for line in lines:
            # Date
            message_date = line.split()[0]
            # User text
            message_text = line.split(':')[3][1:].split(" ")
            # Username (from, :, -1 space after name)
            message_username = line.split("From ")[1].split(":")[0][:-1]
            # Get length of message
            message_len = len(message_text)

            # If new date is newer than latest date, or content is different (for when messages are sent at exact same time)
            if latest_message_date < message_date or (latest_message_date == message_date and (message_text != latest_message_text or latest_message_username != message_username)):
                latest_message_date = message_date
                latest_message_text = message_text
                latest_message_username = message_username
                print("\n" + message_username + " at " + message_date)
                print(message_text)

                # If 1 word
                if message_len == 1:
                    message = message_text[0].split("\n")[0]
                    # If a number and a breakout room number
                    if message.isdigit():
                        add_chat_user_to_breakout_list(message_username, message)

                # If 2 words, it could be a command
                if message_len == 2:
                    # Check for command keyword
                    if message_text[0] == Commands.botKeyWord:
                        message = message_text[1].split("\n")[0]

                        # Force Stop Bot
                        if message == Commands.forceStopBot:
                            print("\n" + "STOPPING BOT")
                            stop_chatbot = True
                            break

                        # Create breakout rooms
                        elif message == Commands.createBreakout:
                            open_zoom_app()
                            create_breakout()

                        elif message == Commands.resetBreakout:
                            reset_breakout()

                        # Not a valid command
                        else:
                            print("\n" + "This is not a valid command")

            # If latestMessageDate is the last message, then no new message are found
            elif latest_message_date == message_date:
                print("\n" + "No new messages found")

        # Sleep to avoid it looping too quick
        if not stop_chatbot:
            sleep(UserPresets.loopDelay)


# logic?
# /pp fstop - stops bot completely, you'd need to add bot again for it to do anything
# /pp create-breakout - creates breakout based on data it received (takes 1 min to listen to command.)
# /pp start-breakout - starts breakout rooms

start_chatbot()
