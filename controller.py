import cv2
import mediapipe as mp
from pynput.keyboard import Key , Controller

mphands=mp.solutions.hands  # to identify hands
draw=mp.solutions.drawing_utils  # to draw the landmarks

Hands=mphands.Hands(max_num_hands=1)
keyboard = Controller()

video=cv2.VideoCapture(0)
video.set(3, 240)
video.set(4, 420)
while True:
    suc,image=video.read()
    image=cv2.flip(image,1)   # to flip mirror image
    image=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)  # better results for mediapipe with RGB images
    results=Hands.process(image)   # object created # process function   
    image=cv2.cvtColor(image,cv2.COLOR_RGB2BGR)    
    tipids=[4,8,12,16,20] 
    lmlist=[]                        
    if results.multi_hand_landmarks:   # multi_hand_landmarks - attribute to get landmarks
        for hand_landmarks in results.multi_hand_landmarks:
            for id,lm in enumerate(hand_landmarks.landmark):
                cx=lm.x   # takes x values from lm   # lm here is object
                cy=lm.y   # takes y values from lm
                lmlist.append([id,cx,cy])   # [0, 0.1449297070503235, 0.9852817058563232], [1, 0.28413084149360657, 0.9510334730148315]
                #print(lmlist)

            if len(lmlist)!=0 and len(lmlist)==21:
                    fingerlist=[]

                    if lmlist[12][1] > lmlist[20][1]:   # x value of 12 > x value of 20 # right hand   
                        if lmlist[tipids[0]][1] > lmlist[tipids[0]-1][1]: # x value of 4 > x value of 3 [open]
                           fingerlist.append(1)
                        else:
                           fingerlist.append(0)
                    else:        # left hand
                        if lmlist[tipids[0]][1] < lmlist[tipids[0]-1][1]:  # x value of 4 < x value of 3 [open]
                           fingerlist.append(1)
                        else:
                            fingerlist.append(0)

                    #other fingers
                    for i in range(1,5):    # for 4 fingers except thumb
                        if lmlist[tipids[i]][2] < lmlist[tipids[i]-2][2]:   # if y value of finger tip(8,12..) < y value of middle point(6,10..)-[not closed]
                           fingerlist.append(1)   # append 1 if open
                        else:
                            fingerlist.append(0)  # append 0 if closed 
    
                    print(fingerlist)

                    if fingerlist==[0,0,0,0,0]:
                      keyboard.press(Key.left) 
                      keyboard.release(Key.right)
                      cv2.putText(image,'Brake',(80,450),cv2.FONT_HERSHEY_COMPLEX,2,(0,0,255),2,)
                    elif fingerlist==[1,1,1,1,1]:
                      keyboard.press(Key.right)
                      keyboard.release(Key.left)
                      cv2.putText(image,'Go',(80,450),cv2.FONT_HERSHEY_COMPLEX,2,(0,255,0),2,)

            draw.draw_landmarks(image,hand_landmarks,mphands.HAND_CONNECTIONS,draw.DrawingSpec(color=(230,123,12),thickness=2,circle_radius=2),draw.DrawingSpec(color=(0,0,0),thickness=2))         
    else:
        keyboard.release(Key.left)
        keyboard.release(Key.right)


    cv2.imshow('Controller',image)
    if cv2.waitKey(1) & 0XFF==ord('q'):
        break
video.release()
cv2.destroyAllWindows()    
