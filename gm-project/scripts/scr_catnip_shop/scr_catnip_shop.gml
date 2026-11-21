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
