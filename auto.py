import autopy as at
import time
import win32api
import win32con

def execute():
    print(at.screen.scale())
    print(at.screen.size())     #屏幕的大小
    switch()

def switch():
    win32api.keybd_event(18,0,0,0)  #alt鍵位碼是18
    win32api.keybd_event(9,0,0,0)  #tab鍵位碼是9
    time.sleep(0.5)
    win32api.keybd_event(13,0,0,0)  #enter鍵位碼是13
    

    win32api.keybd_event(18,0,win32con.KEYEVENTF_KEYUP,0) #釋放按鍵
    win32api.keybd_event(9,0,win32con.KEYEVENTF_KEYUP,0)
    win32api.keybd_event(13,0,win32con.KEYEVENTF_KEYUP,0)
    time.sleep(2)

#主線
win32api.keybd_event(81,0,0,0)  #Q鍵位碼是81

#SKIP
win32api.keybd_event(80,0,0,0)  #P鍵位碼是80


a = at.bitmap.capture_screen(None)

a.save('screen.png')    #截取当前屏幕，在本文件目录下生成了一个名为some的png图片

photo1 = at.bitmap.Bitmap.open('screen.png')
photo2 = at.bitmap.Bitmap.open('1.png')

i=photo1.find_every_bitmap(photo2)  #在图片1中寻找图片2的坐标
print(i)    #打印坐标
at.mouse.smooth_move(1269.0, 76.0)

execute()