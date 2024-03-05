import cv2

class Mark:
    def __init__(self):
        self.__marked = 0
        self.__flag = 0
        self.__ix, self.__iy = 0, 0

    def draw(self, image, number):
        self.image = image
        self.number = number
        self.xyxy = []
        cv2.namedWindow('image')
        cv2.setMouseCallback('image', self.draw_rectangle)
        while (1):
            cv2.imshow('image', self.image)
            if (cv2.waitKey(20) & 0xFF == 13) or self.__marked == self.number:
                break
        cv2.destroyAllWindows()
        return self.xyxy

    def draw_rectangle(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            if self.__flag == 0:
                self.__flag += 1
                self.__ix, self.__iy = x, y
                cv2.circle(self.image, (x, y), 2, (255, 255, 255), -1)
            else:
                self.__flag = 0
                cv2.rectangle(self.image, (self.__ix, self.__iy), (x, y),(255, 255, 255), 2)
                self.xyxy.append([int(min(self.__ix,x)), int(min(self.__iy,y)), int(max(self.__ix,x)), int(max(self.__iy,y))])
                self.__marked += 1