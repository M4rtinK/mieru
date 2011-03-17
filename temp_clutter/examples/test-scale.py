import sys
import clutter

class TestScale:
    def __init__ (self, *args, **kwargs):
        self._stage = clutter.Stage()
        self._stage.set_color(clutter.Color(0, 0, 0, 255))
        self._stage.set_size(300, 300)
        self._stage.connect('key-press-event', clutter.main_quit)

        rect = clutter.Rectangle()
        rect.set_color(clutter.Color(255, 255, 255, 0x99))
        rect.set_size(100, 100)
        rect.set_position(100, 100)
        self._stage.add(rect)

        rect = clutter.Rectangle()
        rect.set_color(clutter.Color(255, 255, 255, 255))
        rect.move_anchor_point_from_gravity(clutter.GRAVITY_CENTER)
        rect.set_size(100, 100)
        rect.set_position(100, 100)
        self._stage.add(rect)
        self._gravity = clutter.GRAVITY_NORTH_WEST
        self._rect = rect

        self._timeline = clutter.Timeline(duration=500)
        self._timeline.set_loop(True)
        self._timeline.connect('completed', self.on_timeline_completed, self)

        alpha = clutter.Alpha(self._timeline, clutter.LINEAR)

        self._behave = clutter.BehaviourScale(0.0, 0.0,
                                              1.0, 1.0,
                                              alpha=alpha)
        self._behave.apply(rect)

        self._stage.show_all()

    def on_timeline_completed (timeline, frame_num, self):
        self._gravity += 1

        if self._gravity > clutter.GRAVITY_CENTER:
            self._gravity = clutter.GRAVITY_NONE

        self._rect.move_anchor_point_from_gravity(self._gravity)

    def run (self):
        self._timeline.start()
        clutter.main()

if __name__ == '__main__':
    test = TestScale()
    test.run()
    sys.exit(0)

