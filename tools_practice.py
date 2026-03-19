from google.genai import types
from google import genai

def calculator(operation : str):
    calculation = eval(operation)

    return calculation

calculator_declaration = types.FunctionDeclaration(
    name="calculator",
    description="take the parameter read its type and calculate the math",
    parameters={
         "type" : "object" , 
        "properties" : {
            "operation" : {
                "type" : "string" ,
                "description" : "any arithmetic operation (for eg : 245 + 89)"
        }
    },
    "required" : ["operation"]
    }
)


tool = types.Tool(function_declarations=[calculator_declaration])

client = genai.Client()

response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents="what is 98 multiplied by 78 ?",
    config= types.GenerateContentConfig(tools=[tool])
)


part = response.candidates[0].content.parts[0]

if part.function_call:
    function_call = response.candidates[0].content.parts[0].function_call

    function_response_part = types.Part.from_function_response(
        name = function_call.name,
        response={"result" : calculator(function_call.args["operation"])},
        
    )

    second_response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=[
            types.Content(role="user" , parts=[types.Part(text="what is 98 * 78")]),
            types.Content(role="model" , parts=[response.candidates[0].content.parts[0]]),
            types.Content(role="user" , parts=[function_response_part]),
            
        ],
        config=types.GenerateContentConfig(tools=[tool])
    )

    print(second_response.text)
else:
    print(response.text)

    
    
