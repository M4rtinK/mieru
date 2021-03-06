//PageFitSelector.qml
import QtQuick 1.0
import UC 1.0

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
        id : modesModel
        // append list items here in place of single ListElements in order to support translation
        Component.onCompleted : {
            append({"name" : qsTr("<b>1:1</b> - original size"),     "key" : "original"})
            append({"name" : qsTr("<b>fit to width</b>"),            "key" : "width"})
            append({"name" : qsTr("<b>fit to height</b>"),           "key" : "height"})
            append({"name" : qsTr("<b>fit to screen</b>"),           "key" : "screen"})
            append({"name" : qsTr("<b>custom</b> - remember scale"), "key" : "custom"})
            append({"name" : qsTr("<b>orientation</b> specific"),    "key" : "orient"})
            append({"name" : qsTr("<b>show the most</b>"),           "key" : "most"})
        }
    }
    function addNop() {
        modesModel.insert(0, {"name" : qsTr("<b>no action</b>"),     "key" : "no action"})
    }
}
