import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

ApplicationWindow {
    id: root
    visible: true
    width: 1080
    height: 720
    title: "AI Code Companion"
    color: "#040712"

    property color panelColor: "#0d1633"
    property color accentColor: "#28d7ff"
    property color warmAccent: "#ff4fd8"

    Rectangle {
        anchors.fill: parent
        gradient: Gradient {
            GradientStop { position: 0.0; color: "#030711" }
            GradientStop { position: 1.0; color: "#081739" }
        }
    }

    Rectangle {
        anchors.fill: parent
        color: "transparent"
        border.width: 2
        border.color: "#205890"
        radius: 12
        anchors.margins: 14
    }

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 24
        spacing: 18

        Rectangle {
            Layout.fillWidth: true
            Layout.preferredHeight: 84
            radius: 12
            color: panelColor
            border.color: accentColor
            border.width: 1

            RowLayout {
                anchors.fill: parent
                anchors.margins: 14

                ColumnLayout {
                    Layout.fillWidth: true

                    Label {
                        text: "AICODE COMPANION"
                        font.pixelSize: 28
                        font.bold: true
                        color: accentColor
                    }
                    Label {
                        text: backend ? backend.statusText : "AI CORE // AWAITING COMMAND"
                        color: "#a9e6ff"
                        font.pixelSize: 14
                    }
                }

                Rectangle {
                    Layout.preferredWidth: 140
                    Layout.preferredHeight: 54
                    color: "#14274d"
                    radius: 10
                    border.color: warmAccent
                    border.width: 1

                    Column {
                        anchors.centerIn: parent
                        spacing: 2

                        Label {
                            text: "ENERGY"
                            color: "#f1d7ff"
                            font.pixelSize: 12
                            horizontalAlignment: Text.AlignHCenter
                        }
                        Label {
                            text: (backend ? backend.energyLevel : 0) + "%"
                            color: warmAccent
                            font.bold: true
                            font.pixelSize: 20
                            horizontalAlignment: Text.AlignHCenter
                        }
                    }
                }
            }
        }

        Rectangle {
            Layout.fillWidth: true
            Layout.fillHeight: true
            radius: 12
            color: panelColor
            border.color: "#255588"
            border.width: 1

            ColumnLayout {
                anchors.fill: parent
                anchors.margins: 16
                spacing: 12

                Label {
                    text: "COMMAND FEED"
                    color: accentColor
                    font.pixelSize: 16
                    font.bold: true
                }

                ListView {
                    id: feed
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    model: logModel
                    clip: true
                    spacing: 8

                    delegate: Rectangle {
                        width: feed.width
                        radius: 8
                        color: "#0f1f3f"
                        border.color: index % 2 === 0 ? "#355f95" : "#6a3f8f"
                        border.width: 1
                        implicitHeight: msg.implicitHeight + 16

                        Label {
                            id: msg
                            anchors.fill: parent
                            anchors.margins: 8
                            color: "#d9f6ff"
                            text: model.text
                            wrapMode: Text.WordWrap
                        }
                    }
                }

                RowLayout {
                    Layout.fillWidth: true
                    spacing: 10

                    TextField {
                        id: promptInput
                        Layout.fillWidth: true
                        placeholderText: "Transmit your command"
                        color: "#ecf8ff"
                        placeholderTextColor: "#7fa8d6"
                        background: Rectangle {
                            color: "#09152e"
                            border.color: "#355f95"
                            radius: 8
                        }
                        onAccepted: sendButton.clicked()
                    }

                    Button {
                        id: sendButton
                        text: "SEND"
                        onClicked: {
                            if (backend) {
                                backend.submit_prompt(promptInput.text)
                            }
                            if (promptInput.text.trim().length > 0) {
                                logModel.append({ text: "PILOT // " + promptInput.text })
                            }
                            promptInput.clear()
                        }
                        background: Rectangle {
                            color: "#102a56"
                            border.color: accentColor
                            border.width: 1
                            radius: 8
                        }
                        contentItem: Text {
                            text: sendButton.text
                            color: accentColor
                            font.bold: true
                            horizontalAlignment: Text.AlignHCenter
                            verticalAlignment: Text.AlignVCenter
                        }
                    }

                    Button {
                        id: rechargeButton
                        text: "RECHARGE"
                        onClicked: if (backend) backend.recharge()
                        background: Rectangle {
                            color: "#2a1a48"
                            border.color: warmAccent
                            border.width: 1
                            radius: 8
                        }
                        contentItem: Text {
                            text: rechargeButton.text
                            color: warmAccent
                            font.bold: true
                            horizontalAlignment: Text.AlignHCenter
                            verticalAlignment: Text.AlignVCenter
                        }
                    }
                }
            }
        }
    }

    ListModel {
        id: logModel
        ListElement { text: "SYSTEM // Nebula navigation systems online" }
        ListElement { text: "SYSTEM // Quantum comms channel stabilized" }
    }

    Connections {
        target: backend
        function onResponseGenerated(responseText) {
            logModel.append({ text: responseText })
        }
    }
}
