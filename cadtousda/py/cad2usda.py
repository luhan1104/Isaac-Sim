import ezdxf

from pxr import Usd, UsdGeom, UsdPhysics, Kind, Sdf, UsdShade

import sys
import os
import json
import math 

def extract_lines(dxf_file_path, layer_name):
    doc=ezdxf.readfile(dxf_file_path)
    msp=doc.modelspace()
    #lines=[]
    lines = set()
    for entity in msp.query('*'):  # 遍历模型空间中的实体
        if entity.dxf.layer == layer_name:
            if entity.dxftype() == "LINE":
                start_point_x = entity.dxf.start.x
                start_point_y = entity.dxf.start.y
                end_point_x = entity.dxf.end.x
                end_point_y = entity.dxf.end.y
                lines.add((start_point_x, 
                              start_point_y,
                              end_point_x,
                              end_point_y))
    # for entity in msp.query('LWPOLYLINE'):
    #     if entity.dxf.layer == "WALL":
    #         lw_polyline = entity
    #         if lw_polyline:
    #             # 获取 LWPOLYLINE 的顶点信息
    #             vertices = lw_polyline.get_points()
    #             # print(vertices)
    #             for i in range(len(vertices)):
    #                 if i == len(vertices)-1:
    #                     start_point_x = vertices[i][0]
    #                     start_point_y = vertices[i][1]
    #                     end_point_x = vertices[0][0]
    #                     end_point_y = vertices[0][1]
    #                 else:
    #                     start_point_x = vertices[i][0]
    #                     start_point_y = vertices[i][1]
    #                     end_point_x = vertices[i+1][0]
    #                     end_point_y = vertices[i+1][1]
    #                 lines.add((start_point_x, 
    #                               start_point_y,
    #                               end_point_x,
    #                               end_point_y))
                    
    return lines

def extract_polylines(dxf_file_path):
    doc=ezdxf.readfile(dxf_file_path)
    msp=doc.modelspace()
    polylines=[]
    for entity in msp.query('*'):  # 遍历模型空间中的实体
        if entity.dxf.layer == "WALL":
            if entity.dxftype() == "LWPOLYLINE":
                lw_polyline = entity
                if lw_polyline:
                    # 获取 LWPOLYLINE 的顶点信息
                    vertices = lw_polyline.get_points()
                    print(vertices)  
    return polylines

def get_car_info(dxf_file_path):
    doc=ezdxf.readfile(dxf_file_path)
    msp=doc.modelspace()
    car_info=[]
    for entity in msp.query('*'):  # 遍历模型空间中的实体
        if entity.dxf.layer == 'L-AGV车体':
            car_info.append((entity.dxf.insert[0],
                       entity.dxf.insert[1],
                       entity.dxf.insert[2],
                       entity.dxf.rotation))
            break
    return car_info

def extract_tag(dxf_file_path):
    doc=ezdxf.readfile(dxf_file_path)
    msp=doc.modelspace()
    insert=[]
    
    for entity in msp.query("INSERT[name=='TAG5X5']"):
        id = 0
        for attrib in entity.attribs:
            if attrib.dxf.tag == 'ID':
                id = int(attrib.dxf.text)
        insert.append((entity.dxf.insert[0],
                       entity.dxf.insert[1],
                       entity.dxf.insert[2],
                       entity.dxf.rotation,
                       id, 'TAG5X5', 'shelf',
                       0.148, 0.148))
    for entity in msp.query("INSERT[name=='TAG2X2']"):
        id = 0
        for attrib in entity.attribs:
            if attrib.dxf.tag == 'ID':
                id = int(attrib.dxf.text)
        insert.append((entity.dxf.insert[0],
                       entity.dxf.insert[1],
                       entity.dxf.insert[2],
                       entity.dxf.rotation,
                       id, 'TAG2X2', '2X2B',
                       0.0529, 0.0529))
        
    for entity in msp.query("INSERT[name=='TAG4X4']"):
        id = 0
        for attrib in entity.attribs:
            if attrib.dxf.tag == 'ID':
                id = int(attrib.dxf.text)
        insert.append((entity.dxf.insert[0],
                       entity.dxf.insert[1],
                       entity.dxf.insert[2],
                       entity.dxf.rotation,
                       id, 'TAG4X4', '4X4',
                       0.1093, 0.1093))
        
    for entity in msp.query("INSERT[name=='TAG2X7']"):
        id = 0
        for attrib in entity.attribs:
            if attrib.dxf.tag == 'ID':
                id = int(attrib.dxf.text)
        insert.append((entity.dxf.insert[0] - 210/2 * math.sin(entity.dxf.rotation * math.pi/180),
                       entity.dxf.insert[1] + 210/2 * math.cos(entity.dxf.rotation * math.pi/180),
                       entity.dxf.insert[2],
                       entity.dxf.rotation,
                       id, 'TAG2X7', '2X7_CS1F4',
                       0.21, 0.057))
    
    for entity in msp.query("INSERT[name=='TAG2XN(1000)']"):
        insert.append((entity.dxf.insert[0] - 1000/2 * math.sin(entity.dxf.rotation * math.pi/180),
                       entity.dxf.insert[1] + 1000/2 * math.cos(entity.dxf.rotation * math.pi/180),
                       entity.dxf.insert[2],
                       entity.dxf.rotation,
                       1, 'TAG2XN', '2XN',
                       1, 0.057))
    for entity in msp.query("INSERT[name=='TAG2XN(2000)']"):
        insert.append((entity.dxf.insert[0] - 2000/2 * math.sin(entity.dxf.rotation * math.pi/180),
                       entity.dxf.insert[1] + 2000/2 * math.cos(entity.dxf.rotation * math.pi/180),
                       entity.dxf.insert[2],
                       entity.dxf.rotation,
                       2, 'TAG2XN', '2XN',
                       2, 0.057))
    for entity in msp.query("INSERT[name=='TAG2XN(3000)']"):
        insert.append((entity.dxf.insert[0] - 3000/2 * math.sin(entity.dxf.rotation * math.pi/180),
                       entity.dxf.insert[1] + 3000/2 * math.cos(entity.dxf.rotation * math.pi/180),
                       entity.dxf.insert[2],
                       entity.dxf.rotation,
                       3, 'TAG2XN', '2XN',
                       3, 0.057))
    
    return insert


