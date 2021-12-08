#coding=utf-8
import autopy
import time
import win32api
import win32con

from autopy import bitmap

win32api.keybd_event(18,0,0,0)  #alt鍵位碼是18
win32api.keybd_event(9,0,0,0)  #tab鍵位碼是9
time.sleep(0.5)
win32api.keybd_event(13,0,0,0)  #enter鍵位碼是13

win32api.keybd_event(18,0,win32con.KEYEVENTF_KEYUP,0) #釋放按鍵
win32api.keybd_event(9,0,win32con.KEYEVENTF_KEYUP,0)
win32api.keybd_event(13,0,win32con.KEYEVENTF_KEYUP,0)
time.sleep(2)

print(autopy.screen.size())
print(autopy.screen.scale())

def mousemove_click(x,y):
    scale = autopy.screen.scale()
    a = autopy.mouse.smooth_move(x / scale, y / scale)
    print(a)
    autopy.mouse.click()

a = autopy.bitmap.capture_screen(None)
a.save('screen.png')    #截取当前屏幕，在本文件目录下生成了一个名为some的png图片
ab = bitmap.Bitmap.open('./screen.png')
bmp = bitmap.Bitmap.open('./pic/main.jpg')
# print(bmp.bounds)
result = ab.find_bitmap(bmp)
print(result)



mousemove_click(900,1000)  # 主線的坐標
    # mousemove_click(1358,504)  # 競技場"前往"的坐標
    # time.sleep(20)#從天墉城城中心/其他地圖走到競技使者花費20s
    # mousemove_click(1334, 650)  # 競技使者對話框中的競技場的坐標




# photo1 = at.bitmap.Bitmap.open('screen.png')
# photo2 = at.bitmap.Bitmap.open('1.png')

# i=photo1.find_every_bitmap(photo2)  #在图片1中寻找图片2的坐标
# print(i)    #打印坐标
# at.mouse.smooth_move(1269.0, 76.0)
