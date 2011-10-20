//import Qt 4.7
import QtQuick 1.0
import com.nokia.meego 1.0
import com.meego 1.0
//import com.nokia.meego 1.0
//import QtDesktop 0.1

//Rectangle {
Window {
    id : mainView
    //color : "blue"
    //width : parent.width
    //height : parent.height
    anchors.fill : parent
    //width: 854
    //height: 480

    function showPage(path, pageId) {
        mangaPage.source = "image://page/" + path + "#" + pageId;
        //mangaPage.source = "../icons/mieru.png";
        }

    MouseArea {
        //width : mainView.width
        //height : mainView.height
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
        anchors.right : parent.right
        anchors.bottom : parent.bottom
        width : Math.min(parent.width,parent.height)/8.0
        height : Math.min(parent.width,parent.height)/8.0
        MouseArea {
            anchors.fill : parent
            drag.filterChildren: true
            onClicked: readingState.toggleFullscreen()
            }
        }
    }