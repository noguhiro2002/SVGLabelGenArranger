import base64
import svgwrite
from svgutils.compose import *
import qrcode
from PIL import Image


def qrcodeGenerate(seatUuid):
    qr = qrcode.QRCode(
    version=4,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=2,
    border=2
    )

    qr.add_data(seatUuid)
    qr.make()
    # _img = qr.make_image(fill_color="black", back_color="#ffffff")
    _img = qr.make_image(fill_color="black")
    _img.save('qrcode.png')
    # print(_img)
    return(_img)

def encodePNGtoBase64(png_location):
    prepend_str = "data:image/png;base64,"
    encoded_str = base64.b64encode(open(png_location, "rb").read()).decode('ascii')
    return(prepend_str + encoded_str)

def replaceImgTextInTempSVG(tempLabelSVGpath, base64encodedQR, siteName, buildingName, roomName, seatName):
    # SVGファイルをテキストファイルとして開く
    with open(tempLabelSVGpath, 'r') as file:
        data = file.read()

    # 特定の文字列を置換する
    ## qrcode
    data = data.replace('_qrcodeInsertHere_', base64encodedQR)
    
    ## seatName
    data = data.replace('_seatName_', seatName)

    ## siteName,buildingName,roomName
    mixSite_building_room=siteName + ", " + buildingName + ", " + roomName
    data = data.replace('_siteName-buildingName-roomName_', mixSite_building_room)

    # 置換後のデータを保存する
    outputFileName=siteName + "_" + buildingName + "_" + roomName + "_" + seatName
    with open(outputFileName+".svg", 'w') as file:
        file.write(data)


tempLabelSVGpath="./templates/type1_temp.svg"
siteName="Kyoto"
buildingName="A10"
roomName="Office1"
seatName="001"
seatUuid="519e2fbf-d719-4399-96d5-0e15b9741129"

Num=50

for i in range(Num):
    NumStr="{:0>3}".format(i)
    qrcodeGenerate(seatUuid)
    base64encodedQR=encodePNGtoBase64("./qrcode.png")
    replaceImgTextInTempSVG(tempLabelSVGpath, base64encodedQR, siteName, buildingName, roomName, NumStr)