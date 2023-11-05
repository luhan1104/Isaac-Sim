import ezdxf

from pxr import Usd, UsdGeom, UsdPhysics, Kind, Sdf, UsdShade

import sys
import os
import json


def extract_tag5X5(dxf_file_path):
    doc=ezdxf.readfile(dxf_file_path)
    msp=doc.modelspace()
    insert = []
    for entity in msp.query("INSERT[name=='EMMA400L']"):
        insert.append((entity.dxf.insert[0],
                       entity.dxf.insert[1] + 480/2,
                       entity.dxf.insert[2],
                       entity.dxf.rotation,
                       3, 'TAG2XN', '2XN',
                       0.48, 0.057))
    for entity in msp.query("INSERT[name=='TAG2XN(1000)']"):
        insert.append((entity.dxf.insert[0],
                       entity.dxf.insert[1] + 480/2,
                       entity.dxf.insert[2],
                       entity.dxf.rotation,
                       3, 'TAG2XN', '2XN',
                       0.48, 0.057))
    for entity in msp.query("INSERT[name=='TAG2XN(2000)']"):
        insert.append((entity.dxf.insert[0],
                       entity.dxf.insert[1] + 480/2,
                       entity.dxf.insert[2],
                       entity.dxf.rotation,
                       3, 'TAG2XN', '2XN',
                       0.48, 0.057))
    for entity in msp.query("INSERT[name=='TAG2XN(3000)']"):
        insert.append((entity.dxf.insert[0],
                       entity.dxf.insert[1] + 480/2,
                       entity.dxf.insert[2],
                       entity.dxf.rotation,
                       3, 'TAG2XN', '2XN',
                       0.48, 0.057))
    print(insert)


# def extract_block_defs(dxf_file_path):

    # for block_def in block_defs:
    #     # 获取块的名称
    #     block_name = block_def.name
    #     print(f"Block Name: {block_name}")
        
    #     # 获取块定义的匿名属性
    #     is_anonymous = block_def.anonymous
    #     print(f"Is Anonymous: {is_anonymous}")

    # for entity in msp:
    #     if entity.dxftype() == 'INSERT':
    #         block_name = entity.dxf.name
    #         block = doc.blocks.get(block_name)
    #         if block is not None:
    #             # 这里 block 包含块定义的信息
    #             print(f"Block Name: {block_name}")
    #             print("Attributes:")
    #             for attribute in block.query('EffectiveName'):
    #                 print(f"Attribute Tag: {attribute.dxf.tag}, Value: {attribute.dxf.text}")
    # for entity in msp.query("INSERT[name=='*U328']"):
    #     print(entity.entities)
        # id = 0
        # print(entity.attribs[0])
        # for attrib in entity.attribs:
        #     print(entity.)
        #     print(attrib.dxf.tag)
        #     if attrib.dxf.tag == 'ID':
        #         id = int(attrib.dxf.text)
        #         print(attrib.dxf.text)
        #         print(id)
    #     insert.append((entity.dxf.insert[0],
    #                    entity.dxf.insert[1],
    #                    entity.dxf.insert[2],
    #                    entity.dxf.rotation,
    #                    entity.dxf.name))
    #     print(entity.block().name)
    # print(insert)

    # for entity in msp.query('*'):
    #     if entity.dxf.layer == 'L-二维码':
    #         car_info.append((entity.dxf.insert[0],
    #                 entity.dxf.insert[1],
    #                 entity.dxf.insert[2],
    #                 entity.dxf.rotation,
    #                 entity.dxf.name))

    # # Collect all anonymous block references starting with '*U'
    # anonymous_block_refs = msp.query('INSERT[name ? "^\*U.+"]')

    # # Collect the references of the 'FLAG' block
    # flag_refs = []
    # for block_ref in anonymous_block_refs:
    #     # Get the block layout of the anonymous block
    #     print(block_ref.dxf.name)
    #     block = doc.blocks.get(block_ref.dxf.name)
    #     # Find all block references to 'FLAG' in the anonymous block
    #     flag_refs.extend(block.query('INSERT[name=="TAG2Xn"]'))

    # # Evaluation example: collect all flag names.
    # flag_numbers = [
    #     flag.get_attrib_text("NAME")
    #     for flag in flag_refs
    #     if flag.has_attrib("NAME")
    # ]

    # print(flag_refs)
    # print(car_info)
    # return insert

def car_info(dxf_file_path):
    doc=ezdxf.readfile(dxf_file_path)
    msp=doc.modelspace()
    car_info = []
    for entity in msp.query('*'):
        if entity.dxf.layer == 'L-AGV车体':
            car_info.append((entity.dxf.insert[0],
                    entity.dxf.insert[1],
                    entity.dxf.insert[2],
                    entity.dxf.rotation,
                    entity.dxf.effectivename))
    print(car_info)
    return car_info

if __name__ == "__main__":
    # n=len(sys.argv)
    # if n<2:
    #     dxf_file_path = "/home/liufeng/isaac_test/cadtousda/dxf/room.dxf"
    #     usd_file_path = "/home/liufeng/isaac_test/cadtousda/usda/room.usda"
    # else:
    #     dxf_file_path = sys.argv[1]
    #     usd_file_path = sys.argv[2]
    dxf_file_path = "/home/liufeng/isaac_test/cadtousda/dxf/jskjy_1020.dxf"
    tag5X5_info = extract_tag5X5(dxf_file_path)
    #car_info = car_info(dxf_file_path)
