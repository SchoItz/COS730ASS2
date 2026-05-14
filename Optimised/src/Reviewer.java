public class Reviewer {

    private final String name;

    public Reviewer(String name) {
        this.name = name;
    }

    public void assignReview(String[] data) {
        MetricTracker.record("Reviewer.assignReview");
    }

    public int getScore() {
        MetricTracker.record("Reviewer.getScore");
        int score = (int) (Math.random() * 70 + 30  );
        return score;
    }
}
