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
