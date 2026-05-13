public class Reviewer {

    private final String name;

    public Reviewer(String name) {
        this.name = name;
    }

    public void assignReview(String[] data) {
        CallTracker.record("Reviewer.assignReview");
        System.out.println("[Reviewer] " + name + " assignReview");
    }

    // Returns score directly — no dependency on EvaluationManager
    public int getScore() {
        CallTracker.record("Reviewer.getScore");
        int score = (int) (Math.random() * 41 + 60);
        System.out.println("[Reviewer] " + name + " getScore: " + score);
        return score;
    }
}
