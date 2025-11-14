package com.idfm.predictMob.presentation

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ArrowBack
import androidx.compose.material.icons.filled.DirectionsBike
import androidx.compose.material.icons.filled.DirectionsBus
import androidx.compose.material.icons.filled.People
import androidx.compose.material.icons.filled.Train
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.RadioButton
import androidx.compose.material3.RadioButtonDefaults
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.material3.TopAppBarDefaults
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.idfm.predictMob.ui.theme.PredicMobTheme


@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun AlternativesScreen(
    onNavigateBack: () -> Unit
) {
    var selectedOption by remember { mutableStateOf(0) }

    Scaffold(
        containerColor = PredicMobTheme.color.White,
        topBar = {
            TopAppBar(
                title = {
                    Text(
                        "Alternatives durables",
                        color = PredicMobTheme.color.Blue,
                        fontSize = 18.sp
                    )
                },
                navigationIcon = {
                    IconButton(onClick = onNavigateBack) {
                        Icon(
                            Icons.Default.ArrowBack,
                            contentDescription = "Back",
                            tint = PredicMobTheme.color.Blue
                        )
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = Color.Transparent
                )
            )
        }
    ) { padding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
        ) {
            // Map Preview
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .height(200.dp)
                    .padding(16.dp)
                    .clip(RoundedCornerShape(16.dp))
                    .background(Color(0xFFE8E4D0))
            ) {
                // Route preview placeholder
                Text(
                    "Route Preview",
                    color = Color.Gray,
                    modifier = Modifier.align(Alignment.Center)
                )
            }


            Text(
                "Votre trajet prévu",
                color = PredicMobTheme.color.Blue,
                fontSize = 16.sp,
                fontWeight = FontWeight.SemiBold,
                modifier = Modifier.padding(horizontal = 16.dp, vertical = 8.dp)
            )

            TransportOptionCard(
                icon = Icons.Default.Train,
                title = "RER A",
                duration = "50 min",
                emissions = "15.2 kg CO₂",
                isSelected = false,
                isYours = true,
                xpReward = -1,
                onSelect = { }
            )

            // Suggestions Section
            Text(
                "Nos suggestions pour réduire votre impact",
                color = PredicMobTheme.color.Blue,
                fontSize = 16.sp,
                fontWeight = FontWeight.SemiBold,
                modifier = Modifier.padding(horizontal = 16.dp, vertical = 8.dp)
            )

            Column(
                modifier = Modifier
                    .weight(1f)
                    .padding(horizontal = 16.dp),
                verticalArrangement = Arrangement.spacedBy(12.dp)
            ) {
                TransportOptionCard(
                    icon = Icons.Default.DirectionsBus,
                    title = "Transports en commun",
                    duration = "1h 10min",
                    emissions = "13.5 kg CO₂",
                    isSelected = selectedOption == 0,
                    xpReward = 100,
                    onSelect = { selectedOption = 0 }
                )

                TransportOptionCard(
                    icon = Icons.Default.DirectionsBike,
                    title = "Vélo électrique",
                    duration = "1h 05min",
                    emissions = "15.1 kg CO₂",
                    isSelected = selectedOption == 1,
                    xpReward = 20,
                    onSelect = { selectedOption = 1 }
                )

                TransportOptionCard(
                    icon = Icons.Default.People,
                    title = "Covoiturage",
                    duration = "55 min",
                    emissions = "7.6 kg CO₂",
                    isSelected = selectedOption == 2,
                    xpReward = 50,
                    onSelect = { selectedOption = 2 }
                )
            }

            // Validate Button
            Button(
                onClick = { /* Validate journey */ },
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(16.dp)
                    .height(56.dp),
                colors = ButtonDefaults.buttonColors(
                    containerColor = PredicMobTheme.color.Blue
                ),
                shape = RoundedCornerShape(12.dp)
            ) {
                Text(
                    "Valider ce trajet",
                    color = Color.Black,
                    fontSize = 16.sp,
                    fontWeight = FontWeight.SemiBold
                )
            }
        }
    }
}

@Composable
fun TransportOptionCard(
    icon: ImageVector,
    title: String,
    duration: String,
    emissions: String,
    xpReward: Int,
    isSelected: Boolean,
    isYours: Boolean = false,
    onSelect: () -> Unit
) {
    val backgroundColor =
        PredicMobTheme.color.Blue.copy(alpha = 0.15f)
    val borderColor = if (isSelected) PredicMobTheme.color.Blue else Color.Transparent

    Surface(
        onClick = {},
        modifier = Modifier.fillMaxWidth(),
        shape = RoundedCornerShape(12.dp),
        color = backgroundColor,
        border = androidx.compose.foundation.BorderStroke(
            width = if (isSelected) 2.dp else 0.dp,
            color = borderColor
        )
    ) {
        Row(
            modifier = Modifier.padding(16.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            // Icon
            Surface(
                shape = CircleShape,
                color = PredicMobTheme.color.White.copy(alpha = 0.5f),
                modifier = Modifier.size(48.dp)
            ) {
                Icon(
                    icon,
                    contentDescription = null,
                    tint = PredicMobTheme.color.BlueDark,
                    modifier = Modifier
                        .padding(12.dp)
                        .size(24.dp)
                )
            }

            Spacer(modifier = Modifier.width(16.dp))

            // Info
            Column(modifier = Modifier.weight(1f)) {
                Text(
                    title,
                    color = PredicMobTheme.color.BlueDark,
                    fontSize = 16.sp,
                    fontWeight = FontWeight.Medium
                )
                Row(
                    horizontalArrangement = Arrangement.spacedBy(8.dp)
                ) {
                    Text(
                        duration,
                        color = PredicMobTheme.color.BlueDark,
                        fontSize = 14.sp
                    )
                    Text("•", color = PredicMobTheme.color.BlueDark)
                    Text(
                        emissions,
                        color = if (emissions.contains("7.6")) PredicMobTheme.color.GreenDark
                        else if (emissions.contains("13.5")) PredicMobTheme.color.OrangeDark
                        else PredicMobTheme.color.Red,
                        fontSize = 14.sp
                    )

                }
                if (xpReward > -1)
                    Text(
                        text = "🎁 +$xpReward Points",
                        color = PredicMobTheme.color.BlueDark,
                        fontSize = 12.sp,
                        fontWeight = FontWeight.SemiBold,
                    )
            }

            // Selection Indicator
            if (!isYours) {
                RadioButton(
                    selected = isSelected,
                    onClick = onSelect,
                    colors = RadioButtonDefaults.colors(
                        selectedColor = PredicMobTheme.color.BlueDark,
                        unselectedColor = PredicMobTheme.color.BlueDark
                    )
                )
            }
        }
    }
}


@Preview
@Composable
fun AlternativesScreenPreview() {
    AlternativesScreen({})
}