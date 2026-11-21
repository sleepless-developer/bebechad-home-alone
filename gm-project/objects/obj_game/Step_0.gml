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

// Spawn Rat Boss
global.boss_timer -= 1;
if (global.boss_timer <= 0 && !instance_exists(obj_rat_boss) && instance_exists(obj_bebechad)) {
    global.boss_count += 1;
    global.boss_timer = 60 * 45;
    var _bx = clamp(obj_bebechad.x + 260, 120, global.world_w - 120);
    var _by = clamp(obj_bebechad.y, 120, global.world_h - 120);
    instance_create_layer(_bx, _by, "Instances", obj_rat_boss);
    scr_dialogue_push("Крысиный Босс #" + string(global.boss_count), spr_portrait_rat, "Хе-хе! Хозяев нет — теперь этот холодильник и весь дом НАШИ!");
    scr_dialogue_push("Bebechad", spr_portrait_cat_angry, "МОЙ ХОЛОДИЛЬНИК?! Ты только что подписал себе приговор!");
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
