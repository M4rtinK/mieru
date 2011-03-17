import sys
sys.path.append('/home/user/software/clutter/clutter_1.0/lib/python2.5/site-packages')
import clutter

is_expanded = False

def on_animation_complete(animation, actor):
    global is_expanded
    is_expanded = not is_expanded
    actor.set_reactive(True)
    print "Animation complete"

def on_button_press(actor, event):
    old_x, old_y = actor.get_position()
    old_width, old_height = actor.get_size()

    if not is_expanded:
        new_x = old_x - 100
        new_y = old_y - 100
        new_width = old_width + 200
        new_height = old_height + 200
        new_angle = 360
        new_color = clutter.Color(0xdd, 0x44, 0xdd, 0xff)
    else:
        new_x = old_x + 100
        new_y = old_y + 100
        new_width = old_width - 200
        new_height = old_height - 200
        new_angle = 0
        new_color = clutter.Color(0x44, 0xdd, 0x44, 0x88)

    vertex = clutter.Vertex(new_width/2, new_height/2, 0)
    animation = actor.animate(clutter.EASE_IN_EXPO, 2000,
                              "x", new_x,
                              "y", new_y,
                              "width", new_width,
                              "height", new_height,
                              "color", new_color,
                              "rotation-angle-z", new_angle,
                              "fixed::rotation-center-z", vertex,
                              "fixed::reactive", False)
    animation.connect('completed', on_animation_complete, actor)

def main(args):
    stage = clutter.Stage()
    stage.connect('destroy', clutter.main_quit)
    stage.set_color(clutter.Color(0x66, 0x66, 0xdd, 0xff))

    rect = clutter.Rectangle(clutter.Color(0x44, 0xdd, 0x44, 0xff))
    rect.set_size(50, 50)
    rect.set_anchor_point(25, 25)
    rect.set_position(stage.get_width()/2, stage.get_height()/2)
    rect.set_opacity(0x88)
    rect.set_reactive(True)
    rect.connect('button-press-event', on_button_press)
    stage.add(rect)

    stage.show()
    clutter.main()

if __name__ == '__main__':
    import sys
    main(sys.argv[1:])
