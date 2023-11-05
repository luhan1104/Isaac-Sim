import ezdxf
from pxr import Usd, UsdGeom

doc = ezdxf.readfile("/home/liufeng/isaac_test/lh/python_usd/demo.dxf")

msp = doc.modelspace()

stage=Usd.Stage.CreateNew('demo.usda')




# for ref in msp.query('INSERT[name=="SCENE"]'):
#     print(str(ref))
#     print(ref.dxf.insert)
#     print(ref.attribs)
#     for entity in ref.virtual_entities():
#         if entity.dxftype() == "LWPOLYLINE":
#             print(str(entity.dxftype()))
#             p1=entity.first
i=0
for ref in msp.query('INSERT[name=="TAG5X5"]'):
    print(ref.dxf.insert)
    print(ref.dxf.insert[0])
    print(type(ref.dxf.insert))
    xform = UsdGeom.Xform.Define(stage, '/demo'+ str(i))
    cube = UsdGeom.Cube.Define(stage, '/demo'+ str(i) + '/tag'+ str(i))
    UsdGeom.XformCommonAPI(xform).SetTranslate((ref.dxf.insert[0], 
                                                ref.dxf.insert[1],
                                                ref.dxf.insert[2]))
    i+=1


line = msp.query("LWPOLYLINE").first
with line.points('xy') as points:
    print("points:", points)

print(stage.GetRootLayer().ExportToString())

for ref in msp.query('LINE'):
    print(ref.dxf.start, ref.dxf.end)

stage.GetRootLayer().Save()