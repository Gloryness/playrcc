import QtQuick 2.0

Rectangle {
    width: 30
    height: 30
    color: "#f0f0f0"

    AnimatedImage {
        id: loading
        x: 0
        y: 0
        width: 30
        height: 30
        fillMode: Image.PreserveAspectFit
        mirror: false
        asynchronous: false
        paused: false
        playing: true
        source: "../images/loading.gif"
    }
}

/*##^##
Designer {
    D{i:0;formeditorZoom:1.25}
}
##^##*/
