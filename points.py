import cv2

def click_event(event, x, y, flags, params):
    global current_list
    
    if event == cv2.EVENT_LBUTTONDOWN:
        print(f'New point: ({x}, {y})')
        current_list.append([x, -y])
        cv2.circle(resized_image, (x, y), 5, (222, 111, 0), -1)
        cv2.imshow('image', resized_image)

    elif event == cv2.EVENT_RBUTTONDOWN:
        if current_list:
            print(f'Segment end at previous point')
            with open('./temp/x_val.txt', 'a') as file:
                file.write(str([coordinate[0] for coordinate in current_list]) + '\n')
            with open('./temp/y_val.txt', 'a') as file:
                file.write(str([coordinate[1] for coordinate in current_list]) + '\n')
            current_list = []
            cv2.circle(resized_image, (x, y), 5, (111, 0, 222), -1)
            cv2.imshow('image', resized_image)
        else:
            print("Cannot end segment without clicking left mouse button first.")

# clear files, before adding new coordinates
open('./temp/x_val.txt', 'w').close()
open('./temp/y_val.txt', 'w').close()

image = cv2.imread('./in/image.png', 1)
resized_image = cv2.resize(image, None, fx=1.7, fy=1.7)

cv2.imshow('image', resized_image)
cv2.setMouseCallback('image', click_event)

current_list = []

cv2.waitKey(0)
cv2.destroyAllWindows()

# combine data into dane.txt
with open('./temp/x_val.txt') as x_file, open('./temp/y_val.txt') as y_file, open('./dane/dane_new.txt', 'w') as dane_file:
    for x_line, y_line in zip(x_file, y_file):
        x_vals = eval(x_line.strip())
        y_vals = eval(y_line.strip())
        
        k = len(x_vals)
        M = 81
        
        line1 = [round(i / (k-1), 3) for i in range(k)]
        dane_file.write(str(line1) + '\n')
        
        dane_file.write(x_line)
        
        dane_file.write(y_line)
        
        u_vals = [round(i / (M-1), 3) for i in range(M)]
        # we can increase/decrease accuracy by adjusting M manually ->
        # -> change the (segment number * 4th) line to a different list of numbers limited by chosen M
        # (generate the list in external code, then replace that line with it)
        
        dane_file.write(str(u_vals) + '\n')
