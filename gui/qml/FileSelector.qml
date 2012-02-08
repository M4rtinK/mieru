import QtQuick 1.0
import com.nokia.meego 1.0
import Qt.labs.folderlistmodel 1.0

Dialog {
  id: fileSelector
  width : parent.width - 30
  property Style platformStyle: SelectionDialogStyle {}

  property variant filterList: [ "*" ]

  property string titleText: "File Selector"
  property variant folderModel: folderModel1
  property variant view: view1
  property string selectedFile: "";

  // go down one view
  function down(path) {
    // slide current view out to the left
    if (folderModel == folderModel1) {
      view = view2
      folderModel = folderModel2;
      view1.state = "exitLeft";
    } else {
      view = view1
      folderModel = folderModel1;
      view2.state = "exitLeft";
    }

    // and slide new view in from right
    view.x = fileSelector.width;
    view.state = "current";
    view.focus = true;
    folderModel.folder = path;
  }

  function up() {
    selectedFile = folderModel.folder;

    var path = folderModel.parentFolder;
    if (folderModel == folderModel1) {
      view = view2
      folderModel = folderModel2;
      view1.state = "exitRight";
    } else {
      view = view1
      folderModel = folderModel1;
      view2.state = "exitRight";
    }
    view.x = -fileSelector.width;
    view.state = "current";
    view.focus = true;
    folderModel.folder = path;
  }

  property Component delegate:
  Component {
    id: defaultDelegate

    Item {
      id: delegateItem
      property bool selected: filePath == selectedFile;

      height: fileSelector.platformStyle.itemHeight
      anchors.left: parent.left
      anchors.right: parent.right

      MouseArea {
        id: delegateMouseArea
        anchors.fill: parent;
        onPressed: selectedFile = filePath;
        onClicked:  {
          if (folderModel.isFolder(index))
             down(filePath);
          else
	     accept();
        }
      }

      Rectangle {
        id: backgroundRect
        anchors.fill: parent
        color: delegateItem.selected ? fileSelector.platformStyle.itemSelectedBackgroundColor : fileSelector.platformStyle.itemBackgroundColor
      }

      BorderImage {
        id: background
        anchors.fill: parent
        border { left: 22; top: 2; right: 2; bottom: 22 }
        source: delegateMouseArea.pressed ? fileSelector.platformStyle.itemPressedBackground :
        delegateItem.selected ? fileSelector.platformStyle.itemSelectedBackground :
                fileSelector.platformStyle.itemBackground
      }

      Text {
        id: itemText
        elide: Text.ElideRight
        color: delegateItem.selected ? fileSelector.platformStyle.itemSelectedTextColor : fileSelector.platformStyle.itemTextColor
        anchors.verticalCenter: delegateItem.verticalCenter
        anchors.left: parent.left
        anchors.right: folderModel.isFolder(index)?downArrow.left:parent.right
        anchors.leftMargin: fileSelector.platformStyle.itemLeftMargin
        anchors.rightMargin: fileSelector.platformStyle.itemRightMargin
        text: fileName;
        font: fileSelector.platformStyle.itemFont
      }

      // add "right" arrow to all directories
      Image {
        id: downArrow
        source: "image://theme/icon-m-common-drilldown-arrow-inverse"
        anchors.right: parent.right;
        anchors.verticalCenter: parent.verticalCenter
	visible: folderModel.isFolder(index)
      }
    }
  }

  title: Item {
    id: header
    height: fileSelector.platformStyle.titleBarHeight

    anchors.left: parent.left
    anchors.right: parent.right
    anchors.top: parent.top
    anchors.bottom: parent.bottom

    Item {
      id: labelField

      anchors.fill:  parent

      Item {
        id: labelWrapper
        anchors.left: parent.left
        anchors.right: closeButton.left

        anchors.bottom:  parent.bottom
        anchors.bottomMargin: fileSelector.platformStyle.titleBarLineMargin

        height: titleLabel.height

        Label {
          id: titleLabel
          x: fileSelector.platformStyle.titleBarIndent
          width: parent.width - closeButton.width
          font: fileSelector.platformStyle.titleBarFont
          color: fileSelector.platformStyle.commonLabelColor
          elide: fileSelector.platformStyle.titleElideMode
          text: fileSelector.titleText
        }
      }

      Image {
        id: closeButton
        anchors.bottom:  parent.bottom
        anchors.bottomMargin: fileSelector.platformStyle.titleBarLineMargin-6
        anchors.right: labelField.right

        opacity: closeButtonArea.pressed ? 0.5 : 1.0
        source: "image://theme/icon-m-common-dialog-close"

        MouseArea {
          id: closeButtonArea
          anchors.fill: parent
          onClicked:  {fileSelector.reject();}
        }
      }
    }

    Rectangle {
      id: headerLine

      anchors.left: parent.left
      anchors.right: parent.right

      anchors.bottom:  header.bottom

      height: 1

      color: "#4D4D4D"
    }
  }

  content: Item {
    id: contentField

    property int maxListViewHeight : visualParent ? visualParent.height * 0.87
        - fileSelector.platformStyle.titleBarHeight
        - fileSelector.platformStyle.contentSpacing - 50
       : fileSelector.parent ? fileSelector.parent.height * 0.87
        - fileSelector.platformStyle.titleBarHeight
        - fileSelector.platformStyle.contentSpacing - 50
     : 350

    height: maxListViewHeight
    width: fileSelector.width
    y : fileSelector.platformStyle.contentSpacing
    clip: true

    // we have two list views and are shifting them left and right
    // for nice animation

    Item {
      id: pathItem
      anchors.left: parent.left
      anchors.right: parent.right
      anchors.top:  parent.top
      height: fileSelector.platformStyle.itemHeight

      property bool canGoUp: folderModel.parentFolder != "" && folderModel.folder != folderModel.parentFolder

      enabled: canGoUp
      MouseArea {
        id: backArea
        anchors.fill: parent
        onClicked:  { up(); }
      }

      // add "left" arrow to go up one directory
      Image {
        id: backButton
        //source: "image://theme/icon-m-startup-back"
        // fix Fremantle CSSU icon availability
        source: platform.incompleteTheme() ? "image://theme/icon-m-toolbar-back-white-selected" :
        "image://theme/icon-m-startup-back"
        anchors.verticalCenter: parent.verticalCenter
        anchors.left: parent.left
	    opacity: parent.canGoUp?(backArea.pressed ? 0.5 : 1.0):0.4
      }

      Label {
        id: pathLabel
        font: fileSelector.platformStyle.itemFont
        color: fileSelector.platformStyle.itemTextColor
        elide: Text.ElideLeft

        text: folderModel.folder

        anchors.verticalCenter: parent.verticalCenter
        anchors.left: backButton.right
        anchors.right: parent.right

        anchors.leftMargin: fileSelector.platformStyle.itemLeftMargin
        anchors.rightMargin: fileSelector.platformStyle.itemRightMargin
      }

      Rectangle {
        id: pathLine

        anchors.left: parent.left
        anchors.right: parent.right

        anchors.bottom:  parent.bottom

        height: 1

        color: "#4D4D4D"
      }
    }

    Item {
      clip: true
      focus: true

      anchors.top: pathItem.bottom
      anchors.bottom: parent.bottom
      width: parent.width

      ListView {
        id: view1
        anchors.top: parent.top
        anchors.bottom: parent.bottom
        x: 0
        width: parent.width
        pressDelay: fileSelector.platformStyle.pressDelay

        FolderListModel {
          id: folderModel1
          nameFilters: filterList
        }

        model: folderModel1
        delegate: defaultDelegate

        states: [
          State {
            name: "current"
            PropertyChanges { target: view1; x: 0 }
          },
          State {
            name: "exitLeft"
            PropertyChanges { target: view1; x: -parent.width }
          },
          State {
            name: "exitRight"
            PropertyChanges { target: view1; x: parent.width }
          }
        ]
        transitions: [
          Transition {
            NumberAnimation { properties: "x"; duration: 250 }
          }
        ]
      }

      ListView {
        id: view2
        anchors.top: parent.top
        anchors.bottom: parent.bottom
        x: parent.width
        width: parent.width
        pressDelay: fileSelector.platformStyle.pressDelay

        FolderListModel {
          id: folderModel2
          nameFilters: filterList
        }

        model: folderModel2
        delegate: defaultDelegate

        states: [
          State {
            name: "current"
            PropertyChanges { target: view2; x: 0 }
          },
          State {
            name: "exitLeft"
            PropertyChanges { target: view2; x: -parent.width }
          },
          State {
            name: "exitRight"
            PropertyChanges { target: view2; x: parent.width }
          }
        ]
        transitions: [
          Transition {
            NumberAnimation { properties: "x"; duration: 250 }
          }
        ]
      }
    }

    MouseArea {
      property int xPos
      enabled: false

      anchors.fill: parent
      onPressed: { console.log("Pressed"); xPos = mouseX; mouse.accepted = false; }
      onReleased: {
        console.log("Swipe: " + mouseX + " " +xPos);
        if (mouseX - xPos > width/5) {
          up();
          mouse.accepted = false;
        }
      }
    }
  }
}

