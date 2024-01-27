import cv2
import mediapipe as mp
from tkinter import *       
import random
import threading
import winsound
def tic():
    winsound.PlaySound("tic.wav",winsound.SND_FILENAME)

def next_turn(row,column):
    global player

    if buttons[row][column]['text'][0] == "[" and check_winner() is False:

        if player == players[0]:

            buttons[row][column]['text'] = player

            if check_winner() is False:
                player = players[1]
                label.config(text=(players[1]+" turn"))

            elif check_winner() is True:
                label.config(text=(players[0]+" wins"))

            elif check_winner() == "Tie":
                label.config(text="Tie!")

        else:

            buttons[row][column]['text'] = player

            if check_winner() is False:
                player = players[0]
                label.config(text=(players[0]+" turn"))

            elif check_winner() is True:
                label.config(text=(players[1]+" wins"))

            elif check_winner() == "Tie":
                label.config(text="Tie!")

def check_winner():
    for row in range(3):
        if buttons[row][0]['text'] == buttons[row][1]['text'] == buttons[row][2]['text']:
            buttons[row][0].config(bg="green")
            buttons[row][1].config(bg="green")
            buttons[row][2].config(bg="green")
            return True

    for column in range(3):
        if buttons[0][column]['text'] == buttons[1][column]['text'] == buttons[2][column]['text']:
            buttons[0][column].config(bg="green")
            buttons[1][column].config(bg="green")
            buttons[2][column].config(bg="green")
            return True

    if buttons[0][0]['text'] == buttons[1][1]['text'] == buttons[2][2]['text']:
        buttons[0][0].config(bg="green")
        buttons[1][1].config(bg="green")
        buttons[2][2].config(bg="green")
        return True

    elif buttons[0][2]['text'] == buttons[1][1]['text'] == buttons[2][0]['text']:
        buttons[0][2].config(bg="green")
        buttons[1][1].config(bg="green")
        buttons[2][0].config(bg="green")
        return True

    elif empty_spaces() is False:

        for row in range(3):
            for column in range(3):
                buttons[row][column].config(bg="yellow")
        return "Tie"

    else:
        return False


def empty_spaces():

    spaces = 9

    for row in range(3):
        for column in range(3):
            if buttons[row][column]['text'][0] != "[":
                spaces -= 1

    if spaces == 0:
        return False
    else:
        return True

def new_game():

    global player

    player = random.choice(players)

    label.config(text=player+" turn")

    for row in range(3):
        for column in range(3):
            buttons[row][column].config(text="["+str(row+1)+","+str(column+1)+"]",bg="#F0F0F0")


def cam():
    cap = cv2.VideoCapture(0)
    mpHands = mp.solutions.hands
    hands = mpHands.Hands()
    mpDraw = mp.solutions.drawing_utils
    fingerCoordinates = [(8, 6), (12, 10), (16, 14), (20, 18)]
    thumbCoordinate = (4,2)
    rep=[]
    cord=[0,0]
    while True:
        success, img = cap.read()
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(imgRGB)
        multiLandMarks = results.multi_hand_landmarks

        if multiLandMarks:
            handPoints = []
            for handLms in multiLandMarks:
                mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

                for idx, lm in enumerate(handLms.landmark):
                    # print(idx,lm)
                    h, w, c = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    handPoints.append((cx, cy))

            for point in handPoints:
                cv2.circle(img, point, 10, (0, 0, 255), cv2.FILLED)

            upCount = 0
            
            for coordinate in fingerCoordinates:
                if handPoints[coordinate[0]][1] < handPoints[coordinate[1]][1]:
                    upCount += 1
            if handPoints[thumbCoordinate[0]][0] > handPoints[thumbCoordinate[1]][0]:
                upCount += 1
            if upCount!=0:
                cv2.putText(img,"00:00:"+str(15-len(rep))+"S", (460,30), cv2.FONT_HERSHEY_PLAIN, 2, (255,0,0), 3)
            cv2.putText(img,player+" turn", (200,30), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,0), 5)
            if cord[0]==0:
                cv2.putText(img, "["+str(upCount)+",]", (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,0), 5)
            
            else:
                cv2.putText(img, "["+str(cord[0])+","+str(upCount)+"]", (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,0), 5)
            if len(rep)==0:
                rep.append(upCount)
            else:
                if upCount==rep[-1]:
                    rep.append(upCount)
                    if len(rep)==15:
                        if 1<=rep[0]<=3:
                            if(cord[0]==0):
                                cord[0]=rep[0]
                                rep=[]
                            else:
                                cord[1]=rep[0]
                                sound = threading.Thread(target=tic)
                                sound.start()
                                next_turn(cord[0]-1,cord[1]-1)
                                cord=[0,0]
                                rep=[]
                        elif rep[0]==5:
                            new_game()
                            rep=[]
                        elif rep[0]==4:
                            cord=[0,0]
                            rep=[]

                else:
                    rep=[]

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

            

        cv2.imshow("tic tac toe camera", img)
        cv2.waitKey(1)
    cap.release() 
    cv2.destroyAllWindows()


opencv = threading.Thread(target=cam)
opencv.start()

window = Tk()
window.title("Tic-Tac-Toe")
players = ["x","o"]
player = random.choice(players)
buttons = [[0 for i in range(3)]for i in range(3)]
label = Label(text=player + " turn", font=('consolas',40))
label.pack(side="top")
reset_button = Label(text="5 to restart", font=('consolas',20))
reset_button.pack(side="top")
frame = Frame(window)
frame.pack()
for row in range(3):
    for column in range(3):
        buttons[row][column] = Button(frame, text="["+str(row+1)+","+str(column+1)+"]",font=('consolas',40), width=5, height=2)
        buttons[row][column].grid(row=row,column=column)
window.mainloop()
