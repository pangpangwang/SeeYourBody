#!/usr/bin/env python
"""This file is a app for See Your Body"""

import wx
from func import * 
import numpy as np
import socket
import matplotlib.pylab as pylab
global_data = []

class MainFrame(wx.Frame):
    #-------------------------------------------------
    # 初始化
    def __init__(self, parent=None):
        #---------------------------------------------
        # 构造函数，即初始化，可以根据需要重构
       
       
        wx.Frame.__init__(self, parent, style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)
        #---------------------------------------------
        # 静态部分
        self.Title = "See Your Body"
        self.Size = (800, 500)
        panel = wx.Panel(self) #创建画板
        panel.SetBackgroundColour((215, 84, 85))
        #staturBar = self.CreateStatusBar()
        
        
        button_read = wx.Button(panel, label="Read", pos=(500, 410),
                        size=(80, 40))
        #button_read.SetWindowStyleFlag(wx.NO_BORDER)
        button_read.SetToolTipString('Read the data from the hadware')
        button_read.SetBackgroundColour('white')
        
        button_save = wx.Button(panel, label="Save", pos=(600, 410),
                        size=(80, 40))
        #button_read.SetWindowStyleFlag(wx.NO_BORDER)
        button_save.SetToolTipString('Save the data')
        button_save.SetBackgroundColour('white')
        
        button_exit = wx.Button(panel, label="Quit", pos=(700, 410),
                size=(80, 40)) #将按钮添加到画板
        button_exit.SetToolTipString('Quit the program')
        #button_exit.SetWindowStyleFlag(wx.NO_BORDER)
        button_exit.SetBackgroundColour('white')
        
        ico = wx.Icon('jianshen.ico', wx.BITMAP_TYPE_ICO)
        self.SetIcon(ico)
        
        #---------------------------------------------
        # 动态部分绑定
        #绑定按钮的单击事件
        self.Bind(wx.EVT_BUTTON, self.OnSave, button_save)
        self.Bind(wx.EVT_BUTTON, self.OnRead, button_read)
        self.Bind(wx.EVT_BUTTON, self.OnCloseMe, button_exit)
        #绑定窗口的关闭事件
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
        
        #---------------------------------------------
    #-------------------------------------------------
    # 动态响应
    def OnRead(self, event):
        global global_data
        with open('test package.txt', 'r') as f:
            cBuffer_raw = f.readlines();  # read as a list
        #--------------------------------------------
        # Read data from socket
        #HOST = '124.16.70.139'
        #PORT = 10001
        #s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #s.connect((HOST, PORT))
        #cBuffer_raw = ''
        #while 1:
            #data_rcv = s.recv(1024)
            #if  data_rcv == "over":
                #break        
            #s.sendall('abc')
            #cBuffer_raw = cBuffer_raw + data_rcv
        
        #s.close()
        #print cBuffer_raw
        #----------------------------------------------
        cBuffer_raw =  ''.join(cBuffer_raw);  # covert to str
        cBuffer_raw = cBuffer_raw.split("35")  # split in " "
        cBuffer_raw = cBuffer_raw[1:] # each data frame is one of the elements
        sum_data = []
        
        
        for each_frame in cBuffer_raw:
            each_frame = each_frame.split(" ")[1:-1];
            #print each_frame
            each_frame_data = [];
            for data in each_frame:
                data_str = '0x' + data
                each_frame_data.append(int(data_str, 16));
            each_frame_data_link = link(each_frame_data)
            #print each_frame_data_link
            each_frame_data_link_tran = tran(each_frame_data_link);
            #print each_frame_data_link_tran
            sum_data.extend(each_frame_data_link_tran)
        
        #print sum_data
        sum_data_filter = Filtering(sum_data*10, 4)
        global_data = sum_data_filter
        #pylab.plot(sum_data_filter)
        #pylab.show()
      
    def OnSave(self, event):
        global global_data
        saveFileDialog = wx.FileDialog(self, "Save data file", "", "",
                                           "txt files (*.txt)|*.txt", wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)        
        if saveFileDialog.ShowModal() == wx.ID_CANCEL:
            return
        else:
            f = open(saveFileDialog.GetPath(), 'w+')
            f.write(str(global_data))
            f.close()
    def OnCloseMe(self, event):
        #dlg = wx.MessageDialog(None, 'Are you want to quit the See Your Body?', 'Exit', wx.YES_NO|wx.ICON_QUESTION)
        #result = dlg.ShowModal()
        #if result == wx.ID_YES:
        self.Close(True)
        
            
    def OnCloseWindow(self, event):
        self.Destroy()
    #-------------------------------------------------
class MainApp(wx.App):
    def OnInit(self):
        
        self.frame = MainFrame()
        self.frame.Show()
        self.SetTopWindow(self.frame)
        return True

if __name__ == '__main__':
    app = MainApp()
    #app = wx.PySimpleApp()
    #frame = MainFrame(parent=None, id=-1)
    #app.SetTopWindow(frame)
    #frame.Show()
    
    app.MainLoop()
