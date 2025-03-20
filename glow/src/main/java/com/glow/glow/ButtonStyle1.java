package com.glow.glow;

import javafx.application.Application;
import javafx.scene.Cursor;
import javafx.scene.control.Button;
import javafx.scene.effect.DropShadow;
import javafx.scene.effect.Glow;
import javafx.scene.input.MouseEvent;
import javafx.scene.paint.Color;
import javafx.scene.text.Font;


/**
 * custom button based on Ruby + Sophie's design.
 * extends {@link javafx.scene.control.Button}
 * has 4 basic arguments, other attributes that affect hte buttons look e.g
 * shadow, or glow can be changed in run time if need be via the SETTER METHODS.
 *
 * @author Harry
 * @version 1.0
 * @since 2025-03-20
 */
public class ButtonStyle1 extends Button {

    private final DropShadow dropShadow;
    private final Glow glow;

    private String defaultStyleSheet,  hoveredStyleSheet, pressedStyleSheet;

    private double dropShadowRadiusHigh;
    private double dropShadowRadiusDefault;
    private double dropShadowSpreadHigh;
    private double dropShadowSpreadDefault;
    private int[] dropShadowColors;
    private double glowLevelDefault;
    private double glowLevelHigh;

    /**
     *
     * @param text - text for button to display (String)
     * @param fontSize - font size (int) (pt size)
     * @param width - width of button (int) (pixels)
     * @param height - height of button (int) (pixels)
     */
    public ButtonStyle1(String text, int fontSize, int width, int height) {
        super(text);
        setPrefSize(width, height);

        // load font (.ttf file in resources/fonts/ ).
        Font calistogaFont = Font.loadFont(getClass().getResourceAsStream("/fonts/Calistoga-Regular.ttf"), fontSize);
        setFont(calistogaFont);


        // settings css style sheet
        defaultStyleSheet = "-fx-background-color: rgba(109, 110, 193); -fx-text-fill: rgba(153, 155, 212); -fx-border-radius: 12;" +
                "-fx-background-radius: 12;";
        hoveredStyleSheet = "-fx-background-color: rgba(109, 110, 193, 0.9); -fx-text-fill: rgba(153, 155, 212); -fx-border-radius: 12;" +
                "-fx-background-radius: 12;";
        pressedStyleSheet = "-fx-background-color: rgba(109, 110, 193, 0.6); -fx-text-fill: rgba(153, 155, 212); -fx-border-radius: 12;" +
                "-fx-background-radius: 12;";
        setStyle(defaultStyleSheet);


        // creating drop shadow object.
        dropShadowRadiusHigh = 12;
        dropShadowRadiusDefault = 12;

        dropShadowSpreadDefault = 0.4;
        dropShadowSpreadHigh = 0.7;
        dropShadowColors = new int[]{109, 110, 193};

        dropShadow = new DropShadow();
        dropShadow.setOffsetX(0);
        dropShadow.setOffsetY(0);
        dropShadow.setRadius(dropShadowRadiusDefault);
        dropShadow.setSpread(dropShadowSpreadDefault);
        dropShadow.setColor(Color.rgb(dropShadowColors[0], dropShadowColors[1], dropShadowColors[2], 0.4));

        // creating glow object
        glowLevelDefault = 0.1;
        glowLevelHigh = 0.2;

        glow = new Glow(glowLevelDefault);
        dropShadow.setInput(glow);
        setEffect(dropShadow);

        setPickOnBounds(false);  // means drop shadow doesn't count as hover area.


        // attaching event handlers to methods.
        setOnMouseEntered(this::onButtonEnterHover);
        setOnMouseExited(this::onButtonExitHover);
        setOnMousePressed(this::onButtonPress);
        setOnMouseReleased(this::onButtonRelease);

    }

    // SLOT METHODS
    private void onButtonPress(MouseEvent event){
        setStyle(pressedStyleSheet);
        dropShadow.setRadius(dropShadowRadiusHigh);
        dropShadow.setSpread(dropShadowSpreadHigh);
        dropShadow.setColor(Color.rgb(dropShadowColors[0], dropShadowColors[1], dropShadowColors[2], 0.5));
    }

    private void onButtonRelease(MouseEvent event){
        setStyle(hoveredStyleSheet);
        dropShadow.setColor(Color.rgb(dropShadowColors[0], dropShadowColors[1], dropShadowColors[2], 0.5));
        dropShadow.setSpread(dropShadowSpreadHigh);
        dropShadow.setRadius(dropShadowRadiusHigh);

    }

    private void onButtonEnterHover(MouseEvent event){
        setStyle(hoveredStyleSheet);
        setCursor(Cursor.HAND);
        dropShadow.setColor(Color.rgb(dropShadowColors[0], dropShadowColors[1], dropShadowColors[2], 0.5));
        dropShadow.setSpread(dropShadowSpreadHigh);
        dropShadow.setRadius(dropShadowRadiusHigh);
        glow.setLevel(glowLevelHigh);

    }

    private void onButtonExitHover(MouseEvent event){
        setStyle(defaultStyleSheet);
        setCursor(Cursor.DEFAULT);
        dropShadow.setColor(Color.rgb(dropShadowColors[0], dropShadowColors[1], dropShadowColors[2], 0.4));
        dropShadow.setRadius(dropShadowRadiusDefault);
        dropShadow.setSpread(dropShadowSpreadDefault);
        glow.setLevel(glowLevelDefault);
    }

    // SETTER METHODS
    public void setShadowAttributes(double defaultRadius, double highRadius, double defaultSpread, double highSpread, int[] colors){
        dropShadowRadiusDefault = defaultRadius;
        dropShadowRadiusHigh = highRadius;
        dropShadowSpreadDefault = defaultSpread;
        dropShadowSpreadHigh = highSpread;
        dropShadowColors = colors;
    }


    public void setGlowAttributes(double glowLvlDefault, double glowLvlHigh){
        glowLevelHigh = glowLvlHigh;
        glowLevelDefault = glowLvlDefault;
    }

    public void setStyleSheets(String defaultSS, String hoveredSS, String pressedSS){
        defaultStyleSheet = defaultSS;
        hoveredStyleSheet = hoveredSS;
        pressedStyleSheet = pressedSS;
        setStyle(defaultStyleSheet);
    }


}