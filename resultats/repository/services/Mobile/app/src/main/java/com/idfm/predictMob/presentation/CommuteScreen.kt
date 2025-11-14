package com.idfm.predictMob.presentation

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
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
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ArrowBack
import androidx.compose.material.icons.filled.DateRange
import androidx.compose.material.icons.filled.Schedule
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.FilterChip
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Switch
import androidx.compose.material3.SwitchDefaults
import androidx.compose.material3.Text
import androidx.compose.material3.TextFieldDefaults
import androidx.compose.material3.TopAppBar
import androidx.compose.material3.TopAppBarDefaults
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.idfm.predictMob.ui.theme.PredicMobTheme

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun CommuteScreen() {
    var selectedTransport by remember { mutableStateOf("Vélo") }
    var saveAsDefault by remember { mutableStateOf(true) }
    var frequencyType by remember { mutableStateOf("Fréquence") }
    val daysOfWeek = listOf("Lun", "Mar", "Mer", "Jeu", "Ven", "Sam", "Dim")
    var selectedDays by remember { mutableStateOf(setOf<String>()) }

    val darkGreen = PredicMobTheme.color.White
    val accentGreen = PredicMobTheme.color.Blue
    var startDestination by remember { mutableStateOf("") }
    var endDestination by remember { mutableStateOf("") }

    Scaffold(
        topBar = {
            TopAppBar(
                title = {
                    Text(
                        "Mon trajet domicile-travail",
                        color = PredicMobTheme.color.Blue,
                        fontSize = 18.sp
                    )
                },
                navigationIcon = {
                    IconButton(onClick = { /* Handle back */ }) {
                        Icon(
                            Icons.Default.ArrowBack,
                            contentDescription = "Retour",
                            tint = Color.White
                        )
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = darkGreen
                )
            )
        },
        containerColor = darkGreen
    ) { padding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
                .verticalScroll(rememberScrollState())
                .padding(24.dp),
            verticalArrangement = Arrangement.spacedBy(24.dp)
        ) {

            Text(
                "Où ?",
                color = PredicMobTheme.color.Blue,
                fontSize = 20.sp,
                fontWeight = FontWeight.Bold
            )
                // Start and End destination fields
                OutlinedTextField(
                    value = startDestination,
                    onValueChange = { startDestination = it },
                    label = { Text("Départ") },
                    modifier = Modifier.fillMaxWidth()
                )
                OutlinedTextField(
                    value = endDestination,
                    onValueChange = { endDestination = it },
                    label = { Text("Arrivée") },
                    modifier = Modifier.fillMaxWidth(),
                )


            // When section
            Text(
                "Quand ?",
                color = PredicMobTheme.color.Blue,
                fontSize = 20.sp,
                fontWeight = FontWeight.Bold
            )

            // Frequency type toggle
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(12.dp)
            ) {
                listOf("Ajouté et fixe", "Fréquence").forEach { type ->
                    OutlinedButton(
                        onClick = { frequencyType = type },
                        border = BorderStroke(
                            1.dp,
                            if (frequencyType == type) accentGreen else PredicMobTheme.color.Blue.copy(
                                alpha = 0.3f
                            )
                        ),
                        colors = ButtonDefaults.outlinedButtonColors(
                            containerColor = if (frequencyType == type) accentGreen.copy(alpha = 0.1f) else Color.Transparent
                        ),
                        shape = RoundedCornerShape(12.dp),
                        modifier = Modifier.weight(1f)
                    ) {
                        Text(
                            type,
                            color = PredicMobTheme.color.Blue,
                            fontWeight = if (frequencyType == type) FontWeight.Bold else FontWeight.Normal
                        )
                    }
                }
            }

            if (frequencyType == "Ajouté et fixe") {
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.spacedBy(12.dp)
                ) {
                    DateTimeField(
                        label = "Date du trajet",
                        value = "24/10/2024",
                        icon = Icons.Default.DateRange,
                        modifier = Modifier.weight(1f)
                    )

                    DateTimeField(
                        label = "Heure de départ",
                        value = "08:30",
                        icon = Icons.Default.Schedule,
                        modifier = Modifier.weight(1f)
                    )
                }
            } else {
                Column(Modifier.fillMaxWidth()) {
                    Text(
                        "Choisissez les jours",
                        color = PredicMobTheme.color.Blue.copy(alpha = 0.7f),
                        fontSize = 14.sp
                    )
                    LazyRow(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.spacedBy(8.dp)
                    ) {
                        daysOfWeek.forEach { day ->
                            item {
                                FilterChip(
                                    selected = selectedDays.contains(day),
                                    onClick = {
                                        selectedDays = if (selectedDays.contains(day)) {
                                            selectedDays - day
                                        } else {
                                            selectedDays + day
                                        }
                                    },
                                    label = { Text(day) },
                                )
                            }
                        }
                    }
                    DateTimeField(
                        label = "Heure de départ",
                        value = "08:30",
                        icon = Icons.Default.Schedule,
                        modifier = Modifier.weight(1f)
                    )
                }
            }

            // How section
            Text(
                "Comment ?",
                color = PredicMobTheme.color.Blue,
                fontSize = 20.sp,
                fontWeight = FontWeight.Bold
            )

            Text(
                "Choisissez votre mode de transport",
                color = PredicMobTheme.color.Blue.copy(alpha = 0.6f),
                fontSize = 14.sp
            )

            // Transport options grid
            Column(
                verticalArrangement = Arrangement.spacedBy(12.dp)
            ) {
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.spacedBy(12.dp)
                ) {
                    TransportOption(
                        label = "Vélo",
                        icon = "🚴",
                        isSelected = selectedTransport == "Vélo",
                        accentColor = accentGreen,
                        onClick = { selectedTransport = "Vélo" },
                        modifier = Modifier.weight(1f)
                    )

                    TransportOption(
                        label = "Marche",
                        icon = "🚶",
                        isSelected = selectedTransport == "Marche",
                        accentColor = accentGreen,
                        onClick = { selectedTransport = "Marche" },
                        modifier = Modifier.weight(1f)
                    )
                }

                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.spacedBy(12.dp)
                ) {
                    TransportOption(
                        label = "Covoiturage",
                        icon = "👥",
                        isSelected = selectedTransport == "Covoiturage",
                        accentColor = accentGreen,
                        onClick = { selectedTransport = "Covoiturage" },
                        modifier = Modifier.weight(1f)
                    )

                    TransportOption(
                        label = "Transports",
                        icon = "🚌",
                        isSelected = selectedTransport == "Transports",
                        accentColor = accentGreen,
                        onClick = { selectedTransport = "Transports" },
                        modifier = Modifier.weight(1f)
                    )
                }

                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.spacedBy(12.dp)
                ) {
                    TransportOption(
                        label = "Voiture élec.",
                        icon = "⚡",
                        isSelected = selectedTransport == "Voiture élec.",
                        accentColor = accentGreen,
                        onClick = { selectedTransport = "Voiture élec." },
                        modifier = Modifier.weight(1f)
                    )

                    TransportOption(
                        label = "Autre",
                        icon = "🛴",
                        isSelected = selectedTransport == "Autre",
                        accentColor = accentGreen,
                        onClick = { selectedTransport = "Autre" },
                        modifier = Modifier.weight(1f)
                    )
                }
            }

            // Options section
            Text(
                "Options",
                color = PredicMobTheme.color.Blue,
                fontSize = 20.sp,
                fontWeight = FontWeight.Bold
            )

            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .background(
                        color = PredicMobTheme.color.Blue.copy(alpha = 0.1f),
                        shape = RoundedCornerShape(12.dp)
                    )
                    .padding(16.dp),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Text(
                    "Enregistrer comme trajet par défaut",
                    color = PredicMobTheme.color.Blue,
                    fontSize = 14.sp
                )

                Switch(
                    checked = saveAsDefault,
                    onCheckedChange = { saveAsDefault = it },
                    colors = SwitchDefaults.colors(
                        checkedThumbColor = Color.White,
                        checkedTrackColor = accentGreen,
                        uncheckedThumbColor = Color.White,
                        uncheckedTrackColor = Color.Gray
                    )
                )
            }

            Spacer(modifier = Modifier.weight(1f))

            // Save button
            Button(
                onClick = { /* Handle save */ },
                modifier = Modifier
                    .fillMaxWidth()
                    .height(56.dp),
                colors = ButtonDefaults.buttonColors(
                    containerColor = accentGreen
                ),
                shape = RoundedCornerShape(12.dp)
            ) {
                Text(
                    "Enregistrer le trajet",
                    color = darkGreen,
                    fontSize = 16.sp,
                    fontWeight = FontWeight.Bold
                )
            }
        }
    }
}

