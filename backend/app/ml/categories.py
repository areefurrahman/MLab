# backend/app/ml/categories.py

class AlgorithmCategory:
    """
    The three top-level groupings your professor requires.
    Same constants-class pattern as ExperimentStatus — no magic strings.
    """
    MACHINE_LEARNING = "machine_learning"
    DEEP_LEARNING = "deep_learning"
    GENERATIVE_AI = "generative_ai"

    LABELS = {
        MACHINE_LEARNING: "Machine Learning Algorithms",
        DEEP_LEARNING: "Deep Learning Algorithms",
        GENERATIVE_AI: "Generative AI (Transformers Model)",
    }