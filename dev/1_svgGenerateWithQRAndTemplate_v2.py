import base64
import svgwrite
from svgutils.compose import *
import qrcode
from PIL import Image
import pandas as pd


class QRCodeLabelGenerator:
    def __init__(self, seatUuid, tempLabelSVGpath, siteName, buildingName, roomName, seatName, outputDir):
        self.seatUuid = seatUuid
        self.tempLabelSVGpath = tempLabelSVGpath
        self.siteName = siteName
        self.buildingName = buildingName
        self.roomName = roomName
        self.seatName = seatName
        self.outputDir = outputDir

    def qrcodeGenerate(self):
        qr = qrcode.QRCode(
        version=4,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=2,
        border=2
        )

        qr.add_data(self.seatUuid)
        qr.make()
        _img = qr.make_image(fill_color="black")
        _img.save('./tmp/qrcode.png')
        return(_img)

    def encodePNGtoBase64(self, png_location):
        prepend_str = "data:image/png;base64,"
        encoded_str = base64.b64encode(open(png_location, "rb").read()).decode('ascii')
        return(prepend_str + encoded_str)

    def replaceImgTextInTempSVG(self, base64encodedQR):
        with open(self.tempLabelSVGpath, 'r') as file:
            data = file.read()

        data = data.replace('_qrcodeInsertHere_', base64encodedQR)
        data = data.replace('_seatName_', self.seatName)

        mixSite_building_room=self.siteName + ", " + self.buildingName + ", " + self.roomName
        data = data.replace('_siteName-buildingName-roomName_', mixSite_building_room)

        outputFileName=self.siteName + "_" + self.buildingName + "_" + self.roomName + "_" + self.seatName
        with open(self.outputDir + "/" + outputFileName+".svg", 'w') as file:
            file.write(data)

    def generate_labels(self):
        self.qrcodeGenerate()
        base64encodedQR=self.encodePNGtoBase64("./tmp/qrcode.png")
        self.replaceImgTextInTempSVG(base64encodedQR)



tempLabelSVGpath="./templates/type1_temp.svg"

# Excelファイルを読み込む
df = pd.read_excel('./input/inputExcel_sample.xlsx')
print(df.size)

df_num_rows = df.shape[0]
print(df_num_rows)

for i in range(df_num_rows):
    seatUuid_tmp = df.loc[i, "seatUuid"]
    siteName_tmp = df.loc[i, "siteName"]
    buildingName_tmp = df.loc[i, "buildingName"]
    roomName_tmp = df.loc[i, "roomName"]
    seatName_tmp = str("{:0>3}".format(df.loc[i, "seatName"]))

    print(seatUuid_tmp, siteName_tmp, buildingName_tmp, roomName_tmp, seatName_tmp)

    QRCodeLabelGenerator(seatUuid_tmp, tempLabelSVGpath, siteName_tmp, buildingName_tmp, roomName_tmp, seatName_tmp, "./output").generate_labels()