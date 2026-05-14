import java.util.ArrayList;
import java.util.List;

public class EvaluationManager {

    Database database;
    NotificationService notificationService;
    private List<Integer> scores;

    public EvaluationManager(Database database, NotificationService notificationService) {
        this.database = database;
        this.notificationService = notificationService;
        this.scores = new ArrayList<>();
    }

    public String startEvaluation(List<Reviewer> reviewers) {
        MetricTracker.record("EvaluationManager.startEvaluation");
        scores = new ArrayList<>();
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
        return outcome;
    }

    public void submitScore(int score) {
        MetricTracker.record("EvaluationManager.submitScore");
        scores.add(score);
        database.saveScore(score);
    }

    private void calculateAverage() {
        MetricTracker.record("EvaluationManager.calculateAverage");
        int sum = 0;
        for (int i = 0; i < scores.size(); i++) sum += scores.get(i);
        double avg = scores.isEmpty() ? 0 : (double) sum / scores.size();
        System.out.println("Average: " + avg);
    }

    private void checkConsensus() {
        MetricTracker.record("EvaluationManager.checkConsensus");
    }

    private String applyRules() {
        MetricTracker.record("EvaluationManager.applyRules");
        int sum = 0;
        for (int i = 0; i < scores.size(); i++) sum += scores.get(i);
        double avg = scores.isEmpty() ? 0 : (double) sum / scores.size();
        String outcome;
        if (avg >= 75) {
            outcome = "accepted";
        } else if (avg >= 50) {
            outcome = "revision";
        } else {
            outcome = "rejected";
        }
        return outcome;
    }
}
