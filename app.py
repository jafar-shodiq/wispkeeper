# import streamlit as st
# from vertexai.generative_models import FunctionDeclaration, Tool, GenerativeModel, ToolConfig, Content, Part
# from google.cloud import bigquery
# from google.api_core.exceptions import BadRequest, NotFound, ResourceExhausted
# from dotenv import load_dotenv
# import os
# import json
# import time
# import datetime as date
# import uuid

# load_dotenv()

# bq_client = bigquery.Client()

# def get_uuid():
#     return str(uuid.uuid4())

# def get_current_timestamp():
#     today = date.datetime.today() + date.timedelta(hours=7)
#     return today.isoformat()

# drone_insert_func = FunctionDeclaration(
#     name="generate_insert_query",
#     description=(
#         "Used when buying an item. "
#         "Start with word 'beli'. "
#         "Generate an INSERT SQL query for logging transactions. "
#         "Use project `wispkeeper`, dataset `queen_authenbytik`, table `transaction`."
#     ),
#     parameters={
#         "type": "object",
#         "properties": {
#             "id": {"type": "string", "description": "Random transaction ID using UUID"},
#             "category": {"type": "string", "description": "Category of the transaction. Both expenses and incomes include: Bag, Shoes"},
#             "brand_name": {"type": "string", "description": "The brand name of the item. Always capitalized"},
#             "color": {"type": "string", "description": "The color of the item. Always capitalized. Always in English, ex. Cokelat -> Brown"},
#             "detail": {"type": "string", "description": "Transaction description, contains user's prompt as-is"},
#             "buy_id": {"type": "string", "description": "Buy ID where buy transaction has been made. Always in uppercase"},
#             "amount_buy": {"type": "integer", "description": "Transaction amount when buying an item in IDR"},
#             "transaction_date_buy": {"type": "string", "description": "Current transaction date"}
#         },
#         "required": ["category", "brand_name", "color", "detail", "amount_buy"],
#     },
# )

# drone_insert_with_condition_func = FunctionDeclaration(
#     name="generate_insert_with_condition_query",
#     description=(
#         "Used when buying an item but with the item condition in the prompt. "
#         "Generate an INSERT SQL query for logging transactions. "
#         "Use project `wispkeeper`, dataset `queen_authenbytik`, table `transaction`."
#     ),
#     parameters={
#         "type": "object",
#         "properties": {
#             "id": {"type": "string", "description": "Random transaction ID using UUID"},
#             "category": {"type": "string", "description": "Category of the transaction. Both expenses and incomes include: Bag, Shoes"},
#             "brand_name": {"type": "string", "description": "The brand name of the item. Always capitalized"},
#             "color": {"type": "string", "description": "The color of the item. Always capitalized. Always in English, ex. Cokelat -> Brown"},
#             "item_condition": {"type": "string", "description": "The condition of the item. NEW: new;baru, NBU: new but used, LNEW: like new, VVGC: very very good condition, VGC: very good condition, GC: good condition, PL: preloved. Always in uppercase"},
#             "detail": {"type": "string", "description": "Transaction description, contains user's prompt as-is"},
#             "buy_id": {"type": "string", "description": "Buy ID where buy transaction has been made. Always in uppercase"},
#             "amount_buy": {"type": "integer", "description": "Transaction amount when buying an item in IDR"},
#             "transaction_date_buy": {"type": "string", "description": "Current transaction date"}
#         },
#         "required": ["category", "brand_name", "color", "item_condition", "detail", "amount_buy"],
#     },
# )

# drone_update_item_cond_func = FunctionDeclaration(
#     name="generate_update_item_cond_query",
#     description=(
#         "Used for updating the condition of the item. "
#         "Generate an UPDATE SQL query for data that has already exist. "
#         "Use project `wispkeeper`, dataset `queen_authenbytik`, table `transaction`."
#     ),
#     parameters={
#         "type": "object",
#         "properties": {
#             "buy_id": {"type": "string", "description": "Buy ID where buy transaction has been made. Always in uppercase"},
#             "brand_name": {"type": "string", "description": "The brand name of the item. Always capitalized"},
#             "item_condition": {"type": "string", "description": "The condition of the item. NEW: new;baru, NBU: new but used, LNEW: like new, VVGC: very very good condition, VGC: very good condition, GC: good condition, PL: preloved. Always in uppercase"}
#         },
#         "required": ["buy_id", "brand_name", "item_condition"],
#     },
# )

