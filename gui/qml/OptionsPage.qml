//OptionPage.qml
//import Qt 4.7
import QtQuick 1.1
import com.nokia.meego 1.0

Page {
    tools: ToolBarLayout {
               ToolIcon { iconId: "toolbar-back"
                  onClicked: pageStack.pop()
                  }
               }
    Label { text : "options page"
        }

    }