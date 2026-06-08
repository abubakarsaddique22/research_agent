# import sys
# from research.crew import ResearchAgentCrew


# def run():
#     inputs = {
#         'topic': 'Artificial Intelligence trends in 2026'
#     }

#     print("\n" + "="*50)
#     print("   AI RESEARCH AGENT STARTING...")
#     print("="*50 + "\n")

#     # Pydantic validated run
#     crew = ResearchAgentCrew()
#     result = crew.run_research(
#         topic=inputs['topic'],
#         depth="detailed"
#     )

#     print("\n" + "="*50)
#     if result.status == "success":
#         print("   RESEARCH COMPLETE!")
#         print(f"   Word Count: {result.word_count}")
#         print(f"   Time: {result.timestamp}")
#     else:
#         print("   RESEARCH FAILED!")
#         print(f"   Error: {result.error_message}")
#     print("="*50 + "\n")
#     print(result.report)


# if __name__ == "__main__":
#     run()