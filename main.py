import pyautogui
from tkinter import Tk, Button
from random import randint, uniform
from time import sleep
from math import dist

gologin_pic = "./res/gologin.png"
profile_pic = "./res/profile.png"
confidence = 0.8
cycle = 5
click_count = 10


def human_move_click(x, y, _from = -3, _to = 3):
    x += randint(_from, _to)
    y += randint(_from, _to)
    pyautogui.moveTo(x, y, duration=uniform(0.4, 1.1), tween=pyautogui.easeInOutQuad)
    sleep(uniform(0.1, 0.3))
    pyautogui.click()

def dedupe_boxes(boxes, threshold=20):
    unique = []
    for box in boxes:
        cx, cy = pyautogui.center(box)
        duplicate = False
        for ubox in unique:
            ux, uy = pyautogui.center(ubox)
            if dist((cx, cy), (ux, uy)) < threshold:
                duplicate = True
                break
        if not duplicate:
            unique.append(box)
    return unique

def on_click()-> bool:
    print('starting...')

    screen_width, screen_height = pyautogui.size()
    center_x, center_y = screen_width // 2, screen_height // 2

    for _ in range(cycle):

        profiles_locations = dedupe_boxes(list(pyautogui.locateAllOnScreen(profile_pic, confidence=confidence)))

        if not profiles_locations:
            print('no profiles running, existing..')
            return False
    
        for profile in profiles_locations:
            print(profile)
            x,y = pyautogui.center(profile)
            human_move_click(x,y)

            for _ in range(click_count):
                sleep(uniform(0.2,0.4))
                human_move_click(center_x, center_y, randint(-30, 0), randint(0, 30))
                pyautogui.hotkey('ctrl', '1')
            
            for _ in range(click_count):
                pyautogui.hotkey('ctrl', '2')
                pyautogui.hotkey('ctrl', 'w')
                sleep(uniform(0.2, 0.4))
                pyautogui.hotkey('ctrl', '1')


    gologin_location = pyautogui.locateOnScreen(gologin_pic, confidence=confidence)
    if not gologin_location:
        print('gologin might not be running, exiting...')
        return False
    
    # clicking on gologin
    x,y = pyautogui.center(gologin_location)
    human_move_click(x,y)

    # just return
    return True

def main():
    root = Tk()
    root.title('Bot v0.0.1 preview')
    root.geometry('300x200')
    button = Button(root, text="Start!", command=on_click)
    button.pack(pady=20)
    root.mainloop()

if __name__ == '__main__':
    main()
