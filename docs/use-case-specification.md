# Use-Case Flow Specification

**Course**: PES University - Dept. of CSE  
**Lab Assignment**: Lab 1: Requirements Engineering & UML Use-Case Modelling  
**Problem Statement #43**: Feature Flag & Dynamic Config Manager  
**Use Case ID**: UC-01  
**Use Case Name**: Manage Percentage-Based Canary Rollout  

---

## 1. Brief Description
The **Release Manager** incrementally updates and manages the rollout percentage of a feature flag across target user cohorts in the production environment. The system computes deterministic user partitions using cryptographic hashing (e.g., MurmurHash3), persists the rollout configuration, generates audit logs, and streams the updated targeting rules in real-time to all connected client SDKs to ensure zero-downtime, canary deployments.

---

## 2. Actors & Stakeholders
- **Primary Actor**: Release Manager
- **Secondary / Supporting Actors**:
  - **Software Engineer**: Author of the feature flag and initial staging test rules.
  - **Client SDK / Application Service**: Evaluates flag rules locally in microservices.
  - **Monitoring & Alerting System**: Observes error rates, P99 latencies, and triggers automated rollbacks if thresholds are breached.

---

## 3. Preconditions
1. The feature flag has been defined, configured with default fallback values, and successfully verified in `Staging`.
2. The Release Manager is authenticated with active Multi-Factor Authentication (MFA) and possesses production write authorization.
3. The centralized configuration backend and streaming distribution channels (SSE/WebSockets) are operational and connected to downstream client SDKs.

---

## 4. Postconditions
- **Success Postconditions**:
  1. The target rollout percentage (e.g., 25%) is persisted in the centralized database.
  2. An immutable audit record is committed documenting the actor ID, timestamp, previous percentage, and new percentage.
  3. Real-time update events are published to all active client SDK instances within 2 seconds.
  4. Incoming user requests falling within the 25% hash bucket deterministically receive the enabled flag value.
- **Failure / Guard Postconditions**:
  1. Rollout percentage remains at the last validated stable value.
  2. No corrupted configuration is broadcasted to client SDKs.
  3. An alert/audit log entry records the rejection or error reason.

---

## 5. Main Success Scenario (Basic Flow)

| Step | Actor Action | System Response |
| :--- | :--- | :--- |
| **1** | Release Manager navigates to the **Feature Flag Management Dashboard** and selects the desired feature toggle (e.g., `checkout_v2_redesign`). | System queries the flag repository and displays current environment states, active targeting rules, metrics, and current rollout percentage (e.g., 5%). |
| **2** | Release Manager selects the `Production` environment tab and inputs the new target rollout percentage (e.g., 25%). | System displays a visual diff of the configuration change and renders the projected user impact cohort estimate. |
| **3** | Release Manager inputs a release change note/ticket reference (e.g., `PROD-ROLLOUT-4402`) and clicks **Submit Rollout Update**. | System initiates validation and authorization check (`«include» Authenticate & Authorize Access`). |
| **4** | — | System validates user permissions and verifies that the percentage is within allowed boundaries (0% to 100%). |
| **5** | — | System commits the updated rule set into the versioned configuration database (`«include» Log Audit Event`). |
| **6** | — | System publishes a real-time state change payload across the active Server-Sent Events (SSE) streaming channel to all connected client SDKs. |
| **7** | Client SDK receives the streaming event. | Client SDK updates its local in-memory rule engine cache and confirms receipt via health ping. |
| **8** | — | System updates the live dashboard displaying rollout status, active subscriber count, and live telemetry metric stream. |

---

## 6. Alternate Flows

### Alternate Flow 6A: Anomaly Detected & Emergency Kill-Switch Activated (`«extend» Trigger Emergency Kill Switch`)
- **Trigger**: During step 7 or 8, the automated Monitoring System or Release Manager detects an error rate spike or latency degradation exceeding safety thresholds (e.g., HTTP 500 error rate $> 1.0\%$).
- **Flow**:
  1. Monitoring System triggers an automated webhook or Release Manager clicks **Emergency Kill Switch**.
  2. System immediately overrides the rollout percentage to `0%` (disabled state).
  3. System broadcasts high-priority kill-switch payload to all connected client SDKs within 500 ms.
  4. SDKs flush active evaluation states and fall back to legacy baseline behavior.
  5. System records an emergency incident log and pages on-call engineering leads.
  6. Use case terminates in safe degraded/reverted state.

### Alternate Flow 6B: Client SDK Network Disconnection & Cache Fallback (`«extend» Fall Back to Local Cache`)
- **Trigger**: During step 6, one or more client SDK instances experience a network partition or backend timeout.
- **Flow**:
  1. Client SDK detects SSE connection drop and logs a transport warning.
  2. Client SDK activates local in-memory fallback cache to continue evaluating existing rules without throwing runtime errors.
  3. SDK initiates background reconnect attempts using exponential backoff with jitter.
  4. Upon reconnection, SDK downloads full configuration snapshot, reconciles delta, and resumes real-time streaming.
  5. Use case resumes at Step 8.

---

## 7. Extension Points & Inclusion Points
- **Inclusion Point**: `«include» Authenticate & Authorize Access` (Executed unconditionally at Step 3 to ensure zero unauthorized production changes).
- **Inclusion Point**: `«include» Log Audit Event` (Executed unconditionally at Step 5 to record immutable audit trail).
- **Extension Point**: `OnMetricBreach` at Step 7/8 $\rightarrow$ extends to `UC-04: Trigger Emergency Kill Switch`.
- **Extension Point**: `OnNetworkFailure` at Step 6/7 $\rightarrow$ extends to `UC-06: Fall Back to Local Cache`.

---

## 8. Special Requirements & Constraints
- **Idempotency**: Flag evaluation hashing must be strictly deterministic across SDK languages (Java, Python, Go, Node.js).
- **Zero Downtime**: Updating flag rollouts must never lock client application evaluation threads.
