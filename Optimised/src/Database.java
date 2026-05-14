import java.util.ArrayList;
import java.util.List;

public class Database {

    private static int revCount = 3;

    public static void setReviewerCount(int n) {
        revCount = n;
    }

    public String saveSubmission(String[] data) {
        MetricTracker.record("Database.saveSubmission");
        return "confirmation";
    }

    public List<String> fetchReviewers() {
        MetricTracker.record("Database.fetchReviewers");
        List<String> reviewerList = new ArrayList<>();
        for (int i = 0; i < revCount; i++) {
            reviewerList.add("Reviewer_" + (char) ('A' + i));
        }
        return reviewerList;
    }

    public void saveScores(List<Integer> scores) {
        MetricTracker.record("Database.saveScores");
    }
}
