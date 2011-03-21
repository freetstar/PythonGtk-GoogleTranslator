#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygtk
import gtk
import gtk.glade
import urllib
import urllib2
import threading
import re
import sys

class translation(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self,name='translation')
        self.url="http://www.google.com/dictionary?langpair=%s|%s&q=%s&hl=en&aq=f"
        self.text=None
        self.trans_in=''
        self.trans_out=''
        self.text_in=None
        self.text_out=None

    def getText(self,widget):
        return widget.get_text()

    def setText(self,widget,text=''):
        widget.set_text(text)
        return True

    def run(self):
        self.setText(self.text_out,'正在翻译')
        self.data=(self.url % (self.trans_in,self.trans_out,self.getText(self.text_in)))
        request=urllib2.Request(self.data)
        conn=urllib2.urlopen(request)
        res=conn.read()
        res=re.findall('<meta name="description".*>',res)
        res=''.join(res)
        tmp1=re.compile('[<[^>].*:').sub("",res)
        tmp2=re.compile('-[^>].*>').sub("",tmp1)
        self.setText(self.text_out,tmp2)

class googleTrans():

    def __init__(self):
        self.flags=True
        self.ui_file='./pyGT.glade'
        self.wTree=gtk.glade.XML(self.ui_file,'window1')
        self.window = self.wTree.get_widget ("window1")
        self.button =self.wTree.get_widget("button1")
        self.window.set_default_size(400,400)
        self.window.set_position(gtk.WIN_POS_CENTER)
        dic={'on_window1_destroy':gtk.main_quit,\
             'on_zh2en_toggled':self.zh2en,\
             'on_en2zh_toggled':self.en2zh,\
             'on_button1_clicked':self.tran
            }
        self.wTree.signal_autoconnect(dic)
        self.window.show_all()

    def zh2en(self,widget):
        self.flags=False
    def en2zh(self,widget):
        self.flags=True

    def tran(self,widget):
        t=translation()
        t.text_in=self.wTree.get_widget('entry1')
        t.text_out=self.wTree.get_widget('entry2')
        if self.flags:
            t.trans_in='en'
            t.trans_out='zh-CN'
        else:
            t.trans_in='zh-CN'
            t.trans_out='en'
        t.setDaemon(True)
        t.start()
    def main(self):
        gtk.main()

if __name__=='__main__':
    gtk.gdk.threads_init()
    app=googleTrans()
    app.main()

