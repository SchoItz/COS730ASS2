import java.util.ArrayList;
import java.util.List;

public class Database {

    private static int reviewerCount = 3;

    public static void setReviewerCount(int n) {
        reviewerCount = n;
    }

    public String saveSubmission(String[] data) {
        MetricTracker.record("Database.saveSubmission");
        return "confirmation";
    }

    public List<String> fetchReviewers() {
        MetricTracker.record("Database.fetchReviewers");
        List<String> reviewerList = new ArrayList<>();
        for (int i = 0; i < reviewerCount; i++) {
            reviewerList.add("Reviewer_" + (char) ('A' + i));
        }
        return reviewerList;
    }

    public void saveScore(int score) {
        MetricTracker.record("Database.saveScore");
    }
}
