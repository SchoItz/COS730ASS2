import java.util.ArrayList;
import java.util.List;

public class EvaluationManager {

    private Database database;
    private NotificationService notificationService;
    private List<Integer> scores;

    public EvaluationManager(Database database, NotificationService notificationService) {
        this.database = database;
        this.notificationService = notificationService;
        this.scores = new ArrayList<>();
    }

    public void startEvaluation(List<Reviewer> reviewers) {
        CallTracker.record("EvaluationManager.startEvaluation");
        scores = new ArrayList<>();  // reset for this evaluation run
        for (Reviewer reviewer : reviewers) {
            reviewer.submitScore(this);
        }
        calculateAverage();
        checkConsensus();
        String outcome = applyRules();
        if (outcome.equals("accepted")) {
            notificationService.notifyAcceptance();
        } else if (outcome.equals("rejected")) {
            notificationService.notifyRejection();
        } else {
            notificationService.notifyRevision();
        }
    }

    public void submitScore(int score) {
        CallTracker.record("EvaluationManager.submitScore");
        scores.add(score);
        database.saveScore(score);
    }

    private void calculateAverage() {
        CallTracker.record("EvaluationManager.calculateAverage");
        double avg = scores.stream().mapToInt(i -> i).average().orElse(0);
        System.out.println("[EvaluationManager] calculateAverage: " + avg);
    }

    private void checkConsensus() {
        CallTracker.record("EvaluationManager.checkConsensus");
        System.out.println("[EvaluationManager] checkConsensus");
    }

    private String applyRules() {
        CallTracker.record("EvaluationManager.applyRules");
        double avg = scores.stream().mapToInt(i -> i).average().orElse(0);
        String outcome;
        if (avg >= 75) {
            outcome = "accepted";
        } else if (avg >= 50) {
            outcome = "revision";
        } else {
            outcome = "rejected";
        }
        System.out.println("[EvaluationManager] applyRules -> " + outcome);
        return outcome;
    }
}
