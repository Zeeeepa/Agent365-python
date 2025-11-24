# Copyright (c) Microsoft. All rights reserved.

"""Unit tests for Agent Settings models."""

import json
import unittest
from datetime import UTC, datetime

from microsoft_agents_a365.settings import (
    AgentSettingProperty,
    AgentSettings,
    AgentSettingsTemplate,
)


class TestAgentSettingProperty(unittest.TestCase):
    """Test cases for the AgentSettingProperty model."""

    def test_default_values(self):
        """Test that default values are correct."""
        prop = AgentSettingProperty()
        self.assertEqual(prop.name, "")
        self.assertEqual(prop.value, "")
        self.assertEqual(prop.type, "string")
        self.assertFalse(prop.required)
        self.assertIsNone(prop.description)
        self.assertIsNone(prop.default_value)

    def test_serialization_roundtrip(self):
        """Test serialization and deserialization."""
        prop = AgentSettingProperty(
            name="testSetting",
            value="testValue",
            type="boolean",
            required=True,
            description="A test setting",
            default_value="false",
        )

        json_str = prop.model_dump_json(by_alias=True)
        deserialized = AgentSettingProperty.model_validate_json(json_str)

        self.assertEqual(deserialized.name, "testSetting")
        self.assertEqual(deserialized.value, "testValue")
        self.assertEqual(deserialized.type, "boolean")
        self.assertTrue(deserialized.required)
        self.assertEqual(deserialized.description, "A test setting")
        self.assertEqual(deserialized.default_value, "false")

    def test_json_alias(self):
        """Test JSON property name aliasing."""
        prop = AgentSettingProperty(
            name="test",
            value="val",
            default_value="default",
        )
        json_str = prop.model_dump_json(by_alias=True)
        data = json.loads(json_str)
        self.assertIn("defaultValue", data)
        self.assertEqual(data["defaultValue"], "default")


class TestAgentSettingsTemplate(unittest.TestCase):
    """Test cases for the AgentSettingsTemplate model."""

    def test_default_values(self):
        """Test that default values are correct."""
        template = AgentSettingsTemplate()
        self.assertEqual(template.id, "")
        self.assertEqual(template.agent_type, "")
        self.assertEqual(template.name, "")
        self.assertIsNone(template.description)
        self.assertEqual(template.version, "1.0")
        self.assertEqual(template.properties, [])

    def test_serialization_roundtrip(self):
        """Test serialization and deserialization."""
        template = AgentSettingsTemplate(
            id="template-123",
            agent_type="custom-agent",
            name="Custom Agent Template",
            description="Template for custom agents",
            version="2.0",
            properties=[
                AgentSettingProperty(name="setting1", value="value1", type="string"),
                AgentSettingProperty(name="setting2", value="true", type="boolean", required=True),
            ],
        )

        json_str = template.model_dump_json(by_alias=True)
        deserialized = AgentSettingsTemplate.model_validate_json(json_str)

        self.assertEqual(deserialized.id, "template-123")
        self.assertEqual(deserialized.agent_type, "custom-agent")
        self.assertEqual(deserialized.name, "Custom Agent Template")
        self.assertEqual(deserialized.description, "Template for custom agents")
        self.assertEqual(deserialized.version, "2.0")
        self.assertEqual(len(deserialized.properties), 2)

    def test_json_alias(self):
        """Test JSON property name aliasing."""
        template = AgentSettingsTemplate(agent_type="test-type")
        json_str = template.model_dump_json(by_alias=True)
        data = json.loads(json_str)
        self.assertIn("agentType", data)
        self.assertEqual(data["agentType"], "test-type")

    def test_can_add_properties(self):
        """Test that properties can be added after construction."""
        template = AgentSettingsTemplate(id="template-123", agent_type="custom-agent")
        template.properties.append(AgentSettingProperty(name="newSetting", value="newValue"))
        self.assertEqual(len(template.properties), 1)
        self.assertEqual(template.properties[0].name, "newSetting")


class TestAgentSettings(unittest.TestCase):
    """Test cases for the AgentSettings model."""

    def test_default_values(self):
        """Test that default values are correct."""
        settings = AgentSettings()
        self.assertEqual(settings.id, "")
        self.assertEqual(settings.agent_instance_id, "")
        self.assertIsNone(settings.template_id)
        self.assertEqual(settings.agent_type, "")
        self.assertEqual(settings.properties, [])
        # Check timestamps are roughly now
        now = datetime.now(UTC)
        self.assertLess(abs((settings.created_at - now).total_seconds()), 5)
        self.assertLess(abs((settings.modified_at - now).total_seconds()), 5)

    def test_serialization_roundtrip(self):
        """Test serialization and deserialization."""
        created_at = datetime(2024, 1, 15, 10, 30, 0, tzinfo=UTC)
        modified_at = datetime(2024, 1, 16, 14, 45, 0, tzinfo=UTC)

        settings = AgentSettings(
            id="settings-456",
            agent_instance_id="instance-789",
            template_id="template-123",
            agent_type="custom-agent",
            created_at=created_at,
            modified_at=modified_at,
            properties=[
                AgentSettingProperty(name="apiKey", value="secret", type="string", required=True)
            ],
        )

        json_str = settings.model_dump_json(by_alias=True)
        deserialized = AgentSettings.model_validate_json(json_str)

        self.assertEqual(deserialized.id, "settings-456")
        self.assertEqual(deserialized.agent_instance_id, "instance-789")
        self.assertEqual(deserialized.template_id, "template-123")
        self.assertEqual(deserialized.agent_type, "custom-agent")
        self.assertEqual(deserialized.created_at, created_at)
        self.assertEqual(deserialized.modified_at, modified_at)
        self.assertEqual(len(deserialized.properties), 1)
        self.assertEqual(deserialized.properties[0].name, "apiKey")

    def test_json_aliases(self):
        """Test JSON property name aliasing."""
        settings = AgentSettings(
            agent_instance_id="instance-1",
            template_id="template-1",
            agent_type="type-1",
        )
        json_str = settings.model_dump_json(by_alias=True)
        data = json.loads(json_str)
        self.assertIn("agentInstanceId", data)
        self.assertIn("templateId", data)
        self.assertIn("agentType", data)
        self.assertIn("createdAt", data)
        self.assertIn("modifiedAt", data)

    def test_can_add_properties(self):
        """Test that properties can be added after construction."""
        settings = AgentSettings(id="settings-123", agent_instance_id="instance-456")
        settings.properties.append(AgentSettingProperty(name="configOption", value="configValue"))
        self.assertEqual(len(settings.properties), 1)
        self.assertEqual(settings.properties[0].name, "configOption")


if __name__ == "__main__":
    unittest.main()
