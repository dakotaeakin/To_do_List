import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 6.0




Window {
    id: window
    width: 800
    height: 480
    visible: true

//Properties:
    //Popup Properties:
    property bool popupClickOffVis: false
    property bool popupVis: false
    property bool popupAddTaskVis: false

    //Function properties:
    property int i: 1

//Functions:
    //Add task functions:
    function addTaskX(task)
    {
        console.log(task)
        testModel.addTaskPy(task)
    }

    function buttonClicked(buttonId)
    {
        console.debug(buttonId, taskName);
    }
    function createButton()
    {
        var component = Qt.createComponent("Button.qml");
        var assignMargin
        var id = `button${i}`
        if (i == 1){
            assignMargin = 20
        } else{
            assignMargin = i * 90
        }


        var button = component.createObject(taskColumn,{
                                                "x":0,
                                                "buttonId": id,
                                                "taskName": "Do the dishes dammit!",
                                                "anchors.left": taskColumn.left,
                                                "anchors.right": taskColumn.right,
                                                "anchors.rightMargin": 20,
                                                "anchors.leftMargin": 20
                                            });

        //Connect the clicked signal of the newly created button
        //to the event handler buttonClicked.
        buttonAddTask.clicked.connect(buttonClicked)
        i += 1

    }
    Connections {
        target: buttonPopupAddTask
        onClicked: {
            addTaskX(textEdit.text)
        }
    }

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
            width: 160
            height: 88
            anchors.verticalCenter: parent.verticalCenter
            source: "images/VooDoo.png"
            mipmap: true
            sourceSize.height: 200
            sourceSize.width: 400
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
        }

    }




    Rectangle {
        id: taskBox
        color: "#ffffff"
        anchors.left: rectangleLeftMenu.right
        anchors.right: parent.right
        anchors.top: rectangleTopMenu.bottom
        anchors.bottom: parent.bottom
        anchors.leftMargin: 0
        anchors.topMargin: 0
        anchors.bottomMargin: 0
        anchors.rightMargin: 0



        Column {
            id: taskColumn
            anchors.fill: parent
            topPadding: 20
            spacing: 5

            Button {
                id: buttonAddTask
                visible: true
                text: qsTr("Add New Task")
                anchors.left: parent.left
                Layout.alignment: Qt.AlignLeft | Qt.AlignTop
                highlighted: false
                flat: false
                anchors.leftMargin: 20

                Connections {
                    target: buttonAddTask
                    onClicked: {
                        popupClickOffVis = true
                        popupVis = true
                        popupAddTaskVis = true
                    }
                }
            }
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


    Rectangle {
        id: popupClickOff
        opacity: 0.5
        visible: popupClickOffVis
        color: "#5f5e5e"
        anchors.fill: parent
        layer.enabled: false
        clip: false

        Button {
            id: buttonClickOff
            opacity: 0
            text: qsTr("")
            anchors.fill: parent
            visible: popupClickOffVis

            Connections {
                target: buttonClickOff
                onClicked: {
                    popupClickOffVis = false
                    popupVis = false
                    popupAddTaskVis = false
                }
            }
        }
    }

    Rectangle {
        id: popup
        width: 400
        height: 200
        visible: popupVis
        color: "#fefefe"
        anchors.verticalCenter: parent.verticalCenter
        anchors.horizontalCenter: parent.horizontalCenter

        Rectangle {
            id: addTask
            color: "#ffffff"
            anchors.fill: parent
            visible: popupAddTaskVis

            TextEdit {
                id: textEdit
                x: 160
                text: qsTr("Enter your task here!
")
                anchors.left: parent.left
                anchors.right: parent.right
                anchors.top: parent.top
                anchors.bottom: parent.bottom
                font.pixelSize: 16
                z: 0
                clip: false
                anchors.bottomMargin: 80
                anchors.rightMargin: 20
                anchors.leftMargin: 20
                anchors.topMargin: 20
            }

            Button {
                id: buttonPopupAddTask
                x: 138
                text: qsTr("Add Task")
                anchors.left: parent.left
                anchors.right: parent.right
                anchors.top: textEdit.bottom
                anchors.bottom: parent.bottom
                anchors.topMargin: 20
                anchors.rightMargin: 150
                anchors.leftMargin: 150
                anchors.bottomMargin: 20





                }
            }
        }

}


