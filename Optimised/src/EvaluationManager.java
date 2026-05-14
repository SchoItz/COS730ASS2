import java.util.ArrayList;
import java.util.List;

public class EvaluationManager {

    private final Database database;

    public EvaluationManager(Database database) {
        this.database = database;
    }

    public String evaluateSubmission(List<Reviewer> reviewers) {
        MetricTracker.record("EvaluationManager.evaluateSubmission");
        List<Integer> scores = new ArrayList<>();
        for (Reviewer reviewer : reviewers) {
            scores.add(reviewer.getScore());
        }
        database.saveScores(scores);
        return calculateResult(scores);
    }

    private String calculateResult(List<Integer> scores) {
        MetricTracker.record("EvaluationManager.calculateResult");
        if (scores.isEmpty()) {
            return "rejected";
        }
        int sum = 0;
        for (int score : scores) {
            sum += score;
        }
        double avg = (double) sum / scores.size();

        boolean consensus = true;
        for (int score : scores) {
            if (Math.abs(score - avg) > 15) {
                consensus = false;
                break;
            }
        }
        String outcome;
        if (avg >= 75) {
            outcome = "accepted";
        } else if (avg >= 50) {
            outcome = "revision";
        } else {
            outcome = "rejected";
        }
        System.out.println("Average: " + avg);
        return outcome;
    }
}
