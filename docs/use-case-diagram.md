# UML Use-Case Diagram Specification

**Course**: PES University - Dept. of CSE  
**Lab Assignment**: Lab 1: Requirements Engineering & UML Use-Case Modelling  
**Problem Statement #43**: Feature Flag & Dynamic Config Manager  
**Primary Domain**: Developer Tools & IT Operations  

---

## 1. Visual Use-Case Diagram (Mermaid)

```mermaid
graph LR
    %% Actors
    subgraph Actors [Actors]
        SE["👤 Software Engineer<br/>(Primary Actor)"]
        RM["👤 Release Manager<br/>(Primary Actor)"]
        SDK["💻 Client SDK / App Service<br/>(Secondary/System Actor)"]
        MON["🚨 Monitoring & Alerting System<br/>(Secondary Actor)"]
    end

    %% System Boundary
    subgraph SystemBoundary ["System Boundary: Feature Flag & Dynamic Config Manager"]
        UC1(["UC-01: Define Feature Flag & Targeting Rules"])
        UC2(["UC-02: Configure Environment Overrides"])
        UC3(["UC-03: Manage Percentage-Based Canary Rollout"])
        UC4(["UC-04: Trigger Emergency Kill Switch"])
        UC5(["UC-05: Synchronize Flags & Configs in Real-Time"])
        UC6(["UC-06: Evaluate Feature Flag at Runtime"])
        UC7(["UC-07: View Audit Logs & Revision Diffs"])
        
        %% Included Use Cases
        UC_AUTH(["UC-08: Authenticate & Authorize Access<br/><i>&lt;&lt;included&gt;&gt;</i>"])
        UC_LOG(["UC-09: Log Audit Event<br/><i>&lt;&lt;included&gt;&gt;</i>"])
        
        %% Extended Use Cases
        UC_CACHE(["UC-10: Fall Back to Local In-Memory Cache<br/><i>&lt;&lt;extended&gt;&gt;</i>"])
        UC_ROLLBACK(["UC-11: Rollback Configuration Version<br/><i>&lt;&lt;extended&gt;&gt;</i>"])
    end

    %% Primary Actor Relationships
    SE --- UC1
    SE --- UC2
    SE --- UC7

    RM --- UC2
    RM --- UC3
    RM --- UC4
    RM --- UC7

    %% Secondary Actor Relationships
    SDK --- UC5
    SDK --- UC6
    MON --- UC4

    %% Include Relationships (Mandatory)
    UC1 -.->|"&lt;&lt;include&gt;&gt;"| UC_AUTH
    UC2 -.->|"&lt;&lt;include&gt;&gt;"| UC_AUTH
    UC3 -.->|"&lt;&lt;include&gt;&gt;"| UC_AUTH
    UC3 -.->|"&lt;&lt;include&gt;&gt;"| UC_LOG
    UC4 -.->|"&lt;&lt;include&gt;&gt;"| UC_LOG

    %% Extend Relationships (Optional / Exceptional / Conditional)
    UC4 -.->|"&lt;&lt;extend&gt;&gt; (On Anomaly Detected)"| UC3
    UC_ROLLBACK -.->|"&lt;&lt;extend&gt;&gt; (On Revision Selected)"| UC7
    UC_CACHE -.->|"&lt;&lt;extend&gt;&gt; (On Network Outage)"| UC5

    %% Styling
    classDef actorStyle fill:#f9f9f9,stroke:#333,stroke-width:2px;
    classDef ucStyle fill:#ebf5fb,stroke:#2980b9,stroke-width:2px;
    classDef incStyle fill:#d6eaf8,stroke:#1b4f72,stroke-width:2px,stroke-dasharray: 5 5;
    classDef extStyle fill:#fdedec,stroke:#922b21,stroke-width:2px,stroke-dasharray: 5 5;

    class SE,RM,SDK,MON actorStyle;
    class UC1,UC2,UC3,UC4,UC5,UC6,UC7 ucStyle;
    class UC_AUTH,UC_LOG incStyle;
    class UC_CACHE,UC_ROLLBACK extStyle;
```

---

## 2. Actors Description

| Actor | Category | Description & Responsibilities |
| :--- | :--- | :--- |
| **Software Engineer** | Primary Actor (Human) | Creates and modifies feature flags, defines targeting rules (user attributes, beta testers), configures staging environment overrides, and verifies flag evaluations in development. |
| **Release Manager** | Primary Actor (Human) | Controls production release gates, orchestrates percentage-based canary rollouts, monitors release health telemetry, executes emergency rollbacks, and inspects audit logs. |
| **Client SDK / Application Service** | Secondary / System Actor | Integrated directly into backend microservices and frontend clients; maintains streaming connection with configuration server and resolves flag states locally with sub-15ms latency. |
| **Monitoring & Alerting System** | Secondary Actor (Automated System) | Ingests telemetry metrics (P99 latency, error rates) and automatically triggers emergency kill switches via webhooks when safety thresholds are violated. |

---

## 3. Relationships Justification

### A. `«include»` Relationships (Mandatory Sub-flows)
1. **`UC-03 (Manage Rollout)` $\xrightarrow{\text{«include»}}$ `UC-08 (Authenticate & Authorize Access)`**:
   - *Justification*: Any modification to production rollout percentages strictly requires identity verification and role-based authorization check before execution.
2. **`UC-03 (Manage Rollout)` $\xrightarrow{\text{«include»}}$ `UC-09 (Log Audit Event)`**:
   - *Justification*: Every rollout modification must unconditionally generate an immutable audit log entry for regulatory and compliance reasons.

### B. `«extend»` Relationships (Optional / Exceptional / Conditional Flows)
1. **`UC-04 (Trigger Emergency Kill Switch)` $\xrightarrow{\text{«extend»}}$ `UC-03 (Manage Percentage-Based Canary Rollout)`**:
   - *Extension Point*: `OnMetricBreach`
   - *Condition*: Triggered only if live health telemetry detects an error spike or latency breach during a canary release, instantly disabling the flag.
2. **`UC-10 (Fall Back to Local Cache)` $\xrightarrow{\text{«extend»}}$ `UC-05 (Synchronize Flags & Configs in Real-Time)`**:
   - *Extension Point*: `OnNetworkFailure`
   - *Condition*: Triggered only when the real-time SSE/WebSocket connection to the centralized configuration backend fails, allowing the client SDK to safely evaluate cached configurations without crashing.
