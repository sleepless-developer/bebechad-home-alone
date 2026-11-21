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
