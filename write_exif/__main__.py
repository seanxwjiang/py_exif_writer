import piexif
from piexif import ImageIFD # 0th
from piexif import ExifIFD # Exif
from piexif import GPSIFD # GPS
from piexif import InteropIFD #interop
import os,sys
# import numpy as np
import pandas as pd

def lon_lat_to_degree_min_sec(value,flag):
    
    degree=int(value)

    
    minute=int(abs(value-degree)*60)


    second=(abs(value-degree)*60-minute)*60
    
    orient=b'N';
    if flag == 'lon':
        if degree>=0:
            orient=b'E'
        else:
            orient=b'W'
    else:
        if degree>=0:
            orient=b'N'
        else:
            orient=b'S'
            
    
    degree_tuple=(abs(degree),1)
    minute_tuple=(abs(minute),1)
    second_tuple=(int(second*1000000),1000000)
    
    result=(degree_tuple,minute_tuple,second_tuple)

#     print(result[0]+','+result[1]+','+result[2])


    return orient,result;



template_fn='.\\template_img.jpeg'
if not os.path.exists(template_fn):
    print("no template image file(template_img.jpeg). This file must exist and have exif with GPS info");
    sys.exit(0)

logfile='./logs.txt'
try:
    data=pd.read_csv(logfile,header=None,sep='\t');
except:
    print('not log file')
    sys.exit(0)

data.columns=['filename','lon','lat','alt']
data.reset_index(drop=True)

for i in range(0,len(data.filename)):
    row=data.loc[i,:]
    target_fn='./'+row.filename
    print(target_fn)
    if not os.path.exists(target_fn):
        print("no file at row"+str(i))
        continue
    
#     piexif.transplant(template_fn,target_fn)
    exif=piexif.load(template_fn)
    
#     print(exif['GPS'])
    longitude=row.lon;
    latitude=row.lat;
    altitude=row.alt;

    
    ori,res=lon_lat_to_degree_min_sec(latitude,'lat')
    exif['GPS'][1]=ori
    exif['GPS'][2]=res
    
    ori,res=lon_lat_to_degree_min_sec(longitude,'lon')
    exif['GPS'][3]=ori
    exif['GPS'][4]=res
    

    
    exif['GPS'][5]=0
    exif['GPS'][6]=(int(altitude*1000000),1000000)
    
#     print(exif['GPS'])
#     print(exif)
    
    new_exif_byte=piexif.dump(exif)

    piexif.insert(new_exif_byte, target_fn) 





os.system("pause")