def create_usd(lines, tag_info, car_info, output_path):
    scale = 1000
    rate = 1.01
    width = 0.02
    stage = Usd.Stage.CreateNew(output_path)
    ref = stage.OverridePrim("/World/EMMA400")
    ref.GetReferences().AddReference("/home/liufeng/isaac_test/cadtousda/usda/EMMA4001.usda")
    refxform = UsdGeom.XformCommonAPI(ref)
    UsdGeom.XformCommonAPI(refxform).SetTranslate((car_info[0][0]/scale, car_info[0][1]/scale, 0))
    # z轴向上
    UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.z)
    # 创建Xform代表3D空间
    xform = UsdGeom.Xform.Define(stage, "/World")
    rotate_degrees = (0.0, 0.0, 0.0)  # 将坐标系旋转90度，使Z轴向上
    xform.AddRotateXOp().Set(rotate_degrees[0])
    xform.AddRotateYOp().Set(rotate_degrees[1])
    xform.AddRotateZOp().Set(rotate_degrees[2])
    i = 0
    for line in lines:
        # 处理直线
        start_point_x = line[0]
        start_point_y = line[1]
        end_point_x = line[2]
        end_point_y = line[3]

        if(abs(start_point_x - end_point_x)<1):
            # 在Xform中创建直线
            xform = UsdGeom.Xform.Define(stage, "/World/Cube"+ str(i))
            cube = UsdGeom.Cube.Define(stage, "/World/Cube"+ str(i))
            # 调整大小
            extentAttr = cube.GetSizeAttr()
            #print(extentAttr.Get())
            extentAttr.Set(1)
            scale_factor = (width, abs(end_point_y - start_point_y)/(scale*rate), 1)  # 缩放因子，分别表示X、Y和Z方向的缩放
            xform.AddScaleOp().Set(value=scale_factor)
            UsdGeom.XformCommonAPI(xform).SetTranslate((start_point_x/scale, (start_point_y + end_point_y)/(2*scale), 0.5))
            CubeSchema = UsdGeom.Cube(cube)
            color = CubeSchema.GetDisplayColorAttr()
            #color.Set([(1, 0, 0)])
            rigid_api = UsdPhysics.RigidBodyAPI.Apply(xform.GetPrim())
            rigid_api.CreateRigidBodyEnabledAttr(True)
            UsdPhysics.CollisionAPI.Apply(xform.GetPrim())
            i+=1
        elif(abs(start_point_y - end_point_y)<1):
            xform = UsdGeom.Xform.Define(stage, "/World/Cube"+ str(i))
            cube = UsdGeom.Cube.Define(stage, "/World/Cube"+ str(i))
            # 调整大小
            extentAttr = cube.GetSizeAttr()
            #print(extentAttr.Get())
            extentAttr.Set(1)
            scale_factor = (abs(end_point_x - start_point_x)/(scale*rate), width, 1)  # 缩放因子，分别表示X、Y和Z方向的缩放
            xform.AddScaleOp().Set(value=scale_factor)
            UsdGeom.XformCommonAPI(xform).SetTranslate(((start_point_x + end_point_x)/(2*scale), start_point_y/scale,  0.5))
            CubeSchema = UsdGeom.Cube(cube)
            color = CubeSchema.GetDisplayColorAttr()
            #color.Set([(1, 0, 0)])
            rigid_api = UsdPhysics.RigidBodyAPI.Apply(xform.GetPrim())
            rigid_api.CreateRigidBodyEnabledAttr(True)
            UsdPhysics.CollisionAPI.Apply(xform.GetPrim())
            i+=1

    j = 0
    for tag in tag_info:
        # 创建材质 二维码
        length = tag[7]/2
        width = tag[8]/2
        material_5X5 = UsdShade.Material.Define(stage, '/TexModel/boardMat_'+ tag[5] +'_'+ str(tag[4]))
        pbrShader_5X5 = UsdShade.Shader.Define(stage, '/TexModel/boardMat_'+ tag[5] +'_'+ str(tag[4]) + '/PBRShader_'+ tag[5] +'_'+ str(tag[4]))
        pbrShader_5X5.CreateIdAttr("UsdPreviewSurface")
        pbrShader_5X5.CreateInput("roughness", Sdf.ValueTypeNames.Float).Set(0.4)
        pbrShader_5X5.CreateInput("metallic", Sdf.ValueTypeNames.Float).Set(0.0)

        material_5X5.CreateSurfaceOutput().ConnectToSource(pbrShader_5X5.ConnectableAPI(), "surface")

        stReader_5X5 = UsdShade.Shader.Define(stage, '/TexModel/boardMat_'+ tag[5] +'_'+ str(tag[4]) + '/stReader_'+tag[5]+'_'+ str(tag[4]))
        stReader_5X5.CreateIdAttr('UsdPrimvarReader_float2')

        diffuseTextureSampler_5X5 = UsdShade.Shader.Define(stage,'/TexModel/boardMat_'+ tag[5] +'_'+ str(tag[4]) + 
                                                           '/diffuseTexture_'+ tag[5] +'_'+ str(tag[4]))
        diffuseTextureSampler_5X5.CreateIdAttr('UsdUVTexture')
        pic_path = "/home/liufeng/isaac_test/cadtousda/tag/"+ tag[5]+"/"+tag[6]+"_"+str(tag[4])+".png"
        if os.path.exists(pic_path):
            diffuseTextureSampler_5X5.CreateInput('file', Sdf.ValueTypeNames.Asset).Set("/home/liufeng/isaac_test/cadtousda/tag/"+ tag[5]+"/"+tag[6]+"_"+str(tag[4])+".png")
        else:
            diffuseTextureSampler_5X5.CreateInput('file', Sdf.ValueTypeNames.Asset).Set("/home/liufeng/isaac_test/lh/6.png")
            print("tag_type:"<< tag[5]<<" id:"<< tag[4]<<" picture is not exist")
            continue
        diffuseTextureSampler_5X5.CreateInput("st", Sdf.ValueTypeNames.Float2).ConnectToSource(stReader_5X5.ConnectableAPI(), 'result')
        diffuseTextureSampler_5X5.CreateOutput('rgb', Sdf.ValueTypeNames.Float3)
        pbrShader_5X5.CreateInput("diffuseColor", Sdf.ValueTypeNames.Color3f).ConnectToSource(diffuseTextureSampler_5X5.ConnectableAPI(), 'rgb')
        xform = UsdGeom.Xform.Define(stage, "/World/"+ tag[5] + "_" + str(j))
        Usd.ModelAPI(xform).SetKind(Kind.Tokens.component)
        billboard = UsdGeom.Mesh.Define(stage, "/World/"+ tag[5] + "_"+ str(j))
        UsdGeom.XformCommonAPI(xform).SetTranslate((tag[0]/scale, 
                                                    tag[1]/scale,
                                                    tag[2]/scale))
        UsdGeom.XformCommonAPI(xform).SetRotate((0, 0, tag[3]))
        billboard.CreatePointsAttr([(-width, -length, 0), (width, -length, 0), (width, length, 0), (-width, length, 0)])
        billboard.CreateFaceVertexCountsAttr([4])
        billboard.CreateFaceVertexIndicesAttr([0,1,2,3])
        billboard.CreateExtentAttr([(-width, -length, 0), (width, length, 0)])
        texCoords = UsdGeom.PrimvarsAPI(billboard).CreatePrimvar("st",
                                            Sdf.ValueTypeNames.TexCoord2fArray,
                                            UsdGeom.Tokens.varying)
        texCoords.Set([(0, 0), (1, 0), (1,1), (0, 1)])
        billboard.GetPrim().ApplyAPI(UsdShade.MaterialBindingAPI)
        UsdShade.MaterialBindingAPI(billboard).Bind(material_5X5)
        j+=1

    # 保存USD文件
    stage.GetRootLayer().Save()


if __name__ == "__main__":
    n=len(sys.argv)
    if n<2:
        dxf_file_path = "/home/liufeng/isaac_test/cadtousda/dxf/jskjy_1020.dxf"
        usd_file_path = "/home/liufeng/isaac_test/cadtousda/usda/jskjy_1020.usda"
    else:
        dxf_file_path = sys.argv[1]
        usd_file_path = sys.argv[2]

    layer_name = ""
    car_type = ""
    current_path = os.getcwd()
    print(current_path)
    configPath=current_path+"/config.json"
    with open(configPath, 'r') as f:
        config_node = json.load(f)
        layer_name = config_node["layer_name"]
        car_type = config_node["car_type"]
    print(layer_name)
    lines = extract_lines(dxf_file_path, layer_name)
    print(len(lines))
    car_info = get_car_info(dxf_file_path)
    tag_info = extract_tag(dxf_file_path)
    print(tag_info)
    create_usd(lines, tag_info, car_info, usd_file_path)



