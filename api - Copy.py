from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI


prompt = ChatPromptTemplate.from_template("explain the math concept with an example{foo}")
model = ChatOpenAI(openai_api_key="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")

functions = [
    {
        "name": "Concept",
        "description": "Math concept",
        "parameters": {
            "type": "object",
            "properties": {
                "setup": {"type": "string", "description": "The name of the concept"},
                "explaination": {
                    "type": "string",
                    "description": "The simple explaination of the concept in fourth grader language with simple analogies",
                },
            },
            "required": ["setup", "explaination"],
        },
    }
]
chain = prompt | model.bind(function_call={"name": "concept"}, functions=functions)


from langchain_core.output_parsers import StrOutputParser

chain = prompt | model | StrOutputParser()

result= chain.invoke({"foo": "3 digit by 2 digit multiplication"})

print (result)



