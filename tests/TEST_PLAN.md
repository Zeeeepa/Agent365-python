# Test Plan for Agent365-Python SDK

**Version:** 1.0  
**Date:** November 24, 2025  
**Status:** Draft  
**Owner:** Team Review Required

---

## Table of Contents

1. [Overview](#overview)
2. [Testing Strategy](#testing-strategy)
3. [Phase 1: Unit Tests](#phase-1-unit-tests)
4. [Phase 2: Integration Tests](#phase-2-integration-tests)
5. [Phase 3: CI/CD Integration](#phase-3-cicd-integration)
6. [Success Criteria](#success-criteria)
7. [Implementation Roadmap](#implementation-roadmap)

---

## Overview

### Purpose
Establish comprehensive test coverage for the Agent365-Python SDK to ensure reliability, maintainability, and quality across all modules.

### Current State
- ✅ Some unit tests exist for `observability` module
- ⚠️ Partial coverage for `runtime` module
- ❌ Missing tests for `tooling` and `notifications` modules
- ⚠️ Limited integration test coverage
- ❌ No automated coverage reporting in CI

### Goals
1. Achieve **80%+ code coverage** across all modules
2. Implement unit tests following Python best practices (`unittest` framework)
3. Create integration tests for cross-module functionality
4. Integrate testing into CI/CD pipeline with automated coverage reporting
5. Establish testing standards for future development

---

## Testing Strategy

### Testing Pyramid

```
       /\
      /  \       Integration Tests
     /    \      - Module interactions
    /      \     - Mocked external services
   /--------\    
  /          \   Unit Tests
 /            \  - Isolated function/class testing
----------------  - 80%+ coverage target
```

### Tools & Framework
- **Framework:** `unittest` + `pytest` runner
- **Coverage:** `pytest-cov`
- **Mocking:** `unittest.mock`
- **Async:** `pytest-asyncio`

### Testing Principles
- **AAA Pattern:** Arrange → Act → Assert
- **FIRST:** Fast, Independent, Repeatable, Self-validating, Timely
- **Naming:** `test_<method>_<condition>_<expected_result>`

---

## Phase 1: Unit Tests

### Phase 1.1: Runtime Module
**Priority:** HIGH

| Module | Test File | Status | Priority |
|--------|-----------|--------|----------|
| `power_platform_api_discovery.py` | `test_power_platform_api_discovery.py` | ✅ Exists | Review & Expand |
| `utility.py` | `test_utility.py` | ✅ Exists | Review & Expand |
| `environment_utils.py` | `test_environment_utils.py` | ❌ Missing | **HIGH** |
| `version_utils.py` | `test_version_utils.py` | ❌ Missing | Medium |

**Key Areas to Test:**
- Environment detection and configuration
- Authentication scope resolution
- Version utilities with deprecation warnings
- Power Platform API discovery

---

### Phase 1.2: Tooling Module
**Priority:** HIGH

**Directory Structure:**
```
tests/tooling/
├── utils/test_utility.py
├── models/test_mcp_server_config.py
└── services/test_mcp_tool_server_configuration_service.py
```

**Key Areas to Test:**
- MCP server configuration and validation
- Environment-based URL generation
- Tools mode handling (Mock vs Platform)
- Gateway discovery and authentication
- Manifest file parsing

---

### Phase 1.3: Notifications Module
**Priority:** HIGH

**Directory Structure:**
```
tests/notifications/
├── models/
│   ├── test_agent_lifecycle_event.py
│   ├── test_agent_notification_activity.py
│   ├── test_email_reference.py
│   └── test_notification_types.py
└── test_agent_notification.py
```

**Key Areas to Test:**
- Activity parsing and entity extraction
- Notification routing and filtering
- Decorator functionality
- Channel and subchannel handling

---

### Phase 1.4: Observability Extensions
**Priority:** MEDIUM

| Extension | Action | Priority |
|-----------|--------|----------|
| `agentframework` | Expand existing tests | Medium |
| `langchain` | Expand existing tests | Medium |
| `openai` | Expand existing tests | Medium |
| `semantickernel` | Expand existing tests | Medium |

**Key Areas to Test:**
- Wrapper functionality
- Trace processing
- Event handling

---

### Phase 1.5: Tooling Extensions
**Priority:** LOW

**Extensions to Test:**
- Agent Framework tooling integration
- Azure AI Foundry tooling integration
- OpenAI tooling integration
- Semantic Kernel tooling integration

---

## Phase 2: Integration Tests

### Phase 2.1: Module Integration
**Priority:** HIGH

**Test Scenarios:**
- Runtime + Observability integration
- Tooling + Runtime integration
- Notifications + Runtime integration
- End-to-end workflow scenarios

**Focus:**
- Cross-module interactions
- Mocked external dependencies
- Configuration propagation
- Error handling across boundaries

---

### Phase 2.2: Extension Integration
**Priority:** MEDIUM

**Test Scenarios:**
- Agent Framework full flow
- LangChain full flow
- OpenAI Agents full flow
- Semantic Kernel full flow

**Focus:**
- End-to-end agent execution with observability
- Tool invocation with MCP servers
- Notification delivery
- Cross-extension compatibility

---

## Phase 3: CI/CD Integration

### Phase 3.1: Test Automation
**Priority:** HIGH

**Setup:**
- GitHub Actions workflow for automated testing
- Multi-version Python matrix (3.9, 3.10, 3.11, 3.12)
- Automated coverage reporting with Codecov
- PR blocking on test failures

---

### Phase 3.2: Coverage Requirements
**Priority:** HIGH

**Configuration:**
- Minimum 80% code coverage enforcement
- Coverage reports in XML, HTML, and terminal formats
- Branch protection rules requiring passing tests
- Coverage trend tracking

---

### Phase 3.3: Pre-commit Hooks
**Priority:** MEDIUM

**Setup:**
- Code formatting checks (ruff)
- Test execution before commit
- YAML validation
- Trailing whitespace cleanup

---

## Success Criteria

### Phase 1: Unit Tests
- ✅ 80%+ code coverage for all modules
- ✅ All tests follow AAA pattern
- ✅ Tests run independently in any order
- ✅ Full suite completes in < 30 seconds

### Phase 2: Integration Tests
- ✅ All major integration points tested
- ✅ 99%+ test reliability
- ✅ External services properly mocked
- ✅ Integration scenarios documented

### Phase 3: CI/CD
- ✅ Automated test execution on all PRs
- ✅ Coverage reports visible and enforced
- ✅ PR merge blocked on test failures or coverage drops
- ✅ Tests pass on Python 3.9-3.12
- ✅ Full suite completes in < 5 minutes

---

## Implementation Roadmap

| Phase | Focus | Deliverables | Owner |
|-------|-------|-------------|-------|
| 1.1 | Runtime Module | `test_environment_utils.py`, `test_version_utils.py` | TBD |
| 1.2 | Tooling Module | All tooling test files | TBD |
| 1.3 | Notifications Module | All notifications test files | TBD |
| 1.4 | Observability Extensions | Expand existing tests | TBD |
| 1.5 | Tooling Extensions | Extension test files | TBD |
| 2.1 | Module Integration | Integration test suite | TBD |
| 2.2 | Extension Integration | Full flow tests | TBD |
| 3 | CI/CD Setup | GitHub Actions, coverage, pre-commit | TBD |

### Key Milestones
- **M1:** Runtime tests complete, baseline coverage established
- **M2:** All core module unit tests complete
- **M3:** Integration test framework in place
- **M4:** Full CI/CD integration, coverage enforcement

---

## References

- [Python unittest Documentation](https://docs.python.org/3/library/unittest.html)
- [pytest Documentation](https://docs.pytest.org/)
- [unittest.mock Guide](https://docs.python.org/3/library/unittest.mock.html)
- Existing tests: `tests/observability/core/` and `tests/runtime/`
