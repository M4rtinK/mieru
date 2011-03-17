#!/usr/bin/python

import sys
import clutter

print clutter.__version__

def actor_foreach (actor, data):
    print 'Actor: ', actor

def on_stage_add (group, element):
    print 'Adding element: ', element

def on_button_press_event (stage, event):
    print str(event)
    stage.foreach(actor_foreach, 'hello')
    clutter.main_quit()

def main (args):
    stage = clutter.Stage()
    stage.set_size(800,600)
    stage.set_color(clutter.color_from_string('DarkSlateGray'))
    stage.connect('actor-added', on_stage_add)
    stage.connect('button-press-event', on_button_press_event)
    
    print "stage color: %s" % (stage.get_color())
   
    color = clutter.Color(0x35, 0x99, 0x2a, 0x66)
    border_color = color.lighten()
    rect = None
    for i in range(1, 10):
        rect = clutter.Rectangle()
        rect.set_position((800 - (80 * i)) / 2, (600 - (60 * i)) / 2)
        rect.set_size(80 * i, 60 * i)

        # colors are either clutter.Color or 4-tuples
        if i % 2 == 0:
            rect.set_color(color)
        else:
            rect.set_color((0x35, 0x99, 0x2a, 0x33))
        
        rect.set_border_width(10)
        rect.set_border_color(border_color)

        stage.add(rect)
        rect.show()

    stage.show()
    clutter.main()

    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
