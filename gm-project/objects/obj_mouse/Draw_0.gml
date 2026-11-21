draw_sprite_ext(spr_mouse_top, 0, x, y, 1, 1, image_angle, flash_timer > 0 ? c_white : c_white, 1);
if (flash_timer > 0) {
    draw_set_color(c_yellow);
    draw_circle(x, y, 11, true);
}
