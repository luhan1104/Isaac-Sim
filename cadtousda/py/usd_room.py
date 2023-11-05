import ezdxf

from pxr import Usd, UsdGeom, UsdPhysics, Kind, Sdf, UsdShade

import sys
import os
import json

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

def extract_tag5X5(dxf_file_path):
    doc=ezdxf.readfile(dxf_file_path)
    msp=doc.modelspace()
    insert=[]
    
    for entity in msp.query("INSERT[name=='TAG5X5']"):
        print(entity.dxf.rotation)
        insert.append((entity.dxf.insert[0],
                       entity.dxf.insert[1],
                       entity.dxf.insert[2],
                       entity.dxf.rotation))
    
    return insert

def extract_tag2XN(dxf_file_path):
    doc=ezdxf.readfile(dxf_file_path)
    msp=doc.modelspace()
    insert=[]
    
    for entity in msp.query("INSERT[name=='TAG2XN']"):
        insert.append((entity.dxf.insert[0],
                       entity.dxf.insert[1],
                       entity.dxf.insert[2],
                       entity.dxf.rotation))
    
    return insert

def extract_ref(dxf_file_path):
    doc=ezdxf.readfile(dxf_file_path)
    msp=doc.modelspace()
    insert=[]
    
    for entity in msp.query("INSERT[name=='REF']"):
        insert.append((entity.dxf.insert[0],
                       entity.dxf.insert[1],
                       entity.dxf.insert[2],
                       entity.dxf.rotation))
    
    return insert


