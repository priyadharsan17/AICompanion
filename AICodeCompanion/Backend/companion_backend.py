from __future__ import annotations

from PySide6.QtCore import QObject, Property, Signal, Slot


class CompanionBackend(QObject):
    statusTextChanged = Signal()
    energyLevelChanged = Signal()
    logGenerated = Signal(str)
    responseGenerated = Signal(str)

    def __init__(self) -> None:
        super().__init__()
        self._status_text = "AI CORE // AWAITING COMMAND"
        self._energy_level = 72

    def get_status_text(self) -> str:
        return self._status_text

    def set_status_text(self, value: str) -> None:
        if self._status_text != value:
            self._status_text = value
            self.statusTextChanged.emit()

    statusText = Property(str, get_status_text, set_status_text, notify=statusTextChanged)

    def get_energy_level(self) -> int:
        return self._energy_level

    def set_energy_level(self, value: int) -> None:
        value = max(0, min(100, value))
        if self._energy_level != value:
            self._energy_level = value
            self.energyLevelChanged.emit()

    energyLevel = Property(int, get_energy_level, set_energy_level, notify=energyLevelChanged)

    @Slot(str)
    def submit_prompt(self, prompt: str) -> None:
        cleaned_prompt = prompt.strip()
        if not cleaned_prompt:
            self.set_status_text("AI CORE // ENTER A VALID COMMAND")
            self.logGenerated.emit("SYSTEM // Command rejected: empty input")
            return

        self.set_status_text("AI CORE // PROCESSING COSMIC QUERY")
        self.logGenerated.emit(f"PILOT // {cleaned_prompt}")
        self.set_energy_level(self._energy_level - 4)
        self.responseGenerated.emit(f"SYNTH RESPONSE // {cleaned_prompt.upper()}")

    @Slot()
    def recharge(self) -> None:
        self.set_energy_level(self._energy_level + 12)
        self.set_status_text("AI CORE // RECHARGING SOLAR MATRIX")
