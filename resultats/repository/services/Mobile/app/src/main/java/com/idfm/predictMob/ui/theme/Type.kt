package com.idfm.predictMob.ui.theme

import androidx.compose.material3.Typography
import androidx.compose.runtime.Immutable
import androidx.compose.runtime.staticCompositionLocalOf
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.Font
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.sp
import com.idfm.predictMob.R

val Typography =
    Typography(bodyLarge = TextStyle(fontFamily = FontFamily.Default, fontWeight = FontWeight.Normal, fontSize = 16.sp, lineHeight = 24.sp, letterSpacing = 0.5.sp)
    )

val LocalTypography = staticCompositionLocalOf {
    PredicMobTypography()
}

// Set of Material typography styles to start with
val Heading = FontFamily(Font(resId = R.font.paris_bold, weight = FontWeight.Bold))
val Body = FontFamily(Font(resId = R.font.idf_voyageur_regular, weight = FontWeight.Normal))



@Immutable
data class PredicMobTypography(
    val h1:TextStyle = TextStyle(fontFamily = Heading, fontWeight = FontWeight.Bold, fontSize = 30.sp),
    val body1:TextStyle = TextStyle(fontFamily = Body, fontWeight = FontWeight.Normal, fontSize = 16.sp),
    val button :TextStyle= TextStyle(fontFamily = Body, fontWeight = FontWeight.Medium, fontSize = 14.sp)
)
