//LineText
import QtQuick 1.1
import com.nokia.meego 1.0

Item {
    id: lineTextMain

    height: lineText.height

    property alias text : lineText.text

    Rectangle {
        height : 2
        color : "black"
        anchors.left : parent.left
        anchors.right : lineText.left
        anchors.verticalCenter : lineText.verticalCenter
    }

    Label {
        id : lineText
        anchors.left : parent.left
    }

    
}