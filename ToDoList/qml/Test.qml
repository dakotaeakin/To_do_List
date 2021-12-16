import QtQuick 2.15
import QtQuick.Controls 2.15

Window {
    id: window
    width: 400
    height: 400
    visible: true

    Rectangle {
        id: rectangle
        x: 100
        y: 160
        width: 200
        height: 200
        color: "#ffffff"

        Button {
            id: button
            x: -22
            y: -72
            text: qsTr("Test")
            onClicked: {
                createSomeButtons()
            }
        }
    }

    function buttonClicked(buttonId)
    {
        console.debug(buttonId);
        testModel.call(buttonId)
    }

    function createSomeButtons()
    {
        //Function creates 4 buttons
        var component = Qt.createComponent("Button.qml");
        for(var i=0;i<4;i++)
        {
            var buttonY = i*55; //Button height : 50 + 5 unit margin
            var button = component.createObject(rectangle,{"x":0,"y":buttonY,"buttonId":i+1});

            //Connect the clicked signal of the newly created button
            //to the event handler buttonClicked.
            button.clicked.connect(buttonClicked)
        }
    }
}
