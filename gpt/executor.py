import json
from .tools import TOOL_FUNCTIONS, TOOL_SCHEMAS
from .utils import convert_to_excel_table


SYSTEM_FIELDS = {
    "download_url",
    "filepath",
}


class ToolExecutor:

    def __init__(self, client):
        self.client = client

    def execute_tool(self, item, context):

        arguments = json.loads(item.arguments)

        if item.name == "create_excel_file":

            if "rows" not in arguments:

                search = context.get("search_product")

                if search and search.get("success"):
                    headers, rows = convert_to_excel_table(
                        search["data"]
                    )

                    arguments["headers"] = headers
                    arguments["rows"] = rows

        if item.name == "send_email":

            excel = context.get("create_excel_file")

            if excel and excel.get("success"):
                arguments["attachment"] = excel["filepath"]

        tool = TOOL_FUNCTIONS.get(item.name)

        if tool is None:
            raise Exception(
                f"{item.name} Tool이 등록되어 있지 않습니다."
            )

        try:
            result = tool(
                context=context,
                **arguments
            )

        except Exception as e:

            result = {
                "success": False,
                "message": str(e)
            }

        # Context에는 전체 결과 저장
        context.set(item.name, result)

        # GPT에게 전달할 데이터 생성
        gpt_result = {
            key: value
            for key, value in result.items()
            if key not in SYSTEM_FIELDS
        }

        return {
            "type": "function_call_output",
            "call_id": item.call_id,
            "output": json.dumps(gpt_result, ensure_ascii=False)
        }

    def run(self, response, context):

        max_iterations = 10
        iteration = 0

        while True:

            iteration += 1

            if iteration > max_iterations:
                raise RuntimeError("Tool 호출 횟수가 최대치를 초과했습니다.")

            tool_outputs = []

            for item in response.output:

                if item.type != "function_call":
                    continue

                tool_outputs.append(
                    self.execute_tool(item, context)
                )

            if not tool_outputs:
                break

            response = self.client.responses.create(
                model="gpt-5",
                previous_response_id=response.id,
                tools=TOOL_SCHEMAS,
                input=tool_outputs
            )

        context.save()

        return response
