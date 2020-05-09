# Zoom Chatbot
My first python script, an attempt at a chatbot for zoom. 

# Current state?
- Version 1, not fully complete. (Missing functionality to make it work for big calls, scroll down for details)
- Currently don't have time to clean up the script. Hoping to clean it up, and python experts please help me clean it up. (I am eager to learn!)

# How it is suppose to work?
- I generate an array of breakout rooms with users, based on what users type in the chat (I read the autosave zoom file, it auto saves every minute)
Once started, it opens zoom, takes a screenshot. Grabs coordinates of breakout room list, takes another screenshot of just that window with the mss library.
cv2 library loads the image, pytesseract library reads the image and translates it to text.
- I filter down the returned value, combine letters to words (it also comes with coordinates).
- I then have the coordinates of all the words in the breakout rooms window (and where the assign buttons are)
- It then goes through the my array of breakout rooms and their users: for example it starts with room 1, it will click the assign button: screenshot the assign window, look for certain user matches, clicks them if there is a match, and so on.
- Add that with a few simple scroll functionalities, and it can assigns as many users as you want to each room. (beware, when more than 8 users, you either need to scroll on the assigns list or use the search).


# Libraries needed to run the script?
- mss (used to take screenshots of the computer)
- cv2 (loads images)
- pytesseract (character recognition from images, translate images to words. Works in combination with cv2)
- pyautogui (used to find coordinates of images on the screen, and to move/click on them)

# What else is needed?
- You need to set your Zoom portal to autosave the chat. Details found here: (https://support.zoom.us/hc/en-us/articles/115004792763-Saving-In-Meeting-Chat)
- Zoom account that is a host, with breakout feature.


# Missing functionalities (critical)
- Assign users when there are more than 8 people. Add scroll or search, when there are more than 8 users, it becomes a list with a search). Currently this feature is the one last element I need to get it to work for big calls.


# Contribute?
- Id love for people to contirbute, it would be greatly appreciated!
