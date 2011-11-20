//LabeledSwitch
import QtQuick 1.1
import com.nokia.meego 1.0

Row {
    id: rowRow
    spacing: 10
    anchors.fill: parent

    property alias text : switchText.text
    property alias checked : switchComponent.checked

    Text {
        id : switchText
        //width : rowRow.width - rowRow.spacing - switchComponent.width
        //height : switchComponent.height
        //verticalAlignment : Text.AlignVCenter
        text : switchComponent.checked ? "Switched on" : "Switched off"
        //font.pixelSize : platformStyle.fontSizeMedium
        font.pointSize : 24
        //color : platformStyle.colorNormalLight
    }

    Switch {
        id: switchComponent

    }
}