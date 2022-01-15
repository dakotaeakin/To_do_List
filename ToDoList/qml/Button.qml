import QtQuick 2.1

Rectangle {
    width: 100
    height: 50
    color: mouse1.pressed ? "blue" : "#3664d4"
    radius: 15
    //Since the buttons are created on the fly,
    //we need to identify the button on which the user
    // has clicked. The id must be unique
    property int buttonId;
    property string taskName;
    property string butDate1;
    property string repeats;


    signal clicked(int buttonId, string taskName, string butDate1, string repeats);

    MouseArea {
        id: mouse1
        opacity: 0
        anchors.fill: parent
        onClicked: parent.clicked(parent.buttonId, parent.taskName, parent.butDate1, parent.repeats)
    }

    Text {
        id: text1
        text: qsTr(taskName)
        anchors.fill: parent
        font.pixelSize: 12
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
    }
}
