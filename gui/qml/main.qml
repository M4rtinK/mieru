//main.qml
import QtQuick 1.1
import com.nokia.meego 1.0
import com.nokia.extras 1.0

PageStackWindow {
    id : rootWindow
    anchors.fill : parent
    initialPage : MainView { id : mainView }

    property bool enableMangaMode : options.get("QMLMangaMode", false)
    property string statsText : ""

    // disable switch & close buttons on Fremantle
    // -> has no effect on other platforms
    property bool allowSwitch : false
    property bool allowClose : false

    // TODO: replace hardcoded value with actual status bar height
    property int statusBarHeight : 36
	
    showStatusBar : options.get("QMLShowStatusBar", false)
    showToolBar   : options.get("QMLRememberToolbarState", false) ? options.get("QMLToolbarState", true) : true

    function showPage(path, pageId) {
        mainView.showPage(path, pageId)
    }

    function setPageNumber(pageNumber) {
        mainView.pageNumber = pageNumber
    }

    function setMaxPageNumber(maxPageNumber) {
        mainView.maxPageNumber = maxPageNumber
    }

    // open a page and push it in the stack
    function openFile(file) {
        // create the Qt component based on the file/qml page to load.
        var component = Qt.createComponent(file)

        // if the page is ready to be managed it is pushed onto the stack
        if (component.status == Component.Ready)
            pageStack.push(component);
        else
            console.log("Error loading: " + component.errorString())
    }

    // handle Mieru shutdown
    function shutdown() {
        mainView.shutdown()
    }

    // Open a dialog with information about how to turn pages
    function openFirstStartDialog() {
        firstStartDialog.open()
    }

    // Open a dialog with information about what's new
    function openReleaseNotesDialog() {
        // load release notes text
        whatsNewDialog.releaseNotesText = readingState.getReleaseNotes()
        // open the dialog
        whatsNewDialog.open()
    }

    FileSelector {
        id : fileSelector
        onAccepted : readingState.openManga(selectedFile)
    }

    PageFitSelector {
        id : pageFitSelector
        onAccepted : mainView.setPageFitMode(pageFitMode)
    }

    PageFitSelector {
        id : tempPageFitSelectorClick
        onAccepted : mainView.setPageFitModeTemp(pageFitMode, "click")
        Component.onCompleted : addNop()
    }
    PageFitSelector {
        id : tempPageFitSelectorDoubleclick
        onAccepted : mainView.setPageFitModeTemp(pageFitMode, "doubleclick")
        Component.onCompleted : addNop()
    }
    function notify(text) {
        console.log("notification: " % text)
        notification.text = text;
        notification.show()
    }
    function abortnotify() {
        notification.hide()
    }

    // First start dialog
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

    // What's new dialog
    WhatsNewDialog {
        id : whatsNewDialog
    }

    InfoBanner {
        id : notification
        timerShowTime : 5000
        height : rootWindow.height / 5.0
        // add margin and prevent overlapping with status bar, if the bar is visible
        y : rootWindow.showStatusBar ? rootWindow.statusBarHeight + 8 : 8
    }

}