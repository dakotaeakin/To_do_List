import QtQuick 2.1

Rectangle {
    width: 100
    height: 50
    color:"blue"
    //Since the buttons are created on the fly,
    //we need to identify the button on which the user
    // has clicked. The id must be unique
    property string buttonId;
    signal clicked(string buttonId);

    MouseArea {
        anchors.fill: parent
        onClicked:parent.clicked(parent.buttonId)
    }
}
