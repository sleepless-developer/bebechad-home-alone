if (kind == "claw") {
    draw_set_color(make_color_rgb(255, 245, 210));
    draw_circle(x, y, rad * 0.65, true);
} else if (kind == "yarn") {
    draw_set_color(make_color_rgb(235, 92, 138));
    draw_circle(x, y, 7, false);
} else if (kind == "bone") {
    draw_set_color(c_white);
    draw_circle(x, y, 4, false);
} else if (kind == "bomb") {
    draw_set_color(make_color_rgb(100, 235, 145));
    draw_circle(x, y, rad, true);
} else if (kind == "cheese") {
    draw_set_color(make_color_rgb(250, 212, 68));
    draw_circle(x, y, 6, false);
}
