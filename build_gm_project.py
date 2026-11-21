#!/usr/bin/env python3
"""
Generates a complete, schema-valid GameMaker LTS 2026 (resourceVersion 2.0) project:
  bebechad-home-alone/gm-project/BebechadHomeAlone.yyp

Uses pure Python stdlib (no external packages required).
"""
import json
import os
import shutil
import struct
import uuid
import zipfile
import zlib

ROOT = os.path.dirname(os.path.abspath(__file__))
RAW_DIR = os.path.join(ROOT, "assets-raw")
GM_DIR = os.path.join(ROOT, "gm-project")
EXPORT_DIR = os.path.join(ROOT, "export")


def write_png(path, w, h, rgba_bytes):
    def chunk(tag, data):
        return (
            struct.pack(">I", len(data))
            + tag
            + data
            + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)
        )

    raw = bytearray()
    stride = w * 4
    for y in range(h):
        raw.append(0)
        raw.extend(rgba_bytes[y * stride : (y + 1) * stride])
    ihdr = struct.pack(">IIBBBBB", w, h, 8, 6, 0, 0, 0)
    png = b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr) + chunk(b"IDAT", zlib.compress(bytes(raw), 9)) + chunk(b"IEND", b"")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(png)


def hex_rgba(h, a=255):
    h = h.lstrip("#")
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), a)


def make_grid_png(path, rows, palette, scale=1):
    gh = len(rows)
    gw = len(rows[0])
    w, h = gw * scale, gh * scale
    buf = bytearray(w * h * 4)
    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            if ch not in palette:
                continue
            r, g, b, a = palette[ch]
            for sy in range(scale):
                for sx in range(scale):
                    idx = ((y * scale + sy) * w + (x * scale + sx)) * 4
                    buf[idx : idx + 4] = bytes((r, g, b, a))
    write_png(path, w, h, buf)


def build_placeholder_sprites():
    # 1) Top-down Mouse Enemy (16x16 scaled x2 = 32x32, WIDER spaced eyes + cute snout & ears!)
    mouse_rows = [
        ".......pp.......",
        "......p..p......",
        "........p.......",
        "......kddk......",
        ".....kggggk.....",
        "....kggllggk....",
        "...kggggggggk...",
        "...kggggggggk...",
        "..kppggggggppk..",
        "..kppggggggppk..",
        "...kggggggggk...",
        "...kgbggggbgk...",
        "....kggllggk....",
        ".....kgppgk.....",
        "......kppk......",
        ".......kk.......",
    ]
    mouse_pal = {
        "k": hex_rgba("#24202e"),
        "d": hex_rgba("#525464"),
        "g": hex_rgba("#878a9c"),
        "l": hex_rgba("#b0b4c4"),
        "p": hex_rgba("#e58096"),
        "b": hex_rgba("#121018"),
    }
    make_grid_png(os.path.join(RAW_DIR, "spr_mouse_top.png"), mouse_rows, mouse_pal, scale=2)

    # 2) Top-down King Rat Boss (32x32 scaled x2 = 64x64, crisp pixel art, centered royal crown, ZERO blue spot!)
    rat_rows = [
        "..............kkkk..............",
        ".............kppppk.............",
        "............kpP..Ppk............",
        ".............kk...pk............",
        ".................kpk............",
        "................kpk.............",
        "..............kkpkk.............",
        "...........kkkdddddkkk..........",
        ".........kkdddddddddddkl........",
        "........kdddgggggggggdddk.......",
        ".......kddgglllllllllggddk......",
        "......kddggllgggggggllggddk.....",
        "......kddgggggggggggggggddk.....",
        ".....kddgggggglllllggggggddk....",
        ".....kddgggggggggggggggggddk....",
        "....kkddggggkggkggkggggddkk.....",
        "...kppkdgkgykgkyhkgkygkdgkppk...",
        "..kpPPpkdkyykgyyykgyykdkpPPpk...",
        "..kpPPpkdkyyyyrryyyyykdkpPPpk...",
        "...kppkdgkkooyyyyyyookkgdkppk...",
        "....kkddgggkoooooooookggddkk....",
        "......kddgggkkkkkkkkkgggddk.....",
        ".......kddggllgggggggllggddk....",
        ".......kddggwbgggggggbwggddk....",
        "........kddgbbgggggggbbgddk.....",
        ".....ssskddggggglllgggggddksss..",
        "....s....kddggglllllgggddk....s.",
        "......ss..kddggpppppgddk..ss....",
        ".....s.....kkddppppddkk.....s...",
        "..............kkpppkk...........",
        "...............kkkkk............",
        "................................",
    ]
    # Cleanly fix row 8 tail & pad to 32
    rat_rows[8] = ".........kkdddddddddddkk........"
    rat_rows = [r[:32].ljust(32, ".") for r in rat_rows]
    rat_pal = {
        "k": hex_rgba("#1c1724"),  # dark outline
        "d": hex_rgba("#454652"),  # dark charcoal fur
        "g": hex_rgba("#676978"),  # mid grey fur
        "l": hex_rgba("#8a8d9e"),  # light dorsal fur
        "p": hex_rgba("#e87b92"),  # pink ears/nose/tail
        "P": hex_rgba("#bf4e68"),  # inner ear shadow
        "b": hex_rgba("#110e18"),  # black eyes
        "w": hex_rgba("#ffffff"),  # eye glint
        "s": hex_rgba("#a8b2c2"),  # whiskers
        "o": hex_rgba("#9c6314"),  # crown dark gold rim
        "y": hex_rgba("#f5c742"),  # crown gold body
        "h": hex_rgba("#fff3a8"),  # crown highlight
        "r": hex_rgba("#e63956"),  # crown ruby jewel
    }
    make_grid_png(os.path.join(RAW_DIR, "spr_rat_boss_top.png"), rat_rows, rat_pal, scale=2)

    # 3) Catnip Leaf Currency ("Кошачья мята", 24x24)
    nip_rows = [
        ".....kk.....",
        "....kllk....",
        "...kllllk...",
        "..kllggllk..",
        ".kllgddgllk.",
        ".klgddddglk.",
        "..kggddggk..",
        "...kggggk...",
        "....kddk....",
        ".....kk.....",
        ".....kd.....",
        ".....kk.....",
    ]
    nip_pal = {
        "k": hex_rgba("#122418"),
        "d": hex_rgba("#24693b"),
        "g": hex_rgba("#44ba68"),
        "l": hex_rgba("#90f5a8"),
    }
    make_grid_png(os.path.join(RAW_DIR, "spr_catnip.png"), nip_rows, nip_pal, scale=2)


def png_size(path):
    with open(path, "rb") as f:
        f.seek(16)
        return struct.unpack(">II", f.read(8))


def save_yy(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)
        f.write("\n")


def save_text(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content.lstrip("\n"))


def make_sprite(name, src_png, center_origin=True):
    w, h = png_size(src_png)
    frame_id = str(uuid.uuid4())
    layer_id = str(uuid.uuid4())
    sdir = os.path.join(GM_DIR, "sprites", name)
    ldir = os.path.join(sdir, "layers", frame_id)
    os.makedirs(ldir, exist_ok=True)
    shutil.copy2(src_png, os.path.join(sdir, f"{frame_id}.png"))
    shutil.copy2(src_png, os.path.join(ldir, f"{layer_id}.png"))

    ox = w // 2 if center_origin else 0
    oy = h // 2 if center_origin else 0
    origin_code = 4 if center_origin else 0

    yy = {
        "$GMSprite": "",
        "%Name": name,
        "bboxMode": 0,
        "bbox_bottom": h - 1,
        "bbox_left": 0,
        "bbox_right": w - 1,
        "bbox_top": 0,
        "collisionKind": 1,
        "collisionTolerance": 0,
        "DynamicTexturePage": False,
        "edgeFiltering": False,
        "For3D": False,
        "frames": [
            {
                "$GMSpriteFrame": "",
                "%Name": frame_id,
                "name": frame_id,
                "resourceType": "GMSpriteFrame",
                "resourceVersion": "2.0",
            }
        ],
        "gridX": 0,
        "gridY": 0,
        "height": h,
        "HTile": False,
        "layers": [
            {
                "$GMImageLayer": "",
                "%Name": layer_id,
                "blendMode": 0,
                "displayName": "default",
                "isLocked": False,
                "name": layer_id,
                "opacity": 100.0,
                "resourceType": "GMImageLayer",
                "resourceVersion": "2.0",
                "visible": True,
            }
        ],
        "name": name,
        "nineSlice": None,
        "origin": origin_code,
        "parent": {"name": "Sprites", "path": "folders/Sprites.yy"},
        "preMultiplyAlpha": False,
        "resourceType": "GMSprite",
        "resourceVersion": "2.0",
        "sequence": {
            "$GMSequence": "",
            "%Name": name,
            "autoRecord": True,
            "backdropHeight": 768,
            "backdropImageOpacity": 0.5,
            "backdropImagePath": "",
            "backdropWidth": 1366,
            "backdropXOffset": 0.0,
            "backdropYOffset": 0.0,
            "events": {
                "$KeyframeStore<MessageEventKeyframe>": "",
                "Keyframes": [],
                "resourceType": "KeyframeStore<MessageEventKeyframe>",
                "resourceVersion": "2.0",
            },
            "eventStubScript": None,
            "eventToFunction": {},
            "length": 1.0,
            "lockOrigin": False,
            "moments": {
                "$KeyframeStore<MomentsEventKeyframe>": "",
                "Keyframes": [],
                "resourceType": "KeyframeStore<MomentsEventKeyframe>",
                "resourceVersion": "2.0",
            },
            "name": name,
            "playback": 1,
            "playbackSpeed": 12.0,
            "playbackSpeedType": 0,
            "resourceType": "GMSequence",
            "resourceVersion": "2.0",
            "showBackdrop": True,
            "showBackdropImage": False,
            "timeUnits": 1,
            "tracks": [
                {
                    "$GMSpriteFramesTrack": "",
                    "builtinName": 0,
                    "events": [],
                    "inheritsTrackColour": True,
                    "interpolation": 1,
                    "isCreationTrack": False,
                    "keyframes": {
                        "$KeyframeStore<SpriteFrameKeyframe>": "",
                        "Keyframes": [
                            {
                                "$Keyframe<SpriteFrameKeyframe>": "",
                                "Channels": {
                                    "0": {
                                        "$SpriteFrameKeyframe": "",
                                        "Id": {"name": frame_id, "path": f"sprites/{name}/{name}.yy"},
                                        "resourceType": "SpriteFrameKeyframe",
                                        "resourceVersion": "2.0",
                                    }
                                },
                                "Disabled": False,
                                "id": str(uuid.uuid4()),
                                "IsCreationKey": False,
                                "Key": 0.0,
                                "Length": 1.0,
                                "resourceType": "Keyframe<SpriteFrameKeyframe>",
                                "resourceVersion": "2.0",
                                "Stretch": False,
                            }
                        ],
                        "resourceType": "KeyframeStore<SpriteFrameKeyframe>",
                        "resourceVersion": "2.0",
                    },
                    "modifiers": [],
                    "name": "frames",
                    "resourceType": "GMSpriteFramesTrack",
                    "resourceVersion": "2.0",
                    "spriteId": None,
                    "trackColour": 0,
                    "tracks": [],
                    "traits": 0,
                }
            ],
            "visibleRange": None,
            "volume": 1.0,
            "xorigin": ox,
            "yorigin": oy,
        },
        "swatchColours": None,
        "swfPrecision": 0.5,
        "textureGroupId": {"name": "Default", "path": "texturegroups/Default"},
        "type": 0,
        "VTile": False,
        "width": w,
    }
    save_yy(os.path.join(sdir, f"{name}.yy"), yy)
    return {"id": {"name": name, "path": f"sprites/{name}/{name}.yy"}}