@Composable
fun DateTimeField(
    label: String,
    value: String,
    icon: ImageVector,
    modifier: Modifier = Modifier
) {
    Column(
        modifier = modifier,
        verticalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        Text(
            label,
            color = PredicMobTheme.color.Blue.copy(alpha = 0.7f),
            fontSize = 12.sp
        )

        Row(
            modifier = Modifier
                .fillMaxWidth()
                .border(
                    width = 1.dp,
                    color = PredicMobTheme.color.Blue.copy(alpha = 0.3f),
                    shape = RoundedCornerShape(12.dp)
                )
                .padding(16.dp),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            Icon(
                icon,
                contentDescription = null,
                tint = PredicMobTheme.color.Blue.copy(alpha = 0.6f),
                modifier = Modifier.size(20.dp)
            )
            Text(
                value,
                color = PredicMobTheme.color.Blue,
                fontSize = 14.sp
            )
        }
    }
}

@Composable
fun TransportOption(
    label: String,
    icon: String,
    isSelected: Boolean,
    accentColor: Color,
    onClick: () -> Unit,
    modifier: Modifier = Modifier
) {
    Box(
        modifier = modifier
            .height(100.dp)
            .border(
                width = if (isSelected) 2.dp else 1.dp,
                color = if (isSelected) accentColor else PredicMobTheme.color.Blue.copy(alpha = 0.3f),
                shape = RoundedCornerShape(12.dp)
            )
            .background(
                color = if (isSelected) accentColor.copy(alpha = 0.1f) else Color.Transparent,
                shape = RoundedCornerShape(12.dp)
            )
            .clickable(onClick = onClick)
            .padding(16.dp),
        contentAlignment = Alignment.Center
    ) {
        Column(
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            Text(
                icon,
                fontSize = 32.sp
            )
            Text(
                label,
                color = PredicMobTheme.color.Blue,
                fontSize = 13.sp,
                fontWeight = if (isSelected) FontWeight.Bold else FontWeight.Normal
            )
        }
    }
}

@Preview
@Composable
fun CommuteScreenPreview() {
    CommuteScreen()
}
