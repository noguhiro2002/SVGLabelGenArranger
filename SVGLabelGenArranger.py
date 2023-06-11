import base64
import svgwrite
from svgutils.compose import *
import qrcode
from PIL import Image
import pandas as pd
import svgutils.transform as st
import re
import os
import glob


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


class SVGArranger:
    def __init__(self, emptyBaseSVGPath, svgPathList, height, width, x_margin, y_margin, outputFileName):
        self.emptyBaseSVGPath = emptyBaseSVGPath
        self.svgPathList = svgPathList
        self.height = height
        self.width = width
        self.x_margin = x_margin
        self.y_margin = y_margin
        self.outputFileName = outputFileName

    def settingSVGSheetSize(self, emptyBaseSVGPath):
        with open(emptyBaseSVGPath, 'r') as file:
            data = file.read()

        data = data.replace('_width_', str(self.width))
        data = data.replace('_height_', str(self.height))

        with open("./tmp/tmp_base.svg", 'w') as file:
            file.write(data)
        
        return("./tmp/tmp_base.svg")
    
    def calculate_svg_layout(self, temp_baseSVGPath):
        svg_base = st.fromfile(temp_baseSVGPath)
        svg_base_root = svg_base.getroot()
        svg_base_width, svg_base_height = svg_base.width, svg_base.height
        svg_base_width, svg_base_height = float(re.findall(r'\d+\.?\d*', svg_base_width)[0]), float(re.findall(r'\d+\.?\d*', svg_base_height)[0])

        child_svg_height=st.fromfile(self.svgPathList[0]).height
        child_svg_height=float(re.findall(r'\d+\.?\d*', child_svg_height)[0])
        Npcs_height= svg_base_height // (child_svg_height + self.y_margin)
        Npcs_height=int(Npcs_height)

        child_svg_width=st.fromfile(self.svgPathList[0]).width
        child_svg_width=float(re.findall(r'\d+\.?\d*', child_svg_width)[0])
        Npcs_width= svg_base_width// (child_svg_width + self.x_margin)
        Npcs_width=int(Npcs_width)

        return(Npcs_height, Npcs_width)

    def svgArrangeForBigSVG(self, temp_baseSVGPath):
        Npcs_height, Npcs_width=self.calculate_svg_layout(temp_baseSVGPath)

        svg_base = st.fromfile(temp_baseSVGPath)
        svg_base_root = svg_base.getroot()

        svgPathListNum=len(self.svgPathList)

        svg_base_root.moveto(0,0)

        for i_width in range(Npcs_width):
            for i_height in range(Npcs_height):
                target_child_svg_num=(i_width * Npcs_height) + i_height
                
                if target_child_svg_num < svgPathListNum:
                    child_svg = st.fromfile(self.svgPathList[target_child_svg_num])
                    child_svg_root = child_svg.getroot()
                    child_svg_width, child_svg_height = child_svg.width, child_svg.height   
                    child_svg_width, child_svg_height = float(re.findall(r'\d+\.?\d*', child_svg_width)[0]), float(re.findall(r'\d+\.?\d*', child_svg_height)[0])

                    moveToXloc= float(self.x_margin) + i_width * (child_svg_width + float(self.x_margin))
                    moveToYloc= float(self.y_margin) + i_height * (child_svg_height + float(self.y_margin))
                    child_svg_root.moveto(moveToXloc, moveToYloc)

                    svg_base.append(child_svg_root)
        
        svg_base.save(self.outputFileName)

    def arrange(self):
        temp_baseSVGPath = self.settingSVGSheetSize(self.emptyBaseSVGPath)
        self.svgArrangeForBigSVG(temp_baseSVGPath)

def get_sorted_svg_files(directory):
    files = glob.glob(directory + '/*.svg')
    file_paths = files
    file_paths.sort(key=lambda x: os.path.basename(x))
    return file_paths