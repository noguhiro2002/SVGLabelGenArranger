from SVGLabelGenArranger import QRCodeLabelGenerator 
from SVGLabelGenArranger import SVGArranger
from SVGLabelGenArranger import get_sorted_svg_files
import pandas as pd
import os

# 1_SVGLabelGenerator

tempLabelSVGpath="./templates/type1_temp.svg"

## Excelファイルを読み込む
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


# 2_ChildSVGArranger_to_BigSVG
## svgファイル一覧pathを入手
directory = "./output" # ここに探索したいディレクトリのパスを入力してください
sorted_svg_files = get_sorted_svg_files(directory)
print(sorted_svg_files)


## Arrange
### Arrange: settings
emptyBaseSVGPath="./lib/empty_temp.svg"
svgPathList=sorted_svg_files
height=450
width=450
x_margin=1
y_margin=1
outputFileName="./output/ForLaserCut.svg"

### Arrange: process
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