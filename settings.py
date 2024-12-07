a = {
    "Глаза":
        ("Eyes", "gender", "eye_fissure_contour", "eye_fissure_opening", "eye_fissure_position",
         "eyelids_position"),
    "Нос":
        ("Eyes", "eye_fissure_contour", "eye_fissure_opening", "eye_fissure_position", "eyelids_position"),
    "Уши":
        ("Eyes", "eye_fissure_contour", "eye_fissure_opening", "eye_fissure_position", "eyelids_position"),
    "Рот":
        ("Eyes", "eye_fissure_contour", "eye_fissure_opening", "eye_fissure_position", "eyelids_position"),
    "Брови":
        ("Eyes", "eye_fissure_contour", "eye_fissure_opening", "eye_fissure_position", "eyelids_position"),
    "Волосы":
        ("Eyes", "eye_fissure_contour", "eye_fissure_opening", "eye_fissure_position", "eyelids_position"),
    "Борода":
        ("Eyes", "eye_fissure_contour", "eye_fissure_opening", "eye_fissure_position", "eyelids_position"),
    "Подбородок":
        ("Eyes", "eye_fissure_contour", "eye_fissure_opening", "eye_fissure_position", "eyelids_position"),
    "Головной убор":
        ("Eyes", "eye_fissure_contour", "eye_fissure_opening", "eye_fissure_position", "eyelids_position"),
    "Одежда":
        ("Eyes", "eye_fissure_contour", "eye_fissure_opening", "eye_fissure_position", "eyelids_position"),
    "Морщины":
        ("Eyes", "eye_fissure_contour", "eye_fissure_opening", "eye_fissure_position", "eyelids_position"),
    "Очки":
        ("Eyes", "eye_fissure_contour", "eye_fissure_opening", "eye_fissure_position", "eyelids_position"),

}
b = {
    "eyes": {
        "base_table": "Eyes",
        "translate": "Глаза",
        "properties": [{
            "name": "gender",
            "translate": "пол",
            "table": "gender"
        },
            {
                "name": "eye_fissure_contour",
                "translate": "контур глазной щели",
                "table": "eye_fissure_contour"
            },
            {
                "name": "eye_fissure_opening",
                "translate": "степень открытия глазной щели",
                "table": "eye_fissure_opening"
            },
            {
                "name": "eye_fissure_position",
                "translate": "положение глазной щели",
                "table": "eye_fissure_position"
            },
            {
                "name": "eyelids_position",
                "translate": "положение века",
                "table": "eyelids_position"
            }
        ]},
    "nose": {
        "base_table": "Nose",
        "translate": "Нос",
        "properties": [{
            "name": "gender",
            "translate": "пол",
            "table": "gender"
        },
            {
                "name": "nose_width",
                "translate": "ширина носа",
                "table": "nose_width"
            },
            {
                "name": "nose_height",
                "translate": "длина носа",
                "table": "nose_height"
            },
            {
                "name": "nose_base",
                "translate": "положение основания носа",
                "table": "nose_base"
            }
        ]},
    "mouth": {
        "base_table": "Mouth",
        "translate": "Рот",
        "properties": [{
            "name": "gender",
            "translate": "пол",
            "table": "gender"
        },
            {
                "name": "mouth_contour_fissure",
                "translate": "контур ротовой щели",
                "table": "mouth_contour_fissure"
            },
            {
                "name": "mouth_position_corners",
                "translate": "положение углов рта",
                "table": "mouth_position_corners"
            },
            {
                "name": "mouth_size",
                "translate": "размер рта",
                "table": "mouth_size"
            },
            {
                "name": "lip_border_width",
                "translate": "ширина кайм губ",
                "table": "lip_border_width"
            }
        ]},
    "ears": {
        "base_table": "Ears",
        "translate": "Уши",
        "properties": [{
            "name": "gender",
            "translate": "пол",
            "table": "gender"
        },
            {
                "name": "ears_size",
                "translate": "ушные раковины",
                "table": "ears_size"
            },
            {
                "name": "ears_prominence",
                "translate": "вид оттопыренности ушной раковины",
                "table": "ears_prominence"
            }
        ]},
    "hair": {
        "base_table": "Hair",
        "translate": "Волосы",
        "properties": [{
            "name": "gender",
            "translate": "пол",
            "table": "gender"
        },
            {
                "name": "hair_line",
                "translate": "линия роста волос",
                "table": "hair_line"
            },
            {
                "name": "hair_long",
                "translate": "длина волос",
                "table": "hair_long"
            },
            {
                "name": "hair_shape",
                "translate": "форма волос",
                "table": "hair_shape"
            }
        ]},
    "eyebrows": {
        "base_table": "Eyebrows",
        "translate": "Брови",
        "properties": [{
            "name": "gender",
            "translate": "пол",
            "table": "gender"
        },
            {
                "name": "eyebrow_width",
                "translate": "ширина бровей",
                "table": "eyebrow_width"
            },
            {
                "name": "eyebrows_length",
                "translate": "длина бровей",
                "table": "eyebrows_length"
            },
            {
                "name": "eyebrow_position",
                "translate": "положение бровей",
                "table": "eyebrow_position"
            }
        ]},
    "chin": {
        "base_table": "Chin",
        "translate": "Подбородок",
        "properties": [{
            "name": "gender",
            "translate": "пол",
            "table": "gender"
        },
            {
                "name": "chin_jawline_contour",
                "translate": "контур линии подбородка",
                "table": "chin_jawline_contour"
            },
            {
                "name": "chin_height",
                "translate": "высота подбородка",
                "table": "chin_height"
            },
            {
                "name": "chin_width",
                "translate": "ширина подбородка",
                "table": "chin_width"
            }
        ]}}
db_path = "database.sqlite"
element_images_path = "/resources/element_images/"
