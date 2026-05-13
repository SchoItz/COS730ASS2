public class main {

    public static void main(String[] args) {
        long StartTime = System.nanoTime();
        String[] data = {"Francois", "Scholtz", "ResearchTitle", "Content"};
        UI ui = new UI();
        ui.submitResearchOutput(data);
        long EndTime = System.nanoTime();
        long durationNs = (EndTime - StartTime);
        long durationMs = durationNs / 1_000_000;
        System.out.println("Execution time: " + durationMs + " ms");
    }
}
