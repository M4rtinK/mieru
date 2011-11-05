//import Qt 4.7
import QtQuick 1.1
import com.nokia.meego 1.0
import com.nokia.extras 1.0
//import com.meego 1.0
//import com.nokia.meego 1.0
//import QtDesktop 0.1

//Rectangle {
PageStackWindow {
    id : mainView
    showStatusBar : false
    anchors.fill : parent

    function showPage(path, pageId) {
        mangaPage.source = "image://page/" + path + "|" + pageId;
        //mangaPage.source = "../icons/mieru.png";
        }

    // ** trigger notifications
    function notify(text) {
        notification.text = text;
        notification.show();
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
        anchors.right : parent.right
        anchors.bottom : parent.bottom
        //opacity : 0
        width : Math.min(parent.width,parent.height)/8.0
        height : Math.min(parent.width,parent.height)/8.0
        MouseArea {
            anchors.fill : parent
            drag.filterChildren: true
            onClicked: readingState.toggleFullscreen()
            }
        }

    InfoBanner {
        id: notification
        timerShowTime : 5000
        }
    }