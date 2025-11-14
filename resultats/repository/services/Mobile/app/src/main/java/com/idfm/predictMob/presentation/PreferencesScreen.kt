package com.idfm.predictMob.presentation

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.automirrored.filled.ArrowForward
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun PreferencesScreen(
    onAlternativesClick: () -> Unit = {},
    onAccessibilityClick: () -> Unit = {},
    onNotificationsClick: () -> Unit = {},
    onPrivacyClick: () -> Unit = {}
) {

        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(horizontal = 16.dp, vertical = 8.dp),
            verticalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            PreferenceItem(
                icon = Icons.Default.DirectionsBus,
                iconBackgroundColor = Color(0xFFBBDEFB),
                title = "Préférences d'alternatives",
                onClick = onAlternativesClick
            )

            PreferenceItem(
                icon = Icons.Default.Accessible,
                iconBackgroundColor = Color(0xFFBBDEFB),
                title = "Préférences d'accessibilité",
                onClick = onAccessibilityClick
            )

            PreferenceItem(
                icon = Icons.Default.Notifications,
                iconBackgroundColor = Color(0xFFBBDEFB),
                title = "Paramètres de notifications",
                onClick = onNotificationsClick
            )

            PreferenceItem(
                icon = Icons.Default.Lock,
                iconBackgroundColor = Color(0xFFBBDEFB),
                title = "Confidentialité et partage",
                onClick = onPrivacyClick
            )
        }
    }

@Composable
fun PreferenceItem(
    icon: ImageVector,
    iconBackgroundColor: Color,
    title: String,
    onClick: () -> Unit,
    modifier: Modifier = Modifier
) {
    Surface(
        modifier = modifier
            .fillMaxWidth()
            .clickable(onClick = onClick),
        shape = RoundedCornerShape(12.dp),
        color = Color.White,
        shadowElevation = 0.5.dp
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically
        ) {
            Row(
                horizontalArrangement = Arrangement.spacedBy(16.dp),
                verticalAlignment = Alignment.CenterVertically
            ) {
                // Icon container
                Surface(
                    shape = RoundedCornerShape(12.dp),
                    color = iconBackgroundColor,
                    modifier = Modifier.size(56.dp)
                ) {
                    Box(
                        contentAlignment = Alignment.Center,
                        modifier = Modifier.fillMaxSize()
                    ) {
                        Icon(
                            imageVector = icon,
                            contentDescription = null,
                            tint = Color(0xFF1976D2),
                            modifier = Modifier.size(28.dp)
                        )
                    }
                }

                // Title
                Text(
                    text = title,
                    fontSize = 17.sp,
                    fontWeight = FontWeight.Normal,
                    color = Color.Black
                )
            }

            // Arrow icon
            Icon(
                imageVector = Icons.AutoMirrored.Filled.ArrowForward,
                contentDescription = "Ouvrir",
                tint = Color.Gray,
                modifier = Modifier.size(24.dp)
            )
        }
    }
}

@Preview
@Composable
fun PreferencesScreenPreview() {
    MaterialTheme {
        PreferencesScreen()
    }
}