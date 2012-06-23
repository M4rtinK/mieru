//PageFitSelector.qml
import Qt 4.7
import QtQuick 1.0
import com.nokia.meego 1.0

SelectionDialog {
    id: pageFitSelector
    property Style platformStyle: SelectionDialogStyle {}
    property string pageFitMode : "original"
    titleText : qsTr("Page fit mode")
    onSelectedIndexChanged : {
        pageFitMode = model.get(selectedIndex).key
        accept()
    }
    model : ListModel {
        // qsTr() does not work for properties...
        ListElement {
            name : QT_TR_NOOP("<b>1:1</b> - original size")
            key : "original"
        }
        ListElement {
            name : QT_TR_NOOP("<b>fit to width</b>")
            key : "width"
        }
        ListElement {
            name : QT_TR_NOOP("<b>fit to height</b>")
            key : "height"
        }
        ListElement {
            name : QT_TR_NOOP("<b>fit to screen</b>")
            key : "screen"
        }
        ListElement {
            name : QT_TR_NOOP("<b>custom</b> - remember scale")
            key : "custom"
        }
        ListElement {
            name : QT_TR_NOOP("<b>orientation</b> specific")
            key : "orient"
        }
        ListElement {
            name : QT_TR_NOOP("<b>show the most</b>")
            key : "most"
        }
    }
}
