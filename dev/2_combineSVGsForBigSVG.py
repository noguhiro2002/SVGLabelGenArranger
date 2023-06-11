import svgutils.transform as st
from svgutils.compose import *


# SVGファイルを読み込む
A = st.fromfile('Kyoto_A10_Office1_001.svg')
B = st.fromfile('Kyoto_A10_Office1_002.svg')
C = st.fromfile('Kyoto_A10_Office1_003.svg')

# 各SVGのルート要素を取得
A_root = A.getroot()
B_root = B.getroot()
C_root = C.getroot()

# ルート要素の名前と属性を表示
# print('Element name:', A_root.tag)
# print('Attributes:', A_root.attrib)

# ルート要素のすべての子要素を表示
# for child in A_root.getchildren():
#     print('Child element name:', child.tag)
#     print('Child attributes:', child.attrib)

# SVGの幅を取得
A_width, _ = A.width, A.height
B_width, _ = B.width, B.height

# SVGの幅を数値に変換（単位を剥がすためにfloat関数を使用）
A_width = float(A_width.strip('mm'))  # 'mm'を剥がす
B_width = float(B_width.strip('mm'))  # 'mm'を剥がす

print("mm:", A_width, B_width)

# mmをptに変換
# A_width *= 2.83465
# B_width *= 2.83465

# print("pt:", A_width, B_width)

# SVGファイルを読み込む
# svg = SVG('empty.svg')
svg = st.fromfile('empty.svg')
svg_root = svg.getroot()

# BとCを適切な位置に移動
# B_root.moveto(A_width, 0)
svg_root.moveto(0,0)
A_root.moveto(1,1)
B_root.moveto(A_width + 1, 0)
C_root.moveto(A_width + B_width + 1, 0)

# AにBとCを追加
# A.append(B_root)
# A.append(C_root)

print(svg_root)

svg.append(A_root)
svg.append(B_root)
svg.append(C_root)

# A.append(B_root)
# A.append(C_root)

# 結果を保存
# A.save('All.svg')
svg.save('All.svg')