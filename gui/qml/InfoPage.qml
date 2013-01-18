//InfoPage.qml
import QtQuick 1.1
import com.nokia.meego 1.1

Page {
    id : infoPage
    anchors.fill : parent
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
        anchors.fill : parent

        Page {
            id : tab1
            anchors.fill : parent
            // background rectangle
            Rectangle {
                anchors.fill : parent
                color : "black"
            }
            ScrollDecorator {
                 flickableItem : infoFlickable
            }
            Flickable {
                id : infoFlickable
                anchors.fill  : parent
                contentWidth  : tab1.width
                contentHeight : 32 + infoHeadline.height + infoFirstPage.height + infoColumn.height + 32
                flickableDirection : Flickable.VerticalFlick
                Item {
                    id : anchorItem
                    width : parent.width
                }
                Label {
                    id : infoHeadline
                    anchors.top : anchorItem.bottom
                    anchors.topMargin : 32
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
                    anchors.topMargin : 32
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
            // background rectangle
            Rectangle {
                anchors.fill : parent
                color : "black"
            }
            Label {
                anchors.top : parent.top
                anchors.topMargin : 64
                anchors.left : parent.left
                anchors.leftMargin : 32
                id : statsHeadline
                text : "<h2>" + qsTr("Usage Statistics") + "</h2>"
                //font.pointSize: 24
            }
            Switch {
                anchors.top : parent.top
                anchors.topMargin : 64
                id : statsSwitch
                anchors.left : statsHeadline.right
                anchors.leftMargin : 64
                
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
            Label {
                id : statsText
                anchors.top : statsHeadline.bottom
                anchors.topMargin : 10
                anchors.left : parent.left
                anchors.leftMargin : 32
                text: stats.statsText
            }

            Button {
                anchors.top : statsText.bottom
                anchors.topMargin : 64
                anchors.left : parent.left
                anchors.leftMargin : 32
                text : qsTr("Reset")
                onClicked : {
                    resetStatsDialog.open()
                }
            }
        }

        Page {
            id: tab3
            anchors.fill : parent
            // background rectangle
            Rectangle {
                anchors.fill : parent
                color : "black"
            }
            ScrollDecorator {
                 flickableItem : aboutFlickable
            }
            Flickable {
                id : aboutFlickable
                anchors.fill  : parent
                anchors.topMargin : 16
                anchors.bottomMargin : 16
                anchors.leftMargin : 16
                anchors.rightMargin : 16
                contentWidth  : tab3.width
                contentHeight : aboutColumn.height + 30
                flickableDirection : Flickable.VerticalFlick
                
                Item {
                    //anchors.horizontalCenter : parent.horizontalCenter
                    width : tab3.width
                    height : childrenRect.height
                    id : aboutColumn
                    Label {
                        id : versionLabel
                        anchors.top : parent.top
                        anchors.horizontalCenter : parent.horizontalCenter
                        text : "<h2>Mieru " + readingState.getVersionString() + "</h2>"
                    }
                    Image {
                        id : mieruIcon
                        anchors.top : versionLabel.bottom
                        anchors.topMargin : 16
                        anchors.horizontalCenter : parent.horizontalCenter
                        width : infoPage.width/4.0
                        height : infoPage.width/4.0
                        smooth : true
                        source : "image://icons/harmattan_icon.svg"
                    }
                    Label {
                        id : mieruDescription
                        anchors.top : mieruIcon.bottom
                        anchors.topMargin : 16
                        anchors.horizontalCenter : parent.horizontalCenter
                        horizontalAlignment: Text.AlignHCenter
                        width : parent.width
                        wrapMode : Text.WordWrap
                        text : qsTr("Mieru is a flexible Manga and comic book reader.")
                    }
                    Label {
                        id : donateLabel
                        anchors.top : mieruDescription.bottom
                        anchors.topMargin : 25
                        anchors.horizontalCenter : parent.horizontalCenter
                        horizontalAlignment: Text.AlignHCenter
                        width : parent.width
                        wrapMode : Text.WordWrap
                        text : qsTr("<b>Do you like Mieru ? Donate !</b>")
                    }
                    Row {
                        id : ppFlattrRow
                        anchors.top : donateLabel.bottom
                        anchors.horizontalCenter : parent.horizontalCenter
                        anchors.topMargin : 64
                        spacing : 64
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
                        anchors.topMargin : 32
                        anchors.horizontalCenter : parent.horizontalCenter
                        url : "1PPnoD4SyeQYgvhJ6L5xkjZ4qE4WMMCe1k"
                    }
                    Column {
                        anchors.top : bitcoinButton.bottom
                        anchors.topMargin : 64
                        spacing : 16
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
            ScrollDecorator {
                flickableItem: aboutFlickable
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
