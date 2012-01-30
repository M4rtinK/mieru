import Qt 4.7
//import QtQuick 1.1
import org.maemo.fremantle 1.0

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