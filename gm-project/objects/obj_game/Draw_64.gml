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
    draw_text(_gw * 0.5 - 120, 72, "КРЫСИНЫЙ БОСС (" + string(max(0, ceil(_b.hp))) + "/" + string(_b.max_hp) + ")");
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
