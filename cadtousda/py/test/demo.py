import ezdxf
from pxr import Usd, UsdGeom

# 读取2D DXF文件
def read_dxf(file_path):
    doc = ezdxf.readfile(file_path)
    modelspace = doc.modelspace()
    entities = modelspace.query('LINE,CIRCLE')  # 仅处理直线和圆形

    return entities

# 创建3D USD文件
def create_usd(entities, output_path):
    stage = Usd.Stage.CreateNew(output_path)

    # 创建Xform代表3D空间
    xform = UsdGeom.Xform.Define(stage, "/my_model")

    for entity in entities:
        if entity.dxftype() == 'LINE':
            # 处理直线
            start_point = entity.dxf.start
            end_point = entity.dxf.end

            # 在Xform中创建直线
            line = UsdGeom.Curves.Define(stage, xform.GetPath().AppendChild("line"))
            line.CreatePointsAttr([start_point, end_point])

        elif entity.dxftype() == 'CIRCLE':
            # 处理圆形
            center = entity.dxf.center
            radius = entity.dxf.radius

            # 在Xform中创建圆形
            circle = UsdGeom.Curves.Define(stage, xform.GetPath().AppendChild("circle"))
            # 这里需要根据圆形的半径和中心点创建点集表示圆
            # 你可以根据需要自行实现这部分逻辑

    # 保存USD文件
    stage.GetRootLayer().Save()

if __name__ == "__main__":
    input_dxf_file = "/home/liufeng/isaac_test/lh/python_usd/demo.dxf"
    output_usd_file = "/home/liufeng/isaac_test/lh/python_usd/output.usd"

    entities = read_dxf(input_dxf_file)
    create_usd(entities, output_usd_file)
