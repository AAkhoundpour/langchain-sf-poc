from langchain_core.callbacks import BaseCallbackHandler


class AgentDebugLogger(BaseCallbackHandler):
    def on_chain_start(self, serialized, inputs, **kwargs):
        print("\n[CHAIN START]")
        print(f"Inputs: {inputs}")

    def on_tool_start(self, serialized, input_str, **kwargs):
        tool_name = serialized.get("name", "unknown_tool")
        print(f"\n[TOOL START] {tool_name}")
        print(f"Input: {input_str}")

    def on_tool_end(self, output, **kwargs):
        print("\n[TOOL END]")
        print(f"Output: {output}")

    def on_llm_start(self, serialized, prompts, **kwargs):
        print("\n[LLM START]")
        for prompt in prompts:
            print(prompt)

    def on_llm_end(self, response, **kwargs):
        print("\n[LLM END]")
        print(response)

    def on_agent_action(self, action, **kwargs):
        print("\n[AGENT ACTION]")
        print(f"Tool: {action.tool}")
        print(f"Tool input: {action.tool_input}")
        print(f"Log: {action.log}")

    def on_agent_finish(self, finish, **kwargs):
        print("\n[AGENT FINISH]")
        print(finish.return_values)
