import curses
from time import sleep
from cv2 import VideoCapture, cvtColor, COLOR_BGR2RGB, imshow, waitKey, destroyAllWindows
from PIL import Image
from shutil import get_terminal_size
from threading import Thread
from moviepy.editor import VideoFileClip

filename = "bad_apple@2160p60fps.mp4"

def resize_image(image: Image):
    terminal_width, terminal_height = get_terminal_size()
    new_width = terminal_width - 2  # Subtract 2 from the width for borders
    new_height = terminal_height - 2  # Subtract 2 from the height for borders
    return image.resize((new_width, new_height))

# Function to map pixels to characters and render in console
def map_pixels_to_characters(image: Image, stdscr: curses.window):
    characters = [' ', '.', ':', '-', '=', '+', '*', '#', '%', '@']
    image = resize_image(image)
    pixels = image.load()

    for y in range(image.height):
        for x in range(image.width):
            r, g, b = pixels[x, y]
            intensity = (r + g + b) // 3
            index = int((intensity / 255) * (len(characters) - 1))
            char = characters[index]
            stdscr.addch(y, x, char)  # Update character at (y, x) position in console

def play_ascii():
    # Setup ncurses
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)
    curses.curs_set(0)

    # Read video file
    video = VideoCapture(filename)

    if not video.isOpened():
        print("Error opening video file.")
        exit()

    success, image = video.read()

    # Render video in console
    while success:
        map_pixels_to_characters(Image.fromarray(cvtColor(image, COLOR_BGR2RGB)), stdscr)
        stdscr.refresh()
        sleep(0.009)

        success, image = video.read()

    # Close ncurses
    curses.echo()
    curses.nocbreak()
    stdscr.keypad(False)
    curses.endwin()

def play_video_cv():
    video = VideoCapture(filename)

    if not video.isOpened():
        print("Error opening video file.")
        exit()

    while True:
        success, frame = video.read()
        if not success:
            break

        imshow("Bad Apple", frame)
        if waitKey(15) & 0xFF == ord('q'):
            break

    video.release()
    destroyAllWindows()

def play_video():
    video = VideoFileClip(filename)
    video.preview(fps=60)

if __name__ == "__main__":
    video_thread = Thread(target=play_video)
    video_thread.start()

    play_ascii()
    video_thread.join()