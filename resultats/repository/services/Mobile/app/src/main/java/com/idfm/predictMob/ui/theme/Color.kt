package com.idfm.predictMob.ui.theme

import androidx.compose.runtime.Immutable
import androidx.compose.runtime.staticCompositionLocalOf
import androidx.compose.ui.graphics.Color


val LocalColor = staticCompositionLocalOf {
    Color()
}

@Immutable
data class Color(
    val Blue :Color = Color(0xFF67B5E8) ,        // couleur identitaire IDFM (approximation) :contentReference[oaicite:3]{index=3}
    val Black: Color = Color(0xFF000000),         // texte noir
    val White : Color = Color(0xFFFFFFFF) ,        // texte ou fond clair
    val GreyLight : Color = Color(0xFFD9D9D9),     // gris clair (pour séparation de contenu) :contentReference[oaicite:4]{index=4}
    val Red : Color = Color(0xFFE4002B)       ,    // rouge coquelicot (interdiction) :contentReference[oaicite:5]{index=5}
    val OrangeDark : Color = Color(0xFFB75B00) ,   // orange foncé (perturbations) :contentReference[oaicite:6]{index=6}
    val GreenDark : Color = Color(0xFF006A4E)   ,  // vert foncé (sorties de secours) :contentReference[oaicite:7]{index=7}
    val BlueDark: Color = Color(0xFF003A6B)      // bleu foncé (obligations) :contentReference[oaicite:8]{index=8}
)