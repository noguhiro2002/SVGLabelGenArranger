# SVGLabelGenArranger
このプログラムは、UUIDと建物の情報を元にQRコードラベルを生成し、それらを大きなSVGファイル上に整理するPythonスクリプトです。This program is a Python script that generates QR code labels based on UUIDs and building information, and arranges them on a large SVG file.


## 必要なライブラリのインストール (Installation)
このプログラムを実行するためには、以下のPythonライブラリが必要です。次のコマンドを用いてこれらをインストールすることができます。To run this program, the following Python libraries are required. You can install them using the following command.

```bash
pip install base64 svgwrite svgutils qrcode pillow pandas
```

## 使い方 (Usage)
1. QRCodeLabelGeneratorクラスを初期化します。このとき、UUID、SVGテンプレートのパス、場所名、建物名、部屋名、座席名、出力ディレクトリを引数として与えます。Initialize the QRCodeLabelGenerator class. At this time, give the UUID, SVG template path, place name, building name, room name, seat name, output directory as arguments.
2. SVGArrangerクラスを初期化します。このとき、ベースとなる空のSVGファイルのパス、配置したいSVGファイルのパスのリスト、高さ、幅、X方向のマージン、Y方向のマージン、出力ファイル名を引数として与えます。Initialize the SVGArranger class. At this time, give the path of the base empty SVG file, the list of paths of SVG files you want to arrange, height, width, X-direction margin, Y-direction margin, output file name as arguments.
3. generate_labelsメソッドとarrangeメソッドを呼び出すことで、ラベルの生成と配置を行います。By calling the generate_labels method and the arrange method, you can generate and arrange labels.


## 実行例 (Example)
以下はこのプログラムの使用例です。This is an example of using this program.

```python
# QRCodeLabelGeneratorの初期化とラベルの生成
label_generator = QRCodeLabelGenerator(
    seatUuid="uuid",
    tempLabelSVGpath="path/to/your/template.svg",
    siteName="site",
    buildingName="building",
    roomName="room",
    seatName="seat",
    outputDir="path/to/output/dir"
)
label_generator.generate_labels()

# SVGArrangerの初期化とラベルの配置
arranger = SVGArranger(
    emptyBaseSVGPath="path/to/your/base.svg",
    svgPathList=["path/to/your/svg1.svg", "path/to/your/svg2.svg"],
    height=1000,
    width=1000,
    x_margin=10,
    y_margin=10,
    outputFileName="path/to/output/file.svg"
)
 arranger.arrange()

```


## 注意 (Note)
QRコードの生成には、qrcodeパッケージを使用しています。qrcode package is used to generate QR codes.
SVGファイルの読み書きには、svgutilsパッケージを使用しています。svgutils package is used to read and write SVG files.
このプログラムはPython 3.xで動作します。This program works with Python 3.x.

## ライセンス (License)
このプロジェクトはMITライセンスの元に公開されています。詳細はLICENSEファイルをご確認ください。This project is licensed under the MIT License - see the LICENSE file for details​1​.