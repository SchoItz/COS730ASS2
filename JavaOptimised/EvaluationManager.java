import java.util.ArrayList;
import java.util.List;

public class EvaluationManager {

    private final Database database;

    public EvaluationManager(Database database) {
        this.database = database;
        // No NotificationService dependency — outcome is returned to caller
    }

    // Returns outcome string; does NOT call NotificationService itself
    public String evaluateSubmission(List<Reviewer> reviewers) {
        CallTracker.record("EvaluationManager.evaluateSubmission");
        List<Integer> scores = new ArrayList<>();
        for (Reviewer reviewer : reviewers) {
            scores.add(reviewer.getScore());
        }
        // Batch persist all scores in a single database call
        database.saveScores(scores);
        return computeResult(scores);
    }

    // All evaluation logic consolidated in one private method
    private String computeResult(List<Integer> scores) {
        CallTracker.record("EvaluationManager.computeResult");
        if (scores.isEmpty()) {
            System.out.println("[EvaluationManager] computeResult -> no scores, rejected");
            return "rejected";
        }
        double avg = scores.stream().mapToInt(i -> i).average().orElse(0);
        boolean consensus = scores.stream().allMatch(s -> Math.abs(s - avg) <= 15);
        System.out.println("[EvaluationManager] avg=" + avg + " consensus=" + consensus);
        String outcome;
        if (avg >= 75) {
            outcome = "accepted";
        } else if (avg >= 50) {
            outcome = "revision";
        } else {
            outcome = "rejected";
        }
        System.out.println("[EvaluationManager] computeResult -> " + outcome);
        return outcome;
    }
}
