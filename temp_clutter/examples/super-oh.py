import sys
sys.path.append('/home/user/software/clutter/clutter_1.0/lib/python2.5/site-packages')
import sys
import clutter
import gtk
import math

class SuperOh (clutter.Group) :
    def __init__ (self, nhands=6):
        clutter.Group.__init__(self)

        self.n_hands = nhands
        self.timeline = clutter.Timeline(5000)

        self.timeline.set_loop(True)
        self.timeline.connect('new-frame', self.on_new_frame)

        def sine_wave (alpha):
            return math.sin(alpha.get_timeline().get_progress() * math.pi)

        self.alpha = clutter.Alpha(self.timeline)
        self.alpha.set_func(sine_wave)

        self.scalers = []
        self.scalers.append(clutter.BehaviourScale(0.5, 0.5, 1.0, 1.0, self.alpha))
        self.scalers.append(clutter.BehaviourScale(1.0, 1.0, 0.5, 0.5, self.alpha))

        self.stage = clutter.Stage(default=True)
        self.stage.set_size(1024, 768)
        self.stage.connect('button-press-event', self.on_button_press)
        self.stage.connect('key-press-event', self.on_key_press)

        self.create_hands()

    def _sine_alpha(self, alpha, foo):
        print "self: %s, alpha: %s, foo: %s" % (self, alpha, foo)
        timeline = alpha.get_timeline()
        progress = timeline.get_progress()
        return math.sin(progress * math.pi)

    def create_hands(self):
        try:
            redhand = clutter.Texture(filename="manga.jpg")
        except Exception:
            print "Unable to load redhand.png"
            sys.exit(1)

        (w, h) = redhand.get_size()

        for i in range(self.n_hands):
            if i == 0:
                hand = redhand
            else:
                hand = clutter.Clone(redhand);

            radius = self.get_radius()
            x = self.stage.get_width() / 2 + radius * math.cos(i * math.pi / (self.n_hands / 2)) - w / 2

            y = self.stage.get_height() / 2 + radius * math.sin (i * math.pi / (self.n_hands / 2)) - h / 2

            hand.set_position (int(x), int(y))

            hand.move_anchor_point_from_gravity(clutter.GRAVITY_CENTER)
            if i % 2:
                self.scalers[0].apply(hand)
            else:
                self.scalers[1].apply(hand)

            hand.show()
            self.add(hand);

    def spin (self):
        self.timeline.start()

    def get_radius (self):
        return (self.stage.get_width () + self.stage.get_height ()) / self.n_hands

    def on_new_frame (self, tl, msecs):
        progress = tl.get_progress()
        self.set_rotation (clutter.Z_AXIS,
                           progress * 360,
                           self.stage.get_width() / 2,
                           self.stage.get_height () / 2,
                           0)
      
        angle = progress * 360

        for i in range(self.n_hands):
            hand = self.get_nth_child(i)
            hand.set_rotation(clutter.Z_AXIS,
                              angle * -6.0,
                              0, 0, 0)

    def on_button_press (self, stage, event):
        if event.button != 1:
            return False

        hand = stage.get_actor_at_pos(clutter.PICK_ALL,
                                      int(event.x),
                                      int(event.y))
        if type(hand) is clutter.Texture or type(hand) is clutter.Clone:
            hand.hide()

        return True

    def on_key_press (self, stage, event):
        if event.keyval == clutter.keysyms.q:
            clutter.main_quit()
            return True

        if event.keyval == clutter.keysyms.r:
            for hand in self:
                hand.show()
            return True

        return False

def main (args):
    stage = clutter.Stage(default=True)
    stage.set_color('#ccccccff')

    hands = SuperOh(8)
    stage.add(hands)
    hands.spin()

    stage.show_all()

    clutter.main()

    return 0
    
if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
