//OptionPage.qml
//import Qt 4.7
import QtQuick 1.1
import com.nokia.meego 1.0

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

            LineText {
                width : optionsPage.width
                text : "Page view"
            }

            SwitchWithText {
                text : "<b>Show statusbar</b>"
                width : optionsPage.width
                checked : rootWindow.showStatusBar
                onCheckedChanged : {
                    rootWindow.showStatusBar = checked
                    options.set("QMLShowStatusBar", checked)
                }
            }
            SwitchWithText {
                text : "<b>Remeber toolbar state</b>"
                width : optionsPage.width
                checked : options.get("QMLRememberToolbarState", false)
                onCheckedChanged : {
                    options.set("QMLRememberToolbarState", checked)
                }
            }

            Label {
                text : "Fullscreen button opacity"
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
                        that were created by the asusred lowest value
                        */
                        outputValue = Math.round(value*100)/100
                    }
                    //update once dragging stopps
                    options.set("QMLFullscreenButtonOpacity", outputValue)
                    mainView.fullscreenButtonOpacity = outputValue
                }

            }

            LineText {
                width : optionsPage.width
                text : "Page scaling"
            }

            SwitchWithText {
                text : "<b>Remeber scale</b>"
                width : optionsPage.width
                checked : mainView.rememberScale
                onCheckedChanged : {
                    mainView.rememberScale = checked
                    options.set("QMLRememberScale", checked)
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