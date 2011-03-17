import sys
import sys
sys.path.append('/home/user/software/clutter/clutter_1.0/lib/python2.5/site-packages')
import clutter

class BehaviourRotate (clutter.Behaviour):
    __gtype_name__ = 'BehaviourRotate'
    def __init__ (self, alpha=None):
        clutter.Behaviour.__init__(self)
        self.set_alpha(alpha)
        self.angle_start = 0.0
        self.angle_end = 359.0

    def do_alpha_notify (self, alpha_value):
        angle = alpha_value * (self.angle_end - self.angle_start)

        for actor in self.get_actors():
            actor.set_rotation(clutter.Z_AXIS, angle,
                               actor.get_x() - 100,
                               actor.get_y() - 100,
                               0)


def main (args):
    stage = clutter.Stage()
    stage.set_size(800, 600)
    stage.set_color(clutter.Color(0xcc, 0xcc, 0xcc, 0xff))
    stage.connect('key-press-event', clutter.main_quit)
    stage.connect('destroy', clutter.main_quit)

    rect = clutter.Rectangle()
    rect.set_position(0, 0)
    rect.set_size(150, 150)
    rect.set_color(clutter.Color(0x33, 0x22, 0x22, 0xff))
    rect.set_border_color(clutter.color_from_string('white'))
    rect.set_border_width(15)
    rect.show()

    knots = ( \
            (   0,   0 ),   \
            ( 300,   0 ),   \
            ( 300, 300 ),   \
            (   0, 300 ),   \
    )

    path = clutter.Path('M 0 0 L 300 0 L 300 300 L 0 300')

    timeline = clutter.Timeline(3000)
    timeline.set_loop(True)
    alpha = clutter.Alpha(timeline, clutter.EASE_OUT_SINE)

    o_behaviour = clutter.BehaviourOpacity(alpha=alpha, opacity_start=0x33, opacity_end=255)
    o_behaviour.apply(rect)

    p_behaviour = clutter.BehaviourPath(alpha, path)
    path.add_move_to(0, 0)
    p_behaviour.apply(rect)

    r_behaviour = BehaviourRotate(alpha)
    r_behaviour.apply(rect)

    stage.add(rect)
    stage.show()

    timeline.start()

    clutter.main()
    
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
