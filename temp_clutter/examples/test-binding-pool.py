import gobject
import clutter
from clutter import cogl, keysyms


class KeyGroup(clutter.Group):
    __gtype_name__ = 'KeyGroup'
    __gsignals__ = {
            "activate": (gobject.SIGNAL_RUN_LAST, None, (clutter.Actor, )),
    }
    def __init__(self):
        clutter.Group.__init__(self)
        self.selected_index = 0

        self.pool = clutter.binding_pool_get_for_class(KeyGroup)
        self.pool.install_action('move-right', keysyms.Right, None,
                self.action_move_right)
        self.pool.install_action('move-left', keysyms.Left, None,
                self.action_move_left)
        self.pool.install_action('activate', keysyms.KP_Enter, None,
                self.action_activate)
        self.pool.install_action('activate', keysyms.Return, None,
                self.action_activate)

        self.connect('key-press-event', self.on_key_press)

    def action_move_left(self, group, action_name, key_val, modifiers):
        print "activated '%s' (k:%d, m: %d)" % (action_name, key_val, modifiers)
        self.selected_index -= 1
        if self.selected_index < 0:
            self.selected_index = self.get_n_children()
        return True

    def action_move_right(self, group, action_name, key_val, modifiers):
        print "activated '%s' (k:%d, m: %d)" % (action_name, key_val, modifiers)
        self.selected_index += 1
        if self.selected_index >= self.get_n_children():
            self.selected_index = 0
        return True

    def action_activate(self, group, action_name, key_val, modifiers):
        print "activated '%s' (k:%d, m: %d)" % (action_name, key_val, modifiers)
        if self.selected_index == -1:
            return False
        child = self.get_nth_child(self.selected_index)
        if child:
            self.emit("activate", child)
            return True
        return False

    def on_key_press(self, actor, event):
        res = self.pool.activate(event.keyval, event.modifier_state, actor)
        if res:
            actor.queue_redraw()
        return res
    
    def do_paint(self):
        children = self.get_children()
        for child in children:
            if children.index(child) == self.selected_index:
                box = clutter.ActorBox(*child.get_allocation_box())
                box.x1 -= 2
                box.y1 -= 2
                box.x2 += 2
                box.y2 += 2
                cogl.set_source_color4ub(255, 255, 0, 224)
                cogl.rectangle(box.x1, box.y1, box.x2, box.y2)
            child.paint()


def on_key_group_activate (key_group, child):
    print "Child %s activated!" % child

if __name__ == '__main__':
    stage = clutter.Stage()
    stage.connect('destroy', clutter.main_quit)

    key_group = KeyGroup()
    stage.add(key_group)

    rect = clutter.Rectangle(clutter.color_from_string('red'))
    rect.set_size(50, 50)
    rect.set_position(0, 0)
    key_group.add(rect)

    rect = clutter.Rectangle(clutter.color_from_string('green'))
    rect.set_size(50, 50)
    rect.set_position(75, 0)
    key_group.add(rect)

    rect = clutter.Rectangle(clutter.color_from_string('blue'))
    rect.set_size(50, 50)
    rect.set_position(150, 0)
    key_group.add(rect)

    key_group.set_position(stage.get_width()/2 - key_group.get_width()/2,
                           stage.get_height()/2 - key_group.get_height()/2)
    key_group.set_reactive(True)
    key_group.connect('activate', on_key_group_activate)
    stage.set_key_focus(key_group)

    stage.show()
    clutter.main()
