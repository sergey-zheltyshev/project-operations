# Data and behavior contracts

## Work item

Required fields: `id`, `project`, `title`, `workflow`, `attention`, `source`, `next_action`. `blocker` is required for blocked attention; `acceptance` is required for done.

Workflow values: backlog, ready, in_progress, review, done. Attention values: none, today, clarify, blocked. Every identity must be unique within an input collection.

## Transition policy

```text
backlog → ready ↔ in_progress → review → done
             ↑          ↑        │
             └──────────┘        └→ in_progress
```

The reference implementation also permits ready → backlog. Done is terminal in this bounded model. Completing a reviewed item requires explicit acceptance evidence and clears its attention projection. A new scope of work should receive a new item rather than silently rewriting accepted history.

## Checkpoint

`project` and `resume_from[]`, where each continuation has item_id, next_action and source. Finished work is omitted. Checkpoints recover context; domain sources retain detailed factual state.

## Ownership matrix

| Concern | Authority |
|---|---|
| Execution status and work-item details | Project source / project board |
| What deserves attention now | Explicit attention selection |
| Cross-project view | Derived references |
| Detailed code, data or research | Domain repository / source system |
| Acceptance of a result | Acceptance evidence attached to work |

This executable model is the portable portfolio companion to an operational design. It does not require a YouGile account or publish private board exports.
