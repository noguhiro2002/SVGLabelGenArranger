import svgutils.transform as st
from svgutils.compose import *
import re


def settingSVGSheetSize(emptySVGPath, height, width):
    # SVGファイルをテキストファイルとして開く
    with open(emptySVGPath, 'r') as file:
        data = file.read()

    # 特定の文字列を置換する
    ## width, height
    data = data.replace('_width_', str(width))
    data = data.replace('_height_', str(height))

    # save template empty base svg file. tmp_base.svg
    with open("tmp_base.svg", 'w') as file:
        file.write(data)
    
    return("tmp_base.svg")

def svgArrangeForBigSVG(outputFileName, temp_baseSVGPath, svgPathList, x_margin, y_margin):
    # SVG_base ファイルを読み込む & root読み込み & width,height get
    svg_base = st.fromfile(temp_baseSVGPath)
    svg_base_root = svg_base.getroot()
    svg_base_width, svg_base_height = svg_base.width, svg_base.height
    svg_base_width, svg_base_height = float(re.findall(r'\d+\.?\d*', svg_base_width)[0]), float(re.findall(r'\d+\.?\d*', svg_base_height)[0])

    # svg_base のheight, widthから印刷可能な枚数を計算
    ## 1. height: N pcs
    child_svg_height=st.fromfile(svgPathList[0]).height
    child_svg_height=float(re.findall(r'\d+\.?\d*', child_svg_height)[0])
    Npcs_height= svg_base_height // (child_svg_height + y_margin)
    Npcs_height=int(Npcs_height)
    print("Npcs_height: ", Npcs_height)

    ## 2. width: N pcs
    child_svg_width=st.fromfile(svgPathList[0]).width
    child_svg_width=float(re.findall(r'\d+\.?\d*', child_svg_width)[0])
    Npcs_width= svg_base_width// (child_svg_width + x_margin)
    Npcs_width=int(Npcs_width)
    print("Npcs_width: ", Npcs_width)

    svgPathListNum=len(svgPathList)
    print("svgPathListNum: ",svgPathListNum)

    svg_base_root.moveto(0,0)

    # move childSVG to baseSVG
    for i_width in range(Npcs_width):
        for i_height in range(Npcs_height):
            target_child_svg_num=(i_width * Npcs_height) + i_height
            print("target_child_svg_num, i_width, Npcs_height, i_height", target_child_svg_num, i_width, Npcs_height, i_height)
            
            if target_child_svg_num < svgPathListNum:
                print(target_child_svg_num)
                child_svg = st.fromfile(svgPathList[target_child_svg_num])
                child_svg_root = child_svg.getroot()
                child_svg_width, child_svg_height = child_svg.width, child_svg.height   
                child_svg_width, child_svg_height = float(re.findall(r'\d+\.?\d*', child_svg_width)[0]), float(re.findall(r'\d+\.?\d*', child_svg_height)[0])

                print("   child_svg_width, child_svg_height, i_width, i_height: ",  child_svg_width, child_svg_height, i_width, i_height)

                moveToXloc= float(x_margin) + i_width * (child_svg_width + float(x_margin))
                moveToYloc= float(y_margin) + i_height * (child_svg_height + float(y_margin))
                child_svg_root.moveto(moveToXloc, moveToYloc)
                # child_svg_root.moveto(i_width * child_svg_width, i_height * child_svg_height)

                print("moveWidth, moveHeight:", moveToXloc, moveToYloc)

                svg_base.append(child_svg_root)
    
    # 結果を保存
    svg_base.save(outputFileName)


svgPathList=[]
for i in range(50):
    svgPathList.append("Kyoto_A10_Office1_" + "{:0>3}".format(i) + ".svg")

height=450
width=450

x_margin=1
y_margin=1

outputFileName="AllCut_1.svg"

temp_baseSVGPath = settingSVGSheetSize("./templates/empty_temp.svg", height, width)
svgArrangeForBigSVG(outputFileName, temp_baseSVGPath, svgPathList, x_margin, y_margin)