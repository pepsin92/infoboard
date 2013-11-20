import Qt 4.7
import QtQuick 1.0
import QtMultimediaKit 1.1

Rectangle {
    signal quit;
    signal finished;

    function resetAll() {
      image.visible = false
      video.visible = false
    }

    function showImage(url) {
      resetAll()

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