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
