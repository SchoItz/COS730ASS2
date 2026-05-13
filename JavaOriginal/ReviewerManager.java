import java.util.ArrayList;
import java.util.List;

public class ReviewerManager {

    private Database database;

    public ReviewerManager(Database database) {
        this.database = database;
    }

    public List<Reviewer> getAvailableReviewers() {
        CallTracker.record("ReviewerManager.getAvailableReviewers");
        List<String> reviewerList = database.fetchReviewers();
        reviewerList = filterConflicts(reviewerList);
        reviewerList = checkWorkload(reviewerList);
        List<Reviewer> filteredReviewers = new ArrayList<>();
        for (String name : reviewerList) {
            filteredReviewers.add(new Reviewer(name));
        }
        System.out.println("[ReviewerManager] filteredReviewers: " + filteredReviewers.size());
        return filteredReviewers;
    }

    private List<String> filterConflicts(List<String> reviewerList) {
        CallTracker.record("ReviewerManager.filterConflicts");
        System.out.println("[ReviewerManager] filterConflicts");
        return reviewerList;
    }

    private List<String> checkWorkload(List<String> reviewerList) {
        CallTracker.record("ReviewerManager.checkWorkload");
        System.out.println("[ReviewerManager] checkWorkload");
        return reviewerList;
    }
}
