from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from GUI.utils import *
import sys
import os
import cv2


class fileWorker(QThread):
    sinOut = pyqtSignal(str)

    def __init__(self, canvas):
        super().__init__()
        self.path = None
        self.canvas = canvas
    
    def load_path(self, path):
        self.path = path
    
    def run(self):
        self.load_frames()

    def load_frames(self):
        if os.path.isdir(self.path):
            self.canvas.imgFrames = []
            files = get_image_list(self.path)
            numFrames = len(files)
            for i, file in enumerate(files):
                frame = cv2.imread(file)
                self.canvas.imgFrames.append(frame)
                if i % 30 == 0:
                    self.sinOut.emit("已加载图片帧 {} / {}".format(i, numFrames))
        else:
            self.canvas.imgFrames = []
            self.canvas.videoCapture = cv2.VideoCapture(self.path)

            numFrames = self.canvas.videoCapture.get(7)
            rval = self.canvas.videoCapture.isOpened()
            i = 0
            while rval:
                rval, frame = self.canvas.videoCapture.read()
                if rval:
                    self.canvas.imgFrames.append(frame)
                if i % 50 == 0:
                    self.sinOut.emit("已加载图片帧 {} / {}".format(i, numFrames))
                i += 1
            # self.canvas.videoCapture = cv2.VideoCapture(self.path)
            # fps = 5
            # total_frame = self.canvas.videoCapture.get(cv2.CAP_PROP_FRAME_COUNT)  # 视频的总帧数
            #
            # for i in range(int(total_frame)):
            #     ret = self.canvas.videoCapture.grab()
            #     if not ret:
            #         print("Error grabbing frame from movie!")
            #         break
            #     if i % fps == 0:
            #         ret, frame = self.canvas.videoCapture.retrieve()
            #         if ret:
            #             self.canvas.imgFrames.append(frame)
            #         else:
            #             print("Error retrieving frame from movie!")
            #             break
            #     if i % 30 == 0:
            #         self.sinOut.emit("已加载图片帧 {} / {}".format(i, numFrames))
        self.sinOut.emit("图片帧已加载完成")