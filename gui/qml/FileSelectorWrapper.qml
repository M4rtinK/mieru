//FileSelectorWrapper.qml
// -> only loads the file selector dialog & it's model once needed
// -> it should also get around the limitations of the FolderListModel,
// that won't notice new files unless recreated

import QtQuick 2.0

Item {
    id : wrapper
    property bool dialogNeeded : false
    property string selectedFile
    property string initialPath : "."
    signal accepted(string selectedFile)
    Loader {
        id : fileSelectorLoader
        source : dialogNeeded ? "FileSelector.qml" : ""
        onLoaded : {
            // set the initial path & open the dialog
            item.down(initialPath)
            console.log("file selector loaded on: " + initialPath)
            item.open()
        }
    }
    Connections {
        target : fileSelectorLoader.item
        onAccepted : {
            console.log("wrapped file-selector accepted on path:")
            console.log(fileSelectorLoader.item.selectedFile)
            // trigger the onAccepted signal
            wrapper.accepted(fileSelectorLoader.item.selectedFile)
            // unload the dialog
            wrapper.dialogNeeded = false
        }
        onRejected : {
            console.log("wrapped file-selector rejected")
            // unload the dialog
            wrapper.dialogNeeded = false
        }

    }

    // remember the starting path
    function down(path) {
        initialPath = path
    }

    // open the dialog on the starting path
    function open() {
        dialogNeeded = true
    }

}
