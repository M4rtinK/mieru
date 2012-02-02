Mieru

Mieru is a flexible manga and comix reader.

Feature overview:
* touch friendly interface combined with handy key shortcuts
* simple and intuitive interface layout
* kinetic scrolling
* all common formats (zip,rar,folder with images, ...) are supported
* resume last open + history
* automatic loading of next/previous chapters/volumes
* multiple page fitting modes
* powerful paging dialog
* easily accessible configuration options

Mieru@Maemo:
* since version 1.0
* uses Hildon widgets + Clutter page view
* uses native notifications
* portrait and autorotation support

Mieru@Harmattan (N9, N950):
* since version 2.0
* uses QML and Qt Components
* pinch zoom support
* improved Open-file dialog (based on Cacheme QML)

Note:
The mobile interface is currently the most advanced one - the desktop interface is currently very simple, but many features can still be accessed using key shortcuts.


Mieru + Qt/QML GUI

Dependencies:
Python 2.5+, Qt Components 1.0+, python-pyside.qtgui, python-pyside.qtdeclarative, python-magic, libmagic, rar and zip

Installing
* install all dependencies
* run mieru.py -u "harmattan"
* the -u parameter specifies the UI, "harmattan" is used due to the Harmattan GUI being the QML one


Mieru + GTK/Clutter GUI

Dependencies:
Python 2.5+, clutter, PyClutter, PyClutter-GTK, libmagic, rar and zip

Installing:
* install all dependencies
* run mieru.py
 * using the -u parameter, you can specifiy the UI, "pc" = desktop ui,  "hildon" = Maemo 5 UI

Package availability
* Harmattan(N9/50):
 * Apps for Meego (http://apps.formeego.com)
 * Ovi store (pending QA)