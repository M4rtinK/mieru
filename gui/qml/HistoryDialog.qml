//HistoryDialog.qml
//import Qt 4.7
import QtQuick 1.1
import com.nokia.meego 1.0

Page {
    tools: ToolBarLayout {
        ToolIcon { iconId: "toolbar-back"
            onClicked: pageStack.pop()
        }
    }
    ListView {
        id: pythonList
        anchors.fill : parent
        //width: 400
        //height: 200


        model: pythonListModel

        delegate: Component {
            Rectangle {
                width: pythonList.width
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
                        controller.thingSelected(model.thing)
                    }
                }
            }
        }
    }
}