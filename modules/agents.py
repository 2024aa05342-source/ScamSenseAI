class EvidenceAgent:

    @staticmethod
    def run(analysis):

        return {
            "identified_red_flags":
                analysis.get(
                    "red_flags",
                    []
                ),

            "supporting_evidence":
                analysis.get(
                    "evidence",
                    []
                )
        }


class KnowledgeAgent:

    @staticmethod
    def run(retrieved_items):

        sources = []

        for item in retrieved_items:

            sources.append(
                item["source"]
            )

        return {
            "knowledge_sources":
                list(set(sources))
        }


class RiskAgent:

    @staticmethod
    def run(analysis):

        return {
            "risk_score":
                analysis.get(
                    "risk_score",
                    0
                ),

            "risk_level":
                analysis.get(
                    "risk_level",
                    "Unknown"
                )
        }


class ReportAgent:

    @staticmethod
    def run():

        return {
            "status":
                "Investigation Report Generated"
        }