def make_script(name, gml_code):
    sdir = os.path.join(GM_DIR, "scripts", name)
    save_text(os.path.join(sdir, f"{name}.gml"), gml_code)
    yy = {
        "$GMScript": "v1",
        "%Name": name,
        "isCompatibility": False,
        "isDnD": False,
        "name": name,
        "parent": {"name": "Scripts", "path": "folders/Scripts.yy"},
        "resourceType": "GMScript",
        "resourceVersion": "2.0",
    }
    save_yy(os.path.join(sdir, f"{name}.yy"), yy)
    return {"id": {"name": name, "path": f"scripts/{name}/{name}.yy"}}


def make_object(name, sprite_name, events):
    """
    events: list of tuples (event_type, event_num, filename, gml_code)
      Create: (0, 0, "Create_0.gml")
      Step:   (3, 0, "Step_0.gml")
      Draw:   (8, 0, "Draw_0.gml")
      DrawGUI:(8, 64, "Draw_64.gml")
    """
    odir = os.path.join(GM_DIR, "objects", name)
    ev_list = []
    for etype, enum, fname, code in events:
        save_text(os.path.join(odir, fname), code)
        ev_list.append(
            {
                "$GMEvent": "v1",
                "%Name": "",
                "collisionObjectId": None,
                "eventNum": enum,
                "eventType": etype,
                "isDnD": False,
                "name": "",
                "resourceType": "GMEvent",
                "resourceVersion": "2.0",
            }
        )
    yy = {
        "$GMObject": "",
        "%Name": name,
        "eventList": ev_list,
        "managed": True,
        "name": name,
        "overriddenProperties": [],
        "parent": {"name": "Objects", "path": "folders/Objects.yy"},
        "parentObjectId": None,
        "persistent": False,
        "physicsAngularDamping": 0.1,
        "physicsDensity": 0.5,
        "physicsFriction": 0.2,
        "physicsGroup": 1,
        "physicsKinematic": False,
        "physicsLinearDamping": 0.1,
        "physicsObject": False,
        "physicsRestitution": 0.1,
        "physicsSensor": False,
        "physicsShape": 1,
        "physicsShapePoints": [],
        "physicsStartAwake": True,
        "properties": [],
        "resourceType": "GMObject",
        "resourceVersion": "2.0",
        "solid": False,
        "spriteId": {"name": sprite_name, "path": f"sprites/{sprite_name}/{sprite_name}.yy"} if sprite_name else None,
        "spriteMaskId": None,
        "visible": True,
    }
    save_yy(os.path.join(odir, f"{name}.yy"), yy)
    return {"id": {"name": name, "path": f"objects/{name}/{name}.yy"}}


# ==============================================================================
# GML SCRIPTS
# ==============================================================================
GML_HOUSE_MAP = r"""
/// @desc 4-room interconnected House layout ("Один дома") for Bebechad!
/// Rooms:
///   (0,0) Гостиная   [0..960, 0..640]
///   (1,0) Кухня      [960..1920, 0..640]
///   (0,1) Подвал     [0..960, 640..1280]
///   (1,1) Задний двор [960..1920, 640..1280]

function scr_house_init() {
    global.world_w = 1920;
    global.world_h = 1280;
    global.mid_x = 960;
    global.mid_y = 640;

    // Solid walls with wide 160px open doorways between all 4 rooms!
    global.house_walls = [
        // Outer perimeter walls (thickness 48px)
        { x1: 0,    y1: 0,    x2: 1920, y2: 48,   brick: true  },
        { x1: 0,    y1: 1232, x2: 1920, y2: 1280, brick: true  },
        { x1: 0,    y1: 0,    x2: 48,   y2: 1280, brick: true  },
        { x1: 1872, y1: 0,    x2: 1920, y2: 1280, brick: true  },

        // Vertical divider between Left (Гостиная/Подвал) and Right (Кухня/Двор)
        { x1: 936, y1: 48,  x2: 984, y2: 240,  brick: false },
        { x1: 936, y1: 400, x2: 984, y2: 880,  brick: true  },
        { x1: 936, y1: 1040,x2: 984, y2: 1232, brick: true  },

        // Horizontal divider between Top (Гостиная/Кухня) and Bottom (Подвал/Двор)
        { x1: 48,   y1: 616, x2: 400,  y2: 664, brick: true  },
        { x1: 560,  y1: 616, x2: 1360, y2: 664, brick: true  },
        { x1: 1520, y1: 616, x2: 1872, y2: 664, brick: true  }
    ];

    // Detailed Furniture & Environment Cover Props across all 4 rooms!
    global.house_props = [
        // Гостиная
        { x1: 150,  y1: 96,   x2: 396,  y2: 184, kind: "sofa",      label: "Диван" },
        { x1: 650,  y1: 96,   x2: 830,  y2: 162, kind: "tv",        label: "ТВ-тумба" },
        { x1: 118,  y1: 430,  x2: 196,  y2: 508, kind: "cat_tree",  label: "Когтеточка" },
        { x1: 780,  y1: 460,  x2: 882,  y2: 534, kind: "bookshelf", label: "Полка" },
        { x1: 72,   y1: 72,   x2: 118,  y2: 118, kind: "plant",     label: "Монстера" },
        { x1: 866,  y1: 72,   x2: 912,  y2: 118, kind: "plant",     label: "Фикус" },
        // Кухня
        { x1: 1050, y1: 62,   x2: 1320, y2: 128, kind: "stove",     label: "Плита и мойка" },
        { x1: 1715, y1: 68,   x2: 1835, y2: 186, kind: "fridge",    label: "Холодильник" },
        { x1: 1290, y1: 254,  x2: 1546, y2: 344, kind: "island",    label: "Остров с сыром" },
        { x1: 1660, y1: 430,  x2: 1806, y2: 526, kind: "dining",    label: "Стол" },
        // Подвал
        { x1: 130,  y1: 790,  x2: 244,  y2: 892, kind: "crates",    label: "Ящики" },
        { x1: 640,  y1: 970,  x2: 758,  y2: 1068,kind: "barrels",   label: "Бочки" },
        { x1: 145,  y1: 1080, x2: 240,  y2: 1166,kind: "crates",    label: "Хлам" },
        // Задний двор
        { x1: 1140, y1: 790,  x2: 1266, y2: 896, kind: "shed",      label: "Сарайчик" },
        { x1: 1580, y1: 990,  x2: 1766, y2: 1076,kind: "planter",   label: "Грядка Мяты" }
    ];

    // Catnip Shop Bowl in Living Room (interact with [E] or press [B] anywhere)
    global.catnip_bowl = { x: 480, y: 196, r: 52 };
}

function scr_house_get_room_name(_x, _y) {
    if (_x < global.mid_x && _y < global.mid_y) return "Гостиная";
    if (_x >= global.mid_x && _y < global.mid_y) return "Кухня";
    if (_x < global.mid_x && _y >= global.mid_y) return "Подвал";
    return "Задний двор";
}

function scr_house_resolve_circle(_inst, _rad) {
    var _lists = [global.house_walls, global.house_props];
    for (var l = 0; l < 2; l++) {
        var _arr = _lists[l];
        for (var i = 0; i < array_length(_arr); i++) {
            var _r = _arr[i];
            var _cx = clamp(_inst.x, _r.x1, _r.x2);
            var _cy = clamp(_inst.y, _r.y1, _r.y2);
            var _dx = _inst.x - _cx;
            var _dy = _inst.y - _cy;
            var _d = point_distance(0, 0, _dx, _dy);
            if (_d < _rad) {
                if (_d > 0.001) {
                    _inst.x = _cx + (_dx / _d) * _rad;
                    _inst.y = _cy + (_dy / _d) * _rad;
                } else {
                    _inst.y -= _rad;
                }
            }
        }
    }
    _inst.x = clamp(_inst.x, 56, global.world_w - 56);
    _inst.y = clamp(_inst.y, 56, global.world_h - 56);
}

function scr_house_draw() {
    // 1) Гостиная (Wood parquet + green patterned carpet rug)
    draw_set_color(make_color_rgb(132, 92, 58));
    draw_rectangle(0, 0, 960, 640, false);
    draw_set_color(make_color_rgb(116, 78, 48));
    for (var py = 48; py < 616; py += 24) {
        draw_line(48, py, 936, py);
    }
    // Cozy Living Room Rug using user's green patterned tile!
    for (var rx = 256; rx < 704; rx += 64) {
        for (var ry = 224; ry < 480; ry += 64) {
            draw_sprite(spr_tile_grass_dark, 0, rx, ry);
        }
    }
    draw_set_color(make_color_rgb(228, 186, 98));
    draw_rectangle(256, 224, 704, 480, true);

    // 2) Кухня (Cream & Terracotta Checkered Tiles)
    for (var kx = 960; kx < 1920; kx += 48) {
        for (var ky = 0; ky < 640; ky += 48) {
            var _alt = (((kx div 48) + (ky div 48)) mod 2) == 0;
            draw_set_color(_alt ? make_color_rgb(224, 214, 192) : make_color_rgb(186, 152, 124));
            draw_rectangle(kx, ky, kx + 48, ky + 48, false);
        }
    }

    // 3) Подвал (Dark stone concrete floor)
    draw_set_color(make_color_rgb(56, 58, 68));
    draw_rectangle(0, 640, 960, 1280, false);
    draw_set_color(make_color_rgb(44, 46, 54));
    for (var bx = 48; bx < 936; bx += 64) draw_line(bx, 664, bx, 1232);
    for (var by = 664; by < 1232; by += 64) draw_line(48, by, 936, by);

    // 4) Задний двор (User's exact grass tile + swaying tall grass overlay!)
    var _sway = sin(current_time * 0.004) * 2;
    for (var gx = 960; gx < 1920; gx += 64) {
        for (var gy = 640; gy < 1280; gy += 64) {
            draw_sprite(spr_tile_grass_dark, 0, gx, gy);
            if (((gx div 64) + (gy div 64)) mod 2 == 0) {
                draw_sprite(spr_tile_grass_overlay, 0, gx + _sway, gy);
            }
        }
    }

    // 5) Draw Walls (tiled with user's exact mossy red brick wall sprite!)
    for (var i = 0; i < array_length(global.house_walls); i++) {
        var _w = global.house_walls[i];
        if (_w.brick) {
            for (var tx = _w.x1; tx < _w.x2; tx += 64) {
                for (var ty = _w.y1; ty < _w.y2; ty += 64) {
                    var _cw = min(64, _w.x2 - tx);
                    var _ch = min(64, _w.y2 - ty);
                    draw_sprite_part(spr_tile_brick_moss, 0, 0, 0, _cw, _ch, tx, ty);
                }
            }
        } else {
            draw_set_color(make_color_rgb(92, 66, 52));
            draw_rectangle(_w.x1, _w.y1, _w.x2, _w.y2, false);
        }
        draw_set_color(make_color_rgb(28, 22, 32));
        draw_rectangle(_w.x1, _w.y1, _w.x2, _w.y2, true);
    }

    // 5b) Doorway wooden thresholds
    draw_set_color(make_color_rgb(168, 124, 78));
    draw_rectangle(936, 240, 984, 400, false);
    draw_rectangle(936, 880, 984, 1040, false);
    draw_rectangle(400, 616, 560, 664, false);
    draw_rectangle(1360, 616, 1520, 664, false);

    // 5c) Basement Glowing Rat Burrows along the brick walls
    var _burrows = [[300, 668], [760, 668], [52, 960]];
    for (var b0 = 0; b0 < array_length(_burrows); b0++) {
        var _bx = _burrows[b0][0], _by = _burrows[b0][1];
        draw_set_color(make_color_rgb(18, 14, 24));
        draw_circle(_bx, _by, 18, false);
        draw_set_color(make_color_rgb(250, 224, 75));
        draw_rectangle(_bx - 6, _by - 2, _bx - 3, _by + 1, false);
        draw_rectangle(_bx + 3, _by - 2, _bx + 6, _by + 1, false);
    }

    // 6) Detailed Pixel-Art Furniture Props by Kind
    for (var i = 0; i < array_length(global.house_props); i++) {
        var _p = global.house_props[i];
        var _x1 = _p.x1, _y1 = _p.y1, _x2 = _p.x2, _y2 = _p.y2;
        var _w = _x2 - _x1, _h = _y2 - _y1;
        draw_set_color(make_color_rgb(20, 16, 26));
        draw_rectangle(_x1 + 5, _y1 + 6, _x2 + 5, _y2 + 6, false);

        if (_p.kind == "sofa") {
            draw_set_color(make_color_rgb(154, 64, 78)); draw_rectangle(_x1, _y1, _x2, _y2, false);
            draw_set_color(make_color_rgb(186, 82, 96)); draw_rectangle(_x1 + 18, _y1 + 22, _x2 - 18, _y2 - 8, false);
            draw_set_color(make_color_rgb(245, 206, 86)); draw_rectangle(_x1 + 26, _y1 + 26, _x1 + 64, _y1 + 58, false);
        } else if (_p.kind == "tv") {
            draw_set_color(make_color_rgb(76, 56, 44)); draw_rectangle(_x1, _y1, _x2, _y2, false);
            draw_set_color(make_color_rgb(30, 34, 46)); draw_rectangle(_x1 + 24, _y1 + 12, _x2 - 24, _y2 - 18, false);
            draw_set_color(make_color_rgb(92, 178, 232)); draw_rectangle(_x1 + 30, _y1 + 18, _x2 - 30, _y2 - 24, false);
        } else if (_p.kind == "cat_tree") {
            draw_set_color(make_color_rgb(188, 146, 98)); draw_rectangle(_x1, _y1, _x2, _y2, false);
            draw_set_color(make_color_rgb(224, 188, 134)); draw_circle(_x1 + _w * 0.5, _y1 + _h * 0.5, 22, false);
        } else if (_p.kind == "plant") {
            draw_set_color(make_color_rgb(168, 92, 62)); draw_circle(_x1 + _w * 0.5, _y1 + _h * 0.5, 18, false);
            draw_set_color(make_color_rgb(64, 168, 86)); draw_circle(_x1 + _w * 0.5, _y1 + _h * 0.5, 14, false);
        } else if (_p.kind == "island") {
            draw_set_color(make_color_rgb(206, 172, 126)); draw_rectangle(_x1, _y1, _x2, _y2, false);
            draw_set_color(make_color_rgb(250, 212, 68)); draw_circle(_x1 + _w * 0.65, _y1 + _h * 0.5, 18, false);
        } else if (_p.kind == "fridge") {
            draw_set_color(make_color_rgb(208, 224, 234)); draw_rectangle(_x1, _y1, _x2, _y2, false);
            draw_set_color(make_color_rgb(245, 198, 82)); draw_rectangle(_x1 + 16, _y1 + 22, _x1 + 36, _y1 + 42, false);
        } else if (_p.kind == "stove") {
            draw_set_color(make_color_rgb(176, 184, 194)); draw_rectangle(_x1, _y1, _x2, _y2, false);
            draw_set_color(make_color_rgb(36, 36, 44));
            draw_circle(_x1 + 44, _y1 + 22, 10, false); draw_circle(_x1 + 88, _y1 + 22, 10, false);
            draw_circle(_x1 + 44, _y1 + 48, 10, false); draw_circle(_x1 + 88, _y1 + 48, 10, false);
        } else if (_p.kind == "planter") {
            draw_set_color(make_color_rgb(122, 82, 48)); draw_rectangle(_x1, _y1, _x2, _y2, false);
            draw_set_color(make_color_rgb(76, 198, 108)); draw_rectangle(_x1 + 8, _y1 + 8, _x2 - 8, _y2 - 8, false);
        } else {
            draw_set_color(make_color_rgb(126, 90, 56)); draw_rectangle(_x1, _y1, _x2, _y2, false);
        }
        draw_set_color(make_color_rgb(24, 18, 30));
        draw_rectangle(_x1, _y1, _x2, _y2, true);
    }

    // 7) Catnip Bowl Shop Landmark in Living Room
    var _cb = global.catnip_bowl;
    draw_set_color(make_color_rgb(70, 214, 122));
    draw_circle(_cb.x, _cb.y, 18, true);
    draw_sprite(spr_catnip, 0, _cb.x, _cb.y);
    draw_set_color(c_white);
}
"""

