import QtQuick 2.12
import QtQuick.Timeline 1.0

Rectangle {
    width: 300
    height: 220
    color: "#f0f0f0"

    Image {
        id: playr_purple1
        x: 0
        y: 107
        source: "../images/playr-purple1.png"
        fillMode: Image.PreserveAspectFit
    }


    Image {
        id: playr_no_purple
        x: 0
        y: 45
        source: "../images/playr-no-purple.png"
        fillMode: Image.PreserveAspectFit
    }

    Image {
        id: key
        x: 23
        y: 36
        width: 175
        height: 172
        source: "../images/smart-key.svg"
        fillMode: Image.PreserveAspectFit
        rotation: -40
    }


    Image {
        id: playr_purple2
        x: 27
        y: 107
        source: "../images/playr-purple2.png"
        fillMode: Image.PreserveAspectFit
    }

    Timeline {
        id: timeline
        animations: [
            TimelineAnimation {
                id: timelineAnimation
                duration: 2000
                loops: 1
                running: true
                to: 2000
                from: 0
            }
        ]
        startFrame: 0
        endFrame: 2000
        enabled: true

        KeyframeGroup {
            target: key
            property: "rotation"
            Keyframe {
                value: -40
                frame: 0
            }
            Keyframe {
                value: 40
                frame: 2000
            }
        }

        KeyframeGroup {
            target: key
            property: "x"
            Keyframe {
                value: 215
                frame: 0
            }

            Keyframe {
                value: 23
                frame: 2000
            }
        }

        KeyframeGroup {
            target: key
            property: "y"
            Keyframe {
                value: -199
                frame: 0
            }

            Keyframe {
                value: 36
                frame: 2000
            }
        }
    }






}

/*##^##
Designer {
    D{i:3;timeline_expanded:true}D{i:8;property:"rotation";target:"key"}D{i:5}
}
##^##*/
