import cv2
import numpy as np

def img_float32(img):
    return img.copy() if img.dtype != 'uint8' else (img/255.).astype('float32')

def over_a(bgimg, fgimg):
    if bgimg[0][0].size==3:
        bgimg=cv2.cvtColor(bgimg,cv2.COLOR_BGR2BGRA)
    if fgimg[0][0].size==3:
        fgimg=cv2.cvtColor(fgimg,cv2.COLOR_BGR2BGRA)
    fgimg, bgimg = img_float32(fgimg),img_float32(bgimg)
    (fb,fg,fr,fa),(bb,bg,br,ba) = cv2.split(fgimg),cv2.split(bgimg)
    color_fg, color_bg = cv2.merge((fb,fg,fr)), cv2.merge((bb,bg,br))
    alpha_fg, alpha_bg = np.expand_dims(fa, axis=-1), np.expand_dims(ba, axis=-1)
    
    color_fg[fa==0]=[0,0,0]
    color_bg[ba==0]=[0,0,0]
    
    a = fa + ba * (1-fa)
    a[a==0]=np.NaN
    color_over = (color_fg * alpha_fg + color_bg * alpha_bg * (1-alpha_fg)) / np.expand_dims(a, axis=-1)
    color_over = np.clip(color_over,0,1)
    color_over[a==0] = [0,0,0]
    
    result_float32 = np.append(color_over, np.expand_dims(a, axis=-1), axis = -1)
    return (result_float32*255).astype('uint8')