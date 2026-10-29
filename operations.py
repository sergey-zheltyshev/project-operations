"""Reference policy model for project ownership, attention and recovery checkpoints."""
from __future__ import annotations

import argparse
from dataclasses import dataclass, replace
import json
from pathlib import Path
from typing import Literal

Workflow = Literal['backlog','ready','in_progress','review','done']
Attention = Literal['none','today','clarify','blocked']


@dataclass(frozen=True)
class WorkItem:
    id: str
    project: str
    title: str
    workflow: Workflow
    attention: Attention
    source: str
    next_action: str
    blocker: str | None = None
    acceptance: str | None = None

    def __post_init__(self):
        if any(not value.strip() for value in [self.id,self.project,self.title,self.source,self.next_action]):
            raise ValueError('Identity, project, source and continuation point are required')
        if self.workflow not in {'backlog','ready','in_progress','review','done'}:
            raise ValueError('Invalid workflow')
        if self.attention not in {'none','today','clarify','blocked'}:
            raise ValueError('Invalid attention')
        if self.attention=='blocked' and not (self.blocker or '').strip():
            raise ValueError('Blocked attention requires a concrete dependency')
        if self.workflow=='done' and not (self.acceptance or '').strip():
            raise ValueError('Completion requires acceptance evidence')


def transition(item: WorkItem, workflow: Workflow, *, acceptance: str | None = None) -> WorkItem:
    allowed={'backlog':{'ready'},'ready':{'backlog','in_progress'},'in_progress':{'ready','review'},'review':{'in_progress','done'},'done':set()}
    if workflow not in allowed[item.workflow]:
        raise ValueError(f'Invalid transition: {item.workflow} → {workflow}')
    return replace(item,workflow=workflow,acceptance=acceptance or item.acceptance,attention='none' if workflow=='done' else item.attention)


def project_attention(items: list[WorkItem], *, today_limit: int = 3) -> dict:
    if today_limit < 1:
        raise ValueError('Today capacity must be positive')
    if len({item.id for item in items})!=len(items):
        raise ValueError('Duplicate canonical work item identity')
    views={name:[] for name in ['today','clarify','blocked']}
    for item in items:
        if item.workflow!='done' and item.attention!='none':
            # Projections contain canonical references, never second editable copies.
            views[item.attention].append({'id':item.id,'project':item.project,'title':item.title,'source':item.source})
    return {'views':views,'capacity':{'today_limit':today_limit,'selected':len(views['today']),'over_limit':len(views['today'])>today_limit}}


def checkpoints(items: list[WorkItem]) -> list[dict]:
    return [{'project':project,'resume_from':[{'item_id':item.id,'next_action':item.next_action,'source':item.source} for item in items if item.project==project and item.workflow!='done']} for project in sorted({item.project for item in items})]


def run(input_path: Path, out: Path):
    payload=json.loads(input_path.read_text(encoding='utf-8'))
    items=[WorkItem(**row) for row in payload['work_items']]
    report={**project_attention(items,today_limit=payload.get('today_limit',3)),'checkpoints':checkpoints(items)}
    out.mkdir(parents=True,exist_ok=True)
    (out/'attention.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(f'{len(items)} canonical work items -> 3 attention views; project provenance preserved.')
    print(f'Output: {out/"attention.json"}')
    return report


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input',type=Path,default=Path(__file__).parent/'examples/work-items.json')
    parser.add_argument('--out',type=Path,default=Path('output'))
    args=parser.parse_args()
    run(args.input,args.out)
