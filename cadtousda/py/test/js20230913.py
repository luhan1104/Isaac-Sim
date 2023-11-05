from pxr import Usd, Vt, UsdGeom, UsdPhysics
#stage = Usd.Stage.Open('../js20230913.usda')
stage = Usd.Stage.Open('../EMMA400_RF.usda')
print(stage.GetRootLayer().ExportToString())

#xform = UsdGeom.Xform.Define(stage, '/World')
#sphere = UsdGeom.Sphere.Define(stage, '/World/Sphere')
print(UsdPhysics.MaterialAPI.Get(stage, '/World/tag1'))
#stage.GetRootLayer().Save()