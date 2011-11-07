//import Qt 4.7
import QtQuick 1.1
import com.nokia.meego 1.0

Page {
    id : mainView
    anchors.fill : parent
    tools : mainViewToolBar

    ToolBarLayout {
        id : mainViewToolBar
        visible: false
        ToolIcon { iconId: "toolbar-view-menu"; onClicked: mainViewMenu.open() }
        ToolIcon { iconSource: "image://icons/view-normal.png"; onClicked: mainView.toggleFullscreen() }
        }

    Menu {
        id : mainViewMenu
        MenuLayout {
            MenuItem {
              text : "Open file"
              onClicked : { fileSelector.down('/home/user/MyDocs');
                  fileSelector.open();
                  }
              }
            }
    }

    function showPage(path, pageId) {
        mangaPage.source = "image://page/" + path + "|" + pageId;
        }

    // ** trigger notifications
    function notify(text) {
        notification.text = text;
        notification.show();
        }

    // ** fullscreen handling
    function toggleFullscreen() {
        console.log("toggle fullscreen");
        /* handle fullscreen button hiding
        it should be only visible with no toolbar */
        fullscreenButton.visible = !fullscreenButton.visible
        rootWindow.showToolBar = !rootWindow.showToolBar;
        }

    MouseArea {
        anchors.fill : parent
        id: prevButton
        objectName: "prevButton"
        drag.filterChildren: true
        onClicked: {
            if (mouseX < width/2.0){
                console.log("previous");
                console.log(readingState.previous());
                }

            else{
                console.log("next");
                console.log(readingState.next());
                }
        }

        Flickable {
            id: pageFlickable
            objectName: "pageFlickable"
            anchors.fill : parent
            contentWidth: mangaPage.width
            contentHeight: mangaPage.height

            Image {
                id: mangaPage
                //PinchArea {
                //    pinch.target : pageFlickable
                //    }
                }
            }
       }

    Image {
        id : fullscreenButton
        source : "image://icons/view-fullscreen.png"
        anchors.right : mainView.right
        anchors.bottom : mainView.bottom
        visible : false
        opacity : 0.1
        width : Math.min(parent.width,parent.height)/8.0
        height : Math.min(parent.width,parent.height)/8.0
        MouseArea {
            anchors.fill : parent
            drag.filterChildren: true
            onClicked: mainView.toggleFullscreen();
            }
        }
    }