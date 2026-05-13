public class CallTracker {

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

    public static void printReport(String label) {
        System.out.println("\n|=============== Call Report [" + label + "] ===============|");
        for (int i = 0; i < size; i++) {
            System.out.printf("| %-50s %d |%n", methods[i], counts[i]);
        }
        System.out.println("|  TOTAL CALLS: " + total() + "|");
        System.out.println("|======================================================|");
    }
}