GML_CATNIP_SHOP = r"""
/// @desc Catnip ("Кошачья мята") upgrade system for Bebechad!

function scr_catnip_shop_init() {
    global.catnip = 10;
    global.shop_open = false;
    global.upgrades = [
        { id: "claws",   name: "Острые Когти",      desc: "+25% урон и радиус царапок",     base_cost: 10, lvl: 0, max_lvl: 8 },
        { id: "yarn",    name: "Клубок-Рикошет",    desc: "+1 отскакивающий клубок",        base_cost: 14, lvl: 0, max_lvl: 5 },
        { id: "bones",   name: "Рыбьи Кости",       desc: "+2 пробивающие кости веером",    base_cost: 18, lvl: 0, max_lvl: 5 },
        { id: "bomb",    name: "Мятная Бомба",      desc: "AoE взрыв мяты и замедление",    base_cost: 22, lvl: 0, max_lvl: 5 },
        { id: "paws",    name: "Турбо-Лапки",       desc: "+16% скорость бега и -КД рывка", base_cost: 12, lvl: 0, max_lvl: 6 },
        { id: "kibble",  name: "Хруст Корма",       desc: "+30 Max HP и лечение 50% HP",    base_cost: 14, lvl: 0, max_lvl: 6 },
        { id: "magnet",  name: "Магнит Мяты",       desc: "+45px магнит и +20% мяты",       base_cost: 15, lvl: 0, max_lvl: 6 },
        { id: "chadcrit",name: "Крит Гигачада",     desc: "+15% крит-шанс и +35% крит-урон",base_cost: 18, lvl: 0, max_lvl: 6 }
    ];
}

function scr_upgrade_level(_id) {
    for (var i = 0; i < array_length(global.upgrades); i++) {
        if (global.upgrades[i].id == _id) return global.upgrades[i].lvl;
    }
    return 0;
}

function scr_upgrade_cost(_u) {
    return round(_u.base_cost * power(1.38, _u.lvl));
}

function scr_upgrade_buy(_idx) {
    if (_idx < 0 || _idx >= array_length(global.upgrades)) return false;
    var _u = global.upgrades[_idx];
    if (_u.lvl >= _u.max_lvl) return false;
    var _cost = scr_upgrade_cost(_u);
    if (global.catnip < _cost) return false;
    global.catnip -= _cost;
    _u.lvl += 1;
    if (_u.id == "kibble" && instance_exists(obj_bebechad)) {
        obj_bebechad.max_hp += 30;
        obj_bebechad.hp = min(obj_bebechad.max_hp, obj_bebechad.hp + round(obj_bebechad.max_hp * 0.5));
    }
    return true;
}
"""