def create_usd(lines, inserts1, inserts2, insert3, output_path):
    stage = Usd.Stage.CreateNew(output_path)
    ref = stage.OverridePrim("/World/EMMA400")
    ref.GetReferences().AddReference("/home/liufeng/isaac_test/cadtousda/usda/EMMA400.usda")
    refxform = UsdGeom.XformCommonAPI(ref)
    UsdGeom.XformCommonAPI(refxform).SetTranslate((3, 5, 0))
    # exist_stage = Usd.Stage.Open("/home/liufeng/isaac_test/cadtousda/EMMA400.usda")
    # z轴向上
    UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.z)
    # 创建材质 5X5 二维码
    material_5X5 = UsdShade.Material.Define(stage, '/TexModel/boardMat_5X5')
    pbrShader_5X5 = UsdShade.Shader.Define(stage, '/TexModel/boardMat_5X5/PBRShader_5X5')
    pbrShader_5X5.CreateIdAttr("UsdPreviewSurface")
    pbrShader_5X5.CreateInput("roughness", Sdf.ValueTypeNames.Float).Set(0.4)
    pbrShader_5X5.CreateInput("metallic", Sdf.ValueTypeNames.Float).Set(0.0)

    material_5X5.CreateSurfaceOutput().ConnectToSource(pbrShader_5X5.ConnectableAPI(), "surface")

    stReader_5X5 = UsdShade.Shader.Define(stage, '/TexModel/boardMat_5X5/stReader_5X5')
    stReader_5X5.CreateIdAttr('UsdPrimvarReader_float2')

    diffuseTextureSampler_5X5 = UsdShade.Shader.Define(stage,'/TexModel/boardMat_5X5/diffuseTexture_5X5')
    diffuseTextureSampler_5X5.CreateIdAttr('UsdUVTexture')
    diffuseTextureSampler_5X5.CreateInput('file', Sdf.ValueTypeNames.Asset).Set("/home/liufeng/isaac_test/lh/6.png")
    diffuseTextureSampler_5X5.CreateInput("st", Sdf.ValueTypeNames.Float2).ConnectToSource(stReader_5X5.ConnectableAPI(), 'result')
    diffuseTextureSampler_5X5.CreateOutput('rgb', Sdf.ValueTypeNames.Float3)
    pbrShader_5X5.CreateInput("diffuseColor", Sdf.ValueTypeNames.Color3f).ConnectToSource(diffuseTextureSampler_5X5.ConnectableAPI(), 'rgb')
    # 2XN 二维码
    material_2XN = UsdShade.Material.Define(stage, '/TexModel/boardMat_2XN')
    pbrShader_2XN = UsdShade.Shader.Define(stage, '/TexModel/boardMat_2XN/PBRShader_2XN')
    pbrShader_2XN.CreateIdAttr("UsdPreviewSurface")
    pbrShader_2XN.CreateInput("roughness", Sdf.ValueTypeNames.Float).Set(0.4)
    pbrShader_2XN.CreateInput("metallic", Sdf.ValueTypeNames.Float).Set(0.0)

    material_2XN.CreateSurfaceOutput().ConnectToSource(pbrShader_2XN.ConnectableAPI(), "surface")

    stReader_2XN = UsdShade.Shader.Define(stage, '/TexModel/boardMat_2XN/stReader_2XN')
    stReader_2XN.CreateIdAttr('UsdPrimvarReader_float2')

    diffuseTextureSampler_2XN = UsdShade.Shader.Define(stage,'/TexModel/boardMat_2XN/diffuseTexture_2XN')
    diffuseTextureSampler_2XN.CreateIdAttr('UsdUVTexture')
    diffuseTextureSampler_2XN.CreateInput('file', Sdf.ValueTypeNames.Asset).Set("/home/liufeng/isaac_test/lh/5.png")
    diffuseTextureSampler_2XN.CreateInput("st", Sdf.ValueTypeNames.Float2).ConnectToSource(stReader_2XN.ConnectableAPI(), 'result')
    diffuseTextureSampler_2XN.CreateOutput('rgb', Sdf.ValueTypeNames.Float3)
    pbrShader_2XN.CreateInput("diffuseColor", Sdf.ValueTypeNames.Color3f).ConnectToSource(diffuseTextureSampler_2XN.ConnectableAPI(), 'rgb')

    stInput_2XN = material_2XN.CreateInput('frame:stPrimvarName', Sdf.ValueTypeNames.Token)
    stInput_2XN.Set('st')
    stReader_2XN.CreateInput('varname',Sdf.ValueTypeNames.Token).ConnectToSource(stInput_2XN)
    # 反光板
    material = UsdShade.Material.Define(stage, '/TexModel/boardMat_REF')
    pbrShader = UsdShade.Shader.Define(stage, '/TexModel/boardMat/PBRShader_REF')
    pbrShader.CreateIdAttr("UsdPreviewSurface")
    pbrShader.CreateInput("Reflection", Sdf.ValueTypeNames.Float).Set(50)
    pbrShader.CreateInput("roughness", Sdf.ValueTypeNames.Float).Set(0.4)
    pbrShader.CreateInput("metallic", Sdf.ValueTypeNames.Float).Set(0.0)
    material.CreateSurfaceOutput().ConnectToSource(pbrShader.ConnectableAPI(), "surface")
    
    
    scale = 1000
    rate = 1.01
    width = 0.02
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
    for insert in inserts1:
        xform = UsdGeom.Xform.Define(stage, "/World/tag5X5_"+ str(j))
        Usd.ModelAPI(xform).SetKind(Kind.Tokens.component)
        billboard = UsdGeom.Mesh.Define(stage, "/World/tag5X5_"+ str(j))
        UsdGeom.XformCommonAPI(xform).SetTranslate((insert[0]/scale, 
                                                    insert[1]/scale,
                                                    insert[2]/scale))
        UsdGeom.XformCommonAPI(xform).SetRotate((0, 0, insert[3]))
        billboard.CreatePointsAttr([(-0.074, -0.074, 0), (0.074, -0.074, 0), (0.074, 0.074, 0), (-0.074, 0.074, 0)])
        billboard.CreateFaceVertexCountsAttr([4])
        billboard.CreateFaceVertexIndicesAttr([0,1,2,3])
        billboard.CreateExtentAttr([(-0.074, -0.074, 0), (0.074, 0.074, 0)])
        texCoords = UsdGeom.PrimvarsAPI(billboard).CreatePrimvar("st",
                                            Sdf.ValueTypeNames.TexCoord2fArray,
                                            UsdGeom.Tokens.varying)
        texCoords.Set([(0, 0), (1, 0), (1,1), (0, 1)])
        billboard.GetPrim().ApplyAPI(UsdShade.MaterialBindingAPI)
        UsdShade.MaterialBindingAPI(billboard).Bind(material_5X5)
        j+=1

    k = 0
    for insert in inserts2:
        xform = UsdGeom.Xform.Define(stage, "/World/tag2XN_"+ str(k))
        Usd.ModelAPI(xform).SetKind(Kind.Tokens.component)
        billboard = UsdGeom.Mesh.Define(stage, "/World/tag2XN_"+ str(k))
        UsdGeom.XformCommonAPI(xform).SetTranslate((insert[0]/scale, 
                                                    insert[1]/scale,
                                                    insert[2]/scale))
        UsdGeom.XformCommonAPI(xform).SetRotate((0, 0, insert[3]))
        billboard.CreatePointsAttr([(-0.24, -0.0285, 0), (-0.24, 0.0285, 0), (0.24, 0.0285, 0), (0.24, -0.0285, 0)])
        billboard.CreateFaceVertexCountsAttr([4])
        billboard.CreateFaceVertexIndicesAttr([0,1,2,3])
        billboard.CreateExtentAttr([(-0.0285, -0.24, 0), (0.285, 0.24, 0)])
        texCoords = UsdGeom.PrimvarsAPI(billboard).CreatePrimvar("st",
                                            Sdf.ValueTypeNames.TexCoord2fArray,
                                            UsdGeom.Tokens.varying)
        texCoords.Set([(0, 0), (1, 0), (1,1), (0, 1)])
        billboard.GetPrim().ApplyAPI(UsdShade.MaterialBindingAPI)
        UsdShade.MaterialBindingAPI(billboard).Bind(material_2XN)
        k+=1

    #print(i)
    l = 0
    for insert in insert3:
        xform = UsdGeom.Xform.Define(stage, "/World/REF_"+ str(l))
        Usd.ModelAPI(xform).SetKind(Kind.Tokens.component)
        cylinder = UsdGeom.Cylinder.Define(stage, "/World/REF_"+ str(l))
        UsdGeom.XformCommonAPI(xform).SetTranslate((insert[0]/scale,
                                                    insert[1]/scale,
                                                    0.25))
        UsdGeom.XformCommonAPI(xform).SetRotate((0, 0, insert[3]))
        cylinder.CreateRadiusAttr(37.5/scale)
        cylinder.CreateHeightAttr(0.5)
        cylinder.GetPrim().ApplyAPI(UsdShade.MaterialBindingAPI)
        UsdShade.MaterialBindingAPI(cylinder.GetPrim()).Bind(material)
        rigid_api = UsdPhysics.RigidBodyAPI.Apply(xform.GetPrim())
        rigid_api.CreateRigidBodyEnabledAttr(True)
        UsdPhysics.CollisionAPI.Apply(xform.GetPrim())
        l+=1

    # 保存USD文件
    stage.GetRootLayer().Save()


if __name__ == "__main__":
    n=len(sys.argv)
    if n<2:
        dxf_file_path = "/home/liufeng/isaac_test/cadtousda/dxf/room.dxf"
        usd_file_path = "/home/liufeng/isaac_test/cadtousda/usda/room.usda"
    else:
        dxf_file_path = sys.argv[1]
        usd_file_path = sys.argv[2]

    layer_name = ""
    current_path = os.getcwd()
    print(current_path)
    configPath=current_path+"/config.json"
    with open(configPath, 'r') as f:
        config_node = json.load(f)
        layer_name = config_node["layer_name"]
    print(layer_name)
    lines = extract_lines(dxf_file_path, layer_name)
    print(len(lines))
    tag5X5_info = extract_tag5X5(dxf_file_path)
    tag2XN_info = extract_tag2XN(dxf_file_path)
    ref_info = extract_ref(dxf_file_path)
    create_usd(lines, tag5X5_info, tag2XN_info, ref_info, usd_file_path)



