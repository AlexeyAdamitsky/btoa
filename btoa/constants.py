import arnold

BT_TYPE_CONSTANTS = {
    "UINT": arnold.AI_TYPE_UINT,
    "STRING": arnold.AI_TYPE_STRING,
    "VECTOR": arnold.AI_TYPE_VECTOR,
    "VECTOR2": arnold.AI_TYPE_VECTOR2
}

BT_LIGHT_CONVERSIONS = {
    "POINT": "point_light",
    "SUN": "distant_light",
    "SPOT": "spot_light"
}

BT_LIGHT_SHAPE_CONVERSIONS = {
    "SQUARE": "quad_light",
    "DISK": "disk_light",
    "RECTANGLE": "cylinder_light"
}

BT_CONVERTIBLE_TYPES = [
    'MESH',
    'FONT',
    'CURVE'
]

BT_SET_LAMBDA = {
    "STRING": lambda n, i, v: n.set_string(i, v),
    #'ARRAY': _AiNodeSetArray,
    "BOOL": lambda n, i, v: n.set_bool(i, v),
    "BYTE": lambda n, i, v: n.set_byte(i, v),
    "INT": lambda n, i, v: n.set_int(i, v),
    "FLOAT": lambda n, i, v: n.set_float(i , v),
    "RGB": lambda n, i, v: n.set_rgb(i, *v),
    "RGBA": lambda n, i, v: n.set_rgba(i, *v),
    "VECTOR": lambda n, i, v: n.set_vector(i, *v),
    "VECTOR2": lambda n, i, v: n.set_vector2(i, *v),
    #"MATRIX": lambda n, i, v: AiNodeSetMatrix(n, i, _AiMatrix(v))
}