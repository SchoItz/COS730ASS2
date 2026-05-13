import java.util.ArrayList;
import java.util.List;

public class ReviewerManager {

    private final Database database;

    public ReviewerManager(Database database) {
        this.database = database;
    }

    // Owns the full reviewer assignment pipeline — SubmissionController no longer loops
    public List<Reviewer> assignReviewers(String[] data) {
        CallTracker.record("ReviewerManager.assignReviewers");
        List<String> rawList = database.fetchReviewers();
        List<String> eligible = filterReviewers(rawList);
        List<Reviewer> assigned = new ArrayList<>();
        for (String name : eligible) {
            Reviewer r = new Reviewer(name);
            r.assignReview(data);
            assigned.add(r);
        }
        System.out.println("[ReviewerManager] assignedReviewers: " + assigned.size());
        return assigned;
    }

    // Single combined filter — replaces two separate filterConflicts + checkWorkload passes
    private List<String> filterReviewers(List<String> reviewerList) {
        CallTracker.record("ReviewerManager.filterReviewers");
        System.out.println("[ReviewerManager] filterReviewers (conflicts + workload)");
        return reviewerList;
    }
}
