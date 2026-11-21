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
