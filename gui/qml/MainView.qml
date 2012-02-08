//MainView.qml
//import Qt 4.7
import QtQuick 1.1
import com.nokia.meego 1.0
import com.nokia.extras 1.0

Page {
    id : mainView
    objectName : "mainView"
    anchors.fill : parent
    tools : mainViewToolBar

    property int maxPageNumber : 1
    property int pageNumber : 1
    property string mangaPath : ""
    property string lastUrl
    property bool rememberScale : options.get("QMLRememberScale", false)
    property bool pageLoaded : false
    property bool pagingFeedback : options.get("QMLPagingFeedback", true)
    property string pageFitMode : options.get("fitMode", "original")

    property alias fullscreenButtonOpacity : fullscreenButton.opacity

    onMangaPathChanged : { reloadPage() }
    onPageNumberChanged : { reloadPage() }

    // workaround for calling python properties causing segfaults
    function shutdown() {
        //console.log("main view shutting down")
    }

    function reloadPage() {
        //console.log("** reloading page **")
        var pageIndex = pageNumber-1
        var url = "image://page/" + mangaPath + "|" + pageIndex;
        // check for false alarms
        if (url != lastUrl) {
          //console.log(mangaPath + " " + pageNumber)
          mangaPage.source = url
              // reset the page position
              pageFlickable.contentX = 0;
              pageFlickable.contentY = 0;
          //update page number in the current manga instance
          //NOTE: this is especially important due to the slider
          readingState.setPageID(pageIndex, mangaPath)
          pageLoaded = true
        }
     }

    function showPage(path, pageId) {
        mainView.mangaPath = path
        var pageNr = pageId+1
        mainView.pageNumber = pageNr
    }

    function restoreContentShift(){
        /* check if restored scale is consistent
           between the independently saved value and the
           value remembered in the manga state
        */
        var mangaStateScale = readingState.getActiveMangaScale()
        if (mangaStateScale==pageFlickable.scale) {
            pageFlickable.contentX = readingState.getActiveMangaShiftX()
            pageFlickable.contentY = readingState.getActiveMangaShiftY()
        }
    }

    function notify(text) {
        // send notifications
        notification.text = text;
        notification.show();
    }

    function toggleFullscreen() {
        /* handle fullscreen button hiding,
        it should be only visible with no toolbar */
        fullscreenButton.visible = !fullscreenButton.visible
        rootWindow.showToolBar = !rootWindow.showToolBar;
        options.set("QMLToolbarState", rootWindow.showToolBar)
    }

    function getScale() {
        return pageFlickable.scale
    }

    function getXShift() {
        return pageFlickable.contentX
    }

    function getYShift() {
        return pageFlickable.contentY
    }

    // restore possible saved rotation lock value
    function restoreRotation() {
        var savedRotation = options.get("QMLmainViewRotation", "auto")
        if ( savedRotation == "auto" ) {
            mainView.orientationLock = PageOrientation.Automatic
        } else if ( savedRotation == "portrait" ) {
            mainView.orientationLock = PageOrientation.LockPortrait
        } else {
            mainView.orientationLock = PageOrientation.LockLandscape
        }
    }

    function showPrevFeedback() {
    // only show with feedback enabled and no feedback in progress
        if (mainView.pagingFeedback && !prevFbTimer.running) {
            prevFbTimer.start()
        }
    }

    function showNextFeedback() {
    // only show with feedback enabled and no feedback in progress
        if (mainView.pagingFeedback && !nextFbTimer.running) {
            nextFbTimer.start()
        }
    }

    /** Page fitting **/

    function setPageFitMode(fitMode) {
        /*
        console.log("SET PAGE FIT MODE")
        console.log(fitMode)
        console.log(mainView.pageFitMode)
        */
        // set page fitting - only update on a mode change
        if (fitMode != mainView.pageFitMode) {
            options.set("fitMode", fitMode)
            mainView.pageFitMode = fitMode
        }
        // scale remembering for
        // * disable for non-custom fitting modes
        // * enable for custom fitting mode
        if (fitMode != "custom") {
            mainView.rememberScale = false
            options.set("QMLRememberScale", false)
        } else {
            mainView.rememberScale = true
            options.set("QMLRememberScale", true)
        }
    }

    onPageFitModeChanged : {
        // trigger page refit
        fitPage(pageFitMode)
    }

    // handle viewport resize
    onWidthChanged : {
        //console.log("mw width " + width)
        fitPage(pageFitMode)
    }
    onHeightChanged : {
        //console.log("mw height " + height)
        fitPage(pageFitMode)
    }

    function fitPage(mode) {
        /*
        console.log("FIT PAGE")
        console.log(mode)
        console.log(mainView.width)
        console.log(mainView.height)
        console.log(mangaPage.sourceSize.width)
        console.log(mangaPage.sourceSize.height)
        */

        // fit the page according to the current fitting mode
        if (mode == "original") {
            // 1 : 1
            pageFlickable.scale = 1.0
        } else if (mode == "width") {
            pageFlickable.scale = mainView.width/mangaPage.sourceSize.width
        } else if (mode == "height") {
            pageFlickable.scale = mainView.height/mangaPage.sourceSize.height
        } else if (mode == "screen") {
            fitPageToScreen()
        } else if (mode == "orient") {
            // fit to screen in portrait, fit to width in landscape
            if (rootWindow.inPortrait) {
                fitPageToScreen()
            } else {
                pageFlickable.scale = mainView.width/mangaPage.sourceSize.width
            }
        } else if (mode == "most") {
            // fit fo to the longest side of the image
            if (pageFlickable.width >= pageFlickable.height) {
                pageFlickable.scale = mainView.width/mangaPage.sourceSize.width
            } else {
                pageFlickable.scale = mainView.height/mangaPage.sourceSize.height
            }

        /* nothing needs to be done for the custom mode
         as the current scale is just used as the initial
         custom scale */
        }
    }

    function fitPageToScreen() {
        // image
        var wi = mangaPage.sourceSize.width
        var hi = mangaPage.sourceSize.height
        var ri = wi/hi
        // screen
        var ws = mainView.width
        var hs = mainView.height
        var rs = ws/hs
        if (rs>ri) {
            pageFlickable.scale = (wi * hs/hi)/wi
        } else {
            pageFlickable.scale = ws/wi
        }
    }

    Component.onCompleted : {
      restoreRotation()
    }

    /** Toolbar **/

    ToolBarLayout {
        id : mainViewToolBar
        visible: false
        ToolIcon {
            id : backTI
            iconId: "toolbar-view-menu"
            onClicked: {
                if (platform.showQuitButton()) {
                    mainViewMenuWithQuit.open()
                } else {
                    mainViewMenu.open()
                }
            }
        }
        //ToolIcon { iconId: "toolbar-previous" }
        ToolButton { id : pageNumbers
                     text : mainView.pageLoaded ? mainView.pageNumber + "/" + mainView.maxPageNumber : "-/-"
                     anchors.top : backTI.top
                     anchors.bottom : backTI.bottom
                     flat : true
                     onClicked : { pagingDialog.open() }
        }
        //ToolIcon { iconId: "toolbar-next" }
        ToolIcon { //iconId: "toolbar-down"
                   // fix for incomplete theme on Fremantle
                   iconId: platform.incompleteTheme() ?
                   "icon-m-common-next" : "toolbar-down"
                   rotation : platform.incompleteTheme() ? 90 : 0
                   onClicked: mainView.toggleFullscreen() }
        //ToolIcon { iconSource: "image://icons/view-normal.png"; onClicked: mainView.toggleFullscreen() }
        }

    /** Main menu **/

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
                    rootWindow.openFile("HistoryPage.qml")
                    }
            }

            MenuItem {
                text : "Info"
                onClicked : {
                    rootWindow.openFile("InfoPage.qml")
                }
            }

            MenuItem {
                text : "Options"
                onClicked : {
                    rootWindow.openFile("OptionsPage.qml")
                    }
            }
        }
    }

    Menu {
        id : mainViewMenuWithQuit
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
                    rootWindow.openFile("HistoryPage.qml")
                    }
            }

            MenuItem {
                text : "Info"
                onClicked : {
                    rootWindow.openFile("InfoPage.qml")
                }
            }

            MenuItem {
                text : "Options"
                onClicked : {
                    rootWindow.openFile("OptionsPage.qml")
                    }
            }

            MenuItem {
                text : "Quit"
                onClicked : {
                    readingState.quit()
                    }
            }
        }
    }

    /** Pinch zoom **/

    PinchArea {
        //anchors.fill : parent
        //onPinchStarted : console.log("pinch started")
        //pinch.target : mangaPage
        //pinch.minimumScale: 0.5
        //pinch.maximumScale: 2
        width: Math.max(pageFlickable.contentWidth, pageFlickable.width)
        height: Math.max(pageFlickable.contentHeight, pageFlickable.height)
        property real initialScale
        property real initialWidth
        property real initialHeight

        onPinchStarted: {
            initialScale = pageFlickable.scale
            initialWidth = pageFlickable.contentWidth
            initialHeight = pageFlickable.contentHeight
            //pageFlickable.interactive = false
            //console.log("start " + pinch.scale)
        }

        onPinchUpdated: {
            // adjust content pos due to drag
            pageFlickable.contentX += pinch.previousCenter.x - pinch.center.x
            pageFlickable.contentY += pinch.previousCenter.y - pinch.center.y

            // resize content
            pageFlickable.resizeContent(initialWidth * pinch.scale, initialHeight * pinch.scale, pinch.center)
            // remember current scale
            pageFlickable.scale = initialScale * pinch.scale

            //console.log("pf " + pageFlickable.contentWidth + " " + pageFlickable.contentHeight)
            //console.log("page " + mangaPage.width + " " + mangaPage.height)
            //console.log("scale " + pageFlickable.scale)
        }

        onPinchFinished: {
            //pageFlickable.interactive = true
            // Move its content within bounds.
            pageFlickable.returnToBounds()
            if (mainView.rememberScale) {
                // save the new scale so that it can
                // be used on the next page
                options.set("QMLMangaPageScale", pageFlickable.scale)
                // override page fitting with the new scale
                if (mainView.pageFitMode != "custom") {
                    mainView.setPageFitMode("custom")
                }
            }
        }
    }

    /** Left/right screen half page switching **/

    MouseArea {
        anchors.fill : parent
        id: prevButton
        objectName: "prevButton"
        drag.filterChildren: true
        onClicked: {
            if (mouseX < width/2.0){
                mainView.showPrevFeedback()
                console.log("previous page");
                readingState.previous();
            }

            else{
                mainView.showNextFeedback()
                console.log("next page");
                readingState.next();
            }
        }

        /** Main manga page flickable **/

        Flickable {
            id: pageFlickable
            property real scale: mainView.rememberScale ? options.get("QMLMangaPageScale", 1.0) : 1.0
            objectName: "pageFlickable"
            anchors.fill : parent
            // center the page if smaller than viewport
            anchors.leftMargin : (contentWidth < mainView.width) ? (mainView.width-contentWidth)/2.0 : 0
            anchors.topMargin : (contentHeight < mainView.height) ? (mainView.height-contentHeight)/2.0 : 0
            contentWidth : mangaPage.width
            contentHeight : mangaPage.height
            /*
            clipping seems to lead to performance degradation so it is only enabled
            once the GUI-page transition starts to prevent the manga-page overlapping
            the new GUI-page during transition
            */
            clip : rootWindow.pageStack.busy

            Image {
                id: mangaPage
                width : sourceSize.width * pageFlickable.scale
                height : sourceSize.height * pageFlickable.scale
                //smooth : !pageFlickable.moving
                smooth : true
                fillMode : Image.PreserveAspectFit
                //width : pageFlickable.contentWidth
                //height : pageFlickable.contentHeight
                // update flickable width once an image is loaded
                /**
                onSourceChanged : {
                    //console.log("SOURCE")
                    //console.log(sourceSize.width + " " + sourceSize.height)
                    //console.log(width + " " + height)

                    // assure page fitting
                    if (mainView.pageFitMode == "custom") {
                        // revert scale remembering on next page
                        // if disabled
                        if (!mainView.rememberScale) {
                            pageFlickable.scale = 1.0
                            mainView.setPageFitMode("original")
                        }
                    }
                    //pageFlickable.contentWidth = sourceSize.width * pageFlickable.scale
                    //pageFlickable.contentHeight = sourceSize.height * pageFlickable.scale
                }
                **/
                onSourceSizeChanged : {
                        if (mainView.pageFitMode != "custom") {
                            mainView.fitPage(mainView.pageFitMode)
                        }
                }
            }
        }
    }

    /** Fullscreen toggle button **/

    ToolIcon {
        id : fullscreenButton
        //source : "image://icons/view-fullscreen.png"
        // fix for incomplete theme on Fremantle
        iconId: platform.incompleteTheme() ?
        "icon-m-common-next" : "toolbar-up"
        rotation : platform.incompleteTheme() ? 270 : 0
        anchors.right : mainView.right
        anchors.bottom : mainView.bottom
        visible : !rootWindow.showToolBar
        opacity : options.get("QMLFullscreenButtonOpacity", 0.5)
        width : Math.min(parent.width,parent.height)/8.0
        height : Math.min(parent.width,parent.height)/8.0
        MouseArea {
            anchors.fill : parent
            drag.filterChildren: true
            onClicked: mainView.toggleFullscreen();
        }
    }

    /** Quick menu **/

    Menu {
        id : pagingDialog
        MenuLayout {
            //width : pagingDialog.width
            id : mLayout

            Row {
                //anchors.left : mLayout.left
                //anchors.right : mLayout.right
                Slider {
                    id : pagingSlider
                    width : mLayout.width*0.9
                    //anchors.topMargin : height*0.5
                    //anchors.left : mLayout.left
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
                    //width : mLayout.width*0.2
                    //anchors.left : pagingSlider.right
                    //anchors.right : mLayout.right
                    value : pagingSlider.value
                    largeSized : true
                }
            }
            Row {
                id : mButtonRow
                property int usableWidth : mLayout.width - 10
                spacing : 10
                Button {
                    text : mainView.pageFitMode
                    iconSource : "image://theme/icon-m-common-expand"
                    width : mButtonRow.usableWidth/2.0
                    onClicked : {
                        pageFitSelector.open()
                    }
                }
                Button {
                    text : "rotation"
                    iconSource : "image://theme/icon-m-common-" + __iconType
                    width : mButtonRow.usableWidth/2.0
                    property string __iconType: (mainView.orientationLock == PageOrientation.LockPrevious) ? "locked" : "unlocked"

                    onClicked: {
                        if (mainView.orientationLock == PageOrientation.LockPrevious) {
                            mainView.orientationLock = PageOrientation.Automatic
                        } else {
                            mainView.orientationLock = PageOrientation.LockPrevious
                        }
                    }
                }
                /*
                platformIconId: "icon-m-common-" + __iconType + __inverseString

                property string __inverseString: style.inverted ? "-inverse" : ""
                */

            }
        }
    }

    /** No pages loaded label **/

    Label {
        anchors.centerIn : parent
        text : "<h1>No pages loaded</h1>"
        visible : !mainView.pageLoaded
    }

    /** Paging feedback **/

    Item {
        id : previousFeedback
        visible : false
        opacity : 0.7
        anchors.verticalCenter : parent.verticalCenter
        anchors.left : parent.left
        anchors.leftMargin : 20
        Image {
            id : previousIcon
            anchors.left : parent.left
            source : "image://theme/icon-m-toolbar-previous"
        }
        /* Text {
            //text : "<b>PREVIOUS</b>"
            anchors.left : previousIcon.right
            anchors.leftMargin : 20
            anchors.verticalCenter : previousIcon.verticalCenter
            style : Text.Outline
            styleColor : "white"
            font.pixelSize : 25
        } */
    }
    Item {
        id : nextFeedback
        visible : false
        opacity : 0.7
        anchors.verticalCenter : parent.verticalCenter
        anchors.right : parent.right
        anchors.rightMargin : 20
        Image {
            id : nextIcon
            anchors.right : parent.right
            source : "image://theme/icon-m-toolbar-next"
        }
        /* Text {
            //text : "<b>NEXT</b>"
            anchors.right : nextIcon.left
            anchors.rightMargin : 20
            anchors.verticalCenter : nextIcon.verticalCenter
            style : Text.Outline
            styleColor : "white"
            font.pixelSize : 25
            //color : "white"
        } */
    }

    Timer {
        id : prevFbTimer
        interval : 500
        // we need to show and hide the feedback
        triggeredOnStart : true
        onTriggered : {
            previousFeedback.visible = !previousFeedback.visible
        }
    }
    Timer {
        id : nextFbTimer
        interval : 500
        // we need to show and hide the feedback
        triggeredOnStart : true
        onTriggered : {
            nextFeedback.visible = !nextFeedback.visible
        }
    }
}