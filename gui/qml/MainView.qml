//MainView.qml
//import Qt 4.7
import QtQuick 1.1
import com.nokia.meego 1.0
import com.nokia.extras 1.0

Page {
    id : mainView
    anchors.fill : parent
    tools : mainViewToolBar

    property int maxPageNumber : 2
    property int pageNumber : 2
    property string mangaPath : ""

    onPageNumberChanged: {
        var pageIndex = pageNumber-1
        mangaPage.source = "image://page/" + mangaPath + "|" + pageIndex;
        //make sure the page number is updated
        //pageNumbers.text = mainView.pageNumber + "/" + mainView.maxPageNumber
        }

    ToolBarLayout {
        id : mainViewToolBar
        visible: false
        ToolIcon { iconId: "toolbar-view-menu"; onClicked: mainViewMenu.open() }
        //ToolIcon { iconId: "toolbar-previous" }
        ToolButton { id : pageNumbers
                     text : mainView.pageNumber + "/" + mainView.maxPageNumber
                     height : parent.height
                     flat : true
                     onClicked : { pagingDialog.open() }
                   }
        //ToolIcon { iconId: "toolbar-next" }
        ToolIcon { iconSource: "image://icons/view-normal.png"; onClicked: mainView.toggleFullscreen() }
        }

    Menu {
        id : mainViewMenu

        MenuLayout {
            MenuItem {
              text : "Open file"
              onClicked : {                   
                  fileSelector.down(readingState.getSavedFileSelectorPath());
                  fileSelector.open();
                  }
              }

            MenuItem {
                text : "History"
                onClicked : {
                    console.log("implement history");
                    }
                }

            MenuItem {
                text : "Options"
                onClicked : {
                    console.log("implement options");
                    }
                }

            MenuItem {
                text : "About"
                onClicked : {
                    console.log("implement about");
                    }
                }
            }
        }

    function showPage(path, pageId) {
        mainView.mangaPath = path
        mainView.pageNumber = pageId+1
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

    Menu {
        id : pagingDialog
        Row {
            Slider {
                //width : pagingColumn.width*0.8
                //anchors.topMargin : height*0.5
                id : pagingSlider
                maximumValue: mainView.maxPageNumber
                minimumValue: 1
                value: mainView.pageNumber
                stepSize: 1
                valueIndicatorVisible: false
                //orientation : Qt.Vertical
                onPressedChanged : {
                    //only load the page once the user stopped dragging to save resources
                    mainView.pageNumber = value
                    }

                }

            CountBubble {
                value : pagingSlider.value
                largeSized : true
                }
            }
        }
    }