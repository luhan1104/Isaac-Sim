#!/usr/bin/env python
# coding=UTF-8

import ezdxf

def extract_lines(dxf_file_path):
    doc=ezdxf.readfile("/home/liufeng/isaac_test/lh/python_usd/jskjy.dxf")
    msp=doc.modelspace()
    lines=[]
    for entity in msp.query('*'):  # 遍历模型空间中的实体
        if entity.dxf.layer == "WALL":
            if entity.dxftype() == "LINE":
                start_point = entity.dxf.start
                end_point = entity.dxf.end
                lines.append((entity.dxf.layer,start_point,end_point))
            # else:
            #     lines.append((entity.dxf.layer,entity.dxftype()))
    print(lines)

if __name__ == "__main__":
    dxf_file_path = "/home/liufeng/isaac_test/lh/python_usd/.dxf"
    extract_lines(dxf_file_path)