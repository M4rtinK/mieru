import sys
import clutter

class HelloClutter:
    def __init__ (self, message):
        self.stage = clutter.Stage()
        self.stage.set_color(clutter.color_from_string('DarkSlateGrey'))
        self.stage.set_size(800, 600)
        self.stage.set_title('My First Clutter Application')
        self.stage.connect('key-press-event', clutter.main_quit)
        self.stage.connect('button-press-event',
                           self.on_button_press_event)

        color = clutter.Color(0xff, 0xcc, 0xcc, 0xdd)

        self.label = clutter.Text()
        self.label.set_font_name('Mono 32')
        self.label.set_text(message)
        self.label.set_color(color)
        (label_width, label_height) = self.label.get_size()
        label_x = self.stage.get_width() - label_width - 50
        label_y = self.stage.get_height() - label_height
        self.label.set_position(label_x, label_y)
        self.stage.add(self.label)

        self.cursor = clutter.Rectangle()
        self.cursor.set_color(color)
        self.cursor.set_size(20, label_height)
        cursor_x = self.stage.get_width() - 50
        cursor_y = self.stage.get_height() - label_height
        self.cursor.set_position(cursor_x, cursor_y)
        self.stage.add(self.cursor)

        self.timeline = clutter.Timeline(500)
        self.timeline.set_loop(True)
        alpha = clutter.Alpha(self.timeline, clutter.LINEAR)
        self.behaviour = clutter.BehaviourOpacity(0xdd, 0, alpha)
        self.behaviour.apply(self.cursor)

    def on_button_press_event (self, stage, event):
        print "mouse button %d pressed at (%d, %d)" % \
              (event.button, event.x, event.y)
    
    def run (self):
        self.stage.show_all()
        self.timeline.start()
        clutter.main()

def main (args):
    if args:
        message = args[0]
    else:
        message = 'Hello, Clutter!'

    app = HelloClutter(message)
    app.run()
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
