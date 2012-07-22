# -*- coding: utf-8 -*-

# [SNIPPET_NAME: How to load a pixbuf in a clutter.Texture]
# [SNIPPET_CATEGORIES: Clutter]
# [SNIPPET_DESCRIPTION: Shows how load a pixbuf from gtk into a clutter.Texture. This example is useful when you are working with an embeded clutter stage.]
# [SNIPPET_AUTHOR: Manuel de la Pena <mandel@themacaque.com>]
# [SNIPPET_DOCS: http://www.themacaque.com/wiki/doku.php?id=clutter:texture_from_pixbuf]
# [SNIPPET_LICENSE: GPL]
import sys
import clutter
from gtk import gdk

class PixbufTexture(clutter.Texture):
    """
    Represents a texture that loads its data from a pixbuf.
    """
    __gtype_name__ = 'PixbufTexture'

    def __init__(self, width, height, pixbuf):
        """
        @type width: int
        @param width: The width to be used for the texture.
        @type height: int
        @param height: The height to be used for the texture.
        @type pixbuf: gdk.pixbuf
        @param pixbuf: A pixbuf from an other widget.
        """
        super(PixbufTexture, self).__init__()
        self.set_width(width)
        self.set_height(height)
        # do we have an alpha value?
        if pixbuf.props.has_alpha:
            bpp = 4
        else:
            bpp = 3

        self.set_from_rgb_data(
            pixbuf.get_pixels(),
            pixbuf.props.has_alpha,
            pixbuf.props.width,
            pixbuf.props.height,
            pixbuf.props.rowstride,
            bpp, 0)
if __name__ == '__main__':
    if len(sys.argv) > 1:
        pixbuf = gdk.pixbuf_new_from_file(sys.argv[1])
        texture = PixbufTexture(300,300, pixbuf)
        stage = clutter.Stage()
        stage.add(texture   )
        stage.set_size(500, 500)
        stage.set_color(clutter.color_from_string("#000"))
        stage.show_all()
        stage.connect('destroy', clutter.main_quit)
        clutter.main()
    else:
        print("Provide the full path to the image to load")

# execute the script providing the full path to the image to load
# example:
# python clutterpixbuftexture.py /home/mandel/Projects/python-snippets/pixbuftexture/clutter/jono.png
