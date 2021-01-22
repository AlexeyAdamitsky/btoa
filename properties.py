import bpy
from bpy.types import Scene, PropertyGroup, Camera
from bpy.props import BoolProperty, IntProperty, FloatProperty, PointerProperty, EnumProperty

class ArnoldOptions(PropertyGroup):
    # Sampling
    aa_samples: IntProperty(
        name="Camera (AA) Samples",
        description="Supersampling control over the number of rays per pixel that will be traced from the camera. The higher the number of samples, the better the anti-aliasing quality, and the longer the render times. The exact number of rays per pixel is the square of this value",
        min=0,
        default=3
        )
    diffuse_samples: IntProperty(
        name="Diffuse Samples",
        description="Controls the number of rays fired when computing the reflected indirect-radiance integrated over the hemisphere. The exact number of hemispherical rays is the square of this value. Increase this number to reduce the indirect diffuse noise",
        min=0,
        default=2
        )
    specular_samples: IntProperty(
        name="Specular Samples",
        description="Controls the number of rays fired when computing the reflected indirect-radiance integrated over the hemisphere weighted by a specular BRDF. The exact number of rays is the square of this value. Increase this number to reduce the indirect specular noise",
        min=0,
        default=2
        )
    transmission_samples: IntProperty(
        name="Transmission Samples",
        description="Controls the number of samples used to simulate the microfacet-based transmission evaluations. Increase this value to resolve any noise in the transmission",
        min=0,
        default=2
        )
    sss_samples: IntProperty(
        name="SSS Samples",
        description="This value controls the number of lighting samples (direct and indirect) that will be taken to estimate lighting within a radius of the point being shaded to compute sub-surface scattering. Higher values produce a cleaner solution but will take longer to render",
        min=0,
        default=2
        )
    volume_samples: IntProperty(
        name="Volume Samples",
        description="Controls the number of sample rays that get fired to compute indirect lighting of the volume",
        min=0,
        default=2
        )
    aa_seed: IntProperty(
        name="AA Seed",
        description="The AA_seed by default is set to the current frame number, so the noise changes at every frame, like film grain. This can be locked so that the sampling noise won't change by setting a value > 0",
        min=0, 
        default=0
        )
    sample_clamp: IntProperty(
        name="Sample Clamp",
        description="If enabled, this control will clamp pixel samples to this specified maximum value. This can make it easier to anti-alias certain high-dynamic-range effects such as bright motion-blurred specular streaks (at the cost of reduced contrast)",
        min=0,
        default=10
        )
    clamp_aovs: BoolProperty(
        name="Clamp AOVs",
        description="With this control enabled the pixel samples of the AOVs will also be clamped. AOV clamping will affect every RGB and RGBA (except the A component) AOV. Currently, there is no way to tell Arnold which AOV's to clamp and which ones to preserve"
        )
    indirect_sample_clamp: IntProperty(
        name="Indirect Sample Clamp",
        description="The threshold to clamp away fireflies from indirect light samples and reduce noise. This works similarly to AA_sample_clamp but preserves specular highlights from direct lighting. Lower values result in more aggressive noise reduction, possibly at the expense of dynamic range",
        min=0,
        default=10
        )
    low_light_threshold: FloatProperty(
        name="Low Light Threshold",
        description="Raising this value can speed up rendering by allowing Arnold to ignore tracing a shadow ray for light samples whose light contribution is below a certain value. The point of low_light_threshold is to save casting shadow rays when Arnold knows that the error from not casting that ray is below a certain amount. This makes sense because below a certain threshold there will be no perceptible difference between shadowed and unshadowed areas",
        min=0,
        default=0.001
        )
    use_adaptive_sampling: BoolProperty()
    adaptive_aa_samples_max: IntProperty(
        name="AA Samples Max",
        description="Sets the maximum amount of supersampling. It controls the per-pixel maximum sampling rate and is equivalent to the units used by AA_samples. Adaptive sampling is enabled when AA_samples_max > Camera (AA) samples and Camera (AA) samples >= 2. Scenes with a large amount of depth of field or motion blur may require higher Max. Camera (AA) values. This parameter can also help with 'buzzing' speculars and hair shading as well",
        min=0, 
        default=0
        )
    adaptive_threshold: FloatProperty(
        name="Adaptive Threshold",
        description="The threshold which triggers/terminates adaptive-AA. This value controls how sensitive to noise the adaptive sampling algorithm gets. Lower numbers will detect more noise. The default value should work well for most scenes",
        min=0,
        default=0.015
        )

    # Ray depth
    total_depth: IntProperty(name="Total Depth", min=0, default=10)
    diffuse_depth: IntProperty(name="Diffuse Depth", min=0, default=1)
    specular_depth: IntProperty(name="Specular Depth", min=0, default=1)
    transmission_depth: IntProperty(name="Transmission Depth", min=0, default=10)
    volume_depth: IntProperty(name="Volume Depth", min=0)
    transparency_depth: IntProperty(name="Transparency Depth", min=0, default=10)

    # Rendering
    bucket_size: IntProperty(
        name="Bucket Size", 
        description="The size of the image buckets. Bigger buckets use more memory, while smaller buckets may perform redundant computations and filtering and thus render slower but give initial faster feedback",
        min=2,
        default=64
        )
    bucket_scanning: EnumProperty(
        name="Bucket Scanning",
        description="Specifies the spatial order in which the image buckets (i.e. threads) will be processed. By default, buckets start in the center of the image and proceed outwards in a spiral pattern",
        items=[
            ('top', "Top", "Top"),
            ('left', "Left", "Left"),
            ('random', "Random", "Random"),
            ('spiral', "Spiral", "Spiral"),
            ('hilbert', "Hilbert", "Hilbert"),
        ],
        default='spiral'
        )
    parallel_node_init: BoolProperty(
        name="Parallel Node Init",
        description="Enables parallel initialization of all scene nodes",
        default=True
        )
    threads: IntProperty(
        name="Threads",
        description="The number of threads used for rendering. Set it to zero to autodetect and use as many threads as cores in the system. Negative values indicate how many cores not to use, so that -3, for instance, will use 29 threads on a 32 logical core machine. Negative values are useful when you want to reserve some of the CPU for non-Arnold tasks"
        )

