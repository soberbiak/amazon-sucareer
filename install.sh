#!/usr/bin/env bash
# Install the Amazon Operations Career Skills into one or more agent skill homes.
# Usage: ./install.sh [codex] [claude] [dsh] [agents] | all

set -euo pipefail

repository_root="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source_root="$repository_root/skills"
skill_names=(
  amazon-ops-evidence
  amazon-ops-greeting
  amazon-ops-interview
  amazon-ops-jd
  amazon-ops-profile
  amazon-ops-resume
  amazon-ops-resume-audit
)

if [[ ! -f "$source_root/amazon-ops-resume/SKILL.md" ]]; then
  echo "error: skill source not found under $source_root" >&2
  exit 1
fi

targets=("$@")
if [[ ${#targets[@]} -eq 0 ]] || [[ "${targets[0]}" == "all" ]]; then
  targets=(codex claude dsh agents)
fi

install_to() {
  local destination_root="$1"
  local label="$2"
  mkdir -p "$destination_root"
  for skill_name in "${skill_names[@]}"; do
    rm -rf "$destination_root/$skill_name"
    cp -R "$source_root/$skill_name" "$destination_root/$skill_name"
  done
  echo "installed ${#skill_names[@]} skills -> $destination_root ($label)"
}

codex_home="${CODEX_HOME:-$HOME/.codex}"
claude_home="$HOME/.claude"
dsh_home="${DSH_HOME:-$HOME/.dsh}"
agents_home="${DSH_AGENTS_HOME:-$HOME/.agents}"

for target in "${targets[@]}"; do
  case "$target" in
    codex)  install_to "$codex_home/skills" "OpenAI Codex" ;;
    claude) install_to "$claude_home/skills" "Claude Code" ;;
    dsh)    install_to "$dsh_home/skills" "DeepSeek Harness" ;;
    agents) install_to "$agents_home/skills" "shared agent skills" ;;
    *)
      echo "error: unknown target '$target' (codex | claude | dsh | agents | all)" >&2
      exit 1
      ;;
  esac
done

echo "Done. Start a new agent session so the skills reload."
