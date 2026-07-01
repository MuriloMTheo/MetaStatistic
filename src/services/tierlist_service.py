import src.analysis.winrate_calculator as wc

class TierListService:
    def __init__(self):
        self.df = wc.winrate_orchestrator()

    def get_tier_list(self, position):
        if position == "ALL":
            return self.df.sort_values(by="WilsonScore", ascending=False)

        return self.df[self.df["Lane"] == position].sort_values(
            by="WilsonScore",
            ascending=False
        )