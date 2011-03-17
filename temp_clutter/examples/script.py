import sys
import clutter
from clutter import cogl

BUFFER = '''
[
  { "id" : "move-timeline",  "type" : "ClutterTimeline", "duration" : 2500 },
  { "id" : "scale-timeline", "type" : "ClutterTimeline", "duration" : 2000 },
  { "id" : "fade-timeline",  "type" : "ClutterTimeline", "duration" : 1500 },
  {
    "id" : "move-behaviour", "type" : "ClutterBehaviourPath",
    "alpha" : {
      "timeline" : "move-timeline",
      "mode" : "ease-out-sine"
    },
    "path" : "M 100 100 L 200 150"
  },
  {
    "id" : "scale-behaviour", "type" : "ClutterBehaviourScale",
    "x-scale-start" : 1.0, "x-scale-end" : 0.7,
    "y-scale-start" : 1.0, "y-scale-end" : 0.7,
    "alpha" : {
      "timeline" : "scale-timeline",
      "mode" : "ease-out-sine"
    }
  },
  {
    "id" : "fade-behaviour", "type" : "ClutterBehaviourOpacity",
    "opacity-start" : 255, "opacity-end" : 0,
    "alpha" : {
      "timeline" : "fade-timeline",
      "mode" : "ease-out-sine"
    }
  },
  {
    "id" : "main-stage",
    "type" : "ClutterStage",
    "color" : "#ffffff",
    "visible" : true,
    "reactive" : true,
    "signals" : [
      { "name" : "key-press-event", "handler" : "do_quit" },
      { "name" : "destroy", "handler" : "do_quit" }
    ],
    "children" : [
      {
        "id" : "red-button",
        "type" : "ClutterRectangle",
        "visible" : true,
        "reactive" : true,
        "color" : "#dd0000",
        "opacity" : 255,
        "x" : 100, "y" : 100, "width" : 300, "height" : 300,
        "rotation" : [
          { "z-axis" : [ 45.0, [ 200, 200 ] ] }
        ],
        "signals" : [
          { "name" : "button-press-event", "handler" : "do_press" }
        ],
        "behaviours" : [
          "move-behaviour",
          "scale-behaviour",
          "fade-behaviour"
        ]
      },
      {
        "id" : "custom-scriptable",
        "type" : "CustomScriptable",
        "visible" : true,
        "filename" : "redhand.png",
        "x" : 100,
        "y" : 100,
        "gravity" : "center",
        "clip-path" : "M 0 0 L 200 100 L 0 200 C 0 200 100 100 0 0 z",
      }
    ]
  }
]
'''


class CustomScriptable(clutter.Texture, clutter.Scriptable):
    __gtype_name__ = 'CustomScriptable'
    def __init__(self):
        clutter.Texture.__init__(self)
        self._path = None

    def do_parse_custom_node(self, script, name, node):
        print 'do_parse_custom_node', name, node
        # This method expects exactly one return value. The value must be
        # a simple type (int, float, string) or a gobject.GObject derived
        # type (or friends like GBoxed, GEnum, GFlags)
        # Return "None" to indicate that the node can't be handled
        if name == 'gravity':
            # Translate the gravity string into an enum. 
            if node == 'north-west':
                gravity = clutter.GRAVITY_NORTH_WEST
            elif node == 'north':
                gravity = clutter.GRAVITY_NORTH
            elif node == 'north-east':
                gravity = clutter.GRAVITY_NORTH_EAST
            elif node == 'west':
                gravity = clutter.GRAVITY_WEST
            elif node == 'center':
                gravity = clutter.GRAVITY_CENTER
            elif node == 'east':
                gravity = clutter.GRAVITY_EAST
            elif node == 'south-west':
                gravity = clutter.GRAVITY_SOUTH_WEST
            elif node == 'south':
                gravity = clutter.GRAVITY_SOUTH
            elif node == 'south-east':
                gravity = clutter.GRAVITY_SOUTH_EAST
            else:
                gravity = clutter.GRAVITY_NONE
            return gravity

        elif name == 'clip_path':
            path = clutter.Path(description=node)
            return path

        # Chain up
        return clutter.Texture.do_parse_custom_node(self, script, name, node)

    def do_set_custom_property(self, script, name, value):
        print 'do_set_custom_property', name, value
        # NOTE: This method does not expect a return value
        if name == 'gravity':
            # Set our custom property 'gravity'.
            self.set_anchor_point_from_gravity(value)
        elif name == 'clip_path':
            self._path = value
        else:
            # Chain up
            clutter.Texture.do_set_custom_property(self, script, name, value)

    def do_paint(self):
        if type(self._path) == clutter.Path:
            cogl.path_new()
            for node in self._path:
                if node.type == clutter.PATH_MOVE_TO:
                    cogl.path_move_to(*node[0])
                elif node.type == clutter.PATH_LINE_TO:
                    cogl.path_line_to(*node[0])
                elif node.type == clutter.PATH_CURVE_TO:
                    cogl.path_curve_to(node[0][0], node[0][1],
                                       node[1][0], node[1][1],
                                       node[2][0], node[2][1])
                elif node.type == clutter.PATH_CLOSE:
                    cogl.path_close()
            cogl.clip_push_from_path()
            clutter.Texture.do_paint(self)
            cogl.clip_pop()
        else:
            clutter.Texture.do_paint(self)

class TestScript:
    def __init__ (self, *args, **kwargs):
        self._score = clutter.Score()

    def do_quit (self, *args):
        print "quitting"
        clutter.main_quit()

    def do_timeline_start (self, score, timeline):
        print "timeline started: %s" % (clutter.get_script_id(timeline))

    def do_press (self, actor, event):
        print "running the score"
        self._score.connect('timeline-started', self.do_timeline_start)
        self._score.connect('completed', self.do_quit)
        self._score.start()

        return True

    def load_script (self):
        self._script = clutter.Script()
        try:
            self._script.load_from_data(BUFFER, -1)
            self._script.connect_signals(self)
        except Exception, exc:
            print "Unable to load buffer: %s" % (exc)
            sys.exit(1)

    def run (self):
        self.load_script()

        self._timelines = self._script.get_objects('move-timeline',
                                                   'scale-timeline',
                                                   'fade-timeline')
        for timeline in self._timelines:
            print "Timeline: %s" % (clutter.get_script_id (timeline))

        self._score.append(timeline=self._timelines[0])
        self._score.append(timeline=self._timelines[1], parent=self._timelines[0])
        self._score.append(timeline=self._timelines[2], parent=self._timelines[1])
        assert(3 == len(self._score.list_timelines()))

        self._stage = self._script.get_object('main-stage')
        self._stage.show_all()

        clutter.main()

        return 0

if __name__ == '__main__':
    test = TestScript()
    sys.exit(test.run())
