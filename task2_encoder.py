# 姓名: [何林励]
# 学号: [202500239]
# 简要描述: 将 PNG 或 PPM 图像编码为 OKTI 文本格式文件（包含A+行宽限制要求）。

import sys
import os
from tkinter import TclError
from SimpleGraphics import loadImage, drawImage
from SimpleGraphics import loadImage, drawImage, close

BLACK = (0, 0, 0)
MAX_LINE_LENGTH = 79  # A+要求(行宽不超过 79 个字符)

def get_pixel_color(img, x, y):
    try:
        return img.getPixel(x, y)
    except AttributeError:
        hex_color = img.get(x, y)
        if isinstance(hex_color, str) and hex_color.startswith("#"):
            return (int(hex_color[1:3], 16), int(hex_color[3:5], 16), int(hex_color[5:7], 16))
        return BLACK

def get_pixel_hex(r, g, b):
    return "%02x%02x%02x" % (r, g, b)

def encode_image(img, filename, width, height):
    f = open(filename, "w")
    f.write("okti\n")
    f.write(str(width) + " " + str(height) + "\n")

    prev = BLACK
    color_list = [BLACK]

    x = 0
    y = 0
    current_line_length = 0

    while y < height:
        current_color = get_pixel_color(img, x, y)#获取像素

        #强制用完整 RGB 格式,查看读图函数是否错误
        encoded_str = "p" + get_pixel_hex(current_color[0], current_color[1], current_color[2])
        is_run = False

        # encoded_str = ""
        # run_length = 0
        # is_run = False
        #
        # # 2. 检查是否可以连续重复 (Run Length Encoding)
        # # 我们需要往后看有多少个和当前相同的像素（最多255个）
        # if current_color == prev:
        #     # 统计连续相同的像素数量
        #     look_x = x
        #     look_y = y
        #     while run_length < 255:
        #         if look_x >= width:
        #             look_x = 0
        #             look_y += 1
        #         if look_y >= height:
        #             break  # 图像到底了，停止
        #
        #         if get_pixel_color(img, look_x, look_y) == current_color:
        #             run_length += 1
        #             look_x += 1
        #         else:
        #             break  # 遇到不同的像素，停止
        #
        #     # 如果至少有一个额外重复，使用 r 或 R
        #     if run_length > 0:
        #         is_run = True
        #         if run_length < 16:
        #             encoded_str = "r%x" % run_length
        #         else:
        #             encoded_str = "R%02x" % run_length
        #
        # # 3. 如果不是连续重复，按优先级判断其他编码方式
        # if not is_run:
        #     if current_color in color_list:
        #         # 编码为历史颜色索引 (i 或 I)
        #         idx = color_list.index(current_color)
        #         if idx < 16:
        #             encoded_str = "i%x" % idx
        #         else:
        #             encoded_str = "I%02x" % idx
        #     else:
        #         # 尝试计算差值 (d)
        #         dr = current_color[0] - prev[0]
        #         dg = current_color[1] - prev[1]
        #         db = current_color[2] - prev[2]
        #
        #         if -8 <= dr <= 7 and -8 <= dg <= 7 and -8 <= db <= 7:
        #             encoded_str = "d%x%x%x" % (dr + 8, dg + 8, db + 8)
        #         else:
        #             # 都不行，使用完整 RGB (p)
        #             encoded_str = "p" + get_pixel_hex(current_color[0], current_color[1], current_color[2])

        if current_line_length + len(encoded_str) > MAX_LINE_LENGTH:
            f.write("\n")
            current_line_length = 0 #A+要求(控制换行、保证行宽)


        f.write(encoded_str)
        current_line_length += len(encoded_str)

        if current_color in color_list:
            idx = color_list.index(current_color)
            if idx != 0:
                color_list.pop(idx)
                color_list.insert(0, current_color)
        else:
            color_list.insert(0, current_color)
            if len(color_list) > 256:
                color_list.pop()

        prev = current_color

        if is_run:
            x += run_length
        else:
            x += 1

        while x >= width:
            x -= width
            y += 1

    f.write("\n")  #文件末尾留一个换行符
    f.close()
    print("编码成功！文件已保存为: " + filename)


def main():
    if len(sys.argv) > 2:
        print("错误：提供了太多命令行参数")
        sys.exit()
    elif len(sys.argv) == 2:
        filename = sys.argv[1]
    else:
        filename = input("请输入要打开的图像文件名 (如 tiny.png)：").strip()

    # 检查文件是否存在
    if not os.path.exists(filename):
        print("错误：文件不存在 " + filename)
        sys.exit()

    try:
        img = loadImage(filename)

        width = img.width()
        height = img.height()

        drawImage(img, 0, 0)

    except TclError:
        print("错误：无法打开或解析该图像文件，请确保格式受支持。")
        sys.exit()
    except Exception as e:
        print("错误：加载图片失败，原因：" + str(e))
        sys.exit()


    base_name = os.path.splitext(filename)[0]
    output_folder = "D:/files/pycharm_file/labtasks/task2encoder_output/"
    output_filename = output_folder + "encoder_output_" + base_name + ".okti"

    encode_image(img, output_filename, width, height)# 调用编码器
    close()  # 强制关闭 SimpleGraphics 的窗口

if __name__ == "__main__":
    main()