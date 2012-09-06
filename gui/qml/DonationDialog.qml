//DonationDialog.qml

import QtQuick 1.1
import com.nokia.meego 1.0

HeaderDialog {
    id : donationDialog
    titleText : qsTr("Choose a donation method:")
    content:Item {
        id: dialogContent
        width : parent.width
        Row {
            id : ppFlattrRow
            anchors.top : parent.top
            anchors.horizontalCenter : parent.horizontalCenter
            anchors.topMargin : 24
            spacing : 32
            PayPalButton {
                id : ppButton
                anchors.verticalCenter : parent.verticalCenter
                url : "https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=martin%2ekolman%40gmail%2ecom&lc=GB&item_name=Mieru%20project&currency_code=EUR&bn=PP%2dDonationsBF%3abtn_donate_LG%2egif%3aNonHosted"
            }
            FlattrButton {
                id : flattrButton
                anchors.verticalCenter : parent.verticalCenter
                url : "http://flattr.com/thing/830372/Mieru-flexible-manga-and-comic-book-reader"
            }
        }
        BitcoinButton {
            id : bitcoinButton
            anchors.top : ppFlattrRow.bottom
            anchors.topMargin : 24
            anchors.horizontalCenter : parent.horizontalCenter
            url : "1PPnoD4SyeQYgvhJ6L5xkjZ4qE4WMMCe1k"
            showBorder : true
        }
    }
}