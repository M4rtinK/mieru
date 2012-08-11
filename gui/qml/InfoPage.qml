//InfoPage.qml
import Qt 4.7
import QtQuick 1.1
import com.nokia.meego 1.0

Page {
    tools: ToolBarLayout {
        ToolIcon {
            iconId: "toolbar-back"
            onClicked: pageStack.pop()
        }
        ButtonRow {
            TabButton {
                text: qsTr("Info")
                tab: tab1
            }
            TabButton {
                text: qsTr("Stats")
                tab: tab2
            }
            TabButton {
                text: qsTr("About")
                tab: tab3
            }
        }
    }

    TabGroup {
        id : tabGroup
        currentTab : tab1

        Page {
            id : tab1
            anchors.fill : parent
            anchors.topMargin    : 30
            anchors.bottomMargin : 30
            anchors.leftMargin   : 30
            anchors.rightMargin  : 30

            ScrollDecorator {
                 flickableItem : infoFlickable
            }
            Flickable {
                id : infoFlickable
                anchors.fill  : parent
                contentWidth  : tab1.width
                contentHeight : infoHeadline.height + infoFirstPage.height + infoColumn.height + 30
                flickableDirection : Flickable.VerticalFlick

                Label {
                    id : infoHeadline
                    anchors.horizontalCenter : parent.horizontalCenter
                    text  : "<h1>" + readingState.getPrettyName() + "</h1>"
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
                    width  : tab1.width / 2.0
                    height : tab1.width / 2.0
                    smooth : true
				}
                Column {
                    id : infoColumn
                    anchors.top : infoFirstPage.bottom
                    anchors.topMargin : 20
                    spacing : 20
					
                    LineText {
                        width : tab1.width
                        text : qsTr("Properties")
                    }
                    Label {
                        text : "<b>" + qsTr("Pages") + ":</b> " + (mainView.maxPageNumber - 1)
                    }
                    Label {
                        text : "<b>" + qsTr("Path") + ":</b> " + mainView.mangaPath
						
                        // explicit width is needed for wrapping to work
                        width    : tab1.width
                        wrapMode : Text.WrapAnywhere
                    }
                    LineText {
                        width : tab1.width
                        text  : qsTr("Online search")
                    }
                    Button {
                        text : "Google"
                        anchors.horizontalCenter : parent.horizontalCenter
                        onClicked : {
                            rootWindow.notify(qsTr("Opening <b>Google</b> search"))
                            Qt.openUrlExternally("http://www.google.com/search?as_q=" + readingState.getPrettyName())
                        }
                    }
                    Button {
                        // TODO: other language mutations
                        text : "Wikipedia"
                        anchors.horizontalCenter : parent.horizontalCenter
                        onClicked : {
                            rootWindow.notify(qsTr("Opening <b>Wikipedia</b> search"))
                            Qt.openUrlExternally("http://en.wikipedia.org/w/index.php?search=" + readingState.getPrettyName() + "&go=Go")
                        }

                    }
                    Button {
                        text : "Manga updates"
                        anchors.horizontalCenter : parent.horizontalCenter
                        onClicked : {
                            rootWindow.notify(qsTr("Opening <b>Manga updates</b> search"))
                            Qt.openUrlExternally("http://www.mangaupdates.com/search.html?search=" + readingState.getPrettyName())
                        }
                    }
                }
            }
        }
        Page {
            id: tab2
            anchors.fill : parent
            anchors.topMargin : 30
            anchors.bottomMargin : 30
            anchors.leftMargin : 30
            anchors.rightMargin : 30
            Text {
               anchors.left : parent.left
               id : statsHeadline
               text : "<b>" + qsTr("Usage Statistics") + "</b>"
               font.pointSize: 24
            }
            Switch {
                id : statsSwitch
                anchors.left : statsHeadline.right
                anchors.leftMargin : 35
                
                onCheckedChanged : {
                    // enable/disable stats and update statsText
                    stats.enabled  = statsSwitch.checked
                    statsText.text = stats.statsText
                }
                
                // workaround for checked property binding loop
                Component.onCompleted : {
                    checked = stats.enabled
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
                text : qsTr("Reset")
                onClicked : {
                    resetStatsDialog.open()
                }
            }
        }

        Page {
            id: tab3
            anchors.fill : parent
            anchors.topMargin : 8
            anchors.bottomMargin : 8
            anchors.leftMargin : 8
            anchors.rightMargin : 8

            ScrollDecorator {
                 flickableItem : aboutFlickable
            }
            Flickable {
                id : aboutFlickable
                anchors.fill  : parent
                contentWidth  : tab3.width
                contentHeight : aboutColumn.height + 30
                flickableDirection : Flickable.VerticalFlick
                
                Column {
                    id : aboutColumn
                    spacing : 25
                    Column {
                        anchors.horizontalCenter : parent.horizontalCenter
                        spacing : 5
                        Label {
                            anchors.horizontalCenter : parent.horizontalCenter
                            text : "<h2>Mieru " + readingState.getVersionString() + "</h2>"
                        }
                        Image {
                            anchors.horizontalCenter : parent.horizontalCenter
                            source : "image://icons/mieru.svg"
                        }
                    }
                    Label {
                        id : mieruDescription
                        anchors.horizontalCenter : parent.horizontalCenter
                        //width    : tab3.width
                        wrapMode : Text.WordWrap
                        text : qsTr("Mieru is a flexible Manga and comic book reader.")
                    }
                    Label {
                        id : donateLabel
                        anchors.horizontalCenter : parent.horizontalCenter
                        text : "<h3>Dou you like modRana ? <b>Donate !</b></h3>"
                    }
                    Row {
                        id : ppFlattrRow
                        anchors.top : donateLabel.bottom
                        anchors.horizontalCenter : parent.horizontalCenter
                        anchors.topMargin : 24
                        spacing : 32
                        PayPalButton {
                            id : ppButton
                            anchors.verticalCenter : parent.verticalCenter
                            url : "https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=martin%2ekolman%40gmail%2ecom&lc=GB&item_name=Mieru%20project&currency_code=EUR&bn=PP%2dDonationsBF%3abtn_donate_LG%2egif%3aNonHosted"
                        }

                        FlattrButton {
                            id : flattrButton
                            anchors.verticalCenter : parent.verticalCenter
                            url : "http://flattr.com/thing/830372/Mieru-flexible-manga-and-comic-book-reader"
                        }
                    }

                    BitcoinButton {
                        id : bitcoinButton
                        anchors.top : ppFlattrRow.bottom
                        anchors.topMargin : 24
                        anchors.horizontalCenter : parent.horizontalCenter
                        url : "1PPnoD4SyeQYgvhJ6L5xkjZ4qE4WMMCe1k"
                    }
                    Column {
                        spacing : 5
                        Label {
                            text : "<b>" + qsTr("main developer") + ":</b> Martin Kolman"
                        }
                        Label {
                            text : "<b>" + qsTr("email") + ":</b> <a href='mailto:mieru.info@gmail.com'>mieru.info@gmail.com</a>"
                            onLinkActivated : Qt.openUrlExternally(link)
                        }
                        Label {
                            text : "<b>" + qsTr("www") + ":</b> <a href='http://m4rtink.github.com/mieru/'>http://m4rtink.github.com/mieru/</a>"
                            onLinkActivated : Qt.openUrlExternally(link)
                        }
                        Label {
                            width : tab3.width
                            text  : "<b>" + qsTr("discussion") + ":</b> " + "<a href='http://forum.meego.com/showthread.php?t=5405'>forum.meego.com</a>"
                            onLinkActivated : Qt.openUrlExternally(link)
                        }
                    }
                }
            }
        }
    }
    
    QueryDialog {
        id : resetStatsDialog
        titleText : qsTr("Reset all usage statistics")
        message : qsTr("Do you really want to reset all usage statistics?")
        acceptButtonText : qsTr("Reset")
        rejectButtonText : qsTr("Cancel")
        onAccepted : { 
            stats.reset()
            statsText.text = stats.statsText
        }
    }
}
