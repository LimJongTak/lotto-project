import requests
import pandas as pd
import os
from collections import Counter

class LottoDataManager:
    def __init__(self, file_path='data/lotto_history.csv'):
        self.file_path = file_path
        self.api_url = "https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo="
        if not os.path.exists('data'):
            os.makedirs('data')

    def get_lotto_data(self, drw_no):
        """특정 회차의 당첨 번호를 API로 가져옴"""
        try:
            response = requests.get(self.api_url + str(drw_no))
            data = response.json()
            if data.get('returnValue') == 'success':
                return {
                    '회차': data['drwNo'],
                    '날짜': data['drwNoDate'],
                    '번호1': data['drwtNo1'],
                    '번호2': data['drwtNo2'],
                    '번호3': data['drwtNo3'],
                    '번호4': data['drwtNo4'],
                    '번호5': data['drwtNo5'],
                    '번호6': data['drwtNo6'],
                    '보너스': data['bnusNo']
                }
        except Exception as e:
            print(f"Error fetching {drw_no}: {e}")
        return None

    def update_history(self):
        """기존 파일에 최신 회차 데이터를 추가함"""
        if os.path.exists(self.file_path):
            df_existing = pd.read_csv(self.file_path)
            last_drw = df_existing['회차'].max()
        else:
            df_existing = pd.DataFrame()
            last_drw = 0

        current_drw = last_drw + 1
        new_data = []

        while True:
            data = self.get_lotto_data(current_drw)
            if data is None: break
            new_data.append(data)
            current_drw += 1

        if new_data:
            df_new = pd.DataFrame(new_data)
            df_final = pd.concat([df_existing, df_new], ignore_index=True)
            df_final.to_csv(self.file_path, index=False, encoding='utf-8-sig')
            return f"{len(new_data)}개 업데이트 완료"
        return "이미 최신 상태입니다."

    def get_analysis_data(self):
        """웹 API에 전달할 분석 요약 데이터 생성"""
        if not os.path.exists(self.file_path):
            return {"error": "데이터 파일이 없습니다. 먼저 업데이트를 진행하세요."}
        
        df = pd.read_csv(self.file_path)
        all_nums = df[['번호1', '번호2', '번호3', '번호4', '번호5', '번호6']].values.flatten()
        counts = Counter(all_nums)
        
        top_10 = [{"number": int(num), "count": int(count)} for num, count in counts.most_common(10)]
        
        return {
            "last_drw": int(df['회차'].max()),
            "last_date": df['날짜'].iloc[-1],
            "total_records": len(df),
            "top_10": top_10
        }