import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;

public class MetricTracker {

    private static final int MAX = 64;
    private static final String[] methods = new String[MAX];
    private static final int[] counts = new int[MAX];
    private static int size = 0;

    public static void record(String method) {
        for (int i = 0; i < size; i++) {
            if (methods[i].equals(method)) {
                counts[i]++;
                return;
            }
        }
        methods[size] = method;
        counts[size] = 1;
        size++;
    }

    public static void reset() {
        for (int i = 0; i < size; i++) {
            methods[i] = null;
            counts[i] = 0;
        }
        size = 0;
    }

    public static int total() {
        int sum = 0;
        for (int i = 0; i < size; i++) {
            sum += counts[i];
        }
        return sum;
    }

    public static void appendToFile(String filePath, String label, String outcome) {
        try (PrintWriter pw = new PrintWriter(new FileWriter(filePath, true))) {
            pw.println("============ Run: " + label + " ============");
            pw.println("Outcome:            " + outcome.toUpperCase());
            pw.println("Total Interactions: " + total());
            pw.println();
        } catch (IOException e) {
            System.err.println("[MetricTracker] Could not write to file: " + e.getMessage());
        }
    }
}
