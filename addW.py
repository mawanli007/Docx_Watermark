# -*- coding:utf-8 -*-
import zipfile
import os
from PIL import Image, ImageDraw

def dfs_get_zip_file(input_path,result):
    
    files = os.listdir(input_path)
    for file in files:
        if os.path.isdir(input_path+'/'+file):
            dfs_get_zip_file(input_path+'/'+file,result)
        else:
            result.append(input_path+'/'+file)

def zip_path(input_path, output_name):
    
    f = zipfile.ZipFile('new'+output_name, 'w', zipfile.ZIP_DEFLATED)
    filelists = []
    dfs_get_zip_file(input_path, filelists)
    for file in filelists:
        # print(file)
        f.write(file, file[len(output_name)-3:])
    f.close()
    return r"/"+output_name

def add_watermark_to_image(image, watermark):
    rgba_image = image.convert('RGBA')
    rgba_watermark = watermark.convert('RGBA')
    
    image_x, image_y = rgba_image.size
    watermark_x, watermark_y = rgba_watermark.size
    
    # 缩放图片
    scale = 10
    watermark_scale = max(image_x / float(scale * watermark_x), image_y / float(scale * watermark_y))
    new_size = (int(watermark_x * watermark_scale), int(watermark_y * watermark_scale))
    rgba_watermark = rgba_watermark.resize(new_size, resample=Image.ANTIALIAS)
    # 透明度
    rgba_watermark_mask = rgba_watermark.convert("L").point(lambda x: min(x, 180))
    rgba_watermark.putalpha(rgba_watermark_mask)
    
    watermark_x, watermark_y = rgba_watermark.size
    # 水印位置
    rgba_image.paste(rgba_watermark, (image_x - watermark_x, image_y - watermark_y), rgba_watermark_mask)
    
    return rgba_image

def addW(docfile, picfile):
    filename = docfile
    sypic = picfile
    pnglist = []
    z = zipfile.ZipFile(filename, 'r')
    z.extractall(filename.split('.')[0])
    for x in z.namelist():
        if x.split('.')[-1] == 'png':
            pnglist.append(x)

    for dir in pnglist:
        pic = filename.split('.')[0] + '/'+ dir
        fo = open(pic, "wb")
        fo.write(z.read(dir))
        fo.close()
        im_before = Image.open(pic)
        im_watermark = Image.open(sypic)
        im_after = add_watermark_to_image(im_before, im_watermark)
        # im_after.show()
        im_after.save(pic)
     
    z.close()

    zip_path(r"./"+filename.split('.')[0], docfile)
    import shutil
    shutil.rmtree(filename.split('.')[0])
    os.remove(filename)
    os.remove(picfile)

    return './new/' + filename

# addW('xx.docx','xx.png')
