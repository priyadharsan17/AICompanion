import unittest

try:
    from AICodeCompanion.Backend import CompanionBackend
except ImportError:  # pragma: no cover - environment without PySide6
    CompanionBackend = None


@unittest.skipIf(CompanionBackend is None, "PySide6 is not available")
class CompanionBackendTests(unittest.TestCase):
    def test_submit_prompt_updates_state_and_emits_response(self):
        backend = CompanionBackend()
        responses = []
        logs = []
        backend.responseGenerated.connect(responses.append)
        backend.logGenerated.connect(logs.append)
        initial_energy = backend.energyLevel

        backend.submit_prompt("launch protocol")

        self.assertEqual(backend.statusText, "AI CORE // PROCESSING COSMIC QUERY")
        self.assertEqual(backend.energyLevel, initial_energy - 4)
        self.assertEqual(logs, ["PILOT // launch protocol"])
        self.assertEqual(responses, ["SYNTH RESPONSE // LAUNCH PROTOCOL"])

    def test_blank_prompt_sets_validation_status(self):
        backend = CompanionBackend()
        logs = []
        backend.logGenerated.connect(logs.append)

        backend.submit_prompt("   ")

        self.assertEqual(backend.statusText, "AI CORE // ENTER A VALID COMMAND")
        self.assertEqual(logs, ["SYSTEM // Command rejected: empty input"])

    def test_submit_prompt_requires_energy(self):
        backend = CompanionBackend()
        logs = []
        responses = []
        backend.logGenerated.connect(logs.append)
        backend.responseGenerated.connect(responses.append)
        backend.energyLevel = 3

        backend.submit_prompt("launch protocol")

        self.assertEqual(backend.statusText, "AI CORE // LOW POWER - RECHARGE REQUIRED")
        self.assertEqual(logs, ["SYSTEM // Command rejected: insufficient energy"])
        self.assertEqual(responses, [])

    def test_recharge_updates_energy_and_status(self):
        backend = CompanionBackend()
        backend.energyLevel = 40
        starting_energy = backend.energyLevel

        backend.recharge()

        self.assertEqual(backend.energyLevel, starting_energy + 12)
        self.assertEqual(backend.statusText, "AI CORE // RECHARGING SOLAR MATRIX")


if __name__ == "__main__":
    unittest.main()
