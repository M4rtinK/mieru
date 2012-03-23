import Qt 4.7
import QtQuick 1.1
import com.nokia.meego 1.0
import com.nokia.extras 1.0

PageStackWindow {
    showStatusBar : options.get("QMLShowStatusBar", false)
    showToolBar : options.get("QMLRememberToolbarState", false) ? options.get("QMLToolbarState", true) : true
    id : rootWindow
    anchors.fill : parent
    initialPage : MainView {
                      id : mainView
                      }

    property string statsText : ""
    property int statusBarHeight : 36
    /* TODO: replace hardcoded value
    with actual status bar height */

    function showPage(path, pageId) {
        mainView.showPage(path, pageId)
        }

    function setPageNumber(pageNumber) {
        mainView.pageNumber = pageNumber;
        }

    function setMaxPageNumber(maxPageNumber) {
        mainView.maxPageNumber = maxPageNumber;
        }

    // ** trigger notifications
    function notify(text) {
        notification.text = text;
        notification.show();
        }

    // ** Open a page and push it in the stack
    function openFile(file) {
        // Create the Qt component based on the file/qml page to load.
        var component = Qt.createComponent(file)
        // If the page is ready to be managed it is pushed onto the stack
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
      id: fileSelector;
      //anchors.fill : rootWindow
      onAccepted: readingState.openManga(selectedFile);
    }

    PageFitSelector {
      id : pageFitSelector
      onAccepted: mainView.setPageFitMode(pageFitMode)
    }

    InfoBanner {
        id: notification
        timerShowTime : 5000
        height : rootWindow.height/5.0
        // prevent overlapping with status bar
        y : rootWindow.showStatusBar ? rootWindow.statusBarHeight + 8 : 8

    }

    QueryDialog {
        id : firstStartDialog
        icon : "image://icons/mieru.svg"
        titleText : "How to turn pages"
        message : "Tap the <b>right half</b> of the screen to go to the <b>next page</b>.<br><br>"
              +" Tap the <b>left half</b> to go to the <b>previous page</b>."
        acceptButtonText : "Don't show again"
        rejectButtonText : "OK"
        onAccepted: {
            options.set("QMLShowFirstStartDialog", false)
        }
    }
}