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
            anchors.fill : parent
            //anchors.verticalCenter : parent.verticalCenter
            anchors.topMargin : 30
            anchors.bottomMargin : 30
            anchors.leftMargin : 30
            anchors.rightMargin : 30
            Column {                         
                Label {
                    text: "Info"
                    //font.pointSize: 24
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
                anchors.leftMargin : 35
                checked : stats.enabled
                onCheckedChanged : {
                    // enable/disable stats and update statsText
                    stats.enabled = statsSwitch.checked
                    statsText.text = stats.statsText
                }
            }
            Text {
                id : statsText
                anchors.top : statsHeadline.bottom
                anchors.topMargin : 10
                text: stats.statsText
                font.pointSize: 24
            }

            Button {
                anchors.top : statsText.bottom
                anchors.topMargin : 50
                text : "Reset"
                onClicked : {
                    resetStatsDialog.open()
                }
            }
        }

        Page {
            id: tab3
            anchors.fill : parent
            //anchors.verticalCenter : parent.verticalCenter
            anchors.topMargin : 20
            anchors.bottomMargin : 30
            anchors.leftMargin : 30
            anchors.rightMargin : 30

            Label {
                id : aboutTitle
                anchors.horizontalCenter : parent.horizontalCenter
                text: "<b>Mieru</b>" + " " + readingState.getVersionString()
                //font.pointSize: 24
            }
            Image {
                id : aboutMieruIcon
                anchors.horizontalCenter : parent.horizontalCenter
                anchors.topMargin : 10
                anchors.top : aboutTitle.bottom
                source : "image://icons/mieru.svg"
            }
            Label {
                id : aboutContactInfo
                anchors.horizontalCenter : parent.horizontalCenter
                //anchors.topMargin : 10
                anchors.top : aboutMieruIcon.bottom
                text: readingState.getAboutText()
                onLinkActivated : {
                    console.log('about text link clicked: ' + link)
                    Qt.openUrlExternally(link)
                }
            Button {
                text : "Donate ?"
                anchors.horizontalCenter : parent.horizontalCenter
                anchors.topMargin : 20
                anchors.top : aboutContactInfo.bottom
                onClicked : {
                    console.log('donation button clicked')
                    Qt.openUrlExternally('https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=martin%2ekolman%40gmail%2ecom&lc=GB&item_name=Mieru%20project&currency_code=EUR&bn=PP%2dDonationsBF%3abtn_donate_LG%2egif%3aNonHosted')
                }
            }
                //font.pointSize: 24
            }

            }
        }
    
    QueryDialog {
        id : resetStatsDialog
        titleText : "Reset all usage statistics ?"
        //message : "Reset all usage statistics ?"
        acceptButtonText : "reset"
        rejectButtonText : "cancel"
        onAccepted : { 
            stats.reset()
            statsText.text = stats.statsText
        }
    }
}
