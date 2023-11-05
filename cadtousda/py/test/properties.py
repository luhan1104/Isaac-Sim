from pxr import Usd, Vt, UsdGeom
stage = Usd.Stage.Open('HelloWorld.usda')
xform = stage.GetPrimAtPath('/hello')
sphere = stage.GetPrimAtPath('/hello/world')

print(xform.GetPropertyNames())

print(sphere.GetPropertyNames())

extentAttr = sphere.GetAttribute('extent')
print(extentAttr.Get())

radiusAttr = sphere.GetAttribute('radius')
print(radiusAttr.Get())
radiusAttr.Set(2)

extentAttr.Set(extentAttr.Get() * 2)

sphereSchema = UsdGeom.Sphere(sphere)

color = sphereSchema.GetDisplayColorAttr()
print(color.Get())

color.Set([(1, 0, 0)])

print(stage.GetRootLayer().ExportToString())
stage.GetRootLayer().Save()