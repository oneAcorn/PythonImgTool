"""
使用示例:
python generate_animation.py -i /path/to/images -o /output/path/animation.xml -d 100 --oneshot

参数说明：

-i/--input: 必填，图片目录路径

-o/--output: 输出文件路径（默认当前目录的animation.xml）

-d/--duration: 每帧持续时间（毫秒，默认100）

--oneshot: 添加此参数表示动画只播放一次
"""
import os
import re
import argparse
from xml.etree import ElementTree as ET
from xml.dom import minidom

def natural_sort_key(s):
    return [int(text) if text.isdigit() else text.lower()
            for text in re.split(r'(\d+)', s)]

def generate_animation_xml(input_dir, output_file, duration=100, oneshot=False):
    # 支持的图片格式
    valid_exts = ('.webp', '.png', '.jpg', '.jpeg')
    
    # 获取并过滤文件
    files = [f for f in os.listdir(input_dir) 
            if f.lower().endswith(valid_exts) and os.path.isfile(os.path.join(input_dir, f))]
    
    if not files:
        print("错误：目录中没有找到图片文件！")
        return False

    # 按自然顺序排序
    files.sort(key=natural_sort_key)

    # 创建XML结构
    root = ET.Element("animation-list")
    root.set("xmlns:android", "http://schemas.android.com/apk/res/android")
    root.set("android:oneshot", str(oneshot).lower())

    for file in files:
        item = ET.SubElement(root, "item")
        item.set("android:drawable", "@drawable/" + os.path.splitext(file)[0])
        item.set("android:duration", str(duration))

    # 生成格式化的XML
    rough_xml = ET.tostring(root, 'utf-8')
    reparsed = minidom.parseString(rough_xml)
    pretty_xml = reparsed.toprettyxml(indent="    ", encoding="utf-8")

    # 在写入文件前添加目录检查（相当于Kotlin的File.mkdirs()）
    output_dir = os.path.dirname(output_file)
    if output_dir:  # 当路径包含目录时才需要创建
        os.makedirs(output_dir, exist_ok=True)  # 自动创建缺失的目录

    # 写入文件
    with open(output_file, 'wb') as f:
        f.write(pretty_xml)

    print(f"成功生成动画XML，共{len(files)}帧")
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='生成Android逐帧动画XML')
    parser.add_argument('-i', '--input', required=True, help='图片目录路径')
    parser.add_argument('-o', '--output', default="animation.xml", help='输出XML路径')
    parser.add_argument('-d', '--duration', type=int, default=100, 
                       help='每帧持续时间（毫秒）')
    parser.add_argument('--oneshot', action='store_true',
                       help='设置为单次播放（默认循环播放）')
    
    args = parser.parse_args()

    generate_animation_xml(
        input_dir=args.input,
        output_file=args.output,
        duration=args.duration,
        oneshot=args.oneshot
    )