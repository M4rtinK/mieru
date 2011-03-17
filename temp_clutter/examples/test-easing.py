import clutter

EASING_MODES = [
        ("linear", clutter.LINEAR),
        ("easeInQuad", clutter.EASE_IN_QUAD),
        ("easeOutQuad", clutter.EASE_OUT_QUAD),
        ("easeInOutQuad", clutter.EASE_IN_OUT_QUAD),
        ("easeInQubic", clutter.EASE_IN_CUBIC),
        ("easeOutCubic", clutter.EASE_OUT_CUBIC),
        ("easeInOutCubic", clutter.EASE_IN_OUT_CUBIC),
        ("easeInQuart", clutter.EASE_IN_QUART),
        ("easeOutQuart", clutter.EASE_OUT_QUART),
        ("easeInOutQuart", clutter.EASE_IN_OUT_QUART),
        ("easeInQuint", clutter.EASE_IN_QUINT),
        ("easeOutQuint", clutter.EASE_OUT_QUINT),
        ("easeInOutQuint", clutter.EASE_IN_OUT_QUINT),
        ("easeInSine", clutter.EASE_IN_SINE),
        ("easeOutSine", clutter.EASE_OUT_SINE),
        ("easeInOutSine", clutter.EASE_IN_OUT_SINE),
        ("easeInExpo", clutter.EASE_IN_EXPO),
        ("easeOutExpo", clutter.EASE_OUT_EXPO),
        ("easeInOutExpo", clutter.EASE_IN_OUT_EXPO),
        ("easeInCirc", clutter.EASE_IN_CIRC),
        ("easeOutCirt", clutter.EASE_OUT_CIRC),
        ("easeInOutCirt", clutter.EASE_IN_OUT_CIRC),
        ("easeInElastic", clutter.EASE_IN_ELASTIC),
        ("easeOutElasic", clutter.EASE_OUT_ELASTIC),
        ("easeInOutElastic", clutter.EASE_IN_OUT_ELASTIC),
        ("easeInBack", clutter.EASE_IN_BACK),
        ("easeOutBack", clutter.EASE_OUT_BACK),
        ("easeInOutBack", clutter.EASE_IN_OUT_BACK),
        ("easeInBounce", clutter.EASE_IN_BOUNCE),
        ("easeOutBounce", clutter.EASE_OUT_BOUNCE),
        ("easeInOutBunce", clutter.EASE_IN_OUT_BOUNCE),
]

def custom_alpha_func(alpha, data):
    import math
    tl = alpha.get_timeline()
    return math.sin(tl.get_progress() * math.pi)

CUSTOM_ALPHA = clutter.alpha_register_func(custom_alpha_func)
EASING_MODES.append(("custom sine", CUSTOM_ALPHA))


class EasingDemo(object):
    def __init__(self):
        self.current_mode = 0
        self.stage = clutter.Stage()
        self.stage.set_color(clutter.Color(0x88, 0x88, 0xdd, 0xff))

        self.rect = clutter.Rectangle()
        self.rect.set_color(clutter.Color(0xee, 0x33, 0, 0xff))
        self.rect.set_anchor_point_from_gravity(clutter.GRAVITY_CENTER)
        self.rect.set_size(50, 50)
        self.rect.set_position(self.stage.get_width()/2,
                               self.stage.get_height()/2)
        self.stage.add(self.rect)

        self.easing_mode_label = clutter.Text()
        self.stage.add(self.easing_mode_label)
        
        self.stage.connect('destroy', clutter.main_quit)
        self.stage.connect('button-press-event', self.on_button_press)
        self.stage.show()
        self.update_label()

    def update_label(self):
        text = "Current mode: %s" % EASING_MODES[self.current_mode][0]
        self.easing_mode_label.set_text('Current: %s' % text)

    def on_button_press(self, stage, event):
        if event.button == 3:
            self.current_mode += 1
            if self.current_mode >= len(EASING_MODES):
                self.current_mode = 0
            self.update_label()
        elif event.button == 1:
            self.rect.animate(EASING_MODES[self.current_mode][1], 500,
                              "x", event.x,
                              "y", event.y)


if __name__ == '__main__':
    # This gives us nice looking fonts ;)
    import cairo
    backend = clutter.backend_get_default()
    options = backend.get_font_options()
    options.set_hint_style(cairo.HINT_STYLE_FULL)
    options.set_antialias(cairo.ANTIALIAS_GRAY)
    backend.set_font_options(options)

    demo = EasingDemo()
    clutter.main()
