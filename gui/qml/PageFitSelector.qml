import QtQuick 1.0
import com.nokia.meego 1.0

SelectionDialog {
    id: pageFitSelector
    property Style platformStyle: SelectionDialogStyle {}
    property string pageFitMode : "original"
    titleText : "Page fit mode"
    onSelectedIndexChanged : {
        pageFitMode = model.get(selectedIndex).key
        accept()
    }
    model : ListModel {
        ListElement {
            name : "<b>1:1</b> - original size"
            key : "original"
        }
        ListElement {
            name : "<b>fit to width</b>"
            key : "width"
        }
        ListElement {
            name : "<b>fit to height</b>"
            key : "height"
        }
        ListElement {
            name : "<b>fit to screen</b>"
            key : "screen"
        }
        ListElement {
            name : "<b>custom</b> - remember scale"
            key : "custom"
        }
        ListElement {
            name : "<b>orientation</b> specific"
            key : "orient"
        }
        ListElement {
            name : "<b>show the most</b>"
            key : "most"
        }
    }
}

