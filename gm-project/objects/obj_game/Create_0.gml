randomize();
scr_house_init();
scr_catnip_shop_init();
scr_dialogue_init();

global.wave = 1;
global.kills = 0;
global.run_time = 0;
global.spawn_timer = 40;
global.boss_timer = 60 * 35; // First Rat Boss at 35s (or press [T] anytime!)
global.boss_count = 0;

instance_create_layer(480, 320, "Instances", obj_bebechad);

// Opening Monologue: Bebechad (gigachad) -> Catttt (outraged!)
scr_dialogue_push("Bebechad", spr_portrait_bebechad, "Хозяева уехали. Весь дом в моём распоряжении. Время чиллить.");
scr_dialogue_push("Bebechad", spr_portrait_cat_angry, "СТОП... ЧТО ЭТО ШУРШИТ НА КУХНЕ И В ПОДВАЛЕ?! МЫШИ?!");
scr_dialogue_push("Bebechad", spr_portrait_bebechad, "Ладно. Разминаем когти. За кошачью мяту я разнесу всю их банду.");