GML_BOSS_MINIGAME = r"""
/// @desc Dialogue Box (bebechad / catttt / rat1 portraits) & Rat Boss Timing Bar + QTE Combo Mini-Game!

function scr_dialogue_init() {
    global.dlg_queue = [];
    global.dlg_active = noone;
    global.dlg_char_idx = 0;

    global.mg_active = false;
    global.mg_boss = noone;
    global.mg_stage = 0;       // 0 = Timing Bar, 1 = QTE Combo Keys
    global.mg_cursor = 0.0;    // 0..1
    global.mg_dir = 1;
    global.mg_zone_min = 0.36;
    global.mg_zone_max = 0.64;
    global.mg_keys = [];
    global.mg_key_idx = 0;
    global.mg_timer = 0;
    global.mg_max_timer = 270; // 4.5s at 60fps
    global.mg_perfect_bar = false;
}

function scr_dialogue_push(_speaker, _portrait_spr, _text) {
    array_push(global.dlg_queue, {
        speaker: _speaker,
        portrait: _portrait_spr,
        text: _text
    });
}

function scr_dialogue_update() {
    if (global.dlg_active == noone) {
        if (array_length(global.dlg_queue) > 0) {
            global.dlg_active = global.dlg_queue[0];
            array_delete(global.dlg_queue, 0, 1);
            global.dlg_char_idx = 0;
        }
        return false;
    }
    var _len = string_length(global.dlg_active.text);
    if (global.dlg_char_idx < _len) {
        global.dlg_char_idx = min(_len, global.dlg_char_idx + 1.2);
    }
    if (keyboard_check_pressed(vk_space) || keyboard_check_pressed(vk_enter) || mouse_check_button_pressed(mb_left)) {
        if (global.dlg_char_idx < _len) {
            global.dlg_char_idx = _len;
        } else {
            global.dlg_active = noone;
        }
    }
    return true;
}

function scr_minigame_start(_boss_inst, _combo_len) {
    global.mg_active = true;
    global.mg_boss = _boss_inst;
    global.mg_stage = 0;
    global.mg_cursor = 0.05;
    global.mg_dir = 1;
    global.mg_timer = 270;
    global.mg_max_timer = 270;
    global.mg_perfect_bar = false;
    global.mg_key_idx = 0;
    global.mg_keys = [];
    var _pool = [
        { vk: ord("W"), lbl: "W" },
        { vk: ord("A"), lbl: "A" },
        { vk: ord("S"), lbl: "S" },
        { vk: ord("D"), lbl: "D" }
    ];
    for (var i = 0; i < _combo_len; i++) {
        array_push(global.mg_keys, _pool[irandom(3)]);
    }
}

function scr_minigame_finish(_success, _perfect) {
    var _b = global.mg_boss;
    global.mg_active = false;
    global.mg_boss = noone;
    if (!instance_exists(_b)) return;
    _b.shield_active = false;
    if (_success) {
        var _dmg = round(_b.max_hp * (_perfect ? 0.34 : 0.25));
        _b.hp -= _dmg;
        _b.stun_timer = 150;
        _b.flash_timer = 18;
        global.catnip += (_perfect ? 20 : 12);
        scr_dialogue_push("Bebechad", spr_portrait_bebechad, _perfect
            ? "ИДЕАЛЬНЫЙ ГИГАЧАД-УДАР! Твой сырный щит рассыпался!"
            : "Щит пробит! Получай лапой, крысиный выскочка!");
    } else {
        if (instance_exists(obj_bebechad)) {
            obj_bebechad.hp = max(1, obj_bebechad.hp - 12);
        }
        scr_dialogue_push("Bebechad", spr_portrait_cat_angry, "МЯУ?! Промахнулся! Щас я тебе покажу!");
    }
}

function scr_minigame_update() {
    if (!global.mg_active) return false;
    global.mg_timer -= 1;
    if (global.mg_timer <= 0) {
        scr_minigame_finish(false, false);
        return true;
    }
    if (global.mg_stage == 0) {
        global.mg_cursor += global.mg_dir * 0.024;
        if (global.mg_cursor >= 1.0) { global.mg_cursor = 1.0; global.mg_dir = -1; }
        if (global.mg_cursor <= 0.0) { global.mg_cursor = 0.0; global.mg_dir = 1; }
        if (keyboard_check_pressed(vk_space) || mouse_check_button_pressed(mb_left)) {
            if (global.mg_cursor >= global.mg_zone_min && global.mg_cursor <= global.mg_zone_max) {
                global.mg_perfect_bar = abs(global.mg_cursor - 0.5) < 0.055;
                global.mg_stage = 1;
                global.mg_timer = min(global.mg_max_timer, global.mg_timer + 90);
            } else {
                scr_minigame_finish(false, false);
            }
        }
    } else {
        var _need = global.mg_keys[global.mg_key_idx];
        if (keyboard_check_pressed(_need.vk)) {
            global.mg_key_idx += 1;
            if (global.mg_key_idx >= array_length(global.mg_keys)) {
                scr_minigame_finish(true, global.mg_perfect_bar);
            }
        }
    }
    return true;
}

/// @desc Cozy Pixel-Wood & Parchment Panel (Theme #3 — Stardew Valley style!)
function scr_ui_draw_wood_panel(_x1, _y1, _x2, _y2) {
    // Drop shadow
    draw_set_color(make_color_rgb(38, 22, 12));
    draw_rectangle(_x1 + 3, _y1 + 4, _x2 + 3, _y2 + 4, false);
    // Outer carved dark wood border
    draw_set_color(make_color_rgb(117, 64, 27));
    draw_rectangle(_x1, _y1, _x2, _y2, false);
    // Warm golden wood inner trim
    draw_set_color(make_color_rgb(217, 162, 89));
    draw_rectangle(_x1 + 4, _y1 + 4, _x2 - 4, _y2 - 4, false);
    // Cream parchment fill
    draw_set_color(make_color_rgb(246, 228, 194));
    draw_rectangle(_x1 + 7, _y1 + 7, _x2 - 7, _y2 - 7, false);
    // Corner golden studs
    draw_set_color(make_color_rgb(255, 240, 196));
    draw_rectangle(_x1 + 2, _y1 + 2, _x1 + 5, _y1 + 5, false);
    draw_rectangle(_x2 - 5, _y1 + 2, _x2 - 2, _y1 + 5, false);
    draw_rectangle(_x1 + 2, _y2 - 5, _x1 + 5, _y2 - 2, false);
    draw_rectangle(_x2 - 5, _y2 - 5, _x2 - 2, _y2 - 2, false);
}

function scr_dialogue_draw_gui(_gw, _gh) {
    if (global.dlg_active == noone) return;
    var _bx1 = 140, _by1 = _gh - 156, _bx2 = _gw - 140, _by2 = _gh - 20;
    scr_ui_draw_wood_panel(_bx1, _by1, _bx2, _by2);
    // Warm framed portrait box
    draw_set_color(make_color_rgb(117, 64, 27));
    draw_rectangle(_bx1 + 12, _by1 + 12, _bx1 + 126, _by1 + 126, false);
    draw_set_color(make_color_rgb(235, 208, 158));
    draw_rectangle(_bx1 + 15, _by1 + 15, _bx1 + 123, _by1 + 123, false);
    draw_sprite_ext(global.dlg_active.portrait, 0, _bx1 + 17, _by1 + 17, 1.65, 1.65, 0, c_white, 1);

    draw_set_color(make_color_rgb(140, 45, 25));
    draw_text(_bx1 + 142, _by1 + 16, global.dlg_active.speaker);
    draw_set_color(make_color_rgb(212, 160, 91));
    draw_line_width(_bx1 + 142, _by1 + 38, _bx2 - 22, _by1 + 38, 2);

    draw_set_color(make_color_rgb(61, 35, 17));
    var _shown = string_copy(global.dlg_active.text, 1, floor(global.dlg_char_idx));
    draw_text_ext(_bx1 + 142, _by1 + 46, _shown, 22, (_bx2 - _bx1) - 166);
    draw_set_color(make_color_rgb(122, 82, 48));
    draw_text(_bx2 - 196, _by2 - 26, "[Пробел / ЛКМ] далее");
}

function scr_minigame_draw_gui(_gw, _gh) {
    if (!global.mg_active) return;
    var _cx = _gw * 0.5, _cy = _gh - 148;
    scr_ui_draw_wood_panel(_cx - 270, _cy - 82, _cx + 270, _cy + 82);

    // Framed portraits
    draw_set_color(make_color_rgb(117, 64, 27));
    draw_rectangle(_cx - 254, _cy - 58, _cx - 154, _cy + 42, false);
    draw_rectangle(_cx + 154, _cy - 58, _cx + 254, _cy + 42, false);
    draw_set_color(make_color_rgb(235, 208, 158));
    draw_rectangle(_cx - 251, _cy - 55, _cx - 157, _cy + 39, false);
    draw_rectangle(_cx + 157, _cy - 55, _cx + 251, _cy + 39, false);
    draw_sprite_ext(spr_portrait_bebechad, 0, _cx - 249, _cy - 53, 1.4, 1.4, 0, c_white, 1);
    draw_sprite_ext(spr_portrait_rat, 0, _cx + 159, _cy - 53, 1.4, 1.4, 0, c_white, 1);

    draw_set_color(make_color_rgb(140, 45, 25));
    draw_text(_cx - 122, _cy - 66, "БОСС-МИНИ-ИГРА: ПРОБИТИЕ ЩИТА!");

    if (global.mg_stage == 0) {
        var _barx = _cx - 134, _bary = _cy - 8, _barw = 268, _barh = 26;
        draw_set_color(make_color_rgb(92, 51, 24));
        draw_rectangle(_barx, _bary, _barx + _barw, _bary + _barh, false);
        draw_set_color(make_color_rgb(76, 186, 86));
        draw_rectangle(_barx + _barw * global.mg_zone_min, _bary, _barx + _barw * global.mg_zone_max, _bary + _barh, false);
        draw_set_color(make_color_rgb(250, 224, 75));
        draw_rectangle(_barx + _barw * 0.45, _bary, _barx + _barw * 0.55, _bary + _barh, false);
        var _kx = _barx + _barw * global.mg_cursor;
        draw_set_color(c_white);
        draw_rectangle(_kx - 3, _bary - 4, _kx + 3, _bary + _barh + 4, false);
        draw_set_color(make_color_rgb(61, 35, 17));
        draw_text(_cx - 112, _cy + 28, "Жми [ПРОБЕЛ] в зелёной зоне!");
    } else {
        draw_set_color(make_color_rgb(61, 35, 17));
        draw_text(_cx - 95, _cy - 28, "ПРОЖМИ QTE-КОМБО:");
        for (var i = 0; i < array_length(global.mg_keys); i++) {
            var _kx = _cx - 80 + i * 48;
            var _done = i < global.mg_key_idx;
            var _cur = i == global.mg_key_idx;
            draw_set_color(_done ? make_color_rgb(108, 201, 104) : (_cur ? make_color_rgb(255, 224, 82) : make_color_rgb(232, 199, 142)));
            draw_rectangle(_kx - 16, _cy - 4, _kx + 16, _cy + 28, false);
            draw_set_color(make_color_rgb(117, 64, 27));
            draw_rectangle(_kx - 16, _cy - 4, _kx + 16, _cy + 28, true);
            draw_set_color(make_color_rgb(45, 24, 10));
            draw_text(_kx - 5, _cy + 4, global.mg_keys[i].lbl);
        }
    }
    // Fuse bar
    var _f = global.mg_timer / global.mg_max_timer;
    draw_set_color(make_color_rgb(107, 61, 30));
    draw_rectangle(_cx - 134, _cy + 58, _cx + 134, _cy + 66, false);
    draw_set_color(make_color_rgb(214, 72, 62));
    draw_rectangle(_cx - 134, _cy + 58, _cx - 134 + 268 * _f, _cy + 66, false);
}
"""

# ==============================================================================
# GML OBJECTS
# ==============================================================================
OBJ_GAME_CREATE = r"""
randomize();
display_set_gui_size(1280, 720);

// Load bundled open-source Cyrillic TTF font (SIL OFL LiberationSans-Bold)
global.ui_font = -1;
if (file_exists("ui_font.ttf")) {
    global.ui_font = font_add("ui_font.ttf", 14, false, false, 0, 0);
}

scr_house_init();
scr_catnip_shop_init();
scr_dialogue_init();

global.wave = 1;
global.kills = 0;
global.run_time = 0;
global.spawn_timer = 40;
global.boss_timer = 60 * 35; // First Rat Boss at 35s (or press [T] anytime!)
global.boss_count = 0;
global.boss_name = "Барон Сырник";
global.visited_kitchen = false;
global.visited_basement = false;
global.visited_yard = false;

instance_create_layer(480, 320, "Instances", obj_bebechad);

// Opening Monologue: Bebechad (gigachad) -> Catttt (outraged!)
scr_dialogue_push("Bebechad", spr_portrait_bebechad, "Хозяева уехали. Весь дом в моём распоряжении. Время чиллить.");
scr_dialogue_push("Bebechad", spr_portrait_cat_angry, "СТОП... ЧТО ЭТО ШУРШИТ НА КУХНЕ И В ПОДВАЛЕ?! МЫШИ?!");
scr_dialogue_push("Bebechad", spr_portrait_bebechad, "Ладно. Разминаем когти. За кошачью мяту я разнесу всю их банду.");
"""

OBJ_GAME_CLEANUP = r"""
if (variable_global_exists("ui_font") && global.ui_font != -1 && font_exists(global.ui_font)) {
    font_delete(global.ui_font);
    global.ui_font = -1;
}
"""

