//OptionPage.qml
import Qt 4.7
import QtQuick 1.0
import org.maemo.fremantle 1.0

Page {
    id : optionsPage
    anchors.fill : parent
    //anchors.verticalCenter : parent.verticalCenter
    anchors.topMargin : 15
    anchors.bottomMargin : 15
    anchors.leftMargin : 15
    anchors.rightMargin : 15

    Flickable {
        anchors.fill : parent
        contentWidth: optionsPage.width
        contentHeight: optionsColumn.height
        Column {
            id : optionsColumn
            spacing : 30
            width : optionsPage.width



            LineText {
                width : optionsPage.width
                text : qsTr("Page view")
            }

            Label {
                text : "<b>" + qsTr("Rotation") + "</b>"
            }
            ButtonRow {
              // synchronize with current orientation lock
              Component.onCompleted : {
                  if (mainView.orientationLock == PageOrientation.Automatic) {
                      checkedButton = bAuto
                  } else if (mainView.orientationLock == PageOrientation.LockPortrait) {
                      checkedButton = bPortrait
                  } else {
                      checkedButton = bLandscape
                  }
              }
              Button {
                id : bAuto
                text : qsTr("auto")
                onClicked : {
                    options.set("QMLmainViewRotation", "auto")
                    mainView.orientationLock = PageOrientation.Automatic
                }
              }
              Button {
                id : bPortrait
                text : qsTr("portrait")
                onClicked : {
                    options.set("QMLmainViewRotation", "portrait")
                    mainView.orientationLock = PageOrientation.LockPortrait
                }
              }
              Button {
                id : bLandscape
                text : qsTr("landscape")
                onClicked : {
                    options.set("QMLmainViewRotation", "landscape")
                    mainView.orientationLock = PageOrientation.LockLandscape
                }
              }
            }

            SwitchWithText {
                text : "<b>" + qsTr("Show status bar") + "</b>"
                checked : rootWindow.showStatusBar
                onCheckedChanged : {
                    rootWindow.showStatusBar = checked
                    options.set("QMLShowStatusBar", checked)
                }
            }
            SwitchWithText {
                text : "<b>" + qsTr("Remember toolbar state") + "</b>"
                checked : options.get("QMLRememberToolbarState", false)
                onCheckedChanged : {
                    options.set("QMLRememberToolbarState", checked)
                }
            }

            Label {
                text : "<b>" + qsTr("Fullscreen button opacity") + "</b>"
            }
            Slider {
                value : mainView.fullscreenButtonOpacity
                minimumValue: 0.0
                maximumValue: 1.0
                stepSize: 0.1
                valueIndicatorText : Math.round(value*100) + " %"
                valueIndicatorVisible: true
                onPressedChanged : {
                    var outputValue
                    //completely transparent items don't receive events
                    if (value == 0) {                        
                        outputValue = 0.01
                    } else {
                        /* round away small fractions
                        that were created by the assured lowest value
                        */
                        outputValue = Math.round(value*100)/100
                    }
                    //update once dragging stops
                    options.set("QMLFullscreenButtonOpacity", outputValue)
                    mainView.fullscreenButtonOpacity = outputValue
                }

            }
            
            LineText {
                width : optionsPage.width
                text : qsTr("Paging options")
            }
            
            Label {
                text : "<b>" + qsTr("Paging mode") + "</b>"
            }
            ButtonRow {
              Component.onCompleted : {
                  var pm = options.get("QMLPagingMode", "screen")
                  if (pm == "screen") {
                      checkedButton = bPMScreen
                  } else if (pm == "edges") {
                      checkedButton = bPMEdges
                  } else {
                      checkedButton = bPMScreen
                  }
              }
              Button {
                id : bPMScreen
                text : qsTr("Whole screen")
                onClicked : {
                    options.set("QMLPagingMode", "screen")
                    mainView.pagingMode = "screen"
                }
              }
              Button {
                id : bPMEdges
                text : qsTr("On edges")
                onClicked : {
                    options.set("QMLPagingMode", "edges")
                    mainView.pagingMode = "edges"
                }
              }
            }
            
            SwitchWithText {
                text : "<b>" + qsTr("Show paging feedback") + "</b>"
                checked : mainView.pagingFeedback
                onCheckedChanged : {
                    mainView.pagingFeedback = checked
                    options.set("QMLPagingFeedback", checked)
                }
            }

            LineText {
                width : optionsPage.width
                text : qsTr("Page scaling")
            }
            SelectorButtonWithText {
                text : "<b>" + qsTr("Page fit mode") + "</b>"
                buttonText : mainView.pageFitMode
                selector : pageFitSelector
            }
            
            LineText {
                width : optionsPage.width
                text : qsTr("Miscellaneous")
            }
            SwitchWithText {
                text : "<b>" + qsTr("Manga reading mode") + "</b>"
                checked : rootWindow.enableMangaMode
                onCheckedChanged : {                                                    
                    rootWindow.enableMangaMode = checked                                  
                    options.set("QMLMangaMode", checked)                            
                } 
            }
        }
    }

    tools: ToolBarLayout {
       ToolIcon { iconId: "toolbar-back"
          onClicked: pageStack.pop()
          }
       }
    }
