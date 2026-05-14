import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;

public class main {

    public static void main(String[] args) {
        int[] revCounts = {70, 80, 90};
        String metFile = "src/metrics.txt";
        String[] data = {"Francois", "Scholtz", "ResearchTitle", "Content"};

        try (PrintWriter pw = new PrintWriter(new FileWriter(metFile, false))) {
            pw.println("============================================================");
            pw.println("  Optimised Implementation - Metrics Report");
            pw.println("============================================================");
            pw.println();
        } catch (IOException e) {
            System.err.println("Could not initialise metrics file: " + e.getMessage());
        }

        long combRun = 0;
        int combInt = 0;

        for (int n : revCounts) {
            Database.setReviewerCount(n);
            MetricTracker.reset();

            Database db = new Database();
            Validator val = new Validator();
            ReviewerManager revMan = new ReviewerManager(db);
            EvaluationManager evalMan = new EvaluationManager(db);
            NotificationService notify = new NotificationService();
            SubmissionController controller = new SubmissionController(
                        val, db, revMan, evalMan, notify);
            UI ui = new UI(controller);
            controller.setUI(ui);

            long start = System.nanoTime();
            String outcome = ui.submitResearchOutput(data);
            long end = System.nanoTime();
            long ms = (end - start) / 1_000_000;
            combRun += ms;
            combInt += MetricTracker.total();

            String label = n + " Reviewers";

            MetricTracker.appendToFile(metFile, label, outcome);
        }

        System.out.println("============================================================");
        System.out.println("Total Runtime: " + combRun + " ms");
        System.out.println("Combined Total Interactions:          " + combInt);
        System.out.println("============================================================");

        try (PrintWriter pw = new PrintWriter(new FileWriter(metFile, true))) {
            pw.println("============================================================");
            pw.println("Total Runtime: " + combRun + " ms");
            pw.println("Combined Total Interactions:          " + combInt);
            pw.println("============================================================");
        } catch (IOException e) {
            System.err.println("Could not write combined runtime: " + e.getMessage());
        }
    }
}

