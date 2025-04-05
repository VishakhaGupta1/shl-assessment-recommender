from fastapi import FastAPI
from pydantic import BaseModel
from recommend import recommend_assessments

app = FastAPI()

class QueryInput(BaseModel):
    query: str

@app.post("/recommend")
def get_recommendations(input: QueryInput):
    result_df = recommend_assessments(input.query)
    result = result_df.to_dict(orient="records")
    return {"results": result}