OBJ_GAME_STEP = r"""
if (keyboard_check_pressed(ord("B")) || keyboard_check_pressed(vk_tab)) {
    if (!global.mg_active && global.dlg_active == noone) {
        global.shop_open = !global.shop_open;
    }
}
if (global.shop_open) {
    for (var k = 0; k < 8; k++) {
        if (keyboard_check_pressed(ord(string(k + 1)))) {
            scr_upgrade_buy(k);
        }
    }
    exit;
}

if (scr_dialogue_update()) exit;
if (scr_minigame_update()) exit;

global.run_time += 1;
global.wave = 1 + (global.run_time div (60 * 20));

// Hotkey [T] to test Rat Boss immediately!
if (keyboard_check_pressed(ord("T")) && !instance_exists(obj_rat_boss)) {
    global.boss_timer = 1;
}

// Spawn mouse horde around player
global.spawn_timer -= 1;
if (global.spawn_timer <= 0 && instance_number(obj_mouse) < min(45, 8 + global.wave * 5)) {
    global.spawn_timer = max(18, 70 - global.wave * 6);
    if (instance_exists(obj_bebechad)) {
        var _ang = irandom(359);
        var _dist = irandom_range(260, 420);
        var _sx = clamp(obj_bebechad.x + lengthdir_x(_dist, _ang), 72, global.world_w - 72);
        var _sy = clamp(obj_bebechad.y + lengthdir_y(_dist, _ang), 72, global.world_h - 72);
        instance_create_layer(_sx, _sy, "Instances", obj_mouse);
    }
}

// Room discovery monologues
if (instance_exists(obj_bebechad)) {
    var _rname = scr_house_get_room_name(obj_bebechad.x, obj_bebechad.y);
    if (_rname == "Кухня" && !global.visited_kitchen) {
        global.visited_kitchen = true;
        scr_dialogue_push("Bebechad", spr_portrait_cat_angry, "Эй! Они пытаются взломать ХОЛОДИЛЬНИК! Там мой тунец!");
    } else if (_rname == "Подвал" && !global.visited_basement) {
        global.visited_basement = true;
        scr_dialogue_push("Bebechad", spr_portrait_bebechad, "Сырой кирпичный подвал... Явно отсюда лезут эти усатые бандиты.");
    } else if (_rname == "Задний Двор" && !global.visited_yard) {
        global.visited_yard = true;
        scr_dialogue_push("Bebechad", spr_portrait_bebechad, "Свежий воздух, мягкая травка... И отличная арена для охоты!");
    }
}

// Spawn Rat Boss
global.boss_timer -= 1;
if (global.boss_timer <= 0 && !instance_exists(obj_rat_boss) && instance_exists(obj_bebechad)) {
    global.boss_count += 1;
    global.boss_timer = 60 * 45;
    var _bx = clamp(obj_bebechad.x + 260, 120, global.world_w - 120);
    var _by = clamp(obj_bebechad.y, 120, global.world_h - 120);
    instance_create_layer(_bx, _by, "Instances", obj_rat_boss);
    var _bidx = (global.boss_count - 1) mod 3;
    if (_bidx == 0) {
        global.boss_name = "Барон Сырник";
        scr_dialogue_push(global.boss_name, spr_portrait_rat, "Хе-хе! Хозяев нет — теперь этот холодильник и весь дом НАШИ!");
        scr_dialogue_push("Bebechad", spr_portrait_cat_angry, "МОЙ ХОЛОДИЛЬНИК?! Ты только что подписал себе приговор!");
    } else if (_bidx == 1) {
        global.boss_name = "Крысолов из Подвала";
        scr_dialogue_push(global.boss_name, spr_portrait_rat, "Ты разбил отряд Барона?! Тогда познай ярость подвального короля!");
        scr_dialogue_push("Bebechad", spr_portrait_bebechad, "Корона криво сидит. Сейчас поправлю — прямо лапой.");
    } else {
        global.boss_name = "Император Хруст";
        scr_dialogue_push(global.boss_name, spr_portrait_rat, "Склонись перед Императором! Весь корм и вся мята принадлежат крысам!");
        scr_dialogue_push("Bebechad", spr_portrait_cat_angry, "МЯТУ?! НА СВЯТОЕ ПОСЯГНУЛ?! Тебе точно конец!");
    }
}

// Smooth camera follow centered on Bebechad
if (instance_exists(obj_bebechad)) {
    var _cam = view_camera[0];
    var _vw = camera_get_view_width(_cam);
    var _vh = camera_get_view_height(_cam);
    var _tx = clamp(obj_bebechad.x - _vw * 0.5, 0, global.world_w - _vw);
    var _ty = clamp(obj_bebechad.y - _vh * 0.5, 0, global.world_h - _vh);
    var _cx = lerp(camera_get_view_x(_cam), _tx, 0.16);
    var _cy = lerp(camera_get_view_y(_cam), _ty, 0.16);
    camera_set_view_pos(_cam, round(_cx), round(_cy));
}
"""

OBJ_GAME_DRAW = r"""
scr_house_draw();
"""

OBJ_GAME_DRAW_GUI = r"""
if (variable_global_exists("ui_font") && global.ui_font != -1 && font_exists(global.ui_font)) {
    draw_set_font(global.ui_font);
}
draw_set_halign(fa_left);
draw_set_valign(fa_top);

var _gw = display_get_gui_width();
var _gh = display_get_gui_height();

// Top HUD bar (Stardew Wood & Parchment Theme #3!)
scr_ui_draw_wood_panel(14, 10, _gw - 14, 58);

var _room_nm = instance_exists(obj_bebechad) ? scr_house_get_room_name(obj_bebechad.x, obj_bebechad.y) : "Дом";
var _hp_txt = instance_exists(obj_bebechad) ? (string(ceil(obj_bebechad.hp)) + "/" + string(obj_bebechad.max_hp)) : "0/0";
draw_set_color(make_color_rgb(61, 35, 17));
draw_text(30, 24, "BEBECHAD | HP: " + _hp_txt + " | Мята: " + string(global.catnip) + " | Волна: " + string(global.wave) + " | Убито: " + string(global.kills) + " | Комната: " + _room_nm);
draw_set_color(make_color_rgb(31, 115, 55));
draw_text(_gw - 365, 24, "[B] Магазин Мяты  [Shift] Рывок  [F] Ульта  [T] Босс");

// Boss HP Bar
if (instance_exists(obj_rat_boss)) {
    var _b = instance_find(obj_rat_boss, 0);
    var _bf = max(0, _b.hp / _b.max_hp);
    draw_set_color(make_color_rgb(117, 64, 27));
    draw_rectangle(_gw * 0.5 - 224, 66, _gw * 0.5 + 224, 94, false);
    draw_set_color(make_color_rgb(84, 32, 24));
    draw_rectangle(_gw * 0.5 - 220, 70, _gw * 0.5 + 220, 90, false);
    draw_set_color(make_color_rgb(212, 68, 62));
    draw_rectangle(_gw * 0.5 - 220, 70, _gw * 0.5 - 220 + 440 * _bf, 90, false);
    draw_set_color(c_white);
    draw_text(_gw * 0.5 - 140, 72, global.boss_name + " (" + string(max(0, ceil(_b.hp))) + "/" + string(_b.max_hp) + ")");
}

// Catnip Shop Modal (Stardew General Store Ledger!)
if (global.shop_open) {
    scr_ui_draw_wood_panel(150, 92, _gw - 150, _gh - 92);
    draw_set_color(make_color_rgb(140, 45, 25));
    draw_text(184, 112, "МАГАЗИН КОШАЧЬЕЙ МЯТЫ — У тебя: " + string(global.catnip) + " мяты   ([1-8] купить, [B] закрыть)");
    for (var i = 0; i < array_length(global.upgrades); i++) {
        var _u = global.upgrades[i];
        var _uy = 152 + i * 54;
        var _cost = scr_upgrade_cost(_u);
        draw_set_color(global.catnip >= _cost ? make_color_rgb(247, 233, 198) : make_color_rgb(232, 206, 162));
        draw_rectangle(184, _uy, _gw - 184, _uy + 44, false);
        draw_set_color(global.catnip >= _cost ? make_color_rgb(47, 133, 69) : make_color_rgb(150, 92, 44));
        draw_rectangle(184, _uy, _gw - 184, _uy + 44, true);
        draw_set_color(make_color_rgb(61, 35, 17));
        draw_text(198, _uy + 12, "[" + string(i + 1) + "] " + _u.name + " (Ур." + string(_u.lvl) + ") — " + _u.desc);
        draw_set_color(make_color_rgb(31, 115, 55));
        draw_text(_gw - 304, _uy + 12, string(_cost) + " мяты");
    }
}

scr_dialogue_draw_gui(_gw, _gh);
scr_minigame_draw_gui(_gw, _gh);
"""

OBJ_BEBECHAD_CREATE = r"""
hp = 100;
max_hp = 100;
hurt_cd = 0;
dash_timer = 0;
dash_cd = 0;
dash_dir = 0;
ult_charge = 100;
ult_timer = 0;
claw_cd = 0;
yarn_cd = 0;
bone_cd = 0;
bomb_cd = 0;
face_dir = 270; // 270 = down (matches 111111.aseprite native orientation!)
"""

