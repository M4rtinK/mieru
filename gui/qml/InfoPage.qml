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

            ScrollDecorator {
                 id: scrolldecorator
                 flickableItem: infoFlickable
            }
            Flickable {
                id : infoFlickable
                anchors.fill : parent
                contentWidth: tab1.width
                contentHeight: infoHeadline.height + infoFirstPage.height + infoCollumn.height + 30

                flickableDirection: Flickable.VerticalFlick

                Label {
                    id : infoHeadline
                    anchors.horizontalCenter : parent.horizontalCenter
                    text: "<h1>" + readingState.getPrettyName() + "</h1>"
                    width : tab1.width
                    wrapMode : Text.WordWrap
                    horizontalAlignment : Text.AlignHCenter
                }
                Image {
                    id : infoFirstPage
                    anchors.horizontalCenter : parent.horizontalCenter
                    anchors.top : infoHeadline.bottom
                    anchors.topMargin : 10
                    source : "image://page/" + mainView.mangaPath + "|0"
                    fillMode : Image.PreserveAspectFit
                    width : tab1.width/2.0
                    height : tab1.width/2.0
                    smooth : true
                Label {
                    anchors.verticalCenter : parent.verticalCenter
                    anchors.leftMargin : 10
                    anchors.left : infoFirstPage.right
                    //var remainingPages = mainView.maxPageNumber -1
                    text: "<h2>+" + (mainView.maxPageNumber-1) + "<br>pages</h2>"
                }

                }
                Column {
                    id : infoCollumn
                    //anchors.horizontalCenter : parent.horizontalCenter
                    anchors.top : infoFirstPage.bottom
                    anchors.topMargin : 20
                    spacing : 20
                    Label {
                        text: "<b>Path</b>"
                    }
                    Label {
                        text: "" + mainView.mangaPath
                        // explicit width is needed for wrapping to work
                        width : tab1.width
                        wrapMode : Text.WrapAnywhere
                    }
                    Label {
                        text: "<h3>Online search</h3>"
                    }
                    Button {
                        text : "Google"
                        onClicked : {
                            mainView.notify("Opening <b>Google</b> search")
                            Qt.openUrlExternally("http://www.google.com/search?as_q=" + readingState.getPrettyName())
                        }
                    }
                    Button {
                        //TODO: other language mutations
                        text : "Wikipedia"
                        onClicked : {
                            mainView.notify("Opening <b>Wikipedia</b> search")
                            Qt.openUrlExternally("http://en.wikipedia.org/w/index.php?search=" + readingState.getPrettyName() + "&go=Go")
                        }

                    }
                    Button {
                        text : "Manga updates"
                        onClicked : {
                            mainView.notify("Opening <b>Manga updates</b> search")
                            Qt.openUrlExternally("http://www.mangaupdates.com/search.html?search=" + readingState.getPrettyName())
                        }
                    }
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
                // eliminate checked property binding loop
                function checkedInit() {
                    return stats.enabled
                }
                checked : checkedInit()

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
                text: "<style type='text/css'>p { margin-bottom:15px; margin-top:0px; }</style>" + readingState.getAboutText()

                onLinkActivated : {
                    console.log('about text link clicked: ' + link)
                    mainView.notify("Opening:<br><b>"+link+"</b>")
                    Qt.openUrlExternally(link)
                }
            Button {
                text : "Donate ?"
                anchors.horizontalCenter : parent.horizontalCenter
                anchors.topMargin : 25
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
