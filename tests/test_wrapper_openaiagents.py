# Copyright (c) Microsoft. All rights reserved.


import unittest

from microsoft_agents_a365.observability.core import configure
from microsoft_agents_a365.observability.extensions.openai import KairoInstrumentorOpenAIAgents


class TestKairoInstrumentorOpenAIAgents(unittest.TestCase):
    """Unit tests for KairoInstrumentorOpenAIAgents class."""

    @classmethod
    def setUpClass(cls):
        """Set up test environment once for all tests."""
        # Configure Kairo for testing
        configure(
            service_name="test-service-openaiAgents",
            service_namespace="test-namespace-openaiAgents",
        )

    def test_instrumentor_initialization(self):
        """Test 1: Verify KairoInstrumentorOpenAIAgents can be initialized successfully."""
        try:
            # Test basic initialization
            instrumentor = KairoInstrumentorOpenAIAgents()

            # Verify the object was created
            self.assertIsNotNone(instrumentor)
            self.assertIsInstance(instrumentor, KairoInstrumentorOpenAIAgents)

            # Check if it has expected attributes/methods
            self.assertTrue(hasattr(instrumentor, "__init__"))

            print("✅ Test 1 passed: KairoInstrumentorOpenAIAgents initialized successfully")

        except Exception as e:
            self.fail(f"KairoInstrumentorOpenAIAgents initialization failed: {e}")

    def test_instrumentor_methods_exist(self):
        """Test 2: Verify KairoInstrumentorOpenAIAgents has expected methods."""
        instrumentor = KairoInstrumentorOpenAIAgents()

        # Test for common instrumentor methods that might exist
        expected_methods = ["__init__", "_instrument"]

        for method_name in expected_methods:
            with self.subTest(method=method_name):
                self.assertTrue(
                    hasattr(instrumentor, method_name),
                    f"Method '{method_name}' should exist on KairoInstrumentorOpenAIAgents",
                )

        # Test that the object responds to dir() without error
        methods_and_attrs = dir(instrumentor)
        self.assertIsInstance(methods_and_attrs, list)
        self.assertGreater(len(methods_and_attrs), 0)

        print("✅ Test 2 passed: KairoInstrumentorOpenAIAgents has expected methods")


class TestKairoInstrumentorIntegration(unittest.TestCase):
    """Integration tests for the instrumentor with the broader Kairo system."""

    def setUp(self):
        """Set up each test with a fresh Kairo configuration."""
        configure(
            service_name="integration-test-service",
            service_namespace="integration-test-namespace",
        )

    def test_instrumentor_with_kairo_configured(self):
        """Test instrumentor behavior when Kairo is properly configured."""
        from microsoft_agents_a365.observability.core import get_tracer, is_configured

        # Verify Kairo is configured
        self.assertTrue(is_configured())

        # Get tracer to ensure it works
        tracer = get_tracer()
        self.assertIsNotNone(tracer)

        # Now create instrumentor
        instrumentor = KairoInstrumentorOpenAIAgents()
        self.assertIsNotNone(instrumentor)

        print("✅ Integration test passed: Instrumentor works with configured Kairo")


def run_comprehensive_tests():
    """Run all tests with detailed output."""
    print("🧪 Running comprehensive Kairo OpenAI Agents Instrumentor tests...")
    print("=" * 80)

    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add test classes
    suite.addTests(loader.loadTestsFromTestCase(TestKairoInstrumentorOpenAIAgents))
    suite.addTests(loader.loadTestsFromTestCase(TestKairoInstrumentorIntegration))

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Summary
    print("\n" + "=" * 80)
    print("🏁 Test Summary:")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")

    if result.wasSuccessful():
        print("🎉 All tests passed!")
        return True
    else:
        print("🔧 Some tests failed. Check output above.")
        return False


if __name__ == "__main__":
    # Run comprehensive tests
    success = run_comprehensive_tests()
    exit(0 if success else 1)
