module com.glow.glow {
    requires javafx.controls;
    requires javafx.fxml;


    opens com.glow.glow to javafx.fxml;
    exports com.glow.glow;
}