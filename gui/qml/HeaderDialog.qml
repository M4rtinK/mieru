//HeaderDialog.qml

import QtQuick 1.1
import com.nokia.meego 1.0

Dialog {
    id : headerDialog
    width : parent.width - 30
    property Style platformStyle: SelectionDialogStyle {}
    property string titleText: "Bitcoin address"
    title: Item {
        id: header
        height: headerDialog.platformStyle.titleBarHeight
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.top: parent.top
        anchors.bottom: parent.bottom
        Item {
            id: labelField
            anchors.fill:  parent
            Item {
                id: labelWrapper
                anchors.left: parent.left
                anchors.right: closeButton.left
                anchors.bottom:  parent.bottom
                anchors.bottomMargin: headerDialog.platformStyle.titleBarLineMargin
                height: titleLabel.height
                Label {
                    id: titleLabel
                    x: headerDialog.platformStyle.titleBarIndent
                    width: parent.width - closeButton.width
                    font: headerDialog.platformStyle.titleBarFont
                    color: headerDialog.platformStyle.commonLabelColor
                    elide: headerDialog.platformStyle.titleElideMode
                    text: headerDialog.titleText
                }
            }
            Image {
                id: closeButton
                anchors.verticalCenter : labelWrapper.verticalCenter
                anchors.right: labelField.right
                opacity: closeButtonArea.pressed ? 0.5 : 1.0
                source: "image://theme/icon-m-common-dialog-close"
                MouseArea {
                    id: closeButtonArea
                    anchors.fill: parent
                    onClicked:  {headerDialog.reject();}
                }
            }
        }
        Rectangle {
            id: headerLine
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.bottom:  header.bottom
            height: 1
            color: "#4D4D4D"
        }
    }
}