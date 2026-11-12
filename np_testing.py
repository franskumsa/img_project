import numpy as np
import cv2
import renewed_storage
req_img=input('enter the image file path')
def get_imgcontour(img_path):
    #reading the image and converting it to gray
    try:
        img=cv2.imread(img_path)
        if len(img.shape)==3:
            gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        else:
            gray=img
    except IOError:
        print('It seems like the file is unreadable')
    _,thresh=cv2.threshold(gray,0,255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    contour,_=cv2.findContours(thresh,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contour:
        raise ValueError ("the image has no sketch in it")
    
    return max(contour, key=cv2.contourArea)
def check_img(req_img):
    img_contour=get_imgcontour(req_img)
    functionExitFlag=0;
    for image_name, img_path in renewed_storage.image_dict.img_dict.items():
        if functionExitFlag==1:
            break;
        if isinstance(img_path,(dict)):
            for image_name2,img_path2 in img_path.items():
                if functionExitFlag==1:
                            break;
                comparison_contour=get_imgcontour(str(img_path2))
                if cv2.matchShapes(comparison_contour, img_contour,cv2.CONTOURS_MATCH_I1,0.0)<0.5:
                    print(f'the shape is most likely {image_name}')
                    functionExitFlag+=1

        else:
            comparison_contour=get_imgcontour(str(img_path))
            if cv2.matchShapes(comparison_contour,img_contour,cv2.CONTOURS_MATCH_I1,0.0)<0.5:
                print(f'The shape is most likely {image_name}')
                functionExitFlag+=1
    if functionExitFlag==0:
         print('There is no matching shape in database')
check_img(req_img)
        