OBJ_BEBECHAD_STEP = r"""
if (global.shop_open || global.dlg_active != noone || global.mg_active) exit;

var _ix = (keyboard_check(ord("D")) || keyboard_check(vk_right)) - (keyboard_check(ord("A")) || keyboard_check(vk_left));
var _iy = (keyboard_check(ord("S")) || keyboard_check(vk_down))  - (keyboard_check(ord("W")) || keyboard_check(vk_up));
var _spd = (3.4 + scr_upgrade_level("paws") * 0.52) * (ult_timer > 0 ? 1.35 : 1.0);

if (hurt_cd > 0) hurt_cd -= 1;
if (dash_cd > 0) dash_cd -= 1;
if (ult_timer > 0) ult_timer -= 1;

// Open Catnip Shop with [E] near Catnip Bowl
if (keyboard_check_pressed(ord("E")) && point_distance(x, y, global.catnip_bowl.x, global.catnip_bowl.y) <= global.catnip_bowl.r) {
    global.shop_open = true;
    exit;
}

// [Shift] Pounce Dash
if (keyboard_check_pressed(vk_shift) && dash_cd <= 0) {
    dash_timer = 14;
    dash_cd = max(45, 120 - scr_upgrade_level("paws") * 14);
    dash_dir = (_ix != 0 || _iy != 0) ? point_direction(0, 0, _ix, _iy) : face_dir;
}

// [F] Gigachad Ultimate!
if (keyboard_check_pressed(ord("F")) && ult_charge >= 100) {
    ult_charge = 0;
    ult_timer = 240;
    with (obj_mouse) {
        if (point_distance(x, y, other.x, other.y) < 220) {
            hp -= 35;
            flash_timer = 10;
        }
    }
}

if (dash_timer > 0) {
    dash_timer -= 1;
    x += lengthdir_x(10.5, dash_dir);
    y += lengthdir_y(10.5, dash_dir);
} else if (_ix != 0 || _iy != 0) {
    var _md = point_direction(0, 0, _ix, _iy);
    x += lengthdir_x(_spd, _md);
    y += lengthdir_y(_spd, _md);
    face_dir = _md;
}
scr_house_resolve_circle(id, 18);

// Find nearest target (mouse or rat boss)
var _tgt = noone, _best = 340;
with (obj_rat_boss) {
    var _d = point_distance(x, y, other.x, other.y);
    if (_d < _best) { _best = _d; _tgt = id; }
}
with (obj_mouse) {
    var _d = point_distance(x, y, other.x, other.y);
    if (_d < _best) { _best = _d; _tgt = id; }
}

// Auto-Attack 1: Claw Swipe
claw_cd -= (ult_timer > 0 ? 1.6 : 1.0);
if (claw_cd <= 0 && instance_exists(_tgt) && _best < 110 + scr_upgrade_level("claws") * 12) {
    claw_cd = 26;
    var _a = point_direction(x, y, _tgt.x, _tgt.y);
    var _dmg = (18 + scr_upgrade_level("claws") * 7) * (ult_timer > 0 ? 1.5 : 1.0);
    var _p = instance_create_layer(x + lengthdir_x(26, _a), y + lengthdir_y(26, _a), "Instances", obj_projectile);
    _p.kind = "claw"; _p.dmg = _dmg; _p.dir = _a; _p.life = 10; _p.rad = 38 + scr_upgrade_level("claws") * 6;
}

// Auto-Attack 2: Bouncing Yarn Ball
if (scr_upgrade_level("yarn") > 0) {
    yarn_cd -= 1;
    if (yarn_cd <= 0 && instance_exists(_tgt)) {
        yarn_cd = max(28, 62 - scr_upgrade_level("yarn") * 6);
        var _a = point_direction(x, y, _tgt.x, _tgt.y);
        var _p = instance_create_layer(x, y, "Instances", obj_projectile);
        _p.kind = "yarn"; _p.dmg = 16 + scr_upgrade_level("yarn") * 5; _p.dir = _a; _p.spd = 6.5; _p.bounces = 2 + scr_upgrade_level("yarn"); _p.life = 120;
    }
}

// Auto-Attack 3: Piercing Fishbone Fan
if (scr_upgrade_level("bones") > 0) {
    bone_cd -= 1;
    if (bone_cd <= 0 && instance_exists(_tgt)) {
        bone_cd = 48;
        var _cnt = 2 + scr_upgrade_level("bones");
        var _base = point_direction(x, y, _tgt.x, _tgt.y);
        for (var i = 0; i < _cnt; i++) {
            var _off = -18 + (36 * i) / max(1, _cnt - 1);
            var _p = instance_create_layer(x, y, "Instances", obj_projectile);
            _p.kind = "bone"; _p.dmg = 14 + scr_upgrade_level("bones") * 4; _p.dir = _base + _off; _p.spd = 8.0; _p.pierce = 3; _p.life = 70;
        }
    }
}

// Auto-Attack 4: Catnip AoE Bomb
if (scr_upgrade_level("bomb") > 0) {
    bomb_cd -= 1;
    if (bomb_cd <= 0 && instance_exists(_tgt)) {
        bomb_cd = max(55, 115 - scr_upgrade_level("bomb") * 10);
        var _p = instance_create_layer(_tgt.x, _tgt.y, "Instances", obj_projectile);
        _p.kind = "bomb"; _p.dmg = 24 + scr_upgrade_level("bomb") * 10; _p.rad = 68 + scr_upgrade_level("bomb") * 12; _p.life = 18;
    }
}
"""

OBJ_BEBECHAD_DRAW = r"""
var _col = hurt_cd > 25 ? c_red : (ult_timer > 0 ? make_color_rgb(255, 232, 110) : c_white);
// Rotate top-down cat sprite cleanly (111111.aseprite faces 270° down by default -> +90 offset!)
draw_sprite_ext(spr_bebechad_top, 0, x, y, 0.85, 0.85, face_dir + 90, _col, 1);
if (ult_timer > 0) {
    draw_set_color(make_color_rgb(250, 224, 75));
    draw_circle(x, y, 30 + sin(current_time * 0.02) * 3, true);
}
"""

OBJ_MOUSE_CREATE = r"""
max_hp = 24 + global.wave * 8;
hp = max_hp;
spd = random_range(1.6, 2.5);
flash_timer = 0;
vx = 0;
vy = 0;
"""

OBJ_MOUSE_STEP = r"""
if (global.shop_open || global.dlg_active != noone || global.mg_active) exit;
if (flash_timer > 0) flash_timer -= 1;

if (instance_exists(obj_bebechad)) {
    var _d = point_direction(x, y, obj_bebechad.x, obj_bebechad.y);
    x += lengthdir_x(spd, _d) + vx;
    y += lengthdir_y(spd, _d) + vy;
    image_angle = _d + 90;
    vx *= 0.82; vy *= 0.82;
    scr_house_resolve_circle(id, 11);

    if (point_distance(x, y, obj_bebechad.x, obj_bebechad.y) < 24 && obj_bebechad.hurt_cd <= 0 && obj_bebechad.dash_timer <= 0) {
        obj_bebechad.hp = max(0, obj_bebechad.hp - 7);
        obj_bebechad.hurt_cd = 34;
        if (obj_bebechad.hp <= 0) room_restart();
    }
}

if (hp <= 0) {
    global.kills += 1;
    if (instance_exists(obj_bebechad)) obj_bebechad.ult_charge = min(100, obj_bebechad.ult_charge + 6);
    var _drop_ch = min(0.95, 0.55 + scr_upgrade_level("magnet") * 0.08);
    if (random(1) < _drop_ch) {
        var _c = instance_create_layer(x, y, "Instances", obj_catnip);
        _c.val = max(1, round(1 + scr_upgrade_level("magnet") * 0.35));
    }
    instance_destroy();
}
"""

OBJ_MOUSE_DRAW = r"""
draw_sprite_ext(spr_mouse_top, 0, x, y, 1, 1, image_angle, flash_timer > 0 ? c_white : c_white, 1);
if (flash_timer > 0) {
    draw_set_color(c_yellow);
    draw_circle(x, y, 11, true);
}
"""

OBJ_RAT_BOSS_CREATE = r"""
max_hp = 380 + global.boss_count * 220;
hp = max_hp;
spd = 1.9;
flash_timer = 0;
stun_timer = 0;
shield_active = false;
phase_triggered_1 = false;
phase_triggered_2 = false;
shoot_cd = 90;
"""

OBJ_RAT_BOSS_STEP = r"""
if (global.shop_open || global.dlg_active != noone || global.mg_active) exit;
if (flash_timer > 0) flash_timer -= 1;
if (stun_timer > 0) { stun_timer -= 1; exit; }

// Trigger Boss Shield + Timing Bar / QTE Combo Mini-Game at 66% and 33% HP!
if (!phase_triggered_1 && hp <= max_hp * 0.66) {
    phase_triggered_1 = true;
    shield_active = true;
    scr_minigame_start(id, 3);
    exit;
}
if (!phase_triggered_2 && hp <= max_hp * 0.33) {
    phase_triggered_2 = true;
    shield_active = true;
    scr_minigame_start(id, 4);
    exit;
}

if (instance_exists(obj_bebechad)) {
    var _d = point_direction(x, y, obj_bebechad.x, obj_bebechad.y);
    x += lengthdir_x(spd, _d);
    y += lengthdir_y(spd, _d);
    image_angle = _d + 90;
    scr_house_resolve_circle(id, 24);

    // Radial cheese volley
    shoot_cd -= 1;
    if (shoot_cd <= 0) {
        shoot_cd = 110;
        for (var k = 0; k < 6; k++) {
            var _p = instance_create_layer(x, y, "Instances", obj_projectile);
            _p.kind = "cheese"; _p.dir = _d + k * 60; _p.spd = 4.2; _p.dmg = 10; _p.life = 130;
        }
    }

    if (point_distance(x, y, obj_bebechad.x, obj_bebechad.y) < 36 && obj_bebechad.hurt_cd <= 0 && obj_bebechad.dash_timer <= 0) {
        obj_bebechad.hp = max(0, obj_bebechad.hp - 14);
        obj_bebechad.hurt_cd = 40;
        if (obj_bebechad.hp <= 0) room_restart();
    }
}

if (hp <= 0) {
    global.kills += 1;
    var _rew = 30 + global.boss_count * 10;
    global.catnip += _rew;
    scr_dialogue_push("Bebechad", spr_portrait_bebechad, "Крысиный Босс повержен! +" + string(_rew) + " Кошачьей Мяты. Кто следующий?");
    instance_destroy();
}
"""

OBJ_RAT_BOSS_DRAW = r"""
draw_sprite_ext(spr_rat_boss_top, 0, x, y, 1.25, 1.25, image_angle, stun_timer > 0 ? make_color_rgb(130, 220, 255) : c_white, 1);
if (shield_active) {
    draw_set_color(make_color_rgb(250, 224, 75));
    draw_circle(x, y, 36, true);
}
"""

OBJ_PROJ_CREATE = r"""
kind = "claw";
dmg = 18;
dir = 0;
spd = 0;
rad = 28;
bounces = 0;
pierce = 1;
life = 30;
hit_list = [];
"""

OBJ_PROJ_STEP = r"""
if (global.shop_open || global.dlg_active != noone || global.mg_active) exit;
life -= 1;
if (life <= 0) { instance_destroy(); exit; }

if (spd > 0) {
    x += lengthdir_x(spd, dir);
    y += lengthdir_y(spd, dir);
}

if (kind == "cheese") {
    if (instance_exists(obj_bebechad) && point_distance(x, y, obj_bebechad.x, obj_bebechad.y) < 20) {
        if (obj_bebechad.hurt_cd <= 0 && obj_bebechad.dash_timer <= 0) {
            obj_bebechad.hp = max(0, obj_bebechad.hp - dmg);
            obj_bebechad.hurt_cd = 30;
            if (obj_bebechad.hp <= 0) room_restart();
        }
        instance_destroy();
    }
    exit;
}

// Player projectile hit detection against mice & rat boss
var _hit_r = (kind == "claw" || kind == "bomb") ? rad : 18;
var _crit_ch = 0.08 + scr_upgrade_level("chadcrit") * 0.15;
var _crit_mul = 1.8 + scr_upgrade_level("chadcrit") * 0.35;

var _targets = [obj_mouse, obj_rat_boss];
for (var t = 0; t < 2; t++) {
    with (_targets[t]) {
        if (point_distance(x, y, other.x, other.y) <= _hit_r) {
            var _already = false;
            for (var h = 0; h < array_length(other.hit_list); h++) {
                if (other.hit_list[h] == id) { _already = true; break; }
            }
            if (!_already) {
                array_push(other.hit_list, id);
                var _final_dmg = other.dmg * (random(1) < _crit_ch ? _crit_mul : 1.0);
                hp -= _final_dmg;
                flash_timer = 8;
                if (object_index == obj_mouse) {
                    vx += lengthdir_x(5, other.dir);
                    vy += lengthdir_y(5, other.dir);
                }
                if (other.kind == "yarn") {
                    if (other.bounces > 0) {
                        other.bounces -= 1;
                        other.dir += irandom_range(100, 220);
                    } else {
                        other.life = 0;
                    }
                } else if (other.kind == "bone") {
                    other.pierce -= 1;
                    if (other.pierce <= 0) other.life = 0;
                }
            }
        }
    }
}
"""

OBJ_PROJ_DRAW = r"""
if (kind == "claw") {
    draw_set_color(make_color_rgb(255, 245, 210));
    draw_circle(x, y, rad * 0.65, true);
} else if (kind == "yarn") {
    draw_set_color(make_color_rgb(235, 92, 138));
    draw_circle(x, y, 7, false);
} else if (kind == "bone") {
    draw_set_color(c_white);
    draw_circle(x, y, 4, false);
} else if (kind == "bomb") {
    draw_set_color(make_color_rgb(100, 235, 145));
    draw_circle(x, y, rad, true);
} else if (kind == "cheese") {
    draw_set_color(make_color_rgb(250, 212, 68));
    draw_circle(x, y, 6, false);
}
"""

