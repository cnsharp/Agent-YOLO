# Agent YOLO

Agent YOLO is an AI-agent extender that brings a unified "YOLO panel" for AI coding agents
(Cursor, Claude, Codex, and many more) into your IDE.
It is available across three IDE families — JetBrains, Visual Studio, and Visual Studio Code.

## Agent YOLO Family

<p align="center">
  <img src="resources/icons/pluginIcon.svg" alt="Agent YOLO">
</p>
<p align="center">
  <a href="https://plugins.jetbrains.com/plugin/33442-agent-yolo/"><img src="https://upload.wikimedia.org/wikipedia/commons/9/9c/IntelliJ_IDEA_Icon.svg" width="90" alt="IntelliJ IDEA"></a>
  &nbsp;&nbsp;&nbsp;
  <a href="https://marketplace.visualstudio.com/items?itemName=CnSharpStudio.yolo"><img src="https://upload.wikimedia.org/wikipedia/commons/5/59/Visual_Studio_Icon_2019.svg" width="90" alt="Visual Studio"></a>
  &nbsp;&nbsp;&nbsp;
  <a href="https://marketplace.visualstudio.com/items?itemName=cnsharp.agentyolo"><img src="https://upload.wikimedia.org/wikipedia/commons/9/9a/Visual_Studio_Code_1.35_icon.svg" width="90" alt="Visual Studio Code"></a>
</p>

