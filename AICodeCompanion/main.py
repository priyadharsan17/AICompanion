from __future__ import annotations

import sys
from pathlib import Path

from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine

from Backend import CompanionBackend


if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()

    backend = CompanionBackend()
    engine.rootContext().setContextProperty("backend", backend)

    qml_path = Path(__file__).resolve().parent / "Screens" / "Main.qml"
    engine.load(str(qml_path))

    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec())
