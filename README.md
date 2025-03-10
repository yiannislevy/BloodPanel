# BloodPanel
Currently implemented fronted and backend communication via fastAPI for pdf uploading and saving onto /uploads folder along current timestamp

## Todos:

1. How do we continue from there? Define a good pydantic model schema
2. Choose DB: postgres+sqlalchemy? and implement it
3. What is the strategy onwards; per pdf received send the file directly to mistral ocr ai and save output on db?
4. verify this all works and then next steps might include: multiple file uploads, a basic list of the lab tests and structured viewing of the results, dashboard.