# drone_update_sold_func = FunctionDeclaration(
#     name="generate_update_sold_query",
#     description=(
#         "Used for updating sell amount and sell date. "
#         "Generate an UPDATE SQL query for data that has already exist"
#         "Use project `wispkeeper`, dataset `queen_authenbytik`, table `transaction`."
#     ),
#     parameters={
#         "type": "object",
#         "properties": {
#             "buy_id": {"type": "string", "description": "Buy ID where buy transaction has been made. Always in uppercase"},
#             "brand_name": {"type": "string", "description": "The brand name of the item. Always capitalized"},
#             "amount_sold": {"type": "integer", "description": "Transaction amount when an item is sold in IDR"},
#             "transaction_date_sold": {"type": "string", "description": "Current transaction date"}
#         },
#         "required": ["buy_id", "brand_name", "amount_sold", "transaction_date_sold"],
#     },
# )





# tool = Tool(
#     function_declarations=[
#         drone_insert_func,
#         drone_insert_with_condition_func,
#         drone_update_item_cond_func,
#         drone_update_sold_func
#     ]
# )


# model = GenerativeModel(
#     model_name="gemini-1.5-flash",
#     tools=[tool]
# )

# st.title("Transaction Management Chatbot")
# st.write("Enter a prompt to interact with the chatbot:")

# prompt = st.text_input("Enter your prompt here")

# # prompt = "beli tas brand chanel diamond quilt warna cream kondisi preloved 1.52jt"
# # prompt = "beli tas brand chanel square quilt warna cokelat 1.92jt"
# # prompt = "beli tas brand fossil polkadot warna hijau kondisi gc 3.519jt"
# # prompt = "update chanel 4677 kondisi vgc"
# # prompt = "terjual chanel 4677 3.1jt"

# if st.button("Send") and prompt:
#     var_uuid = get_uuid().upper()
#     buy_id = var_uuid[:4]
#     current_timestamp = get_current_timestamp()
#     chat_session = model.start_chat(history=[])
#     st.write("Processing...")
        
#     response = chat_session.send_message(prompt)
#     response_part = response.candidates[0].content.parts[0]

#     if hasattr(response_part, "function_call") and response_part.function_call is not None:
#         try:
#             params = {key: value for key, value in response_part.function_call.args.items()}
                
#             if response_part.function_call.name == "generate_insert_query":
#                 cleaned_query = """
#                 INSERT INTO `wispkeeper.queen_authenbytik.transaction`
#                 (id, category, brand_name, color, detail, buy_id, amount_buy, transaction_date_buy)
#                 VALUES (@id, @category, @brand_name, @color, @detail, @buy_id, @amount_buy, @transaction_date_buy)
#                 """
#                 job_config = bigquery.QueryJobConfig(
#                     query_parameters=[
#                         bigquery.ScalarQueryParameter("id", "STRING", var_uuid),
#                         bigquery.ScalarQueryParameter("category", "STRING", params.get("category")),
#                         bigquery.ScalarQueryParameter("brand_name", "STRING", params.get("brand_name")),
#                         bigquery.ScalarQueryParameter("color", "STRING", params.get("color")),
#                         bigquery.ScalarQueryParameter("detail", "STRING", params.get("detail")),
#                         bigquery.ScalarQueryParameter("buy_id", "STRING", buy_id),
#                         bigquery.ScalarQueryParameter("amount_buy", "INTEGER", params.get("amount_buy")),
#                         bigquery.ScalarQueryParameter("transaction_date_buy", "DATETIME", current_timestamp),
#                     ]
#                 )
                
#                 query_job = bq_client.query(cleaned_query, job_config=job_config)
#                 query_job.result()
                
#                 st.write(f"""
#                 INSERT Succeeded!
#                 ID: {buy_id}
#                 Category: {params["category"]}
#                 Brand: {params["brand_name"]}
#                 Color: {params["color"]}
#                 Amount Buy: {params["amount_buy"]}
#                 Date Buy: {current_timestamp}
#                 """)
            
