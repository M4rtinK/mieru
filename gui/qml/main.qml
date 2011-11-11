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

    FileSelector {
      id: fileSelector;
      anchors.fill : rootWindow
      onAccepted: readingState.openManga(selectedFile);
      }

    InfoBanner {
        id: notification
        timerShowTime : 5000
        height : rootWindow.height/5.0
        }

    }