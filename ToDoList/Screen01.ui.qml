import QtQuick
import QtQuick.Controls
import ToDoList 1.0

Rectangle {
    id: rectangle1
    width: Constants.width
    height: Constants.height

    color: Constants.backgroundColor

    Rectangle {
        id: rectangleTopMenu
        x: 300
        height: 66
        color: "#ffffff"
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.top: parent.top
        anchors.topMargin: 0
        anchors.rightMargin: 0
        anchors.leftMargin: 0

        Button {
            id: buttonLeftMenu
            x: 24
            text: qsTr("Button")
            anchors.verticalCenter: parent.verticalCenter
        }

        Image {
            id: imageLogo
            x: 130
            width: 135
            height: 46
            anchors.verticalCenter: parent.verticalCenter
            source: "images/place_holder.png"
            anchors.verticalCenterOffset: 0
            fillMode: Image.PreserveAspectFit
        }

        Button {
            id: buttonGoToToday
            x: 271
            text: qsTr("Button")
            anchors.verticalCenter: parent.verticalCenter
            anchors.verticalCenterOffset: 0
        }

        Button {
            id: buttonPrev
            x: 421
            width: 20
            height: 20
            text: qsTr("<")
            anchors.verticalCenter: parent.verticalCenter
        }

        Button {
            id: buttonNext
            x: 459
            width: 20
            height: 20
            text: qsTr(">")
            anchors.verticalCenter: parent.verticalCenter
            anchors.verticalCenterOffset: 0
        }

        Button {
            id: buttonDate
            x: 517
            text: qsTr("Button")
            anchors.verticalCenter: parent.verticalCenter
        }

        Button {
            id: buttonDisplay
            x: 639
            text: qsTr("Button")
            anchors.verticalCenter: parent.verticalCenter
        }

        Button {
            id: buttonSettings
            x: 760
            width: 25
            height: 19
            text: qsTr("Button")
            anchors.verticalCenter: parent.verticalCenter

            Connections {
                target: buttonSettings
                onClicked: createButton()
            }
        }
    }

    Rectangle {
        id: rectangle
        color: "#ffffff"
        anchors.left: rectangleLeftMenu.right
        anchors.right: parent.right
        anchors.top: rectangleTopMenu.bottom
        anchors.bottom: parent.bottom
        anchors.leftMargin: 0
        anchors.topMargin: 0
        anchors.bottomMargin: 0
        anchors.rightMargin: 0


        Button {
            id: button
            x: 333
            y: 77
            text: qsTr("Button")
            anchors.left: parent.left
            anchors.right: parent.right
            highlighted: false
            flat: false
            anchors.rightMargin: 20
            anchors.leftMargin: 20
        }
    }

    Rectangle {
        id: rectangleLeftMenu
        width: 0
        color: "#ffffff"
        anchors.left: parent.left
        anchors.top: rectangleTopMenu.bottom
        anchors.bottom: parent.bottom
        anchors.bottomMargin: 0
        anchors.leftMargin: 0
        anchors.topMargin: 0

        Rectangle {
            id: rectangle3
            x: 40
            height: 84
            color: "#2e2a4b"
            anchors.verticalCenter: parent.verticalCenter
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.rightMargin: 51
            anchors.leftMargin: 51
        }
    }
}
