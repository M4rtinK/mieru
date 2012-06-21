import Qt 4.7
import QtQuick 1.0
import org.maemo.fremantle 1.0
import org.maemo.extras 1.0

PageStackWindow {
    id : rootWindow
    anchors.fill : parent
    initialPage : MainView { id : mainView }

    property bool enableMangaMode : options.get("QMLMangaMode", false)
    property string statsText : ""
	// TODO: replace hardcoded value with actual status bar height
    property int statusBarHeight : 36
	
	showStatusBar : options.get("QMLShowStatusBar", false)
    showToolBar   : options.get("QMLRememberToolbarState", false) ? options.get("QMLToolbarState", true) : true

    function showPage(path, pageId) {
        mainView.showPage(path, pageId)
    }

    function setPageNumber(pageNumber) {
        mainView.pageNumber = pageNumber;
    }

    function setMaxPageNumber(maxPageNumber) {
        mainView.maxPageNumber = maxPageNumber;
    }

    // open a page and push it in the stack
    function openFile(file) {
        // create the Qt component based on the file/qml page to load.
        var component = Qt.createComponent(file)

        // if the page is ready to be managed it is pushed onto the stack
        if (component.status == Component.Ready)
            pageStack.push(component);
        else
            console.log("Error loading: " + component.errorString());
    }

    // handle Mieru shutdown
    function shutdown() {
        mainView.shutdown()
    }

    // open dialog with information about how to turn pages
    function openFirstStartDialog() {
        firstStartDialog.open()
    }

    FileSelector {
        id : fileSelector;
        onAccepted : readingState.openManga(selectedFile);
    }

    PageFitSelector {
        id : pageFitSelector
        onAccepted : mainView.setPageFitMode(pageFitMode)
    }

    InfoBanner {
        id : notification
        timerShowTime : 5000
        height : rootWindow.height / 5.0
        // prevent overlapping with status bar
        y : rootWindow.showStatusBar ? rootWindow.statusBarHeight + 8 : 8
    }
    function notify(text) {
        if(platform.getPlatformID() == "maemo5") {
            // TODO: fix notification on Fremantle and remove this
            console.log("NOTIFY: " + text);
        }
        else {
            notification.text = text;
            notification.show();
        }
    }

    QueryDialog {
        id : firstStartDialog
        icon : "image://icons/mieru.svg"
        titleText : qsTr("How to turn pages")
        message :   qsTr("Tap the <b>right half</b> of the screen to go to the <b>next page</b>.") + "<br><br>"
                  + qsTr("Tap the <b>left half</b> to go to the <b>previous page</b>.")
        acceptButtonText : qsTr("Don't show again")
        rejectButtonText : qsTr("OK")
        onAccepted : {
            options.set("QMLShowFirstStartDialog", false)
        }
    }
}
