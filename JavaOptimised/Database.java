import java.util.ArrayList;
import java.util.List;

public class Database {

    public String saveSubmission(String[] data) {
        CallTracker.record("Database.saveSubmission");
        System.out.println("[Database] saveSubmission");
        return "confirmation";
    }

    public List<String> fetchReviewers() {
        CallTracker.record("Database.fetchReviewers");
        System.out.println("[Database] fetchReviewers");
        List<String> reviewerList = new ArrayList<>();
        reviewerList.add("Reviewer_A");
        reviewerList.add("Reviewer_B");
        reviewerList.add("Reviewer_C");
        return reviewerList;
    }

    // Batch save: one call for all scores instead of N individual calls
    public void saveScores(List<Integer> scores) {
        CallTracker.record("Database.saveScores");
        System.out.println("[Database] saveScores (batch): " + scores);
    }
}
