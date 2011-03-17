import clutter
from clutter import cogl


class MultiTexture(clutter.Actor):
    __gtype_name__ = 'MultiTexture'
    def __init__(self):
        clutter.Actor.__init__(self)

        self.alpha_tex = self._load_texture('redhand_alpha.png')
        self.redhand_tex = self._load_texture('redhand.png')
        self.light_tex = self._load_texture('light0.png')

        self.material = cogl.Material()
        self.material.set_layer(0, self.alpha_tex)
        self.material.set_layer(1, self.redhand_tex)
        self.material.set_layer(2, self.light_tex)

        self.tex_matrix = cogl.Matrix()
        self.rot_matrix = cogl.Matrix()

        self.rot_matrix.translate(0.5, 0.5, 0)
        self.rot_matrix.rotate(10.0, 0, 0, 1.0)
        self.rot_matrix.translate(-0.5, -0.5, 0)

        width = self.redhand_tex.get_width()
        height = self.redhand_tex.get_height()
        self.set_size(width, height)
        self.connect('notify::rotation-angle-y', self.on_rotation_notify)

    def _load_texture(self, filename):
        return cogl.texture_new_from_file(filename,
               cogl.TEXTURE_NO_SLICING, cogl.PIXEL_FORMAT_ANY)

    def do_paint(self):
        tex_coords = (
                0,   0,   1,   1,
                0,   0,   1,   1,
                0,   0,   1,   1,
        )
        cogl.set_source(self.material)
        cogl.rectangle_with_multitexture_coords(0, 0, 200, 200, tex_coords)

    def on_rotation_notify(self, actor, pspec):
        angle = self.get_property('rotation-angle-y')
        self.tex_matrix.multiply(self.tex_matrix, self.rot_matrix)
        self.material.set_layer_matrix(2, self.tex_matrix)



if __name__ == '__main__':
    stage = clutter.Stage()
    stage.set_color(clutter.Color(0x61, 0x56, 0x56, 0xff))
    stage.connect('destroy', clutter.main_quit)

    multi_tex = MultiTexture()
    multi_tex.set_position(stage.get_width()/2 - multi_tex.get_width()/2,
                           stage.get_height()/2 - multi_tex.get_height()/2)
    stage.add(multi_tex)

    timeline = clutter.Timeline(5000)
    timeline.set_loop(True)
    alpha = clutter.Alpha(timeline, clutter.LINEAR)
    r_behave = clutter.BehaviourRotate(clutter.Y_AXIS, 0.0, 360.0, alpha=alpha)
    r_behave.set_center(multi_tex.get_width()/2, 0, 0)
    r_behave.apply(multi_tex)
    timeline.start()

    stage.show()
    clutter.main()

