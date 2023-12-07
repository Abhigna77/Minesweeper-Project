
from openai import OpenAI

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--query", default=None, type=str, required=True, help="Enter your query: ")
parser.add_argument("--api_key", default=None, type=str, required=True, help="Enter your OpenAI API key: ")
args = parser.parse_args()
client = OpenAI(api_key=args.api_key)

prompt="""You need to answer the given query by giving an output in JSON format of the tools, argument names, argument values which are needed to solve the query.If the query cannot be solved by the list of tools I provide then outout an empty list.
The following is the list of tools,argument names,descriptions,examples etc. Understand the functionality of each tool and argument:
[{"tool_name":"works_list",
 "Description":"Returns a list of work items matching the request",
 "ArgumentName":"applies_to_part",
 "ArgumentDescription":"Filters for work belonging to any of the provided parts",
 "ArgumentType":"array of strings",
 "ArgumentValueExample":"Example:["FEAT-123","ENH-123","PROD-123","CAPL-123"]"},
 {"tool_name":"works_list",
  "Description":"Returns a list of work items matching the request",
  "ArgumentName":"created_by",
  "ArgumentDescription":"Filters for work created by any of these users",
  "ArgumentType":"array of strings",
   "ArgumentValueExample":"Example:["DEVU-123"]"},
 {"tool_name":"works_list",
  "Description":"Returns a list of work items matching the request",
  "ArgumentName":"issue.priority",
  "ArgumentDescription":"Filters for issues with any of the provided priorities. Allowed values: p0, p1, p2,p3",
  "ArgumentType":"array of strings",
  "ArgumentValueExample":"[]"},
 {"tool_name":"works_list",
  "Description":"Returns a list of work items matching the request",
  "ArgumentName":"issue.rev_orgs",
  "ArgumentDescription":"Filters for issues with any of the provided Rev organizations",
  "ArgumentType":"array of strings",
  "ArgumentValueExample":"Example:["REV-123""},
 {"tool_name":"works_list",
  "Description":"Returns a list of work items matching the request",
  "ArgumentName":"limit",
  "ArgumentDescription":"The maximum number of works to return. The default is'50'",
  "ArgumentType":"integer (int32)",
 "ArgumentValueExample":"[]"},
 {"tool_name":"works_list",
  "Description":"Returns a list of work items matching the request",
  "ArgumentName":"owned_by",
  "ArgumentDescription":"Filters for work owned by any of these users",
  "ArgumentType":"array of strings",
  "ArgumentValueExample":"Example:["DEVU-123"]"},
 {"tool_name":"works_list",
  "Description":"Returns a list of work items matching the request",
  "ArgumentName":"stage.name",
  "ArgumentDescription":"Filters for records in the provided stage(s) by name",
  "ArgumentType":"array of strings",
  "ArgumentValueExample":"[]"},
 {"tool_name":"works_list",
  "Description":"Returns a list of work items matching the request",
  "ArgumentName":"ticket.needs_response",
  "ArgumentDescription":"Filters for tickets that need a response",
  "ArgumentType":"boolean",
  "ArgumentValueExample":"[]"},
 {"tool_name":"works_list",
  "Description":"Returns a list of work items matching the request",
  "ArgumentName":"ticket.rev_org",
  "ArgumentDescription":"Filters for tickets associated with any of the provided Rev organizations",
  "ArgumentType":"array of strings",
  "ArgumentValueExample":"Example:["REV-123"]"},
 {"tool_name":"works_list",
  "Description":"Returns a list of work items matching the request",
  "ArgumentName":"ticket.severity",
  "ArgumentDescription":"Filters for tickets with any of the provided severities. Allowed values: blocker, high, low, medium"},
 {"tool_name":"works_list",
  "Description":"Returns a list of work items matching the request",
  "ArgumentName":"ticket.source_channel",
  "ArgumentDescription":"Filters for tickets with any of the provided source channels",
  "ArgumentType":"array of strings"},
 {"tool_name":"works_list",
  "Description":"Returns a list of work items matching the request",
  "ArgumentName":"type",
  "ArgumentDescription":"Filters for work of the provided types. Allowed values: issue, ticket, task",
  "ArgumentType":"array of strings"},
 {"tool_name":"summarize_objects",
  "Description":"Summarizes a list of objects. The logic of how to summarize a particular object type is an internal implementation detail.",
  "ArgumentName":"objects",
  "ArgumentDescription":"List of objects to summarize",
  "ArgumentType":"array of objects"},
 {"tool_name":"prioritize_objects",
  "Description":"Returns a list of objects sorted by priority. The logic of what constitutes priority for a given object is an internal implementation detail.",
  "ArgumentName":"objects",
  "ArgumentDescription":"A list of objects to be prioritized",
  "ArgumentType":"array of objects"},
 {"tool_name":"add_work_items_to_sprint",
  "Description":"Adds the given work items to the sprint",
  "ArgumentName":"work_ids",
  "ArgumentDescription":"A list of work item IDs to be added to the sprint",
  "ArgumentType":"array of objects"},
 {"tool_name":"add_work_items_to_sprint",
  "Description":"Adds the given work items to the sprint",
  "ArgumentName":"sprint_id",
  "ArgumentDescription":"The ID of the sprint to which the work items should be added",
  "ArgumentType":"str"},
 {"tool_name":"get_sprint_id",
  "Description":"Returns the ID of the current sprint"},
 {"tool_name":"get_similar_work_item",
  "Description":"Returns a list of work items that are similar to the given work item",
  "ArgumentName":"work_id ",
  "ArgumentDescription":"The ID of the work item for which you want to find similar items",
  "ArgumentType":"string"},
 {"tool_name":"search_object_by_name",
  "Description":"Given a search string, returns the id of a matching object in the system of record. If multiple matches are found, it returns the one where the confidence is highest.",
  "ArgumentName":"query",
  "ArgumentDescription":"The search string, could be for example customer’s name, part name, user name.",
  "ArgumentType":"string"},
 {"tool_name":"create_actionable_tasks_from_text",
  "Description":"Given a text, extracts actionable insights, and creates tasks for them, which are kind of a work item.",
  "ArgumentName":"text",
  "ArgumentDescription":"The text from which the actionable insights need to be created.",
  "ArgumentType":"string"},
 {"tool_name":"who_am_i",
  "Description":"Returns the ID of the current user"}]


To reference the value of the ith tool in the chain, use $$PREV[i] as argument value. i =
0, 1, .. j-1; j = current tool’s index in the array
If the query could not be answered with the given set of tools, output an empty list instead.


  Sample queries and their outputs:
  [{"Query":"Summarize issues similar to don:core:dvrv-us-1:devo/0:issue/1"},
"Output":[
{
"tool_name": "get_similar_work_items",
"arguments": [
{
"argument_name": "work_id",
"argument_value": "don:core:dvrv-us-1:devo/0:issue/1"
}
]
},
{
"tool_name": "summarize_objects",
"arguments": [
{
"argument_name": "objects",
"argument_value": "$$PREV[0]"
}
]
}
],
{"Query":"What is the meaning of life?",
"Output":[]},
{"Query":"Prioritize my P0 issues and add them to the current sprint",
"Output":[
{
"tool_name": "whoami",
"arguments": []
},
{
"tool_name": "works_list",
"arguments": [
{
"argument_name": "issue.priority",
"argument_value": "p0"
},
{
"argument_name": "owned_by",
"argument_value": "$$PREV[0]"
}
]
},
{
"tool_name": "prioritize_objects",
"arguments": [
{
"argument_name": "objects",
"argument_value": "$$PREV[1]"
}
]
},
{
"tool_name": "get_sprint_id",
"arguments": []
},
{
"tool_name": "add_work_items_to_sprint",
"arguments": [
{
"argument_name": "work_ids",
"argument_value": "$$PREV[2]"
},
{
"argument_name": "sprint_id",
"argument_value": "$$PREV[3]"
}
]
}
]},
{"Query":"Summarize high severity tickets from the customer UltimateCustomer",
"Output":
{
"tool_name": "search_object_by_name",
"arguments": [
{
"argument_name": "query",
"argument_value": "UltimateCustomer"
}
]
},
{
"tool_name": "works_list",
"arguments": [
{
"argument_name": "ticket.rev_org",
"argument_value": "$$PREV[0]"
}
]
},
{
"tool_name": "summarize_objects",
"arguments": [
{
"argument_name": "objects",
"argument_value": "$$PREV[1]"
}
]
}
]},
{"Query":"What are my all issues in the triage stage under part FEAT-123? Summarize them.",
"Output":[
{
"tool_name": "whoami",
"arguments": []
},
{
"tool_name": "works_list",
"arguments": [
{
"argument_name": "stage.name",
"argument_value": "triage"
},
{
"argument_name": "applies_to_part",
"argument_value": "FEAT-123"
},
{
"argument_name": "owned_by",
"argument_value": "$$PREV[0]"
}
]
},
{
"tool_name": "summarize_objects",
"arguments": [
{
"argument_name": "objects",
"argument_value": "$$PREV[1]"
}
]
}
]},
{"Query":"List all high severity tickets coming in from slack from customer Cust123 and generate a summary of them.",
"Output":[
{
"tool_name": "search_object_by_name",
"arguments": [
{
"argument_name": "query",
"argument_value": "Cust123"
}
]
},
{
"tool_name": "works_list",
"arguments": [
{
"argument_name": "ticket.rev_org",
"argument_value": "$$PREV[0]"
},
{
"argument_name": "ticket.severity",
"argument_value": "high"
},
{
"argument_name": "ticket.source_channel",
"argument_value": "slack"
}
]
},
{
"tool_name": "summarize_objects",
"arguments": [
{
"argument_name": "objects",
"argument_value": "$$PREV[1]"
}
]
}
]},
{"Query":"Given a customer meeting transcript T, create action items and add them to my current sprint",
"Output":[
{
"tool_name": "create_actionable_tasks_from_text",
"arguments": [
{
"argument_name": "text",
"argument_value": "T"
}
]
},
{
"tool_name": "get_sprint_id",
"arguments": []
},
{
"tool_name": "add_work_items_to_sprint",
"arguments": [
{
"argument_name": "work_ids",
"argument_value": "$$PREV[0]"
},
{
"argument_name": "sprint_id",
"argument_value": "$$PREV[1]"
}
]
}
]},
{"Query":"Get all work items similar to TKT-123, summarize them, create issues from that summary, and prioritize them",
"Output":[
{
"tool_name": "get_similar_work_items",
"arguments": [
{
"argument_name": "work_id",
"argument_value": "TKT-123"
}
]
},
{
"tool_name": "create_actionable_tasks_from_text",
"arguments": [
{
"argument_name": "text",
"argument_value": "$$PREV[0]"
}
]
},
{
"tool_name": "prioritize_objects",
"arguments": [
{
"argument_name": "objects",
"argument_value": "$$PREV[1]"
}
]
}
]
}]
The output is in JSON format. This is my problem statement. 
Example:Now if the query is "Retrieve work items associated with the Rev organisation 'REV-123' and owned by the user 'DEVU-789' , Summarize them and prioritize by severity.",
then the steps u need to follow are the steps the model should follow in recursion of thought (RoT).You should output all these steps when a new query is given to you,along with the output.

1.Divide the problem into subproblems:

Subproblem 1: Retrieve work items associated with the Rev organisation 'REV-123'.
Subproblem 2: Filter work items from Subproblem 1 to only include those owned by the user 'DEVU-789.'
Subproblem 3: Summarize the work items obtained from Subproblem 2.
Subproblem 4: Prioritize the summarized work items by severity.

2.Generate GO and STOP tokens:
GO
... Subproblem 1 ...
... Subproblem 2 ...
... Subproblem 3 ...
... Subproblem 4 ...
STOP

3.Solve each subproblem recursively:

For Subproblem 1, use the "works_list" tool with the argument "ticket.rev_org" set to "REV-123."
For Subproblem 2, use the "works_list" tool with the arguments "owned_by" set to "DEVU-789" and "objects" set to the output of Subproblem 1.
Subproblem 3 does not require further division and can be solved directly using the "summarize_objects" tool with the argument "objects" set to the output of Subproblem 2.
Subproblem 4 does not require further division and can be solved directly using the "prioritize_objects" tool with the argument "objects" set to the output of Subproblem 3.

4.Use appropriate tools and combine the outputs of Subproblems 1, 2, 3, and 4.Replace the corresponding THINK tokens with the actual results obtained from each subproblem.
The final answer is the prioritized list of work items associated with 'REV-123,' owned by 'DEVU-789,' and summarized.

"[
    {
        ""tool_name"": ""works_list"",
        ""arguments"": [
            {
                ""argument_name"": ""ticket.rev_org"",
                ""argument_value"": ""REV-123""
            },
            {
                ""argument_name"": ""owned_by"",
                ""argument_value"": ""DEVU-789""
            }
        ]
    },
    {
        ""tool_name"": ""summarize_objects"",
        ""arguments"": [
            {
                ""argument_name"": ""objects"",
                ""argument_value"": ""$$PREV[0]""
            }
        ]
    },
    {
        ""tool_name"": ""prioritize_objects"",
        ""arguments"": [
            {
                ""argument_name"": ""objects"",
                ""argument_value"": ""$$PREV[1]""
            }
        ]
    }
]
"




Now follow the same approach,after looking at the example above and answer the query. Refer to the sample queries and the outputs I had given.
Give the final output in json format. """
add = f"{args.query}. I would like u to follow the steps through which the problem can be solved like the example above and reach the end output."
tup = (prompt,add)
prompt_final = ' '.join(tup)


completion = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {
            "role": "user",
            "content": prompt_final,
        },
    ],
)
print(completion.choices[0].message.content)