OBJ_CATNIP_CREATE = r"""
val = 3;
"""

OBJ_CATNIP_STEP = r"""
if (global.shop_open || global.dlg_active != noone || global.mg_active) exit;
if (instance_exists(obj_bebechad)) {
    var _d = point_distance(x, y, obj_bebechad.x, obj_bebechad.y);
    var _mag = 95 + scr_upgrade_level("magnet") * 45;
    if (_d < _mag) {
        var _a = point_direction(x, y, obj_bebechad.x, obj_bebechad.y);
        x += lengthdir_x(6.5, _a);
        y += lengthdir_y(6.5, _a);
    }
    if (_d < 20) {
        global.catnip += val;
        instance_destroy();
    }
}
"""

OBJ_CATNIP_DRAW = r"""
draw_sprite(spr_catnip, 0, x, y + sin(current_time * 0.008 + x) * 2);
"""


def build_room():
    inst_id = f"inst_{uuid.uuid4().hex[:8]}"
    rm_yy = {
        "$GMRoom": "v1",
        "%Name": "rm_house",
        "creationCodeFile": "",
        "inheritCode": False,
        "inheritCreationOrder": False,
        "inheritLayers": False,
        "instanceCreationOrder": [{"name": inst_id, "path": "rooms/rm_house/rm_house.yy"}],
        "isDnd": False,
        "layers": [
            {
                "$GMRInstanceLayer": "",
                "%Name": "Instances",
                "depth": 0,
                "effectEnabled": True,
                "effectType": None,
                "gridX": 32,
                "gridY": 32,
                "hierarchyFrozen": False,
                "inheritLayerDepth": False,
                "inheritLayerSettings": False,
                "inheritSubLayers": True,
                "inheritVisibility": True,
                "instances": [
                    {
                        "$GMInstance": "v1",
                        "%Name": inst_id,
                        "colour": 4294967295,
                        "frozen": False,
                        "hasCreationCode": False,
                        "ignore": False,
                        "imageIndex": 0,
                        "imageSpeed": 1.0,
                        "inheritCode": False,
                        "inheritedItemId": None,
                        "inheritItemSettings": False,
                        "isDnd": False,
                        "name": inst_id,
                        "objectId": {"name": "obj_game", "path": "objects/obj_game/obj_game.yy"},
                        "properties": [],
                        "resourceType": "GMInstance",
                        "resourceVersion": "2.0",
                        "rotation": 0.0,
                        "scaleX": 1.0,
                        "scaleY": 1.0,
                        "x": 480.0,
                        "y": 320.0,
                    }
                ],
                "layers": [],
                "name": "Instances",
                "properties": [],
                "resourceType": "GMRInstanceLayer",
                "resourceVersion": "2.0",
                "userdefinedDepth": False,
                "visible": True,
            },
            {
                "$GMRBackgroundLayer": "",
                "%Name": "Background",
                "animationFPS": 15.0,
                "animationSpeedType": 0,
                "colour": 4279964952,
                "depth": 100,
                "effectEnabled": True,
                "effectType": None,
                "gridX": 32,
                "gridY": 32,
                "hierarchyFrozen": False,
                "hspeed": 0.0,
                "htiled": False,
                "inheritLayerDepth": False,
                "inheritLayerSettings": False,
                "inheritSubLayers": True,
                "inheritVisibility": True,
                "layers": [],
                "name": "Background",
                "properties": [],
                "resourceType": "GMRBackgroundLayer",
                "resourceVersion": "2.0",
                "spriteId": None,
                "stretch": False,
                "userdefinedDepth": False,
                "visible": True,
                "vspeed": 0.0,
                "vtiled": False,
                "x": 0,
                "y": 0,
            },
        ],
        "name": "rm_house",
        "parent": {"name": "Rooms", "path": "folders/Rooms.yy"},
        "parentRoom": None,
        "physicsSettings": {
            "inheritPhysicsSettings": False,
            "PhysicsWorld": False,
            "PhysicsWorldGravityX": 0.0,
            "PhysicsWorldGravityY": 10.0,
            "PhysicsWorldPixToMetres": 0.1,
        },
        "resourceType": "GMRoom",
        "resourceVersion": "2.0",
        "roomSettings": {
            "Height": 1280,
            "inheritRoomSettings": False,
            "persistent": False,
            "Width": 1920,
        },
        "sequenceId": None,
        "views": [
            {
                "hborder": 32,
                "hport": 720,
                "hspeed": -1,
                "hview": 360,
                "inherit": False,
                "objectId": None,
                "vborder": 32,
                "visible": True,
                "vspeed": -1,
                "wport": 1280,
                "wview": 640,
                "xport": 0,
                "xview": 160,
                "yport": 0,
                "yview": 140,
            },
            *[
                {
                    "hborder": 32,
                    "hport": 768,
                    "hspeed": -1,
                    "hview": 768,
                    "inherit": False,
                    "objectId": None,
                    "vborder": 32,
                    "visible": False,
                    "vspeed": -1,
                    "wport": 1024,
                    "wview": 1024,
                    "xport": 0,
                    "xview": 0,
                    "yport": 0,
                    "yview": 0,
                }
                for _ in range(7)
            ],
        ],
        "viewSettings": {
            "clearDisplayBuffer": True,
            "clearViewBackground": False,
            "enableViews": True,
            "inheritViewSettings": False,
        },
        "volume": 1.0,
    }
    save_yy(os.path.join(GM_DIR, "rooms", "rm_house", "rm_house.yy"), rm_yy)
    return {"id": {"name": "rm_house", "path": "rooms/rm_house/rm_house.yy"}}


def build_options():
    save_yy(
        os.path.join(GM_DIR, "options", "main", "options_main.yy"),
        {
            "$GMMainOptions": "v1",
            "%Name": "Main",
            "name": "Main",
            "option_author": "Bebechad Team",
            "option_collision_compatibility": False,
            "option_copy_on_write_enabled": False,
            "option_draw_colour": 4294967295,
            "option_gameguid": str(uuid.uuid4()),
            "option_gameid": "0",
            "option_game_speed": 60,
            "option_mips_for_3d_textures": False,
            "option_sci_usesci": False,
            "option_spine_licence": False,
            "option_steam_app_id": "0",
            "option_template_description": "Bebechad: Home Alone — Top-down Cat vs Mice & Rat Bosses",
            "option_template_icon": "${base_options_dir}/main/template_icon.png",
            "option_template_image": "${base_options_dir}/main/template_image.png",
            "option_window_colour": 255,
            "resourceType": "GMMainOptions",
            "resourceVersion": "2.0",
        },
    )
    save_yy(
        os.path.join(GM_DIR, "options", "windows", "options_windows.yy"),
        {
            "$GMWindowsOptions": "v1",
            "%Name": "Windows",
            "name": "Windows",
            "option_windows_allow_fullscreen_switching": True,
            "option_windows_borderless": False,
            "option_windows_company_info": "Bebechad",
            "option_windows_copyright_info": "",
            "option_windows_description_info": "Bebechad: Home Alone",
            "option_windows_display_cursor": True,
            "option_windows_display_name": "Bebechad: Home Alone",
            "option_windows_enable_steam": False,
            "option_windows_disable_sandbox": False,
            "option_windows_interpolate_pixels": False,
            "option_windows_product_info": "BebechadHomeAlone",
            "option_windows_resize_window": True,
            "option_windows_scale": 0,
            "option_windows_start_fullscreen": False,
            "option_windows_vsync": True,
            "resourceType": "GMWindowsOptions",
            "resourceVersion": "2.0",
        },
    )


