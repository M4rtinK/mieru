//HistoryDialog.qml
//import Qt 4.7
import QtQuick 1.1
import com.nokia.meego 1.0

Page {
    id : historyPage
    property bool deleteModeEnabled : false

    // update the history list model at startup
    Component.onCompleted : readingState.updateHistoryListModel()

    tools: ToolBarLayout {
        ToolIcon {
            id : histBack
            iconId : "toolbar-back"
            onClicked : pageStack.pop()
        }
        ToolButton {
            width : 120
            text : "Delete"
            visible : deleteModeEnabled
            anchors.verticalCenter : parent.verticalCenter
            onClicked: {
                historyListModel.removeChecked()
                historyPage.deleteModeEnabled = false
                readingState.updateHistoryListModel()
                
            }
        }
        ToolButton {
            width : 120
            text: "Cancel"
            visible : deleteModeEnabled
            anchors.verticalCenter : parent.verticalCenter
            onClicked: historyPage.deleteModeEnabled = false
        }
        ToolIcon {
            id : histMenu
            iconId : "toolbar-view-menu"
            onClicked : historyMenu.open()
        }
    }

    Menu {
        id : historyMenu

        MenuLayout {
            MenuItem {
              text : historyPage.deleteModeEnabled ? "Don't delete items" : "Delete items"
              onClicked : {
                  historyPage.deleteModeEnabled = !historyPage.deleteModeEnabled
                  rootWindow.notify("Select items to delete")
            }
        }
            MenuItem {
                text : "Erase history"
                onClicked : {
                    eraseHistoryDialog.open()
                    }
            }
        }
    }

    ListView {
        id: historyList
        anchors.fill : parent
        Label {
            visible : (historyList.count == 0) ? true : false
            text : "<b>The history list is empty</b>"
            horizontalAlignment : Text.AlignHCenter
            anchors.verticalCenter : historyList.verticalCenter
            width : parent.width
            height : 80
            }



        model: historyListModel

        delegate: Component {
            Rectangle {
                width: historyList.width
                height: 80
                color: model.thing.checked?"#00B8F5":(index%2?"#eee":"#ddd")
                Label {
                    id: title
                    elide: Text.ElideRight
                    text: model.thing.name
                    //color: "white"
                    color: (model.thing.checked?"white":"black")
                    font.bold: true
                    anchors.leftMargin: 10
                    anchors.fill: parent
                    verticalAlignment: Text.AlignVCenter
                }
                MouseArea {
                    anchors.fill: parent
                    onClicked: {
                        if (historyPage.deleteModeEnabled) {
                            historyListController.toggled(historyListModel, model.thing)
                        }
                        else {
                            pageStack.pop()
                            historyListController.thingSelected(model.thing)
                        }
                    }
                }
            }
        }
    }
    QueryDialog {
        id : eraseHistoryDialog
        titleText : "Erase history ?"
        message : "Do you want to erase the history of all mangas and comic books opened by Mieru ?"
        acceptButtonText : "erase"
        rejectButtonText : "cancel"
        onAccepted : {
            readingState.eraseHistory()
            readingState.updateHistoryListModel()
        }
    }
}