# Changelog #

## Alpha v0.2.0 ##

This alpha release focused largely on bug fixes and some small new features after the initial alpha release.

- We completely refactored how BtoA talks to the Arnold SDK in an effort to move toward a truly GPL-compliant add-on. BtoA no longer makes direct calls to the Arnold API and instead interacts with a `btoa` middle-man module, passing data as generic Python objects (strings, ints, floats, lists, etc). We understand this alone may not be enough and are actively talking with Autodesk and other parties to ensure we do everything we can to be compliant with the license.

- Added support for:
    - Fonts
    - Curves
    - Checkerboard shader
    - Cell noise shader
    - Color correction shader

- BtoA now supports Arnold 6.0.1.0 through 6.2.0.1 out-of-the-box.

- Fixes bug that kept users from setting the path to their Arnold SDK installation in the add-on preferences.

- AiStandardSurface node now supports "subsurface type", "transmission depth" parameters.

- Cylinder light gizmo now scales to fit the size of the underlying rectangle light for better viewport visualization.

- Fixes bug that let Arnold nodes show up in non-Arnold node editor spaces.

- Adds depth-of-field focus object to camera panel for better DOF rendering support.

- Light shadow color now renders properly.

- Other minor bug fixes

## Alpha v0.1.0 ##

This is the first publicly available alpha meant for community testing.

- Supported on Windows, macOS, and Linux (RedHat Enterprise or compatible)
- Includes support for geometry meshes and the modifier stack.
- Basic light support, including point lights, spot lights, distant lights, quad lights, disk lights, and cylinder lights.
- Supports rendering to the Render Result window, but not in  the viewport yet.
- Basic material/node support
    - Ambient occlusion shader
    - Car paint shader
    - Flat shader
    - Lambert shader
    - Standard surface shader
    - Matte shader
    - Shadow matte shader
    - Wireframe shader
    - Image shader
    - UV projection shader
    - Coordinate space convenience node
- Basic color management support, defaulting to Filmic if no custom OCIO config is set.
- Respects visibility settings in Outliner for rendering
