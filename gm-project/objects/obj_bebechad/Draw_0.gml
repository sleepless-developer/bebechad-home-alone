var _col = hurt_cd > 25 ? c_red : (ult_timer > 0 ? make_color_rgb(255, 232, 110) : c_white);
// Rotate top-down cat sprite cleanly (111111.aseprite faces 270° down by default -> +90 offset!)
draw_sprite_ext(spr_bebechad_top, 0, x, y, 0.85, 0.85, face_dir + 90, _col, 1);
if (ult_timer > 0) {
    draw_set_color(make_color_rgb(250, 224, 75));
    draw_circle(x, y, 30 + sin(current_time * 0.02) * 3, true);
}
