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
        //ToolIcon { iconId: "toolbar-previous" }
        ToolButton { id : pageNumbers
                     text : "1/12"
                     height : parent.height
                     flat : true
                     onClicked : { pagingMenu.open() }
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

    Menu {
        id : pagingMenu
        MenuLayout {
            MenuItem {
                text : "First Page"
                onClicked : {
                    console.log("implement paging first page");
                    }
                }

            MenuItem {
                text : "Last Page"
                onClicked : {
                    console.log("implement paging last page");
                    }
                }

            Slider {
                width : parent.width*0.8
                //anchors.topMargin : height*0.5
                id : pagingSlider
                maximumValue: 150
                minimumValue: 0
                value: 75
                stepSize: 1
                valueIndicatorVisible: true
                }

            TextField {
                anchors.left : pagingSlider.right
                anchors.top : pagingSlider.top
                width: parent.width*0.2
                text: pagingSlider.value
                validator: IntValidator{bottom: pagingSlider.minimumValue; top: pagingSlider.maximumValue}
                }

            MenuItem {
                text : "Done"
                onClicked : {
                    console.log("implement paging done");
                    }
                }

            }
        }

    function showPage(path, pageId, pageNumbersString) {
        mangaPage.source = "image://page/" + path + "|" + pageId;
        pageNumbers.text = pageNumbersString;
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