| Product | Platform | Marketplace |
| --- | --- | --- |
| **Agent YOLO for IntelliJ** | JetBrains (IntelliJ IDEA and other IntelliJ-based IDEs) | [JetBrains Marketplace](https://plugins.jetbrains.com/plugin/33442-agent-yolo/) |
| **Agent YOLO for Visual Studio** | Microsoft Visual Studio | [Visual Studio Marketplace](https://marketplace.visualstudio.com/items?itemName=CnSharpStudio.yolo) |
| **Agent YOLO for Visual Studio Code** | Visual Studio Code | [Visual Studio Marketplace](https://marketplace.visualstudio.com/items?itemName=cnsharp.agentyolo) |

## Repositories

| Product | GitHub Repository |
| --- | --- |
| Agent YOLO for IntelliJ | https://github.com/cnsharp/YOLO-IntelliJ |
| Agent YOLO for Visual Studio | https://github.com/cnsharp/YOLO-VS |
| Agent YOLO for Visual Studio Code | https://github.com/cnsharp/YOLO-VSC |

> **Related:** [`ai-agents-terminal-vsc`](https://github.com/cnsharp/ai-agents-terminal-vsc) is a side project that provides a Terminal Agent Launcher on the status bar, and serves as the upstream of *Agent YOLO for Visual Studio Code* (YOLO-VSC is a fork of it). Agent and resource changes on the VS Code side should be made in `ai-agents-terminal-vsc` first, then ported to YOLO-VSC.

## Supported agents

The agent list below is shared across the whole **Agent YOLO** family (IntelliJ, Visual Studio, and VS Code editions). It is generated from `agents.json` in the [YOLO-VS](https://github.com/cnsharp/YOLO-VS) repository — that file is the single source of truth, so new or changed agents are added there and synced to the other editions. Any agent not listed works as a custom tool: configure it in the IDE settings and fill in its flags yourself.

| id | display name | command | website |
|---|---|---|---|
| claude | Claude Code | `claude` | <a href="https://claude.ai/"><img src="resources/icons/agents/claude.svg" height="20" alt="Claude Code"></a> |
| codex | Codex | `codex` | <a href="https://openai.com/codex"><img src="resources/icons/agents/codex.svg" height="20" alt="Codex"></a> |
| cursor | Cursor | `agent` | <a href="https://cursor.com/cli"><img src="resources/icons/agents/cursor.svg" height="20" alt="Cursor"></a> |
| copilot | GitHub Copilot | `copilot` | <a href="https://github.com/features/copilot"><img src="resources/icons/agents/copilot.svg" height="20" alt="GitHub Copilot"></a> |
| opencode | OpenCode | `opencode` | <a href="https://opencode.ai/"><img src="resources/icons/agents/opencode.png" height="20" alt="OpenCode"></a> |
| aider | Aider | `aider` | <a href="https://aider.chat/"><img src="resources/icons/agents/aider.svg" height="20" alt="Aider"></a> |
| cline | Cline | `cline` | <a href="https://cline.bot/"><img src="resources/icons/agents/cline.svg" height="20" alt="Cline"></a> |
| continue | Continue | `cn` | <a href="https://continue.dev/"><img src="resources/icons/agents/continue.svg" height="20" alt="Continue"></a> |
| openclaw | OpenClaw | `openclaw` | <a href="https://openclaw.ai/"><img src="resources/icons/agents/openclaw.svg" height="20" alt="OpenClaw"></a> |
| kiro | Kiro | `kiro-cli` | <a href="https://kiro.dev/"><img src="resources/icons/agents/kiro.svg" height="20" alt="Kiro"></a> |
| goose | Goose | `goose` | <a href="https://block.github.io/goose/"><img src="resources/icons/agents/goose.svg" height="20" alt="Goose"></a> |
| crush | Charm Crush | `crush` | <a href="https://charm.sh/crush"><img src="resources/icons/agents/crush.png" height="20" alt="Charm Crush"></a> |
| amp | Amp | `amp` | <a href="https://ampcode.com/"><img src="resources/icons/agents/amp.svg" height="20" alt="Amp"></a> |
| kimi | Kimi | `kimi` | <a href="https://kimi.moonshot.cn/"><img src="resources/icons/agents/kimi.png" height="20" alt="Kimi"></a> |
| qwen-code | Qwen Code | `qwen` | <a href="https://qwen.ai/qwencode"><img src="resources/icons/agents/qwen-code.png" height="20" alt="Qwen Code"></a> |
| trae | TraeCode | `traecli` | <a href="https://www.trae.ai/"><img src="resources/icons/agents/trae.svg" height="20" alt="TraeCode"></a> |
| codebuddy | CodeBuddy | `codebuddy` | <a href="https://www.codebuddy.ai/"><img src="resources/icons/agents/codebuddy.svg" height="20" alt="CodeBuddy"></a> |
| qoder | Qoder | `qoder` | <a href="https://qoder.com/"><img src="resources/icons/agents/qoder.svg" height="20" alt="Qoder"></a> |
| devin | Devin | `devin` | <a href="https://devin.ai/"><img src="resources/icons/agents/devin.svg" height="20" alt="Devin"></a> |
| grok | Grok | `grok` | <a href="https://grok.com/"><img src="resources/icons/agents/grok.svg" height="20" alt="Grok"></a> |
| antigravity | Antigravity | `agy` | <a href="https://antigravity.google/"><img src="resources/icons/agents/antigravity.png" height="20" alt="Antigravity"></a> |
| mistral-vibe | Mistral Vibe | `vibe` | <a href="https://mistral.ai/"><img src="resources/icons/agents/mistral-vibe.svg" height="20" alt="Mistral Vibe"></a> |
| kilo | Kilo Code | `kilo` | <a href="https://kilocode.ai/"><img src="resources/icons/agents/kilo.svg" height="20" alt="Kilo Code"></a> |
| hermes | Hermes | `hermes` | <a href="https://hermes-agent.nousresearch.com/"><img src="resources/icons/agents/hermes.png" height="20" alt="Hermes"></a> |
| pi | Pi | `pi` | <a href="https://pi.dev/"><img src="resources/icons/agents/pi.svg" height="20" alt="Pi"></a> |
| droid | Droid | `droid` | <a href="https://factory.ai/"><img src="resources/icons/agents/droid.svg" height="20" alt="Droid"></a> |
| aug | Auggie | `auggie` | <a href="https://augmentcode.com/"><img src="resources/icons/agents/aug.svg" height="20" alt="Auggie"></a> |
| rovo | Rovo Dev | `rovo` | <a href="https://rovo.atlassian.com/"><img src="resources/icons/agents/rovo.svg" height="20" alt="Rovo Dev"></a> |
| prime-agent | Prime Agent | `prime-agent` | <a href="https://www.primeintellect.ai/"><img src="resources/icons/agents/prime-agent.png" height="20" alt="Prime Agent"></a> |
| autohand | Autohand | `autohand` | <a href="https://autohand.ai/"><img src="resources/icons/agents/autohand.svg" height="20" alt="Autohand"></a> |
| command-code | Command Code | `command-code` | <a href="https://commandcode.ai/"><img src="resources/icons/agents/command-code.svg" height="20" alt="Command Code"></a> |
| ante | Ante | `ante` | <a href="https://antigma.ai/"><img src="resources/icons/agents/ante.svg" height="20" alt="Ante"></a> |
| codebuff | Codebuff | `codebuff` | <a href="https://codebuff.com/"><img src="resources/icons/agents/codebuff.png" height="20" alt="Codebuff"></a> |
| omp | OMP | `omp` | <a href="https://ohmyposh.dev/"><img src="resources/icons/agents/omp.svg" height="20" alt="OMP"></a> |
| agoragentic | Agoragentic | `agoragentic-mcp` | <a href="https://agoragentic.com"><img src="resources/icons/agents/agoragentic.png" height="20" alt="Agoragentic"></a> |
| cortex-code | Cortex Code | `cortex` | <a href="https://docs.snowflake.com/en/user-guide/cortex-code/cortex-code"><img src="resources/icons/agents/cortex-code.png" height="20" alt="Cortex Code"></a> |
| corust-agent | Corust Agent | `corust` | <a href="https://corust.ai/"><img src="resources/icons/agents/corust-agent.svg" height="20" alt="Corust Agent"></a> |
| crow-cli | Crow CLI | `crow-cli` | <a href="https://crow-ai.dev"><img src="resources/icons/agents/crow-cli.svg" height="20" alt="Crow CLI"></a> |
| deepagents | DeepAgents | `deepagents-acp` | <a href="https://docs.langchain.com/oss/javascript/deepagents/overview"><img src="resources/icons/agents/deepagents.svg" height="20" alt="DeepAgents"></a> |
| dirac | Dirac | `dirac` | <a href="https://dirac.run"><img src="resources/icons/agents/dirac.svg" height="20" alt="Dirac"></a> |
| dimcode | DimCode | `dim` | <a href="https://dimcode.dev/docs/acp.html"><img src="resources/icons/agents/dimcode.png" height="20" alt="DimCode"></a> |
| fast-agent | Fast Agent | `fast-agent` | <a href="https://fast-agent.ai"><img src="resources/icons/agents/fast-agent.svg" height="20" alt="Fast Agent"></a> |
| glm-agent | GLM Agent | `glm-acp-agent` | <a href="https://github.com/stefandevo/glm-acp-agent"><img src="resources/icons/agents/glm-agent.svg" height="20" alt="GLM Agent"></a> |
| harn | Harn | `harn` | <a href="https://harnlang.com"><img src="resources/icons/agents/harn.svg" height="20" alt="Harn"></a> |
| junie | Junie | `junie` | <a href="https://junie.jetbrains.com"><img src="resources/icons/agents/junie.svg" height="20" alt="Junie"></a> |
| minion-code | Minion Code | `minion-code` | <a href="https://github.com/femto/minion-code"><img src="resources/icons/agents/minion-code.svg" height="20" alt="Minion Code"></a> |
| nova | Nova | `nova` | <a href="https://www.compassap.ai/portfolio/nova.html"><img src="resources/icons/agents/nova.svg" height="20" alt="Nova"></a> |
| poolside | Poolside | `pool` | <a href="https://poolside.ai"><img src="resources/icons/agents/poolside.svg" height="20" alt="Poolside"></a> |
| sigit | siGit Code | `sigit` | <a href="https://smbcloud.xyz"><img src="resources/icons/agents/sigit.png" height="20" alt="siGit Code"></a> |
| stakpak | Stakpak | `stakpak` | <a href="https://stakpak.dev"><img src="resources/icons/agents/stakpak.png" height="20" alt="Stakpak"></a> |
| vtcode | VT Code | `vtcode` | <a href="https://github.com/vinhnx/VTCode"><img src="resources/icons/agents/vtcode.png" height="20" alt="VT Code"></a> |