def main():
    build_placeholder_sprites()
    if os.path.exists(GM_DIR):
        shutil.rmtree(GM_DIR)
    os.makedirs(GM_DIR, exist_ok=True)

    resources = []

    # Sprites
    sprite_specs = [
        ("spr_bebechad_top", "spr_bebechad_top.png", True),
        ("spr_portrait_bebechad", "spr_portrait_bebechad.png", False),
        ("spr_portrait_cat_angry", "spr_portrait_cat_angry.png", False),
        ("spr_portrait_rat", "spr_portrait_rat.png", False),
        ("spr_tile_grass_dark", "tile_grass_dark.png", False),
        ("spr_tile_grass_overlay", "tile_grass_overlay.png", False),
        ("spr_tile_brick_moss", "tile_brick_moss.png", False),
        ("spr_mouse_top", "spr_mouse_top.png", True),
        ("spr_rat_boss_top", "spr_rat_boss_top.png", True),
        ("spr_catnip", "spr_catnip.png", True),
    ]
    for sname, fname, centered in sprite_specs:
        resources.append(make_sprite(sname, os.path.join(RAW_DIR, fname), centered))

    # Scripts
    resources.append(make_script("scr_house_map", GML_HOUSE_MAP))
    resources.append(make_script("scr_catnip_shop", GML_CATNIP_SHOP))
    resources.append(make_script("scr_boss_minigame", GML_BOSS_MINIGAME))

    # Objects
    resources.append(
        make_object(
            "obj_game",
            None,
            [
                (0, 0, "Create_0.gml", OBJ_GAME_CREATE),
                (3, 0, "Step_0.gml", OBJ_GAME_STEP),
                (8, 0, "Draw_0.gml", OBJ_GAME_DRAW),
                (8, 64, "Draw_64.gml", OBJ_GAME_DRAW_GUI),
                (12, 0, "CleanUp_0.gml", OBJ_GAME_CLEANUP),
            ],
        )
    )
    resources.append(
        make_object(
            "obj_bebechad",
            "spr_bebechad_top",
            [
                (0, 0, "Create_0.gml", OBJ_BEBECHAD_CREATE),
                (3, 0, "Step_0.gml", OBJ_BEBECHAD_STEP),
                (8, 0, "Draw_0.gml", OBJ_BEBECHAD_DRAW),
            ],
        )
    )
    resources.append(
        make_object(
            "obj_mouse",
            "spr_mouse_top",
            [
                (0, 0, "Create_0.gml", OBJ_MOUSE_CREATE),
                (3, 0, "Step_0.gml", OBJ_MOUSE_STEP),
                (8, 0, "Draw_0.gml", OBJ_MOUSE_DRAW),
            ],
        )
    )
    resources.append(
        make_object(
            "obj_rat_boss",
            "spr_rat_boss_top",
            [
                (0, 0, "Create_0.gml", OBJ_RAT_BOSS_CREATE),
                (3, 0, "Step_0.gml", OBJ_RAT_BOSS_STEP),
                (8, 0, "Draw_0.gml", OBJ_RAT_BOSS_DRAW),
            ],
        )
    )
    resources.append(
        make_object(
            "obj_projectile",
            None,
            [
                (0, 0, "Create_0.gml", OBJ_PROJ_CREATE),
                (3, 0, "Step_0.gml", OBJ_PROJ_STEP),
                (8, 0, "Draw_0.gml", OBJ_PROJ_DRAW),
            ],
        )
    )
    resources.append(
        make_object(
            "obj_catnip",
            "spr_catnip",
            [
                (0, 0, "Create_0.gml", OBJ_CATNIP_CREATE),
                (3, 0, "Step_0.gml", OBJ_CATNIP_STEP),
                (8, 0, "Draw_0.gml", OBJ_CATNIP_DRAW),
            ],
        )
    )

    # Room
    resources.append(build_room())
    build_options()

    # Virtual Folders + .yyp (GMProject resourceVersion 2.0 for GameMaker LTS 2026)
    folders = ["Sprites", "Scripts", "Objects", "Rooms"]
    folder_nodes = []
    for fn in folders:
        fyy = {
            "$GMFolder": "",
            "%Name": fn,
            "folderPath": f"folders/{fn}.yy",
            "name": fn,
            "resourceType": "GMFolder",
            "resourceVersion": "2.0",
        }
        save_yy(os.path.join(GM_DIR, "folders", f"{fn}.yy"), fyy)
        folder_nodes.append(fyy)

    # Included Files: bundle open-source Cyrillic font (LiberationSans-Bold, SIL OFL 1.1)
    included_files = []
    font_src = os.path.join(RAW_DIR, "ui_font.ttf")
    if os.path.exists(font_src):
        datafiles_dir = os.path.join(GM_DIR, "datafiles")
        os.makedirs(datafiles_dir, exist_ok=True)
        shutil.copy2(font_src, os.path.join(datafiles_dir, "ui_font.ttf"))
        included_files.append(
            {
                "$GMIncludedFile": "",
                "%Name": "ui_font.ttf",
                "CopyToMask": -1,
                "filePath": "datafiles",
                "name": "ui_font.ttf",
                "resourceType": "GMIncludedFile",
                "resourceVersion": "2.0",
            }
        )

    yyp = {
        "$GMProject": "v1",
        "%Name": "BebechadHomeAlone",
        "AudioGroups": [
            {
                "$GMAudioGroup": "",
                "%Name": "audiogroup_default",
                "name": "audiogroup_default",
                "resourceType": "GMAudioGroup",
                "resourceVersion": "2.0",
                "targets": -1,
            }
        ],
        "configs": {"children": [], "name": "Default"},
        "defaultScriptType": 1,
        "Folders": folder_nodes,
        "IncludedFiles": included_files,
        "isEcma": False,
        "LibraryEmitters": [],
        "MetaData": {"IDEVersion": "2024.11.0.179"},
        "name": "BebechadHomeAlone",
        "resources": resources,
        "resourceType": "GMProject",
        "resourceVersion": "2.0",
        "RoomOrderNodes": [{"roomId": {"name": "rm_house", "path": "rooms/rm_house/rm_house.yy"}}],
        "templateType": "game",
        "TextureGroups": [
            {
                "$GMTextureGroup": "",
                "%Name": "Default",
                "autocrop": True,
                "border": 2,
                "compressFormat": "bz2",
                "customOptions": "",
                "directory": "",
                "groupParent": None,
                "isScaled": True,
                "loadType": "default",
                "mipsToGenerate": 0,
                "name": "Default",
                "resourceType": "GMTextureGroup",
                "resourceVersion": "2.0",
                "targets": -1,
            }
        ],
    }
    save_yy(os.path.join(GM_DIR, "BebechadHomeAlone.yyp"), yyp)
    print(f"Generated GameMaker LTS 2026 project with {len(resources)} resources at {GM_DIR}")
    audit_gm_project()
    build_transfer_packages()


def audit_gm_project():
    """Verify every .yyp/.yy JSON, sprite PNG, GML script, event, room, and IncludedFile."""
    yyp_path = os.path.join(GM_DIR, "BebechadHomeAlone.yyp")
    with open(yyp_path, "r", encoding="utf-8") as f:
        yyp = json.load(f)

    errors = []
    # Check all referenced resources
    for r in yyp.get("resources", []):
        rel = r["id"]["path"]
        full = os.path.join(GM_DIR, rel.replace("/", os.sep))
        if not os.path.isfile(full):
            errors.append(f"Missing resource: {rel}")
            continue
        with open(full, "r", encoding="utf-8") as rf:
            data = json.load(rf)
        rtype = data.get("resourceType")
        if rtype == "GMSprite":
            sdir = os.path.dirname(full)
            for fr in data.get("frames", []):
                fid = fr["name"]
                fpng = os.path.join(sdir, f"{fid}.png")
                if not os.path.isfile(fpng):
                    errors.append(f"Missing sprite frame PNG: {fpng}")
                else:
                    with open(fpng, "rb") as pf:
                        if pf.read(8) != b"\x89PNG\r\n\x1a\n":
                            errors.append(f"Invalid PNG header: {fpng}")
                for lyr in data.get("layers", []):
                    lid = lyr["name"]
                    lpng = os.path.join(sdir, "layers", fid, f"{lid}.png")
                    if not os.path.isfile(lpng):
                        errors.append(f"Missing sprite layer PNG: {lpng}")
        elif rtype == "GMScript":
            gml = os.path.join(os.path.dirname(full), f"{data['name']}.gml")
            if not os.path.isfile(gml):
                errors.append(f"Missing script GML: {gml}")
        elif rtype == "GMObject":
            odir = os.path.dirname(full)
            ev_prefix = {0: "Create", 3: "Step", 8: "Draw", 12: "CleanUp"}
            for ev in data.get("eventList", []):
                pref = ev_prefix.get(ev["eventType"])
                if pref:
                    egml = os.path.join(odir, f"{pref}_{ev['eventNum']}.gml")
                    if not os.path.isfile(egml):
                        errors.append(f"Missing object event GML: {egml}")
        elif rtype == "GMRoom":
            if len(data.get("views", [])) != 8:
                errors.append(f"Room {data['name']} has {len(data.get('views', []))} views (expected 8)")

    # Check folders
    for fld in yyp.get("Folders", []):
        fp = os.path.join(GM_DIR, fld["folderPath"].replace("/", os.sep))
        if not os.path.isfile(fp):
            errors.append(f"Missing folder .yy: {fld['folderPath']}")

    # Check IncludedFiles
    for inc in yyp.get("IncludedFiles", []):
        ip = os.path.join(GM_DIR, inc["filePath"].replace("/", os.sep), inc["name"])
        if not os.path.isfile(ip):
            errors.append(f"Missing IncludedFile: {ip}")

    # Check RoomOrderNodes
    for rn in yyp.get("RoomOrderNodes", []):
        rp = os.path.join(GM_DIR, rn["roomId"]["path"].replace("/", os.sep))
        if not os.path.isfile(rp):
            errors.append(f"Missing RoomOrderNode: {rn['roomId']['path']}")

    # Check options
    for opt in ("options/main/options_main.yy", "options/windows/options_windows.yy"):
        op = os.path.join(GM_DIR, opt.replace("/", os.sep))
        if not os.path.isfile(op):
            errors.append(f"Missing option file: {opt}")
        else:
            with open(op, "r", encoding="utf-8") as of:
                json.load(of)

    if errors:
        raise RuntimeError("GameMaker project audit FAILED:\n  - " + "\n  - ".join(errors))
    print(f"[AUDIT PASSED] {len(yyp['resources'])} resources, {len(yyp['IncludedFiles'])} IncludedFiles, 8 room views, all JSON & PNG verified.")


HOW_TO_OPEN_RU = """============================================================
  BEBECHAD: ОДИН ДОМА — ПЕРЕНОС В GAMEMAKER (LTS 2026 / 2024+)
============================================================

СПОСОБ 1 (САМЫЙ БЫСТРЫЙ — через файл BebechadHomeAlone.yyz):
  1. Перенеси файл BebechadHomeAlone.yyz на другой компьютер.
  2. Открой GameMaker (2024+ / LTS 2026).
  3. Нажми File -> Import (Файл -> Импорт) и выбери BebechadHomeAlone.yyz.
  4. Выбери папку, куда распаковать проект -> нажми F5 (Run)!

СПОСОБ 2 (Через этот архив BebechadHomeAlone_GameMaker_Portable.zip):
  1. Распакуй папку BebechadHomeAlone в любую папку без спецсимволов
     (например, C:\\Games\\BebechadHomeAlone).
  2. Открой GameMaker -> Open -> выбери BebechadHomeAlone\\BebechadHomeAlone.yyp
     (или просто дважды кликни по BebechadHomeAlone.yyp).
  3. Нажми F5 (Run) для запуска игры!

ЧТО УЖЕ ВШИТО В ПРОЕКТ (ничего докачивать не нужно):
  - Все спрайты и портреты Bebechad / Catttt / Rat1 / тайлы окружения
  - Встроенный кириллический шрифт ui_font.ttf (LiberationSans-Bold, SIL OFL)
    в папке datafiles/ — русский текст работает сразу на любом ПК!
  - Фиксированный GUI 1280x720 (одинаково красиво на любом мониторе)
  - 4 комнаты дома (Гостиная, Кухня, Подвал, Задний Двор)
  - 3 уникальных Крысиных Босса + босс-мини-игры (тайминг-бар + QTE)
  - Магазин Кошачьей Мяты и уютный интерфейс в стиле Stardew (вариант #3)

УПРАВЛЕНИЕ В ИГРЕ:
  WASD / Стрелки   — движение кота Bebechad (авто-атаки срабатывают сами)
  Shift            — рывок (Pounce Dash)
  F                — Ульта Гигачада (когда шкала 100%)
  B / Tab / E      — Магазин Кошачьей Мяты (E рядом с миской в гостиной)
  1–8              — быстрая покупка улучшений в магазине
  Пробел / ЛКМ     — пролистать диалог / попасть в зелёную зону мини-игры
  T                — мгновенно призвать Крысиного Босса (для теста)
"""


def build_transfer_packages():
    os.makedirs(EXPORT_DIR, exist_ok=True)
    yyz_path = os.path.join(EXPORT_DIR, "BebechadHomeAlone.yyz")
    zip_path = os.path.join(EXPORT_DIR, "BebechadHomeAlone_GameMaker_Portable.zip")

    # 1) Native GameMaker .yyz archive (files directly at archive root!)
    with zipfile.ZipFile(yyz_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for dirpath, dirnames, filenames in os.walk(GM_DIR):
            dirnames.sort()
            for fname in sorted(filenames):
                full = os.path.join(dirpath, fname)
                arcname = os.path.relpath(full, GM_DIR).replace(os.sep, "/")
                zf.write(full, arcname)

    # 2) Portable ZIP with BebechadHomeAlone/ folder + Russian instructions
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        zf.writestr("КАК_ОТКРЫТЬ.txt", HOW_TO_OPEN_RU.encode("utf-8"))
        for dirpath, dirnames, filenames in os.walk(GM_DIR):
            dirnames.sort()
            for fname in sorted(filenames):
                full = os.path.join(dirpath, fname)
                rel = os.path.relpath(full, GM_DIR).replace(os.sep, "/")
                zf.write(full, f"BebechadHomeAlone/{rel}")

    print(f"[EXPORT READY] {yyz_path} ({os.path.getsize(yyz_path) / 1024:.1f} KB)")
    print(f"[EXPORT READY] {zip_path} ({os.path.getsize(zip_path) / 1024:.1f} KB)")


if __name__ == "__main__":
    main()
