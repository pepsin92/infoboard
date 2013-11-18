import Qt 4.7
import QtQuick 1.0
import QtMultimediaKit 1.1

Rectangle {
    signal quit;
    signal finished;

    function resetAll() {
      timer.stop()
      image.visible = false
      video.visible = false
    }

    function showImage(url, time_sec) {
      resetAll()

      timer.interval = time_sec * 1000
      timer.start()
      image.source = url
      image.visible = true
    }

    function showVideo(url) {
      resetAll()

      video.source = url
      video.visible = true
      video.play()
    }

    anchors.fill: parent; color: "black"

    Timer {
      id: timer
      interval: 500
      repeat: false
      onTriggered: finished()
    }

    Video {
      id: video
      visible: false
      anchors.fill: parent
      smooth: true
      onStopped: finished()
      onError: finished()
      onPaused: finished()
    }

    Image {
      id: image
      visible: false
      anchors.fill: parent
      fillMode: Image.PreserveAspectFit
      smooth: true
    }

    MouseArea {
        anchors.fill: parent
        onClicked: quit()
    }

    focus: true
    Keys.onEscapePressed: quit()
}