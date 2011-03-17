import gobject
import clutter

class SampleChildMeta(clutter.ChildMeta):
    """
    An example ChildMeta

    This is an example ChildMeta implementation with only one property.
    If 'allocate-hidden' is set True, the SampleBox container allocates
    the actor's space if it's hidden.
    """
    __gtype_name__ = 'SampleChildMeta'
    __gproperties__ = {
            'allocate-hidden': (gobject.TYPE_BOOLEAN, 'Allocate hidden',
                'Allocate space when hidden', True,
                gobject.PARAM_CONSTRUCT|gobject.PARAM_READWRITE),
    }
    def __init__(self):
        self._allocate_hidden = True

    def do_get_property(self, pspec):
        if pspec.name == 'allocate-hidden':
            return self._allocate_hidden

    def do_set_property(self, pspec, value):
        if pspec.name == 'allocate-hidden':
            self._allocate_hidden = value


class SampleBox(clutter.Actor, clutter.Container):
    """
    An example Box container.

    This is a very simple 'Box' container with a dynamic layout.
    """
    __gtype_name__ = 'SampleBox'
    __gproperties__ = {
            'orientation': (gobject.TYPE_INT, 'Orientation', 'Box orientation',
                0, 1, 0, gobject.PARAM_READWRITE),
    }
    HORIZONTAL = 0
    VERTICAL = 1
    def __init__(self, orientation=0):
        clutter.Actor.__init__(self)
        self._orientation = orientation
        self._children = []

    def set_orientation(self, orientation):
        self._orientation = orientation
        self.notify("orientation")
        self.queue_relayout()

    def get_orientation(self):
        return self._orientation

    def do_get_property(self, pspec):
        if pspec.name == 'orientation':
            return self.get_orientation()

    def do_set_property(self, pspec, value):
        if pspec.name == 'orientation':
            self.set_orientation(value)

    def do_add(self, *children):
        for child in children:
            if child in self._children:
                raise Exception("Actor %s is already a children of %s" % (
                    child, self))
            self._children.append(child)
            child.set_parent(self)
            self.queue_relayout()
    
    def do_remove(self, *children):
        for child in children:
            if child in self._children:
                self._children.remove(child)
                child.unparent()
                self.queue_relayout()
            else:
                raise Exception("Actor %s is not a child of %s" % (
                    child, self))

    def do_get_preferred_width(self, for_height):
        min_width = 0
        natural_width = 0
        for child in self._children:
            if not child.props.visible and not \
                    self.child_get_property(child, 'allocate-hidden'):
                continue
            child_min_width, child_natural_width = child.get_preferred_width(
                    for_height)
            if self._orientation == self.HORIZONTAL:
                min_width += child_min_width
                natural_width += child_natural_width
            else:
                min_width = max(min_width, child_min_width)
                natural_width = max(natural_width, child_natural_width)
        return (min_width, natural_width)

    def do_get_preferred_height(self, for_width):
        min_height = 0
        natural_height = 0
        for child in self._children:
            if not child.props.visible and not \
                    self.child_get_property(child, 'allocate-hidden'):
                continue
            child_min_height, child_natural_width = child.get_preferred_height(
                    for_width)
            if self._orientation == self.HORIZONTAL:
                min_height = max(min_height, child_min_height)
                natural_height = max(natural_height, child_natural_width)
            else:
                min_height += child_min_height
                natural_height += child_natural_width
        return (min_height, natural_height)


    def do_allocate(self, box, flags):
        child_x = child_y = 0
        for child in self._children:
            if not child.props.visible and not \
                    self.child_get_property(child, 'allocate-hidden'):
                continue
            w, h = child.get_preferred_size()[2:]
            child_box = clutter.ActorBox()
            child_box.x1 = child_x
            child_box.y1 = child_y
            child_box.x2 = child_box.x1 + w
            child_box.y2 = child_box.y1 + h
            child.allocate(child_box, flags)
            if self._orientation == self.HORIZONTAL:
                child_x += w
            else:
                child_y += h
        clutter.Actor.do_allocate(self, box, flags)

    def do_foreach(self, func, data=None):
        for child in self._children:
            func(child, data)
        
    def do_paint(self):
        for actor in self._children:
            actor.paint()

    def do_pick(self, color):
        clutter.Actor.do_pick(self, color)
        for actor in self._children:
            actor.paint()

SampleBox.install_child_meta(SampleChildMeta)


if __name__ == '__main__':
    def on_button_press(box, event):
        box.props.orientation = not box.props.orientation
        return True

    def on_child_button_pressed(actor, event):
        print 'Rectangle with color %s pressed' % actor.get_color()

    def on_key_press(stage, event, box):
        from clutter import keysyms
        if event.keyval == keysyms.h:
            for child in box:
                do_allocate = box.child_get_property(child,
                        'allocate-hidden')
                box.child_set_property(child, 'allocate-hidden',
                        not do_allocate)
            box.queue_relayout()

    import random
    stage = clutter.Stage()
    stage.connect('destroy', clutter.main_quit)

    box = SampleBox()
    for i in range(10):
        rect = clutter.Rectangle()
        color = clutter.Color(random.randint(0, 255), random.randint(0, 255),
                random.randint(0, 255), 255)
        rect.set_color(color)
        rect.set_size(50, 50)
        rect.set_reactive(True)
        rect.connect('button-press-event', on_child_button_pressed)
        box.add(rect)
        box.child_set_property(rect, 'allocate-hidden', False)
        if i % 2:
            rect.hide()

    stage.add(box)
    box.set_reactive(True)

    info = clutter.Text()
    info.set_text("Press 'h' to allocate hidden actors.\n" +
            "Click the container actor to change it's orientation.")
    stage.add(info)
    info.set_y(stage.get_height() - info.get_height() - 10)

    box.connect('button-press-event', on_button_press)
    stage.connect('key-press-event', on_key_press, box)

    stage.show()
    clutter.main()
