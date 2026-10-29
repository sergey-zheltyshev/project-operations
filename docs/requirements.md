# Requirements and verification

| ID | Requirement | Executable verification |
|---|---|---|
| PO-01 | Keep canonical identity in each global projection | `test_projection_preserves_canonical_identity_and_does_not_change_workflow` |
| PO-02 | Require a concrete dependency for Blocked attention | `test_blocker_requires_concrete_dependency` |
| PO-03 | Require acceptance evidence before completion | `test_done_requires_acceptance` |
| PO-04 | Reject invalid workflow jumps | `test_invalid_jump_is_rejected` |
| PO-05 | Signal WIP overflow without silently hiding work | `test_capacity_is_signal_not_silent_truncation` |
| PO-06 | Preserve continuation point and source in checkpoints | `test_recovery_checkpoint_has_next_action_and_source` |

## Acceptance walkthrough

1. Install the dependencies specified in the README.
2. Run the demonstration with no private configuration.
3. Inspect the generated output against the documented data contract.
4. Run the automated test command.
5. Confirm malformed, conflicting or out-of-order inputs follow the documented behavior.

Tests exercise the implementation and its failure boundaries. Synthetic fixtures are clearly separated from operational data. See the repository's CI workflow for the repeatable validation command.
