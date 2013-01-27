//HistoryPage.qml
import QtQuick 1.1
import com.nokia.meego 1.0

Page {
    id : historyPage
    property bool deleteModeEnabled : false

    // update the history list model at startup
    Component.onCompleted : readingState.updateHistoryListModel()

    tools: ToolBarLayout {
        ToolIcon {
            id : histBack
            iconId : "toolbar-back"
            onClicked : pageStack.pop()
        }
        ToolButton {
            text : qsTr("Delete")
            visible : deleteModeEnabled
            // FIXME: buttons are not aligned vertically in toolbar
            anchors.verticalCenter : histBack.verticalCenter
            onClicked: {
                historyListModel.removeChecked()
                historyPage.deleteModeEnabled = false
                readingState.updateHistoryListModel()
            }
        }
        ToolButton {
            text: qsTr("Cancel")
            visible : deleteModeEnabled
            // FIXME: buttons are not aligned vertically in toolbar
            anchors.verticalCenter : histBack.verticalCenter
            onClicked: {
                rootWindow.abortnotify()
                historyListModel.uncheckAll()
                historyPage.deleteModeEnabled = false
                readingState.updateHistoryListModel()
            }
        }
        ToolIcon {
            id : histMenu
            iconId : "toolbar-view-menu"
            onClicked : historyMenu.open()
        }
    }

    Menu {
        id : historyMenu

        MenuLayout {
            MenuItem {
                text : historyPage.deleteModeEnabled ? qsTr("Do not delete items") : qsTr("Delete items")
                onClicked : {
                    historyPage.deleteModeEnabled = !historyPage.deleteModeEnabled
                    rootWindow.notify(qsTr("Select items to delete"))
                }
            }
            MenuItem {
                text : qsTr("Erase history")
                onClicked : {
                    eraseHistoryDialog.open()
                }
            }
        }
    }

	ListView {
		id: historyList
		anchors.fill : parent
		Label {
			visible : (historyList.count == 0) ? true : false
			text : "<b>" + qsTr("no entries") + "</b>"
			horizontalAlignment : Text.AlignHCenter
			anchors.verticalCenter : historyList.verticalCenter
			width : parent.width
			height : 80
		}
		model: historyListModel

		delegate: Component {
			Rectangle {
				width: historyList.width
				height: 80
				color: model.thing.checked?"#00B8F5":(index%2?"#eee":"#ddd")
				Label {
					id: title
					elide: Text.ElideRight
					text: model.thing.name
					color: (model.thing.checked?"white":"black")
					font.bold: true
					anchors.leftMargin: 10
					anchors.fill: parent
					verticalAlignment: Text.AlignVCenter
				}
				MouseArea {
					anchors.fill: parent
					onClicked: {
						if (historyPage.deleteModeEnabled) {
							historyListController.toggled(historyListModel, model.thing)
						}
						else {
							pageStack.pop()
							historyListController.thingSelected(model.thing)
						}
					}
				}
			}
		}
	}
	
    QueryDialog {
        id : eraseHistoryDialog
        titleText : qsTr("Erase history")
        message : qsTr("Do you want to erase the history of all mangas and comic books opened by Mieru?")
        acceptButtonText : qsTr("Erase")
        rejectButtonText : qsTr("Cancel")
        onAccepted : {
            readingState.eraseHistory()
            readingState.updateHistoryListModel()
        }
    }
}