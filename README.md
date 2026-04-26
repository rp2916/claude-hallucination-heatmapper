# 🔍 Semantic Hallucination Heatmapper (Claude Skill)

A custom skill built for Anthropic's Claude that acts as an automated fact-checker. It forces the AI to "show its doubt" by evaluating its own factual consistency and visually highlighting potential hallucinations in real-time.

## 🚀 How It Works

Large Language Models (LLMs) often suffer from "blind confidence" and lack epistemic uncertainty. This tool uses a **Self-Consistency Evaluator** approach:
1. **Multi-Sampling:** It intercepts the user's prompt and queries the Claude API multiple times in the background with a high temperature.
2. **Text Comparison:** It uses Python's `difflib` to cross-examine the generated claims against each other.
3. **Color-Coded Heatmap:** It outputs the final response wrapped in HTML color tags to indicate confidence:
   * 🟢 **Green Text:** High confidence (Claude agreed with itself across all samples).
   * 🟡 **Yellow Text:** Medium confidence (Minor phrasing variations or slight discrepancies).
   * 🔴 **Red Text:** High hallucination risk (Claude gave conflicting facts/dates/names every time).

## 📂 Project Structure

* `heatmapper.py`: The core Python logic that runs inside Claude's code execution sandbox. It handles the background API calls and the semantic text comparison.
* `SKILL.md`: The YAML-configured instructions that tell Claude's UI how and when to trigger the skill.

## 🛠️ Installation & Usage

To use this natively inside your Claude interface:

1. Download or clone this repository to your local machine.
2. Select both `heatmapper.py` and `SKILL.md` and compress them into a single `.zip` file.
3. Open Claude in your browser.
4. Navigate to **Customize > Skills** in the sidebar.
5. Click **+ Create skill**, select **Upload a skill**, and upload your `.zip` file.
6. Toggle the skill **On**.

**To trigger it in chat, simply say:** *"[Your prompt here]. Use my heatmapper skill to verify."*

## ⚠️ Prerequisites

Because this script runs inside Claude's sandbox but needs to generate fresh background samples, **it requires an Anthropic API Key.** When you trigger the skill for the first time in a chat, Claude will ask you to provide your API key. Ensure your Anthropic Developer account is funded, as the background API calls (even using the cheaper Haiku model) will consume a very small amount of credits per use.
