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
