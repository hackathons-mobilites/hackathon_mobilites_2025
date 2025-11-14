package com.idfm.predictMob.presentation

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.idfm.predictMob.ui.theme.PredicMobTheme

// Color palette
private val DarkBackground = Color(0xFF1A1D26)
private val CardBackground = Color(0xFF252932)
private val AccentBlue = Color(0xFF4A9EFF)
private val TextPrimary = Color(0xFFFFFFFF)
private val TextSecondary = Color(0xFFB0B6C3)
private val RedAlert = Color(0xFFFF4444)
private val OrangeAlert = Color(0xFFFF8844)
private val YellowAlert = Color(0xFFFFBB33)

data class TrainAlert(
    val type: AlertType,
    val title: String,
    val from: String,
    val to: String,
    val time: String,
    val timeAgo: String,
    val actionText: String
)

enum class AlertType(val color: Color, val icon: ImageVector) {
    DELAY(OrangeAlert, Icons.Default.AccessTime),
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun TrainAlertsScreen() {
    var selectedFilter by remember { mutableStateOf("recent") }
    
    val alerts = listOf(
        TrainAlert(
            type = AlertType.DELAY,
            title = "Grève Annoncée",
            from = "Paris",
            to = "Marseille",
            time = "14:30",
            timeAgo = "il y a 2 min",
            actionText = "Voir les détails"
        ),
        TrainAlert(
            type = AlertType.DELAY,
            title = "Retard Estimé",
            from = "Lyon",
            to = "Lille",
            time = "09:15",
            timeAgo = "il y a 15 min",
            actionText = "Voir alternatives"
        ),
        TrainAlert(
            type = AlertType.DELAY,
            title = "Léger retard",
            from = "Bordeaux",
            to = "Nantes",
            time = "18:00",
            timeAgo = "il y a 45 min",
            actionText = "Confirmer"
        )
    )
    

        Column(
            modifier = Modifier
                .fillMaxSize()
                .verticalScroll(rememberScrollState())
        ) {
            // Filter chips
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 16.dp, vertical = 12.dp),
                horizontalArrangement = Arrangement.spacedBy(12.dp)
            ) {
                FilterChip(
                    selected = selectedFilter == "recent",
                    onClick = { selectedFilter = "recent" },
                    label = { 
                        Row(
                            verticalAlignment = Alignment.CenterVertically,
                            horizontalArrangement = Arrangement.spacedBy(6.dp)
                        ) {
                            Icon(
                                Icons.Default.UnfoldMore,
                                contentDescription = null,
                                modifier = Modifier.size(16.dp)
                            )
                            Text("Plus récent")
                        }
                    },
                    colors = FilterChipDefaults.filterChipColors(
                        containerColor = CardBackground,
                        selectedContainerColor = AccentBlue.copy(alpha = 0.3f),
                        labelColor = TextPrimary,
                        selectedLabelColor = AccentBlue
                    )
                )
                
                FilterChip(
                    selected = selectedFilter == "urgent",
                    onClick = { selectedFilter = "urgent" },
                    label = { 
                        Row(
                            verticalAlignment = Alignment.CenterVertically,
                            horizontalArrangement = Arrangement.spacedBy(6.dp)
                        ) {
                            Icon(
                                Icons.Default.PriorityHigh,
                                contentDescription = null,
                                modifier = Modifier.size(16.dp),
                                tint = RedAlert
                            )
                            Text("Urgence")
                        }
                    },
                    colors = FilterChipDefaults.filterChipColors(
                        containerColor =  PredicMobTheme.color.BlueDark,
                        selectedContainerColor = RedAlert.copy(alpha = 0.2f),
                        labelColor = TextPrimary,
                        selectedLabelColor = RedAlert
                    )
                )
            }
            
            // Alert cards
            alerts.forEach { alert ->
                AlertCard(alert)
                Spacer(modifier = Modifier.height(12.dp))
            }
            
            // Empty state
            EmptyAlertState()
        }

}

@Composable
fun AlertCard(alert: TrainAlert) {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = 16.dp),
        colors = CardDefaults.cardColors(
            containerColor =  PredicMobTheme.color.Blue.copy(alpha = 0.3f)
        ),
        shape = RoundedCornerShape(12.dp)
    ) {
        Row(
            modifier = Modifier.fillMaxWidth()
        ) {
            // Colored vertical bar
            Box(
                modifier = Modifier
                    .width(4.dp)
                    .height(120.dp)
                    .background(
                        alert.type.color,
                        shape = RoundedCornerShape(topStart = 12.dp, bottomStart = 12.dp)
                    )
            )
            
            Column(
                modifier = Modifier
                    .weight(1f)
                    .padding(16.dp)
            ) {
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.Top
                ) {
                    Row(
                        verticalAlignment = Alignment.CenterVertically,
                        horizontalArrangement = Arrangement.spacedBy(12.dp)
                    ) {
                        Icon(
                            alert.type.icon,
                            contentDescription = null,
                            tint = alert.type.color,
                            modifier = Modifier.size(24.dp)
                        )
                        
                        Text(
                            text = alert.title,
                            fontSize = 18.sp,
                            fontWeight = FontWeight.SemiBold,
                            color =  PredicMobTheme.color.BlueDark
                        )
                    }
                    
                    Text(
                        text = alert.timeAgo,
                        fontSize = 12.sp,
                        color =  PredicMobTheme.color.BlueDark
                    )
                }
                
                Spacer(modifier = Modifier.height(8.dp))
                
                Text(
                    text = "${alert.from} → ${alert.to}, ${alert.time}",
                    fontSize = 14.sp,
                    color =  PredicMobTheme.color.BlueDark
                )
                
                Spacer(modifier = Modifier.height(12.dp))
                
                Button(
                    onClick = { /* Handle action */ },
                    colors = ButtonDefaults.buttonColors(
                        containerColor =  PredicMobTheme.color.BlueDark
                    ),
                    shape = RoundedCornerShape(8.dp)
                ) {
                    Text(
                        text = alert.actionText,
                        fontSize = 14.sp
                    )
                    if (alert.actionText.contains("alternatives")) {
                        Spacer(modifier = Modifier.width(4.dp))
                        Icon(
                            Icons.Default.ArrowForward,
                            contentDescription = null,
                            modifier = Modifier.size(16.dp)
                        )
                    }
                }
            }
        }
    }
}

@Composable
fun EmptyAlertState() {
    Column(
        modifier = Modifier
            .fillMaxWidth()
            .padding(32.dp),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Icon(
            Icons.Default.NotificationsOff,
            contentDescription = null,
            tint = AccentBlue.copy(alpha = 0.5f),
            modifier = Modifier.size(64.dp)
        )
        
        Spacer(modifier = Modifier.height(16.dp))
        
        Text(
            text = "Aucune alerte",
            fontSize = 20.sp,
            fontWeight = FontWeight.SemiBold,
            color = TextPrimary
        )
        
        Spacer(modifier = Modifier.height(8.dp))
        
        Text(
            text = "Aucune alerte pour vos prochains trajets.\nNous vous préviendrons si quelque chose\nchange.",
            fontSize = 14.sp,
            color = TextSecondary,
            textAlign = androidx.compose.ui.text.style.TextAlign.Center,
            lineHeight = 20.sp
        )
    }
}

@Preview
@Composable
fun TrainAlertsScreenPreview() {
    MaterialTheme {
        TrainAlertsScreen()
    }
}