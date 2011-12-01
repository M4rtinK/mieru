import Qt 4.7
import QtQuick 1.1
import Qt.labs.components 1.1
import com.nokia.meego 1.0
import com.nokia.extras 1.0

//Rectangle {
PageStackWindow {
    showStatusBar : false
    id : rootWindow
    anchors.fill : parent
    initialPage : MainView {
                      id : mainView
                      }

    property string statsText : ""

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

    function openFirstStartDialog() {
        firstStartDialog.open()
    }

    FileSelector {
      id: fileSelector;
      //anchors.fill : rootWindow
      onAccepted: readingState.openManga(selectedFile);
    }

    InfoBanner {
        id: notification
        timerShowTime : 5000
        height : rootWindow.height/5.0
    }

    QueryDialog {
        id : firstStartDialog
        icon : "image://icons/mieru.svg"
        titleText : "How to turn pages"
        message : "Tapp the <b>right half</b> of the screen to go to the <b>next page</b>.<br><br>"
              +" Tapp the <b>left half</b> to go to the <b>previous page</b>."
        acceptButtonText : "Don't show again"
        rejectButtonText : "OK"
        onAccepted: {
            options.set("QMLShowFirstStartDialog", false)
        }
    }
}