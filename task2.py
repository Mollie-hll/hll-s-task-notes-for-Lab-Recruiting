# 姓名: 何林励
# 学号: 202500239
# 简要描述: 解码 OKTI 文本图像格式并显示图像。

import sys
import os
import tkinter as tk
from PIL import Image


def load_okti(filename):#从 OKTI 文件中加载图像
    if not os.path.exists(filename):
        print("错误：无法打开文件 " + filename)
        sys.exit()

    try:
        f = open(filename, "r")
        header = f.readline().strip()
    except OSError:
        print("错误：无法打开文件 " + filename)
        sys.exit()

    if header != "okti":
        print("错误：文件不是 OKTI 文件，第一行为 " + header)
        f.close()
        sys.exit()

    size_line = f.readline().strip()
    parts = size_line.split()
    try:
        width = int(parts[0])
        height = int(parts[1])
    except ValueError:
        print("错误：图像尺寸解析失败")
        f.close()
        sys.exit()

    if width <= 0 or height <= 0:
        print("错误：图像尺寸无效")
        f.close()
        sys.exit()

    pixels = []
    prev = (0, 0, 0)
    color_list = [(0, 0, 0)]
    total = width * height

    rest = f.read()
    f.close()

    stream = rest.replace("\n", "").replace("\r", "").replace(" ", "").replace("\t", "")# 移除所有空白字符

    i = 0
    while len(pixels) < total:
        if i >= len(stream):
            print("错误：像素数据不足")
            sys.exit()

        t = stream[i]

        if t == 'p':
            r = int(stream[i + 1:i + 3], 16)
            g = int(stream[i + 3:i + 5], 16)
            b = int(stream[i + 5:i + 7], 16)
            i += 7
            new_pixel = (r, g, b)

        elif t == 'd':
            dr = int(stream[i + 1], 16) - 8
            dg = int(stream[i + 2], 16) - 8
            db = int(stream[i + 3], 16) - 8
            i += 4
            new_pixel = ((prev[0] + dr) % 256,
                         (prev[1] + dg) % 256,
                         (prev[2] + db) % 256)

        elif t == 'r':
            count = int(stream[i + 1], 16)
            i += 2
            for _ in range(count):
                pixels.append(prev)
            continue

        elif t == 'R':
            count = int(stream[i + 1:i + 3], 16)
            i += 3
            for _ in range(count):
                pixels.append(prev)
            continue

        elif t == 'i':
            idx = int(stream[i + 1], 16)
            i += 2
            new_pixel = color_list[idx]

        elif t == 'I':
            idx = int(stream[i + 1:i + 3], 16)
            i += 3
            new_pixel = color_list[idx]

        else:
            print("错误：无效像素类型 '" + t + "'")
            sys.exit()

        pixels.append(new_pixel)
        prev = new_pixel

        # 【核心修复】只有在生成全新像素（p, d）或重复像素（r, R）时，才更新列表
        # 如果当前类型是 'i' 或 'I'，说明颜色已经存在于列表中，直接跳过，绝对不能修改列表！
        if t not in ('i', 'I'):
            if new_pixel in color_list:
                color_list.remove(new_pixel)
            color_list.insert(0, new_pixel)
            if len(color_list) > 256:
                color_list.pop()

    # 画图部分：
    scale = 10
    root = tk.Tk()
    root.title(filename)
    canvas = tk.Canvas(root, width=width * scale, height=height * scale)
    canvas.pack()

    for y in range(height):
        for x in range(width):
            r, g, b = pixels[y * width + x]
            color = '#%02x%02x%02x' % (r, g, b)
            canvas.create_rectangle(x * scale, y * scale, (x + 1) * scale, (y + 1) * scale, fill=color, outline=color)

    # 新建并保存图片
    # 终极安全检查：强行将所有像素限制在合法的 RGB 范围内
    safe_pixels = [(max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b))) for (r, g, b) in pixels]
    save_img = Image.new("RGB", (width, height))
    save_img.putdata(safe_pixels)  # 用安全的像素列表去保存
    save_img.save(r"D:/files\pycharm_file/labtasks/taskoutput1.2/" + filename + ".png")
    print("图片已成功保存为：D:/files/pycharm_file/labtasks/taskoutput1.2/" + filename + ".png")

    root.mainloop()

#主程序：
def main():
    if len(sys.argv) > 2:
        print("错误：提供了太多命令行参数")
        sys.exit()
    elif len(sys.argv) == 2:
        filename = sys.argv[1]
    else:
        filename = input("请输入图像文件名：").strip()

    load_okti(filename)


if __name__ == "__main__":
    main()