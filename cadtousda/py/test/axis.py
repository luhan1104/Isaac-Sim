from pxr import Usd, UsdGeom, Gf

# Create a new USD stage
stage = Usd.Stage.CreateNew("camera_setup.usda")

# Define the root layer
root = stage.DefinePrim("/")

# Create a camera
camera = UsdGeom.Camera.Define(stage, "/camera")

# Set camera parameters (e.g., focal length, horizontal aperture)
camera.GetFocalLengthAttr().Set(50.0)
camera.GetHorizontalApertureAttr().Set(36.0)
camera.GetVerticalApertureAttr().Set(24.0)

# Create a transform for the camera
camera_xform = UsdGeom.Xform.Define(stage, "/camera_xform")

# Set the camera's position and orientation
camera_xform.AddTranslateOp().Set(value=Gf.Vec3d(0.0, 0.0, 0.0))  # Set camera position
camera_xform.AddRotateZOp().Set(value=90.0)  # Rotate the camera 90 degrees around Z-axis

# Connect the camera to the transform
# camera_xform.GetPrim().GetReferences().AddReference(camera.GetPath())

# Save the USD file
stage.GetRootLayer().Save()
