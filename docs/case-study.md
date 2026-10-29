# Project Operations — case study

## The problem

A global task board improves visibility but often becomes a second backlog. Work drifts between boards, context is lost after pauses and a selected priority gets confused with a workflow status.

## The challenge

Give the owner a small global view while preserving project ownership, independent workflow state and enough context to resume real work after an interruption.

## The solution

Keep one canonical work item in its project. Derive global attention views by reference, separate attention from execution status, and use short recovery checkpoints that point back to the real source.

## Decisions that shaped the system

**Workflow and attention are orthogonal.** Ready/in progress/review describes project execution. Today/clarify/blocked describes global attention. Changing one does not silently change the other.

**A projection is a reference.** Global views carry canonical item IDs, project provenance and source pointers. They do not create separately editable work-item copies.

**Recovery is not reporting.** A checkpoint answers where to resume and which source to open. It is not a copied backlog or a chronological activity log.

**Capacity is visible, not destructive.** Three items is the default Today target. Over-capacity produces a signal while preserving the full selected set rather than hiding work.

## The result

The reference scenario projects four work items into Today, Clarify and Blocked views while retaining their canonical IDs and project provenance. Executable policies reject missing blockers, invalid transitions, duplicate identities and completion without acceptance evidence.

## Evidence to inspect

Run the README demonstration, inspect its generated output, then follow the [requirements and verification matrix](requirements.md) to the tests. [Contracts](contracts.md) describe the meanings and boundaries of the output.

## Contribution

Problem decomposition, system modeling, integration design, implementation and verification are presented together. Public-release engineering includes synthetic fixtures, portable configuration and executable checks. Commercial metrics and third-party service behavior are not inferred from a local demonstration.

[Return to overview](../README.md)
