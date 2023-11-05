from pxr import Usd, UsdGeom

stage = Usd.Stage.Open('HelloWorld.usda')
xform = stage.GetPrimAtPath('/hello')
stage.SetDefaultPrim(xform)
UsdGeom.XformCommonAPI(xform).SetTranslate((1, 2, 3))
print(stage.GetRootLayer().ExportToString())
stage.GetRootLayer().Save()