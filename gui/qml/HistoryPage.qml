//HistoryDialog.qml
//import Qt 4.7
import QtQuick 1.1
import com.nokia.meego 1.0

Page {
    id : historyPage
    property bool showDeleteIcon : false
    tools: ToolBarLayout {
        ToolIcon { iconId: "toolbar-back"
            onClicked: pageStack.pop()
        }
        ToolIcon { iconId: "toolbar-view-menu"
            onClicked: historyMenu.open()
        }
    }

    Menu {
        id : historyMenu

        MenuLayout {
            MenuItem {
              text : "Show delete icon"
              onClicked : {
                  historyPage.showDeleteIcon = !historyPage.showDeleteIcon
            }
        }
            MenuItem {
                text : "Erase history"
                onClicked : {
                    console.log("erase history")
                    }
            }
        }
    }

    ListView {
        id: historyList
        anchors.fill : parent
        //width: 400
        //height: 200


        model: historyListModel

        delegate: Component {
            Rectangle {
                width: historyList.width
                height: 80
                color: ((index % 2 == 0)?"#222":"#111")
                Label {
                    id: title
                    elide: Text.ElideRight
                    text: model.thing.name
                    color: "white"
                    font.bold: true
                    anchors.leftMargin: 10
                    anchors.fill: parent
                    verticalAlignment: Text.AlignVCenter
                }
                MouseArea {
                    anchors.fill: parent
                    onClicked: { 
                        pageStack.pop()
                        historyListController.thingSelected(model.thing)                        
                    }
                }
                ToolIcon {
                    iconId: "toolbar-delete"
                    height : 80
                    anchors.right : parent.right
                    visible : historyPage.showDeleteIcon
                    onClicked : console.log("delete item")
                }
            }
        }
    }
}