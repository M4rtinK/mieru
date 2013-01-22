//whatsNewDialog.qml

import QtQuick 1.1
import com.nokia.meego 1.0

HeaderDialog {
    id : whatsNewDialog
    titleText : "What's new in Mieru " + readingState.getNumericVersionString()
    property string releaseNotesText : ""
    content:Item {
        id: dialogContent
        height : rootWindow.inPortrait ? rootWindow.width * 0.90 : rootWindow.height * 0.85
        anchors.left : parent.left
        anchors.right : parent.right
        Flickable {
            id : notesFlickable
            anchors.top : parent.top
            anchors.topMargin : 8
            width : parent.width
            anchors.bottom : lowerBlock.top
            anchors.bottomMargin : 8
            clip : true
            contentHeight : releaseNotes.height
            contentWidth : parent.width
            interactive : releaseNotes.height > height
            Label {
                id : releaseNotes
                anchors.left : parent.left
                anchors.leftMargin : 4
                width : parent.width-12
                text : releaseNotesText
                wrapMode : Text.WordWrap
                color : "white"
                onLinkActivated : {
                    rootWindow.notify(qsTr("Opening link"))
                    Qt.openUrlExternally(link)
                }
            }
        }
        ScrollDecorator {
            flickableItem: notesFlickable
        }
        Item {
            id : lowerBlock
            height : childrenRect.height
            anchors.left : parent.left
            anchors.right : parent.right
            anchors.bottom : parent.bottom
            anchors.horizontalCenter : parent.horizontalCenter
            Rectangle {
                id: line
                color : "#4D4D4D"
                height : 1
                anchors {
                    left: parent.left
                    right : parent.right
                    bottom : donationLabel.top
                    bottomMargin : 8
                }
            }
            Label {
                id : donationLabel
                anchors.bottom : donationButton.top
                anchors.bottomMargin : 16
                anchors.horizontalCenter : parent.horizontalCenter
                text : qsTr("<b>Do you like Mieru ? Donate !</b>")
                color : "white"
            }
            Button {
                id : donationButton
                anchors.bottom : hideButton.top
                anchors.bottomMargin : 24
                anchors.horizontalCenter : parent.horizontalCenter
                text : qsTr("How to donate ?")
                onClicked : {
                    whatsNewDialog.close()
                    donationDialog.open()
                }
            }
            Button {
                id : hideButton
                //anchors.top : donationButton.bottom
                anchors.bottom : parent.bottom
                anchors.horizontalCenter : parent.horizontalCenter
                text : qsTr("Don't show again")
                onClicked : {
                    whatsNewDialog.close()
                    readingState.disableReleaseNotesForCurrentVersion()
                }
            }
        }
    }
    DonationDialog {
        id : donationDialog
    }
}