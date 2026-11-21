if (variable_global_exists("ui_font") && global.ui_font != -1 && font_exists(global.ui_font)) {
    font_delete(global.ui_font);
    global.ui_font = -1;
}
