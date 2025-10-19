# Copyright (c) Microsoft. All rights reserved.


import os
import unittest

from opentelemetry import baggage, context, trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter

from microsoft_agents_a365.observability.core import config as telemetry_config
from microsoft_agents_a365.observability.core.constants import (
    CORRELATION_ID_KEY,
    GEN_AI_AGENT_AUID_KEY,
    GEN_AI_AGENT_BLUEPRINT_ID_KEY,
    GEN_AI_AGENT_ID_KEY,
    GEN_AI_AGENT_UPN_KEY,
    GEN_AI_CALLER_ID_KEY,
    HIRING_MANAGER_ID_KEY,
    OPERATION_SOURCE_KEY,
    TENANT_ID_KEY,
)
from microsoft_agents_a365.observability.core.middleware.baggage_builder import BaggageBuilder


class TestBaggageBuilder(unittest.TestCase):
    """Test the BaggageBuilder class."""

    @classmethod
    def setUpClass(cls):
        """Save the original tracer provider."""
        cls._original_provider = trace.get_tracer_provider()

    @classmethod
    def tearDownClass(cls):
        """Restore the original tracer provider."""
        if hasattr(cls, "_original_provider"):
            trace.set_tracer_provider(cls._original_provider)
        # Force OpenTelemetryScope to refresh its tracer
        from microsoft_agents_a365.observability.core.opentelemetry_scope import OpenTelemetryScope

        OpenTelemetryScope._tracer = None

    def setUp(self):
        """Set up test fixtures."""
        # Enable telemetry for tests
        os.environ["ENABLE_OBSERVABILITY"] = "true"

        # Clear any existing context/baggage before each test
        context.detach(context.attach({}))

    def tearDown(self):
        """Clean up after each test."""
        # Clear context
        context.detach(context.attach({}))

    def test_baggage_builder_sets_values(self):
        """Test that BaggageBuilder sets baggage values correctly."""
        tenant = "tenant-1"
        agent = "agent-1"
        corr = "corr-1"

        # Use the baggage builder within a context
        with BaggageBuilder().tenant_id(tenant).agent_id(agent).correlation_id(corr).build():
            # Assert inside scope - baggage should be set
            current_baggage = baggage.get_all()
            self.assertEqual(current_baggage.get(TENANT_ID_KEY), tenant)
            self.assertEqual(current_baggage.get(GEN_AI_AGENT_ID_KEY), agent)
            self.assertEqual(current_baggage.get(CORRELATION_ID_KEY), corr)

        # Assert after exiting scope - baggage should be restored/cleared
        current_baggage = baggage.get_all()
        self.assertIsNone(current_baggage.get(TENANT_ID_KEY))
        self.assertIsNone(current_baggage.get(GEN_AI_AGENT_ID_KEY))
        self.assertIsNone(current_baggage.get(CORRELATION_ID_KEY))
        print("✅ BaggageBuilder sets and restores values correctly!")

    def test_all_baggage_keys(self):
        """Test all baggage key setter methods."""
        with (
            BaggageBuilder()
            .operation_source("sdk")
            .tenant_id("tenant-1")
            .agent_id("agent-1")
            .agent_auid("auid-1")
            .agent_upn("upn-1")
            .agent_blueprint_id("blueprint-1")
            .correlation_id("corr-1")
            .caller_id("caller-1")
            .hiring_manager_id("manager-1")
            .build()
        ):
            current_baggage = baggage.get_all()
            self.assertEqual(current_baggage.get(OPERATION_SOURCE_KEY), "sdk")
            self.assertEqual(current_baggage.get(TENANT_ID_KEY), "tenant-1")
            self.assertEqual(current_baggage.get(GEN_AI_AGENT_ID_KEY), "agent-1")
            self.assertEqual(current_baggage.get(GEN_AI_AGENT_AUID_KEY), "auid-1")
            self.assertEqual(current_baggage.get(GEN_AI_AGENT_UPN_KEY), "upn-1")
            self.assertEqual(current_baggage.get(GEN_AI_AGENT_BLUEPRINT_ID_KEY), "blueprint-1")
            self.assertEqual(current_baggage.get(CORRELATION_ID_KEY), "corr-1")
            self.assertEqual(current_baggage.get(GEN_AI_CALLER_ID_KEY), "caller-1")
            self.assertEqual(current_baggage.get(HIRING_MANAGER_ID_KEY), "manager-1")
        print("✅ All baggage keys work correctly!")

    def test_baggage_propagates_to_child_spans(self):
        """Test that baggage values are copied as attributes onto parent and child spans via SpanProcessor."""
        # Configure global telemetry; this will add the SpanProcessor automatically.
        # Use a temporary tracer provider with our in-memory exporter for assertion.
        exporter = InMemorySpanExporter()
        provider = TracerProvider()
        provider.add_span_processor(SimpleSpanProcessor(exporter))
        trace.set_tracer_provider(provider)
        # Invoke SDK configure to attach Kairo span processor (agent processor)
        telemetry_config.configure(
            service_name="baggage-test-service",
            service_namespace="baggage.test",
            logger_name="kairo-test",
        )
        tracer = telemetry_config.get_tracer(__name__)

        tenant = "tenant-propagation-test"
        agent = "agent-propagation-test"

        # Create baggage before starting spans so processor can copy it
        with BaggageBuilder().tenant_id(tenant).agent_id(agent).build():
            with tracer.start_as_current_span("parent_span") as parent_span:
                # Attributes should now include baggage-derived keys
                parent_attrs = getattr(parent_span, "attributes", {})
                self.assertEqual(
                    parent_attrs.get(TENANT_ID_KEY),
                    tenant,
                    "Parent span missing tenant attribute from baggage",
                )
                self.assertEqual(
                    parent_attrs.get(GEN_AI_AGENT_ID_KEY),
                    agent,
                    "Parent span missing agent attribute from baggage",
                )

                # Nested child span should also receive baggage-derived attributes at start
                with tracer.start_as_current_span("child_span") as child_span:
                    child_attrs = getattr(child_span, "attributes", {})
                    self.assertEqual(
                        child_attrs.get(TENANT_ID_KEY),
                        tenant,
                        "Child span missing tenant attribute from baggage",
                    )
                    self.assertEqual(
                        child_attrs.get(GEN_AI_AGENT_ID_KEY),
                        agent,
                        "Child span missing agent attribute from baggage",
                    )

        # Ensure spans exported contain these attributes (export happens on end)
        finished_spans = exporter.get_finished_spans()
        # Find parent and child by name
        names = {s.name: s for s in finished_spans}
        self.assertIn("parent_span", names, "parent_span not exported")
        self.assertIn("child_span", names, "child_span not exported")
        self.assertEqual(names["parent_span"].attributes.get(TENANT_ID_KEY), tenant)
        self.assertEqual(names["parent_span"].attributes.get(GEN_AI_AGENT_ID_KEY), agent)
        self.assertEqual(names["child_span"].attributes.get(TENANT_ID_KEY), tenant)
        self.assertEqual(names["child_span"].attributes.get(GEN_AI_AGENT_ID_KEY), agent)

    def test_baggage_reset_after_scope_exit(self):
        """Test that all baggage values are completely reset/cleared after exiting scope."""
        # First, set some initial baggage values outside the builder scope
        initial_ctx = baggage.set_baggage("existing_key", "existing_value")
        context.attach(initial_ctx)

        # Verify initial baggage exists
        initial_baggage = baggage.get_all()
        self.assertEqual(initial_baggage.get("existing_key"), "existing_value")

        # Use BaggageBuilder to set all possible values
        with (
            BaggageBuilder()
            .operation_source("test_sdk")
            .tenant_id("test-tenant")
            .agent_id("test-agent")
            .agent_auid("test-auid")
            .agent_upn("test-upn")
            .agent_blueprint_id("test-blueprint")
            .correlation_id("test-correlation")
            .caller_id("test-caller")
            .hiring_manager_id("test-manager")
            .build()
        ):
            # Inside scope - verify all baggage values are set
            scoped_baggage = baggage.get_all()
            self.assertEqual(scoped_baggage.get(OPERATION_SOURCE_KEY), "test_sdk")
            self.assertEqual(scoped_baggage.get(TENANT_ID_KEY), "test-tenant")
            self.assertEqual(scoped_baggage.get(GEN_AI_AGENT_ID_KEY), "test-agent")
            self.assertEqual(scoped_baggage.get(GEN_AI_AGENT_AUID_KEY), "test-auid")
            self.assertEqual(scoped_baggage.get(GEN_AI_AGENT_UPN_KEY), "test-upn")
            self.assertEqual(scoped_baggage.get(GEN_AI_AGENT_BLUEPRINT_ID_KEY), "test-blueprint")
            self.assertEqual(scoped_baggage.get(CORRELATION_ID_KEY), "test-correlation")
            self.assertEqual(scoped_baggage.get(GEN_AI_CALLER_ID_KEY), "test-caller")
            self.assertEqual(scoped_baggage.get(HIRING_MANAGER_ID_KEY), "test-manager")
            # Original baggage should still exist
            self.assertEqual(scoped_baggage.get("existing_key"), "existing_value")

        # After exiting scope - verify ALL BaggageBuilder values are cleared
        final_baggage = baggage.get_all()

        # All BaggageBuilder keys should be None/cleared
        self.assertIsNone(final_baggage.get(OPERATION_SOURCE_KEY))
        self.assertIsNone(final_baggage.get(TENANT_ID_KEY))
        self.assertIsNone(final_baggage.get(GEN_AI_AGENT_ID_KEY))
        self.assertIsNone(final_baggage.get(GEN_AI_AGENT_AUID_KEY))
        self.assertIsNone(final_baggage.get(GEN_AI_AGENT_UPN_KEY))
        self.assertIsNone(final_baggage.get(GEN_AI_AGENT_BLUEPRINT_ID_KEY))
        self.assertIsNone(final_baggage.get(CORRELATION_ID_KEY))
        self.assertIsNone(final_baggage.get(GEN_AI_CALLER_ID_KEY))
        self.assertIsNone(final_baggage.get(HIRING_MANAGER_ID_KEY))

        # Original baggage should be restored
        self.assertEqual(final_baggage.get("existing_key"), "existing_value")

        print("✅ All baggage values are properly reset after scope exit!")


if __name__ == "__main__":
    unittest.main()
