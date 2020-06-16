import numpy as np
import cv2
import random

def collision_with_apple(appleposition, scores):
    appleposition = [random.randrange(1,50)*10,random.randrange(10,60)*10]
    for position in snake_position:
        if appleposition == position:
            appleposition = [random.randrange(1, 50) * 10, random.randrange(10, 60) * 10]
    scores += 1
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(img, 'Your Score is {}'.format(scores), (50, 50), font, 10, (0, 255, 255), 2, cv2.LINE_AA)
    return appleposition, scores

def collision_with_boundaries(snakehead):
    if snakehead[0]>=500 or snakehead[0]<0 or snakehead[1]>=600 or snakehead[1]<100 :
        return 1
    else:
        return 0

def collision_with_self(snakeposition):
    if len(snakeposition) !=0:
        snake_head = snake_position[0]
        if snake_head in snake_position[1:]:
            return 1
        else:
            return 0


img = np.zeros((600, 500, 3), dtype='uint8')
color = (255,255,255)
#cv2.rectangle(img,(0,100),(img.shape[1],0),color,-1)
# Initial Snake and Apple position
snake_position = [[250, 250], [240, 250], [230, 250]]
apple_position = [random.randrange(1, 50) * 10, random.randrange(10, 60) * 10]

for position in snake_position:
    if apple_position == position:
        apple_position = [random.randrange(10, 50) * 10, random.randrange(10, 60) * 10]

score = 0
prev_button_direction = 1
button_direction = 1
snake_head = [250, 250]

cv2.namedWindow('Snake Game',cv2.WINDOW_NORMAL)
cv2.resizeWindow('Snake Game',500,600)

while True:
    color = (255, 255, 255)
    cv2.rectangle(img, (0, 100), (img.shape[1], 0), color, -1)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(img, 'Your Score is {}'.format(score), (120, 50), font, 1, (0, 0, 0), 2, cv2.LINE_AA)
    cv2.namedWindow('Snake Game',cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Snake Game',500,600)
    cv2.imshow('Snake Game', img)
    #cv2.waitKey(1)
    img = np.zeros((600, 500, 3), dtype='uint8')
    img[:] = [100,100,0]
    # Display Apple
    cv2.rectangle(img, (apple_position[0], apple_position[1]), (apple_position[0] + 10, apple_position[1] + 10),
                  (0, 255, 255), 2)
    # Display Snake
    for position in snake_position:
        cv2.rectangle(img, (position[0], position[1]), (position[0] + 10, position[1] + 10), (0, 0, 255), 1) # snake color

    # Takes step after fixed time
    k = cv2.waitKey(150)

    # 0-Left, 1-Right, 3-Up, 2-Down, q-Break
    # a-Left, d-Right, w-Up, s-Down

    if (k == ord('4') or k == ord('a')) and prev_button_direction != 1:
        button_direction = 0
    elif (k == ord('6') or k == ord('d')) and prev_button_direction != 0:
        button_direction = 1
    elif (k == ord('8') or k == ord('w')) and prev_button_direction != 2:
        button_direction = 3
    elif (k == ord('2') or k == ord('s')) and prev_button_direction != 3:
        button_direction = 2
    elif k == ord('p'):
        cv2.waitKey(0)
    elif k == ord('q'):
        break
    else:
        button_direction = button_direction
    prev_button_direction = button_direction

    # Change the head position based on the button direction
    if button_direction == 1:
        snake_head[0] += 10
    elif button_direction == 0:
        snake_head[0] -= 10
    elif button_direction == 2:
        snake_head[1] += 10
    elif button_direction == 3:
        snake_head[1] -= 10

    # Increase Snake length on eating apple
    if snake_head == apple_position:
        apple_position, score = collision_with_apple(apple_position, score)
        snake_position.insert(0, list(snake_head))

    else:
        snake_position.insert(0, list(snake_head))
        if len(snake_position) !=0:
            snake_position.pop()

    # On collision kill the snake and print the score
    if  collision_with_self(snake_position) == 1:
        font = cv2.FONT_HERSHEY_SIMPLEX
        img = np.zeros((500, 500, 3), dtype='uint8')
        cv2.putText(img, 'Game over!', (140, 230), font, 1, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.imshow('Snake Game', img)

        cv2.putText(img, 'Your Score is {}'.format(score), (120, 270), font, 1, (255, 255, 255), 2,cv2.LINE_AA)

        cv2.namedWindow('Snake Game', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Snake Game', 600, 500)

        cv2.imshow('Snake Game', img)
        cv2.waitKey(2500)
        cv2.imwrite('D:/downloads/ii.jpg', img)
        break

    if collision_with_boundaries(snake_head) == 1:
        if snake_head[0]>=500:
            snake_head[0] = snake_head[0] % 500
            snake_position.insert(0, list(snake_head))
            if len(snake_position) != 0:
                snake_position.pop()

        elif snake_head[0]<=0:
            snake_head[0] = snake_head[0] + 500
            snake_position.insert(0, list(snake_head))
            if len(snake_position) != 0:
                snake_position.pop()

        elif snake_head[1]>=600:
            snake_head[1] = snake_head[1] % 500
            snake_position.insert(0, list(snake_head))
            if len(snake_position) != 0:
                snake_position.pop()

        elif snake_head[1]<=100:
            snake_head[1] = snake_head[1] + 500
            snake_position.insert(0, list(snake_head))
            if len(snake_position) != 0:
                snake_position.pop()

    if cv2.getWindowProperty('Snake Game', cv2.WND_PROP_AUTOSIZE) ==-1:
        break


cv2.destroyAllWindows()
