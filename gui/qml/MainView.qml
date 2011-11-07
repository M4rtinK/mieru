//import Qt 4.7
import QtQuick 1.1
import com.nokia.meego 1.0

Page {
    id : mainView
    anchors.fill : parent
    tools : mainViewToolBar

    ToolBarLayout {
        id: mainViewToolBar
        visible: false
        ToolIcon { iconId: "toolbar-view-menu"; onClicked: {pageStack.pop(); } }
        ToolIcon { iconSource: "image://icons/view-normal.png"; onClicked: mainView.toggleFullscreen() }
        }

    function showPage(path, pageId) {
        mangaPage.source = "image://page/" + path + "|" + pageId;
        //mangaPage.source = "../icons/mieru.png";
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
            //width: mainView.width
            //height: mainView.height
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
        width : Math.min(parent.width,parent.height)/8.0
        height : Math.min(parent.width,parent.height)/8.0
        MouseArea {
            anchors.fill : parent
            drag.filterChildren: true
            onClicked: mainView.toggleFullscreen();
            //onClicked: fileSelector.open();
            //onClicked: readingState.toggleFullscreen()
            }
        }
    }