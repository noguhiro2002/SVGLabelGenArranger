import svgutils.transform as st
from svgutils.compose import *
import re
import os
import glob

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
    # currnetWorkDir=os.getcwd()
    # os.chdir(directory)
    files = glob.glob(directory + '/*.svg')
    # file_paths = [os.path.join(directory, file) for file in files]
    file_paths = files
    file_paths.sort(key=lambda x: os.path.basename(x))
    # os.chdir(currnetWorkDir)
    return file_paths


##########

# svgファイル一覧pathを入手
directory = "./output" # ここに探索したいディレクトリのパスを入力してください
sorted_svg_files = get_sorted_svg_files(directory)
print(sorted_svg_files)


# Arrange
## Arrange: settings
emptyBaseSVGPath="./lib/empty_temp.svg"
svgPathList=sorted_svg_files
height=450
width=450
x_margin=1
y_margin=1
outputFileName="./output/ForLaserCut.svg"

## Arrange: process
print(os.getcwd())

arranger=SVGArranger(emptyBaseSVGPath, svgPathList, height, width, x_margin, y_margin, outputFileName)
temp_baseSVGPath=arranger.settingSVGSheetSize(emptyBaseSVGPath)
Npcs_height, Npcs_width=arranger.calculate_svg_layout(temp_baseSVGPath)

onePageSVGListNum=Npcs_height*Npcs_width
print("onePageSVGListNum: ",onePageSVGListNum)

totalPageNum=len(svgPathList) // onePageSVGListNum + 1
print("totalPageNum: ", totalPageNum)

for currentProcessPageNum in range(totalPageNum):
    print("currentProcessPageNum:",currentProcessPageNum)
    cutChildSVGRange_start = currentProcessPageNum * onePageSVGListNum
    cutChildSVGRange_end = cutChildSVGRange_start + onePageSVGListNum
    print(cutChildSVGRange_start, cutChildSVGRange_end)
    arranger=SVGArranger(emptyBaseSVGPath, svgPathList[cutChildSVGRange_start:cutChildSVGRange_end], height, width, x_margin, y_margin, "./output/ForLaserCut_" + str(currentProcessPageNum) + ".svg")
    arranger.arrange()