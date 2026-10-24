# 姓名: [何林励]
# 学号: [202500239]
# 简要描述: 将图像编码为OKTI文本格式文件

import sys
import os
import tkinter as tk
from tkinter import TclError

from SimpleGraphics import loadImage, drawImage, close

BLACK = (0, 0, 0)
MAX_LINE_LENGTH = 79  #A+要求(行宽不超过79个字符)


class DummyImage:
    def __init__(self, w, h, p):
        self._w = w
        self._h = h
        self._p = p

    def width(self):
        return self._w

    def height(self):
        return self._h

    def getPixel(self, x, y):
        return self._p[y * self._w + x]


def load_image_custom(filename):
    root = tk.Tk()
    root.withdraw()
    try:
        tk_img = tk.PhotoImage(file=filename)
        width = tk_img.width()
        height = tk_img.height()

        pixels = []
        for y in range(height):
            for x in range(width):
                hex_color = tk_img.get(x, y)
                if isinstance(hex_color, str) and hex_color.startswith("#"):
                    r = int(hex_color[1:3], 16)
                    g = int(hex_color[3:5], 16)
                    b = int(hex_color[5:7], 16)
                else:
                    r, g, b = 0, 0, 0
                pixels.append((r, g, b))
        root.destroy()
        return DummyImage(width, height, pixels)

    except Exception as e:
        print("读取图片失败：", e)
        root.destroy()
        sys.exit()


def get_pixel_color(img, x, y):
    """获取图像在 (x, y) 处的 RGB 三元组。

    参数:
        img: 图像对象（DummyImage 或 tk.PhotoImage）
        x, y: 像素坐标
    返回:
        (r, g, b) 元组
    """
    try:
        return img.getPixel(x, y)
    except AttributeError:
        hex_color = img.get(x, y)
        if isinstance(hex_color, str) and hex_color.startswith("#"):
            return (int(hex_color[1:3], 16),
                    int(hex_color[3:5], 16),
                    int(hex_color[5:7], 16))
        return BLACK


def get_pixel_hex(r, g, b):
    """把 RGB 三元组转成 6 位十六进制字符串。"""
    return "%02x%02x%02x" % (r, g, b)


def encode_image(img, filename, width, height):
    """把图像编码为 OKTI 文本格式并写入文件。"""
    f = open(filename, "w")
    f.write("okti\n")
    f.write(str(width) + " " + str(height) + "\n")

    prev = BLACK
    color_list = [BLACK]

    x = 0
    y = 0
    current_line_length = 0
    last_char = "\n"

    while y < height:
        current_color = get_pixel_color(img, x, y)
        encoded_str = ""

        if current_color == prev:
            run_length = 1
            look_x = x
            look_y = y

            while run_length < 256:
                look_x += 1
                if look_x >= width:
                    look_x = 0
                    look_y += 1

                if look_y >= height:
                    break
                if get_pixel_color(img, look_x, look_y) != current_color:
                    break
                run_length += 1

            extra = run_length - 1
            if extra < 16:
                encoded_str = "r%x" % extra
            else:
                encoded_str = "R%02x" % extra

            x += run_length
            while x >= width:
                x -= width
                y += 1

        else:
            idx = -1
            for i, c in enumerate(color_list):
                if c == current_color:
                    idx = i
                    break

            if idx != -1:
                if idx < 16:
                    encoded_str = "i%x" % idx
                else:
                    encoded_str = "I%02x" % idx
            else:
                dr = current_color[0] - prev[0]
                dg = current_color[1] - prev[1]
                db = current_color[2] - prev[2]
                if -8 <= dr <= 7 and -8 <= dg <= 7 and -8 <= db <= 7:
                    encoded_str = "d%x%x%x" % (dr + 8, dg + 8, db + 8)
                else:
                    encoded_str = "p" + get_pixel_hex(current_color[0], current_color[1], current_color[2])

            x += 1
            while x >= width:
                x -= width
                y += 1

        if current_line_length + len(encoded_str) > MAX_LINE_LENGTH:
            f.write("\n")
            current_line_length = 0

        f.write(encoded_str)
        last_char = encoded_str[-1]
        current_line_length += len(encoded_str)

        if current_color in color_list:
            color_list.remove(current_color)
        color_list.insert(0, current_color)

        if len(color_list) > 256:
            color_list.pop()

        prev = current_color

    if last_char != "\n":
        f.write("\n")
    f.close()
    print("编码成功！文件已保存为: " + filename)


def parse_ppm(filename):
    with open(filename, "rb") as f:
        magic = f.readline().strip()
        if magic not in (b"P3", b"P6"):
            print("错误：目前只支持 PPM 格式 (P3 或 P6)")
            sys.exit()

        line = f.readline()
        while line.startswith(b"#"):
            line = f.readline()
        width, height = map(int, line.split())

        max_val = int(f.readline().strip())

        pixels = []
        if magic == b"P6":
            pixel_data = f.read()
            start_idx = 0
            while start_idx < len(pixel_data) and pixel_data[start_idx] in b" \t\r\n":
                start_idx += 1

            pixel_data = pixel_data[start_idx:]
            for i in range(0, width * height * 3, 3):
                pixels.append((pixel_data[i], pixel_data[i + 1], pixel_data[i + 2]))
        else:
            data = f.read().split()
            for i in range(width * height):
                pixels.append((int(data[i * 3]), int(data[i * 3 + 1]), int(data[i * 3 + 2])))
    return width, height, pixels


def main():
    if len(sys.argv) > 2:
        print("错误：提供了太多命令行参数")
        sys.exit()
    elif len(sys.argv) == 2:
        filename = sys.argv[1]
    else:
        filename = input("请输入要打开的图像文件名 (如 tiny.ppm)：").strip()

    if not os.path.exists(filename):
        print("错误：文件不存在 " + filename)
        sys.exit()

    try:
        width, height, pixels = parse_ppm(filename)
        img = DummyImage(width, height, pixels)
        print("====== 读图成功，前 5 个像素颜色为： ======")
        for i in range(min(5, len(pixels))):
            print(img.getPixel(i, 0))
    except Exception:
        img = load_image_custom(filename)
        width = img.width()
        height = img.height()
        print("====== 读图成功，前 5 个像素颜色为： ======")
        for i in range(min(5, width * height)):
            print(img.getPixel(i, 0))

    base_name = os.path.splitext(os.path.basename(filename))[0]
    output_folder = "D:/files/pycharm_file/labtasks/task2encoder_output/"

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    output_filename = output_folder + "encoder_output_" + base_name + ".okti"

    encode_image(img, output_filename, width, height)


if __name__ == "__main__":
    main()
