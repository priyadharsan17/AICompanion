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
        backend.responseGenerated.connect(responses.append)

        backend.submit_prompt("launch protocol")

        self.assertEqual(backend.statusText, "AI CORE // PROCESSING COSMIC QUERY")
        self.assertEqual(backend.energyLevel, 68)
        self.assertEqual(responses, ["SYNTH RESPONSE // LAUNCH PROTOCOL"])

    def test_blank_prompt_sets_validation_status(self):
        backend = CompanionBackend()

        backend.submit_prompt("   ")

        self.assertEqual(backend.statusText, "AI CORE // ENTER A VALID COMMAND")


if __name__ == "__main__":
    unittest.main()
