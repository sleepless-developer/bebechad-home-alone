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
