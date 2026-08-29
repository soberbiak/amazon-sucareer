# Install the Amazon Operations Career Skills into one or more agent skill homes.
# Usage: .\install.ps1 -Target codex,claude,dsh,agents

param(
  [string]$Target = "all"
)

$ErrorActionPreference = "Stop"
$repositoryRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$sourceRoot = Join-Path $repositoryRoot "skills"
$skillNames = @(
  "amazon-ops-evidence",
  "amazon-ops-greeting",
  "amazon-ops-interview",
  "amazon-ops-jd",
  "amazon-ops-profile",
  "amazon-ops-resume",
  "amazon-ops-resume-audit"
)

if (-not (Test-Path -LiteralPath (Join-Path $sourceRoot "amazon-ops-resume\SKILL.md"))) {
  throw "Skill source not found under $sourceRoot"
}

function Install-Skills([string]$DestinationRoot, [string]$Label) {
  New-Item -ItemType Directory -Path $DestinationRoot -Force | Out-Null
  foreach ($skillName in $skillNames) {
    $destination = Join-Path $DestinationRoot $skillName
    if (Test-Path -LiteralPath $destination) {
      Remove-Item -LiteralPath $destination -Recurse -Force
    }
    Copy-Item -LiteralPath (Join-Path $sourceRoot $skillName) -Destination $destination -Recurse
  }
  Write-Host "installed $($skillNames.Count) skills -> $DestinationRoot ($Label)"
}

$targets = if ($Target -eq "all") { @("codex", "claude", "dsh", "agents") } else { $Target -split "," }
$codexHome = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $HOME ".codex" }
$claudeHome = Join-Path $HOME ".claude"
$dshHome = if ($env:DSH_HOME) { $env:DSH_HOME } else { Join-Path $HOME ".dsh" }
$agentsHome = if ($env:DSH_AGENTS_HOME) { $env:DSH_AGENTS_HOME } else { Join-Path $HOME ".agents" }

foreach ($targetName in $targets) {
  switch ($targetName.Trim()) {
    "codex"  { Install-Skills (Join-Path $codexHome "skills") "OpenAI Codex" }
    "claude" { Install-Skills (Join-Path $claudeHome "skills") "Claude Code" }
    "dsh"    { Install-Skills (Join-Path $dshHome "skills") "DeepSeek Harness" }
    "agents" { Install-Skills (Join-Path $agentsHome "skills") "shared agent skills" }
    default { throw "Unknown target '$targetName'. Use codex, claude, dsh, agents, or all." }
  }
}

Write-Host "Done. Start a new agent session so the skills reload."
