import numpy as np
import cv2
import renewed_storage

req_img=input('enter the image file path: ')
def get_img_contour(img_path):
    
    try:
        
        img=cv2.imread(img_path)
        
        if len(img.shape)==3:
            gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
           
        else:
            gray=img
    except IOError:
        print ('It seems there is a problem loading the file... ')

    _, thresh=cv2.threshold(gray,127,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)# this line converts the gray scale image to black and white image(stored in thresh). since cv2 processes white as the figure INV is used.
    contours,_=cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)#_ is just a place holder since that part of the function output is not needed.
    if not contours:
        raise ValueError('the file has no sketch in it! ')
    return max(contours, key=cv2.contourArea)# contours is a list
def check_contour(req_img):
    
    contour1=get_img_contour(req_img)
    counter=0
    for name,saved_img in renewed_storage.image_dict.img_dict.items():
        if counter==1:
            break
        if isinstance(saved_img,dict):
            #print('the printed is: '+renewed_storage.image_dict[name][saved_img2])
            for second_name,saved_img2 in saved_img.items():
                if counter==1:
                    break
                contour_2=get_img_contour(str(saved_img2))
                if cv2.matchShapes(contour_2 ,contour1,cv2.CONTOURS_MATCH_I1,0.0)<0.5:
                    print(f'the shape is most likely {name}')
                    counter+=1
                else:
                    print('---')
        else:
           # print('the asvd image is: '+saved_img)
            contour0=get_img_contour(saved_img)#saved_img is the name of the image stored in the img_dict.
            if cv2.matchShapes(contour1, contour0,cv2.CONTOURS_MATCH_I1, 0.0)<0.5:
                print(f'the shape is most likely {name}')
                counter+=1
            else:
                print('---') 
    if counter==0:
        print('Unable to determine the component type' 
check_contour(req_img)
