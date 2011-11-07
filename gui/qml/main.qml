import Qt 4.7
import QtQuick 1.1
import Qt.labs.components 1.1
import com.nokia.meego 1.0
import com.nokia.extras 1.0

//Rectangle {
PageStackWindow {
    showStatusBar : false
    //showToolBar : true
    id : rootWindow
    anchors.fill : parent
    initialPage : MainView {
                      id : mainView
                      }

    function showPage(path, pageId) {
        mainView.showPage(path, pageId)
        }

    function removeToolbars() {
      console.log("RRRRRRR remove toolbars");
      commonTools.visible = false;
      rootWindow.showStatusBar = false;
      rootWindow.showToolBar = false;
      }

    // ** trigger notifications
    function notify(text) {
        notification.text = text;
        notification.show();
        }

/*    FileSelector { id: fileSelector;
      anchors.fill : rootWindow
      onAccepted: console.log("Acepted: "+ selectedFile);
      }
*/
    InfoBanner {
        id: notification
        timerShowTime : 5000
        height : rootWindow.height/5.0
        }

    }