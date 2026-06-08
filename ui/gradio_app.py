import gradio as gr
import sys
import os

# Add path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from research.crew import ResearchAgentCrew


# ─────────────────────────────────────────
# RESEARCH FUNCTION — Called by Gradio
# ─────────────────────────────────────────

def run_research(topic: str, depth: str) -> tuple:
    """
    Gradio will call this function
    Returns: report, status, word_count
    """

    # Empty check
    if not topic.strip():
        return (
            "❌ Error: Topic cannot be empty",
            "❌ Failed",
            "0 words"
        )

    # Too short check
    if len(topic.strip()) < 3:
        return (
            "❌ Error: Topic must be at least 3 characters long",
            "❌ Failed",
            "0 words"
        )

    try:
        # Run crew
        crew = ResearchAgentCrew()
        result = crew.run_research(topic=topic, depth=depth)

        # Error check
        if result.status == "error":
            return (
                f"❌ Error: {result.error_message}",
                "❌ Failed",
                "0 words"
            )

        # Success
        return (
            result.report,
            "✅ Success",
            f"{result.word_count} words"
        )

    except Exception as e:
        return (
            f"❌ Unexpected error: {str(e)}",
            "❌ Failed",
            "0 words"
        )


# ─────────────────────────────────────────
# GRADIO UI
# ─────────────────────────────────────────

def create_ui():
    with gr.Blocks(
        title="AI Research Agent",
        theme=gr.themes.Soft()
    ) as demo:

        # ── Header ──
        gr.Markdown("""
        # 🔍 AI Research Agent
        ### Powered by CrewAI + Tavily Search
        Enter any topic and get a professional research report automatically.
        """)

        # ── Input Section ──
        with gr.Row():
            with gr.Column(scale=3):
                topic_input = gr.Textbox(
                    label="Research Topic",
                    placeholder="e.g. Artificial Intelligence trends in 2026",
                    lines=2
                )
            with gr.Column(scale=1):
                depth_input = gr.Dropdown(
                    label="Research Depth",
                    choices=["quick", "detailed", "comprehensive"],
                    value="detailed"
                )

        # ── Buttons ──
        with gr.Row():
            submit_btn = gr.Button(
                "🚀 Start Research",
                variant="primary",
                size="lg"
            )
            clear_btn = gr.Button(
                "🗑️ Clear",
                variant="secondary",
                size="lg"
            )

        # ── Status Bar ──
        with gr.Row():
            status_output = gr.Textbox(
                label="Status",
                interactive=False,
                scale=2
            )
            word_count_output = gr.Textbox(
                label="Word Count",
                interactive=False,
                scale=1
            )

        # ── Output Section ──
        report_output = gr.Markdown(
            label="Research Report",
            value="Report will appear here..."
        )

        # ── Example Topics ──
        gr.Examples(
            examples=[
                ["Artificial Intelligence trends in 2026", "detailed"],
                ["LangChain vs LangGraph comparison", "comprehensive"],
                ["Python FastAPI best practices", "quick"],
                ["Machine Learning in Healthcare", "detailed"],
                ["Agentic AI future scope", "comprehensive"],
            ],
            inputs=[topic_input, depth_input],
            label="Example Topics — Click to Try"
        )

        # ── Button Actions ──
        submit_btn.click(
            fn=run_research,
            inputs=[topic_input, depth_input],
            outputs=[report_output, status_output, word_count_output],
            show_progress=True
        )

        clear_btn.click(
            fn=lambda: ("", "detailed", "Report will appear here...", "", ""),
            outputs=[topic_input, depth_input, report_output,
                     status_output, word_count_output]
        )

    return demo


# ─────────────────────────────────────────
# RUN APPLICATION
# ─────────────────────────────────────────

if __name__ == "__main__":
    demo = create_ui()
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False
    )