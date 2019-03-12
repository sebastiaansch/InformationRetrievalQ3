import pyltr

class MRR(pyltr.metrics.err.ERR):
    def evaluate(self, qid, targets):
        residual = 1.0
        result = 0.0
        for i, t in enumerate(targets[:self.k]):
            assert t <= self.highest_score
            if t == 1:
                return 1 / (i+1);
        return result
