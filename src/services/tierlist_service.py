import src.analysis.winrate_calculator as wc

class TierListService:
    def get_tier_list(self, position: str):

        df = wc.winrate_orchestrator()
        if position == "ALL":
            return df.sort_values(by="WilsonScore", ascending=False)
        return df[(df["Lane"] == position)].sort_values(by="WilsonScore", ascending=False)
    
if __name__ == "__main__":
    service = TierListService()
    df = service.get_tier_list("SUPPORT")
    print(df.head(50))