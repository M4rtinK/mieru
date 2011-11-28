//OptionPage.qml
//import Qt 4.7
import QtQuick 1.1
import com.nokia.meego 1.0

Page {
    id : optionsPage
    anchors.fill : parent
    //anchors.verticalCenter : parent.verticalCenter
    anchors.topMargin : 15
    anchors.bottomMargin : 15
    anchors.leftMargin : 15
    anchors.rightMargin : 15
    Flickable {
        anchors.fill : parent
        contentWidth: optionsPage.width
        contentHeight: optionsColumn.height
        Column {
            id : optionsColumn
            spacing : 10
            Label { text : "options page"
            }
            LineText {
                text : "Page scaling"
                width : optionsPage.width
            }
            Rectangle {
                width : optionsPage.width
                height : 2
                color : "black"
            }
            SwitchWithText {
                text : "Remeber scale"
                width : optionsPage.width
                checked : mainView.rememberScale
                onCheckedChanged : {
                    mainView.rememberScale = checked
                    options.set("QMLRememberScale", checked)
                }
            }
        }
    }

    tools: ToolBarLayout {
               ToolIcon { iconId: "toolbar-back"
                  onClicked: pageStack.pop()
                  }
               }
    }