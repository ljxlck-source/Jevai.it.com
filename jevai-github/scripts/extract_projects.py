from html.parser import HTMLParser
from pathlib import Path
import json
import argparse
class Parser(HTMLParser):
 def __init__(self):
  super().__init__();self.rows=[];self.row=None;self.field=None
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=='li':self.row={'category':a.get('data-cat'),'name':'','url':'','originalDescription':'','starsSnapshot':''}
  if self.row is not None:
   if tag=='a':self.row['url']=a.get('href','');self.field='name'
   if tag=='span':self.field={'pi__desc':'originalDescription','pi__star':'starsSnapshot'}.get(a.get('class'))
 def handle_data(self,data):
  if self.row is not None and self.field:self.row[self.field]+=data
 def handle_endtag(self,tag):
  if tag in ['a','span']:self.field=None
  if tag=='li' and self.row:
   self.rows.append({k:' '.join(v.split()) for k,v in self.row.items()});self.row=None
args=argparse.ArgumentParser(description='Re-import the original 46-project HTML export.')
args.add_argument('html_file', type=Path)
source=args.parse_args().html_file
p=Parser();p.feed(source.read_text())
translations=[
('jev-router','Route Claude Code tasks to a suitable lower-cost model from a defined set of candidates.'),
('jev-agent-skill-router','Choose a skill for an agent, with explicit no-skill and review paths when the match is uncertain.'),
('jcm-router','A local proxy that selects a Claude model and reasoning effort for each message.'),
('jev-router · prismhq','A LiteLLM-based router that uses Jev to choose a model for each request.'),
('fx','A coding agent from Vercel Labs that uses Jev for permission-review decisions.'),
('jev-axi','Assess shell commands for destructive actions, data transfer, remote execution and weakened security before an agent acts.'),
('jev-guard','A guard layer for coding agents that evaluates prompt injection and potentially dangerous operations.'),
('is-malicious','Inspect dependency source and build files, then examine suspicious files and lines more closely.'),
('pi-heed','Check whether an agent’s next action actually follows the user’s request.'),
('jev-git','Scan changes for secrets and destructive commands before a Git commit or push.'),
('Abide','Watch coding-agent changes and flag potential violations of project rules for review.'),
('Clean Code Judge','Evaluate pull-request files against 31 code-quality questions, then pass findings to a writing model.'),
('DiffJury','Triage pull requests by risk and decide which reviewer should handle them.'),
('limpet','Check completion criteria before an agent announces that a task is finished.'),
('Hunch','Write coding rules in plain language and check them locally or on pull requests.'),
('Browserbase + Jev','Kyle Jeong’s browser-agent demonstration: Jev chooses an action; Stagehand carries it out.'),
('jev-ultrafast','A browser-use agent that lets Jev select the next action and uses a generative model when text is needed.'),
('Jev Browser','A browser-automation project built around Jev decisions at each step.'),
('unclutter','A browser extension that identifies distracting page elements and removes them.'),
('typesafe-adblock','A Chrome extension that turns ad detection into a series of yes-or-no judgments.'),
('public-browser','Let coding agents operate a real Chrome browser, with Jev helping choose actions.'),
('Sniff Test','Check paragraphs for vague phrasing, repetitive endings and other writing patterns using focused judgments.'),
('pagegrade','Evaluate sections of a web page for clarity, writing quality and SEO.'),
('JevSlop','Evaluate note.com articles across eight dimensions and combine them into a content-quality score.'),
('citation-verifier','Use Claude to locate cited passages and Jev to assess support, with a person making the final call.'),
('Email triage · Ryan Vogel','A demonstration of categorizing email, judging priority, detecting spam and deciding whether a reply is needed.'),
('Notra','A marketing-analytics platform exploring Jev for brand-visibility classification.'),
('Email intent routing','Classify incoming messages as invoices or general email and send them to the corresponding workflow.'),
('jev-curate','Filter synthetic datasets using condition judgments and confidence, saving accepted and rejected records separately.'),
('CV screener','A resume-screening experiment with editable criteria and reusable scores. Human review remains essential.'),
('typeful-triage','An issue-triage dashboard covering type, severity, urgency, duplicates and next steps, with recorded human corrections.'),
('fast-jev-compaction','Keep useful tool calls and results in a coding session while removing irrelevant context without summarizing it.'),
('yoshi','A proxy layer for Claude Code and Codex that evaluates which conversation history is still needed.'),
('wakegate','Check whether a scheduled agent wake-up is necessary before waking a larger model.'),
('Jev Trader · Jarrod Watts','A block-by-block trading experiment. The shared demonstration shows dry-run mode; it is not evidence of profitability.'),
('HA-Jev','A Home Assistant integration that answers questions about home state with choices, scores and probabilities.'),
('jevinci','An experimental painter that selects pixel colors in parallel and uses confidence to vary brush width.'),
('pacman-jev','An open-source Pac-Man experiment where Jev chooses which direction to move next.'),
('tetris-ai','Browser Tetris playable by a built-in planner, Jev or a chat model.'),
('Jev Pong','A Pong experiment comparing model-controlled decisions as the ball moves.'),
('robo-harness','A robotic-arm workbench that selects joint actions from candidates and includes a spending limit.'),
('jevcal','Fit confidence thresholds to labeled examples and estimate fallback rates, with checks for model changes.'),
('When reranking does not help','A reported test of 33,047 entries and 164 queries where Jev-only reranking did not outperform vector retrieval.'),
('NanoJev','An independent 0.6B-parameter decision-model implementation with training code, weights and data.'),
('Laya','An independent non-autoregressive decision-model project supporting three question types.'),
('kev','A small independent decision-model experiment based on Qwen2.5-0.5B, designed to train and run on a MacBook.')]
assert len(p.rows)==len(translations)==46
for i,(r,(name,desc)) in enumerate(zip(p.rows,translations)):
 r.update(id=f'project-{i+1:02}',name=name,description=desc,kind='Repository' if 'github.com/' in r['url'] else 'Demo / report')
root=Path(__file__).resolve().parents[1]
(root/'content/projects.json').write_text(json.dumps(p.rows,ensure_ascii=False,indent=2))
print('Extracted and translated 46 projects; all source URLs preserved.')
