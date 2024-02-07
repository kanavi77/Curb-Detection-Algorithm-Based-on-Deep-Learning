 
import glob
import os
import cv2
import time


 
def picvideo(path, size):
    filelist = os.listdir(path)   
    filelist.sort(key=lambda x: int(x[:-4]))   
    '''
    fps:
    帧率：1秒钟有n张图片写进去[控制一张图片停留5秒钟，那就是帧率为1，重复播放这张图片5次] 
    如果文件夹下有50张 534*300的图片，这里设置1秒钟播放5张，那么这个视频的时长就是10秒
    '''
    fps =10
    file_path = r"./" + "test.mp4"   
    fourcc = cv2.VideoWriter_fourcc('D', 'I', 'V', 'X')   

    video = cv2.VideoWriter(file_path, fourcc, fps, size)

    for item in filelist:
        if item.endswith('.jpg'):   
            item = path + '/' + item
            img = cv2.imread(item)   
            video.write(img)   

    video.release()   

picvideo('./trainyolo_curb/', (480, 272))