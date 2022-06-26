import os
import cv2
import time
import threading
import queue
import imutils

class RtspCapture:
    def __init__(self, name):
        self.name = name
        self.cap = cv2.VideoCapture(self.name)
        self.q = queue.Queue()
        t = threading.Thread(target=self._reader)
        t.daemon = True
        t.start()

  # read frames as soon as they are available, keeping only most recent one
    def _reader(self):
        while True:
            try:
                ret, frame = self.cap.read()
                if not self.q.empty():
                    try:
                        self.q.get_nowait()   # discard previous (unprocessed) frame
                    except queue.Empty:
                        pass
                self.q.put(frame)
            except :
                print("reconnect camera")
                print(2)
                self.cap=cv2.VideoCapture(self.name)



            # if (self.cap.read()[0] == False) :
            #         print("not connected camera")
            #         while 1:
            #             self.cap=cv2.VideoCapture(self.name)
            #             if (self.cap.isOpened()):
            #                 print("connected camera")
            #                 # time.sleep(1)
            #                 break
            # else:
            #     ret, frame = self.cap.read()
            #     if not ret:
                    
            #         print("reconnect camera")
            #         while 1:
            #             self.cap=cv2.VideoCapture(self.name)
            #             if (self.cap.isOpened()):
            #                 print("reconnect camera success")
            #                 # time.sleep(1)
            #                 break
                   
            #     if not self.q.empty():
            #         try:
            #             self.q.get_nowait()   # discard previous (unprocessed) frame
            #         except queue.Empty:
            #             pass
            #     self.q.put(frame)

    def read(self):
        return self.q.get()




















# class VideoCapture:
#     def __init__(self, name):
#         self.name = name
#         self.cap = cv2.VideoCapture(self.name)
#         self.q = queue.Queue()
#         t = threading.Thread(target=self._reader)
#         t.daemon = True
#         t.start()

#   # read frames as soon as they are available, keeping only most recent one
#     def _reader(self):
#         while True:
#             if (self.cap.read()[0] == False) :
#                 try :
#                     print("not connected camera")
#                     self.cap=cv2.VideoCapture(self.name)
#                 except :
#                     pass
#                 # continue
#             else:
#                 ret, frame = self.cap.read()
#                 if not ret:
#                     try :
#                         print("reconnect camera")
#                         self.cap = cv2.VideoCapture(self.name)
#                     # continue
#                     except :
#                         pass
#                 if not self.q.empty():
#                     try:
#                         self.q.get_nowait()   # discard previous (unprocessed) frame
#                     except queue.Empty:
#                         pass
#                 self.q.put(frame)

#     def read(self):
#         return self.q.get()