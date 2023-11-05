from pxr import Usd, UsdGeom

stage = Usd.Stage.CreateNew('HelloWorld.usda')
xform = UsdGeom.Xform.Define(stage, '/hello')
sphere = UsdGeom.Sphere.Define(stage, '/hello/world')
stage.GetRootLayer().Save()