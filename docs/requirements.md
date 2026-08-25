# Software Requirements Specification (SRS) - Lab 1

**Course**: PES University - Dept. of CSE  
**Lab Assignment**: Lab 1: Requirements Engineering & UML Use-Case Modelling  
**Problem Statement #43**: Feature Flag & Dynamic Config Manager  
**Primary Domain**: Developer Tools & IT Operations  
**Target Stakeholders / Actors**: Software Engineer, Release Manager  

---

## 1. Problem Context & Overview
A centralized configuration and feature toggling platform supporting percentage-based user cohort rollouts, environment overrides, and real-time client SDK flag synchronization. The system enables engineering and operations teams to safely test in production, decouple deployment from release, execute gradual canary releases, and instantly disable problematic features via kill-switches without redeploying code.

---

## 2. Functional Requirements (FR-001 to FR-005)

| ID | Type | Description | Priority | Acceptance Criteria | Rationale |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **FR-001** | Functional | The system shall evaluate dynamic user targeting rules (e.g., User ID hash, Beta cohort tag, email domain, geographic region) and return accurate, deterministic boolean feature flag states. | **High** | **Pass**: A 10% canary rollout cohort consistently evaluates to `true` for users whose hashed identifier falls within [0, 10), and returns `false` for users outside the bucket.<br>**Fail**: A user outside the designated cohort or hash range receives an enabled flag state. | Enables safe canary testing and targeted experiment rollouts to minimize blast radius without code redeployments. |
| **FR-002** | Functional | The system shall allow configuration keys (strings, numbers, JSON schemas) and flag states to be set globally and overridden per environment (e.g., Development, Staging, Production) with role-based access control. | **High** | **Pass**: Modifying a configuration value or toggle in the `Staging` environment takes effect in Staging without altering the `Production` value; non-admin users cannot alter Production values.<br>**Fail**: Environment values bleed across environments or unauthorized users override production configuration. | Prevents configuration drift across deployment stages and allows safe pre-production validation of runtime flags. |
| **FR-003** | Functional | The system shall stream flag evaluation rules and dynamic configuration updates in real-time to connected client SDKs via Server-Sent Events (SSE) or WebSockets, with automatic in-memory cache sync. | **High** | **Pass**: Connected SDK client applications reflect published flag state changes in local memory within $\le 2$ seconds of publication without service restart.<br>**Fail**: Client SDK continues evaluating stale flag rules $>2$ seconds after update or fails to reconcile after network reconnect. | Eliminates polling overhead and ensures critical operational toggle adjustments propagate immediately across distributed microservices. |
| **FR-004** | Functional | The system shall provide an instantaneous global emergency kill-switch mechanism to disable a feature flag or revert configuration to a default safe baseline across all client nodes in one operation. | **Critical** | **Pass**: Triggering the kill-switch propagates a disabled state to all active client SDK instances within 500 ms and logs the initiating actor and timestamp.<br>**Fail**: Flag remains active on cached client nodes after kill-switch activation, or partial rollout states persist. | Protects production system stability by immediately neutralizing critical bugs, memory leaks, or outages caused by newly released features. |
| **FR-005** | Functional | The system shall maintain an immutable, chronological audit log capturing all flag creations, rule modifications, percentage adjustments, and environment overrides, including actor identity, timestamp, previous state, and new state diff. | **Medium** | **Pass**: Every configuration mutation generates an immutable log entry displaying exact JSON diffs and actor credentials, viewable and filterable in the dashboard.<br>**Fail**: Configuration changes occur without an audit record, or log entries are editable/deletable. | Ensures security compliance, accountability, operational governance, and root-cause analysis during post-incident reviews. |

---

## 3. Non-Functional Requirements (NFR-001 & NFR-002)

| ID | Type | Description | Priority | Acceptance Criteria | Rationale |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **NFR-001** | Performance & Latency | The feature flag evaluation API and SDK local in-memory evaluation engine must execute flag resolution with a P99 response latency of under 15 ms under a peak load of 50,000 requests per second (RPS). | **High** | **Pass**: Benchmark load testing confirms P99 latency $\le 15$ ms at 50,000 RPS with local cache hits $> 99.5\%$ and CPU utilization under 70%.<br>**Fail**: P99 latency exceeds 15 ms or evaluation engine introduces perceptible overhead to host application threads. | Feature flag evaluations sit directly on the synchronous critical path of user requests; any evaluation latency compounds overall system response time. |
| **NFR-002** | Security & High Availability | The system must enforce Role-Based Access Control (RBAC) with Multi-Factor Authentication (MFA) for production overrides and guarantee 99.99% service availability with graceful local cache fallback if the centralized backend becomes unreachable. | **Critical** | **Pass**: Unauthorized engineers are denied write access to Production flags, and client SDKs continue serving the last-known good cached configurations without throwing runtime exceptions during a full backend outage.<br>**Fail**: A centralized server outage causes client application crashes, or an unauthenticated request modifies production settings. | High availability and strict operational security guard against wide-scale service disruption and accidental misconfigurations in production. |
