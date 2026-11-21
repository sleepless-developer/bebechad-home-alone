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
