draw_sprite_ext(spr_rat_boss_top, 0, x, y, 1.25, 1.25, image_angle, stun_timer > 0 ? make_color_rgb(130, 220, 255) : c_white, 1);
if (shield_active) {
    draw_set_color(make_color_rgb(250, 224, 75));
    draw_circle(x, y, 36, true);
}
