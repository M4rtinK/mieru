//PayPalButton.qml

import QtQuick 1.1
import com.nokia.meego 1.0

Rectangle {
    id : ppButton
    color : ppMA.pressed ? "yellow" : "gold"
    smooth : true
    radius : 30
    width : 210
    height : 60
    property string url : ""

    Label {
        anchors.horizontalCenter : parent.horizontalCenter
        anchors.verticalCenter : parent.verticalCenter
        text : "<h2>PayPal</h2>"
    }
    MouseArea {
        id : ppMA
        anchors.fill : parent
        onClicked : {
            console.log('PayPal button clicked')
            rootWindow.notify(qsTr("Opening <b>PayPal</b> donation page, <b>thanks</b>!"))
            Qt.openUrlExternally(url)
        }
    }
}


