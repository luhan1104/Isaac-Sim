import ezdxf

# 打开DXF文件
doc = ezdxf.readfile("/home/liufeng/isaac_test/cadtousda/dxf/jskjy.dxf")

# 获取模型空间（Modelspace）
msp = doc.modelspace()

# 获取 LWPOLYLINE 对象
lw_polyline = None
for entity in msp.query('LWPOLYLINE'):
    if entity.dxf.layer == "WALL":
        lw_polyline = entity
        if lw_polyline:
            # 获取 LWPOLYLINE 的顶点信息
            vertices = lw_polyline.get_points()
            print(vertices)