class ArnoldCamera(PropertyGroup):
    # Basic lens settings
    camera_type: EnumProperty(
        name="Type",
        items=[
            ('cyl_camera', "Cylindrical ", "Cylindrical "),
            ('fisheye_camera', "Fisheye", "Fisheye"),
            ('ortho_camera', "Orthographic", "Orthographic"),
            ('persp_camera', "Perspective", "Perspective"),
            ('spherical_camera', "Spherical", "Spherical"),
            ('vr_camera', "VR", "VR"),
            ('uv_camera', "UV", "UV"),
        ],
        default='persp_camera'
    )

    exposure: FloatProperty(name="Exposure")

    # DOF
    enable_dof: BoolProperty(name="Enable DOF")
    focus_distance: FloatProperty(name="Focus Distance")
    aperture_size: FloatProperty(name="Size", min=0)
    aperture_blades: IntProperty(name="Blades", min=0)
    aperture_rotation: FloatProperty(name="Rotation")
    aperture_blade_curvature: FloatProperty(name="Curvature", min=-1, max=1)
    aperture_aspect_ratio: FloatProperty(name="Aspect Ratio", min=0, default=1)
    flat_field_focus: BoolProperty(name="Flat Field Focus")

    # Shutter
    shutter_start: FloatProperty(name="Shutter: Start")
    shutter_end: FloatProperty(name="Shutter: Stop")

    shutter_type: EnumProperty(
        name="Shutter Type",
        items=[
            ('box', "Box", "Box"),
            ('triangle', "Triangle", "Triangle"),
            #('curve', "Curve", "Curve")
        ],
        default='box'
    )

    rolling_shutter: EnumProperty(
        name="Rolling Shutter",
        items=[
            ('off', "Off", "Off"),
            ('top', "Top", "Top"),
            ('bottom', "Bottom", "Bottom"),
            ('left', "Left", "Left"),
            ('right', "Right", "Right")
        ],
        default='off'
    )
    rolling_shutter_duration: FloatProperty(name="Rolling Shutter: Duration")

def register():
    bpy.utils.register_class(ArnoldOptions)
    bpy.utils.register_class(ArnoldCamera)
    Scene.arnold_options = PointerProperty(type=ArnoldOptions)
    Camera.arnold = PointerProperty(type=ArnoldCamera)

def unregister():
    del Camera.arnold
    del Scene.arnold_options
    bpy.utils.unregister_class(ArnoldCamera)
    bpy.utils.unregister_class(ArnoldOptions)