#             elif response_part.function_call.name == "generate_insert_with_condition_query":
#                 cleaned_query = """
#                 INSERT INTO `wispkeeper.queen_authenbytik.transaction`
#                 (id, category, brand_name, color, detail, item_condition, buy_id, amount_buy, transaction_date_buy)
#                 VALUES (@id, @category, @brand_name, @color, @detail, @item_condition, @buy_id, @amount_buy, @transaction_date_buy)
#                 """
#                 job_config = bigquery.QueryJobConfig(
#                     query_parameters=[
#                         bigquery.ScalarQueryParameter("id", "STRING", var_uuid),
#                         bigquery.ScalarQueryParameter("category", "STRING", params.get("category")),
#                         bigquery.ScalarQueryParameter("brand_name", "STRING", params.get("brand_name")),
#                         bigquery.ScalarQueryParameter("color", "STRING", params.get("color")),
#                         bigquery.ScalarQueryParameter("detail", "STRING", params.get("detail")),
#                         bigquery.ScalarQueryParameter("item_condition", "STRING", params.get("item_condition")),
#                         bigquery.ScalarQueryParameter("buy_id", "STRING", buy_id),
#                         bigquery.ScalarQueryParameter("amount_buy", "INTEGER", params.get("amount_buy")),
#                         bigquery.ScalarQueryParameter("transaction_date_buy", "DATETIME", current_timestamp),
#                     ]
#                 )
                
#                 query_job = bq_client.query(cleaned_query, job_config=job_config)
#                 query_job.result()
                
#                 st.write(f"""
#                 INSERT Succeeded!
#                 ID: {buy_id}
#                 Category: {params["category"]}
#                 Brand: {params["brand_name"]}
#                 Color: {params["color"]}
#                 Condition: {params["item_condition"]}
#                 Amount Buy: {params["amount_buy"]}
#                 Detail: {params["detail"]}
#                 Date Buy: {current_timestamp}
#                 """)

#             elif response_part.function_call.name == "generate_update_item_cond_query":
#                 cleaned_query = """
#                 UPDATE `wispkeeper.queen_authenbytik.transaction`
#                 SET item_condition = @item_condition
#                 WHERE buy_id = @buy_id
#                 AND brand_name = @brand_name
#                 """
                
#                 job_config = bigquery.QueryJobConfig(
#                     query_parameters=[
#                         bigquery.ScalarQueryParameter("item_condition", "STRING", params.get("item_condition")),
#                         bigquery.ScalarQueryParameter("buy_id", "STRING", params.get("buy_id")),
#                         bigquery.ScalarQueryParameter("brand_name", "STRING", params.get("brand_name"))
#                     ]
#                 )
                
#                 query_job = bq_client.query(cleaned_query, job_config=job_config)
#                 query_job.result()
                
#                 st.write(f"""
#                 UPDATE Succeeded!
#                 ID: {params["buy_id"]}
#                 Brand: {params["brand_name"]}
#                 Condition: {params["item_condition"]}
#                 """)

#             elif response_part.function_call.name == "generate_update_sold_query":
#                 cleaned_query = """
#                 UPDATE `wispkeeper.queen_authenbytik.transaction`
#                 SET amount_sold = @amount_sold, transaction_date_sold = @transaction_date_sold
#                 WHERE buy_id = @buy_id
#                 AND brand_name = @brand_name
#                 """
                
#                 job_config = bigquery.QueryJobConfig(
#                     query_parameters=[
#                         bigquery.ScalarQueryParameter("amount_sold", "INTEGER", params.get("amount_sold")),
#                         bigquery.ScalarQueryParameter("transaction_date_sold", "DATETIME", current_timestamp),
#                         bigquery.ScalarQueryParameter("buy_id", "STRING", params.get("buy_id")),
#                         bigquery.ScalarQueryParameter("brand_name", "STRING", params.get("brand_name"))
#                     ]
#                 )
                
#                 query_job = bq_client.query(cleaned_query, job_config=job_config)
#                 query_job.result()
                
#                 st.write(f"""
#                 UPDATE Succeeded!
#                 ID: {params["buy_id"]}
#                 Brand: {params["brand_name"]}
#                 Amount Sold: {params["amount_sold"]}
#                 Date Sold: {current_timestamp}
#                 """)
            
#         except BadRequest as e:
#             st.write(f"Query failed: {e.message}")
#         except NotFound as e:
#             st.write(f"Resource not found: {e.message}")      
#         except Exception as e:
#             st.write(f"Unexpected error: {e}")




# st.write("### Current Transactions in BigQuery")
# query = """
# SELECT *
# FROM `wispkeeper.queen_authenbytik.transaction`
# ORDER BY `transaction_date_buy` DESC
# """
# try:
#     query_job = bq_client.query(query)
#     results = query_job.result()
#     rows = [dict(row) for row in results]
#     if rows:
#         st.write("Scroll to view all columns")
#         st.dataframe(rows, use_container_width=True)
#     else:
#         st.write("No data found in the transaction table.")
# except Exception as e:
#     st.write(f"Failed to fetch data: {e}")











import streamlit as st

st.write("HELLOOO")