//OptionsPage.qml
//import Qt 4.7
import QtQuick 1.1
import com.nokia.meego 1.0

Page {
    tools: ToolBarLayout {
        ToolIcon { iconId: "toolbar-back"
            onClicked: pageStack.pop()
        }
        ButtonRow {
            platformStyle: TabButtonStyle { }
            TabButton {
                text: "Info"
                tab: tab1
            }
            TabButton {
                text: "Stats"
                tab: tab2
            }
            TabButton {
                text: "About"
                tab: tab3
            }
        }
           }
    TabGroup {
        id: tabGroup

        currentTab: tab1

        Page {
           id: tab1
           Column {
               spacing: 10

               Text {
                   text: "Info"
               }
           }
        }
        Page {
            id: tab2
            anchors.fill : parent
            //anchors.verticalCenter : parent.verticalCenter
            anchors.topMargin : 30
            anchors.bottomMargin : 30
            anchors.leftMargin : 30
            anchors.rightMargin : 30
            Text {
               anchors.left : parent.left
               id : statsHeadline
               text : "<b>Usage Statistics</b>"
               font.pointSize: 24
            }
            Switch {
                id : statsSwitch
                anchors.left : statsHeadline.right
                anchors.leftMargin : 30
                checked : stats.enabled
                onCheckedChanged : {
                    // enable/disable stats and update statsText
                    stats.enabled = checked
                    statsText.text = stats.statsText
                }
            }
            Text {
                id : statsText
                anchors.top : statsHeadline.bottom
                anchors.topMargin : 20
                text: stats.statsText
                font.pointSize: 24
            }

            /*LabeledSwitch {
              text : checked ? "Stats enabled" : "Stats disabled"
            }*/
        }

        Page {
            id: tab3
            Column {
                spacing: 10

                Text {
                    text: "About"
               }
           }
        }
    }
}
