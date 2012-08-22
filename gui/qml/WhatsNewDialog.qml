//whatsNewDialog.qml

import QtQuick 1.1
import com.nokia.meego 1.0

HeaderDialog {
    id : whatsNewDialog
    titleText : "What's new in Mieru " + readingState.getNumericVersionString()
    content:Item {
        id: dialogContent
        height : rootWindow.inPortrait ? rootWindow.width * 0.8 : rootWindow.height * 0.8
        anchors.left : parent.left
        anchors.right : parent.right

        Flickable {
            id : notesFlickable
            anchors.top : parent.top
            anchors.topMargin : 16
            width : parent.width
            anchors.bottom : donationLabel.top
            clip : true
            contentHeight : releaseNotes.height
            contentWidth : releaseNotes.width
            interactive : releaseNotes.height > height
            Label {
                id : releaseNotes
                anchors.left : parent.left
                anchors.leftMargin : 16
                text : readingState.getReleaseNotes()
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
        Label {
            id : donationLabel
            anchors.bottom : donationButton.top
            anchors.horizontalCenter : parent.horizontalCenter
            text : qsTr("<b>Do you like Mieru ? Donate !</b>")
            color : "white"
        }
        Button {
            id : donationButton
            anchors.bottom : hideButton.top
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
    DonationDialog {
        id : donationDialog
    }
}