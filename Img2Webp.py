from PIL import Image
import os
import re

'''
转换图片到webp

imgPath: 图片目录(无文件名)
fileName: 图片名(无后缀名)
suffix: 图片原始后缀名
'''
def handleConversion (imgPath,fileName,suffix):
  fileFullPath = os.path.join(imgPath,fileName + suffix)
  #print('fileName--->', fileFullPath)
  saveFullPath = os.path.join(imgPath,fileName + ".webp")
  print('saveFullPath--->', saveFullPath)
  im = Image.open(fileFullPath).convert("RGBA")
  #参考 https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html
  # https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html#webp
  # lossless:是否无损压缩,默认false. quality 压缩比,越高质量越高,0-100,默认80.
  im.save(saveFullPath, 'WEBP',lossless=False,quality=80)
  # os.remove(fileFullPath)
  
def isImg(file):
  imgReg = r'(jpeg|jpg|png)$'
  isImg = re.findall(imgReg,file) != []
  return isImg

'''
遍历多级目录下所有图片
'''
def iterateImg(path,callback):
  files = os.listdir(path)
  for file in files:
    subFilePath = os.path.join(path,file)
    if isImg(file):
      callback(path,file)
    elif os.path.isdir(subFilePath):
      iterateImg(subFilePath,callback)

def converseImgCallback(path,file):
  handleConversion(path,getFileNameWithoutSuffix(file),getFileSuffix(file))
  #删除原始图片
  deletePath = os.path.join(path,file)
  os.remove(deletePath)

'''
获取文件后缀名
'''
def getFileSuffix(file):
  suffixIndex = file.rindex(".")
  suffix = file[suffixIndex:len(file)]
  return suffix

'''
获取没有后缀名的文件名
'''
def getFileNameWithoutSuffix(file):
  suffixIndex = file.rindex(".")
  rFileName= file[0:suffixIndex]
  return rFileName

def main():
  #遍历所有图片转换为webp,并删除原始图片
  iterateImg('./',converseImgCallback)

if __name__ == '__main__':
  main()