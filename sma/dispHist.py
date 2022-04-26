# -*- coding: utf-8 -*-
"""
Created on Mon Oct 18 17:43:48 2021

@author: rfantasia
"""
import numpy as np
from PIL import Image
import argparse
import cv2
ftifpath='C:/Users/rfantasia/anacondaProjects/ffp/102221_analysis/Amanda/'
ftif=ftifpath+'2021-10-07_ORBIT_Cas9_Stem1_PreliminaryTests_Ex0_Only_ORBIT_10ms_100Hz_5000Frames_posXY0_channels_t0_posZ0_1'


def disp_hist(file):

    refPt = []
    sets=file+'trdir/histsets'
    filename=file+'trdir/hist2d'
    infor=file+'trdir/histpar'

    fileptr = open(filename+'.stack','rb')
    fileptrSets = open(sets+'.list','rb')
    fileptrInfo = open(infor+'.info','rb')
    frnum=1

  
    frame = np.fromfile(fileptr,dtype='int32')
    histlist=np.fromfile(fileptrSets,dtype='int32')
    histinfo=np.fromfile(fileptrInfo,dtype='int32')
    histsearch=np.reshape(histlist,[len(histlist)//3,3])
    print(frame.shape)
    print(histlist.shape)
    print(histinfo.shape)

    histnum=histinfo[3]
    histpercol=20
    histrow=int(histnum/histpercol)    #histinfo[3]
    res=histinfo[0]


    fileptr.seek(0) 

    result = Image.new('F', (histrow*res,histpercol*res))
    for j in range (0,histrow):
        for i in range (0,histpercol):
        #print((i+(j*histpercol)))
            fileptr.seek((i+(j*histpercol))*res*res*4) 
            frame2 = np.fromfile(fileptr,dtype='int32',count=res*res)
            frame2 = np.reshape(frame2,[res,res])
            frame2 = np.transpose(frame2)
            frame2 = np.rot90(np.rot90(np.rot90(frame2)))
            frame2=frame2
            im2 =Image.fromarray(frame2)
        #print(i)
            result.paste(im2, box=((j*res),(i*res)))
       
    
   
    # j=j+1
    
# result = Image.new('F', (res*2, res))

# result.paste(im=im2, box=(res, 0))
    img = np.array(result)

#result.show(result)
    avgnonzero = img[np.nonzero(img)].mean() #this might be bad practice
    img=np.array((img/avgnonzero)*255).astype('uint8')#but here i am sclaing my image based on avg non zero to gray scale 




    refPt = []
    
    grayImage = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    heatmap = cv2.applyColorMap(grayImage, cv2.COLORMAP_MAGMA)
    def click_event(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            print(x+(k*histperrow*30),",",y)
            refPt.append([x+(k*histperrow*30),y])
            # l=[(x+(k*histperrow*30)),y]
            # print(l)
            # l=np.array(l)
            # lnp=l//30
            # tes=lnp*[histpercol,1]
            # tes=sum(tes)
            # testt=histsearch[x]
            # print(testt)
            font = cv2.FONT_HERSHEY_SIMPLEX
            strXY = str(x+(k*histperrow*30) )+", "+str(y)
            cv2.putText(imgcrop, strXY, (x,y), font, 0.5, (255,0,0), 2)
            cv2.imshow('heatmap',imgcrop)
    
    savePt=[]
    histperrow=20
    t=img.size//(600*histperrow*30)
    for k in range (0,t):
        imgcrop=heatmap[0:(histpercol*30),k*histperrow*30:(k+1)*30*histperrow]
        cv2.imshow('heatmap',imgcrop )
        cv2.namedWindow('heatmap')
        cv2.setMouseCallback("heatmap", click_event)
        key=cv2.waitKey(0)
        if key == 27: break
        

    cv2.destroyAllWindows()
    refptnp=np.array(refPt)
    refsc=refptnp//30
    test=refsc*[histpercol,1]
    sum_of_rows = np.sum(test, axis = 1)
    out=histsearch[sum_of_rows]
    #return refptnp , refsc , test ,sum_of_rows , out
#reverse for loop

#calling the mouse click event


# cv2.namedWindow('image')
# cv2.setMouseCallback('image', on_click)
#print(test)
# for i in range (0,histnum):    
#         curhist = (resolution,resolution))