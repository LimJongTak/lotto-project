from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from lotto_manager import LottoDataManager
import random

app = FastAPI()
manager = LottoDataManager()

# React(방법 B) 연동을 위한 보안 설정 (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 주소에서 접근 허용 (개발 단계)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "running", "service": "Lotto Analysis API Server"}

@app.get("/api/update")
def update_lotto_data():
    """데이터 수집 명령 API"""
    result = manager.update_history()
    return {"message": result}

@app.get("/api/analysis")
def get_lotto_analysis():
    """분석 결과 제공 API"""
    return manager.get_analysis_data()

@app.get("/api/recommend/{budget}")
def get_recommend(budget: int):
    """예산에 따른 번호 추천 API"""
    num_lines = budget // 1000
    if num_lines == 0:
        return {"error": "금액이 너무 적습니다."}

    # 간단한 추천 로직 (전체 번호 중 랜덤)
    recommendations = []
    for _ in range(num_lines):
        line = sorted(random.sample(range(1, 46), 6))
        recommendations.append(line)

    return {
        "budget": budget,
        "lines": num_lines,
        "results": recommendations
    }

# 서버 실행 (터미널에서 실행 시: uvicorn main:app --reload)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)