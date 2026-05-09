---
layout: title-slide
---

# Data Engineering

---
layout: blue-sidebar
---

::header::

# Data Engineering

::content::

<div class="concept-shell">
  <div class="concept-step" v-click>
    <strong>Moving data</strong>
    <p>Getting raw data from sources (files, APIs, databases) into a place where it can be used.</p>
  </div>
  <div class="concept-step" v-click>
    <strong>Transforming data</strong>
    <p>Cleaning, validating, joining, and reshaping data so it is fit for a specific question.</p>
  </div>
  <div class="concept-step" v-click>
    <strong>Serving data</strong>
    <p>Making the result reliably available — to a dashboard, an API, an ML model, or another team.</p>
  </div>
  <div class="concept-step action" v-click>
    <strong>Data engineering is the plumbing</strong>
    <p>Analysts and scientists depend on it being invisible when it works and loud when it breaks.</p>
  </div>
</div>

---
layout: blue-sidebar
---

::header::

# Orchestration

::content::

<div class="concept-shell">
  <div class="concept-step">
    <strong>Scheduling</strong>
    <p>Run this pipeline daily at 06:00, or whenever the upstream data arrives.</p>
  </div>
  <div class="concept-step" v-click>
    <strong>Dependency management</strong>
    <p>Do not start the enrichment step until the ingest step has finished successfully.</p>
  </div>
  <div class="concept-step" v-click>
    <strong>Retry and alerting</strong>
    <p>If a step fails, retry it up to three times, then page someone.</p>
  </div>
  <div class="concept-step" v-click>
    <strong>Observability</strong>
    <p>Show exactly what ran, when, how long it took, and what output it produced.</p>
  </div>
  <div class="concept-step action" v-click>
    <strong>Airflow's role</strong>
    <p>Airflow is the orchestrator. Your Python code is the work. Airflow manages everything around it.</p>
  </div>
</div>


---
layout: blue-sidebar
---

::header::

## DagRun

::content::

- Every time we trigger a pipeline, an instance(object) of the dag is created
- This instance has the information of all tasks that needs to run in that pipeline
- It has a state success/failure
- You can clear a DagRun to run again in the same instance

---
layout: blue-sidebar
---

::header::

## Task Instances

::content::

- Similar to DagRun, TaskInstances are created for per task per dag on trigger
- TaskInstances has states like `Success,Failure,Skipped,Running`
- You can clear a specific task to rerun again

---
layout: blue-title-slide
---

# Mini-Exercise

### Explore DagRun and Task Instance in UI