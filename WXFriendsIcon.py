# -*- coding:utf-8 -*-
import itchat
import os
import math
import PIL.Image as Image

#创建微信二维码，扫描登陆，并更新好友列表
itchat.auto_login()
friends = itchat.get_friends(update=True)
#计算好友总数
friendsNum = len(friends)
#列表第一位是自己的微信号
user = friends[0]["PYQuanPin"][0:]
#打印好友列表第一位即自己有多少好友
print(user,' have ',friendsNum,' friends.')
#创建文件夹并改入该目录，用来存放好友头像图片
os.mkdir(user)
os.chdir(user)
#遍历好友列表，下载头像图片
for i in friends:
    try:
        i['img'] = itchat.get_head_img(userName=i["UserName"])
        i['ImageName'] = i["UserName"][1:] + '.jpg'
    except:
        print('Get '+i["UserName"][1:]+' fail')
    fileImage = open(i['ImageName'],'wb')
    fileImage.write(i['img'])
    fileImage.close()
#创建头像图片列表
imageList = os.listdir(os.getcwd())
imageNum = len(imageList)
#每张图片的大小为64*64的正方形
eachSize = 64
#每行图片的数量为好友总数开根号加1
eachLine = int(math.sqrt(imageNum)) + 1
print("单个图像边长", eachSize, "像素；每行共", eachLine, "个图像；最终图像边长", eachSize*eachLine)
#创建新画布，将好友头像图片贴图拼接
toImage = Image.new('RGB', (eachSize*eachLine, eachSize*eachLine))
x = 0
y = 0
for i in imageList:
    try:
        img = Image.open(i)
    except:
        print("打开图像失败", i)
    img = img.resize((eachSize, eachSize), Image.ANTIALIAS)
    toImage.paste(img, (x*eachSize, y*eachSize))
    x += 1
    if  x == eachLine:
        x = 0
        y += 1
print("图像拼接完成")
#显示拼接完成后的图片
toImage.show()

os.chdir(os.path.pardir)

iconName = friends[0]["PYQuanPin"][0:]+".jpg"
#保存图片
toImage.save(iconName)
#通过文件传输，发送到手机
itchat.send_image(iconName, "filehelper")
#退出微信
itchat.logout()
