# TODO Pane

**This is not implemented yet**


A personal project for learning LLMs a bit better. A way to try out if there is a way to utilize local LLMs for task prioritization and potential completion. 

The goal is to have a single pane of glass for all the things that need to be done.

## Ideas and components

As much as possible, everything is done locally as Calendar and TODO contain a lot of private data.

- TODO Application: OmniFocus Pro
- Time planning: MacOS Calendar that has a lot of calendars in them, and those require additional classification. The main calendar used is [stored in Synology Calendar](https://www.synology.com/en-global/dsm/feature/calendar)
- Prioritization inputs: Just local config file for now, in TOML format.
- LLM: Variety of backends depending on experimentation: using [Simon's LLM](https://llm.datasette.io/en/stable/). Choosing so they can run on Mac Mini M1, currently allowing for orca-2-13b, Meta-Llama-3-8B-Instruct and nous-hermes-llama2-13b as the most promising models

## Next

- Better task breakdown and automation; bridge between tasks from todo and Obsidian entries
- Integrate e-mail? How much of that is actually used? That said, would it be useful to use LLM to sift through the dumping-grouond email for useful bits?
- Integration goal and value-based learning planning?
- Ingest NAS documents for things like expiration dates and renewals
