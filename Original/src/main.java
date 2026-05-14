import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;

public class main {

    public static void main(String[] args) {
        int[] reviewerCounts = {70, 80, 90};
        String outFile = "src/metrics.txt";
        String[] data = {"Francois", "Scholtz", "ResearchTitle", "Content"};

        try (PrintWriter pw = new PrintWriter(new FileWriter(outFile, false))) {
            pw.println("============================================================");
            pw.println("  Original Implementation - Metrics Report");
            pw.println("  Generated: " + new java.util.Date());
            pw.println("============================================================");
            pw.println();
        } catch (IOException e) {
            }

        long combinedRuntime = 0;
        int combinedInteractions = 0;

        for (int n : reviewerCounts) {
            Database.setReviewerCount(n);
            MetricTracker.reset();

            UI ui = new UI();

            long start = System.nanoTime();
            String outcome = ui.submitResearchOutput(data);
            long end = System.nanoTime();
            long ms = (end - start) / 1_000_000;
            combinedRuntime += ms;
            combinedInteractions += MetricTracker.total();

            String label = n + " Reviewers";

            MetricTracker.appendToFile(outFile, label, outcome);
        }

        System.out.println("============================================================");
        System.out.println("Total Runtime: " + combinedRuntime + " ms");
        System.out.println("Combined Total Interactions:          " + combinedInteractions);
        System.out.println("============================================================");

        try (PrintWriter pw = new PrintWriter(new FileWriter(outFile, true))) {
            pw.println("============================================================");
            pw.println("Total Runtime: " + combinedRuntime + " ms");
            pw.println("Combined Total Interactions:          " + combinedInteractions);
            pw.println("============================================================");
        } catch (IOException e) {
                    }
    }
}

