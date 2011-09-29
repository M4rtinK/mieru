//import Qt 4.7
import QtQuick 1.0
//import com.meego 1.0
//import com.nokia.meego 1.0
//import QtDesktop 0.1

Rectangle {
    id : mainView
    //width : parent.width
    //height : parent.height
    //anchors.fill : parent
    //width: 854
    //height: 480

    function showPage(path, pageId) {
        mangaPage.source = "image://page/" + path + "#" + pageId;
        //mangaPage.source = "../icons/mieru.png";
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
            anchors.left : parent.left
            width: mainView.width
            height: mainView.height
            contentWidth: mangaPage.width
            contentHeight: mangaPage.height

            Image {
              id: mangaPage
            }
       }
    }
}