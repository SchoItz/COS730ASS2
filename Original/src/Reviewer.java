public class Reviewer {

    private final String name;

    public Reviewer(String name) {
        this.name = name;
    }

    public void assignReview(String[] data) {
        MetricTracker.record("Reviewer.assignReview");
    }

    public void submitScore(EvaluationManager evaluationManager) {
        MetricTracker.record("Reviewer.submitScore");
        int score = (int) (Math.random() * 70 + 30);
        evaluationManager.submitScore(score);
    }
}
