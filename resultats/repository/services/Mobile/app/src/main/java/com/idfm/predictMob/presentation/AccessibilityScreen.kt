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
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Accessibility
import androidx.compose.material.icons.filled.AccessibleForward
import androidx.compose.material.icons.filled.ArrowBack
import androidx.compose.material.icons.filled.DirectionsWalk
import androidx.compose.material.icons.filled.Elevator
import androidx.compose.material.icons.filled.Groups
import androidx.compose.material.icons.filled.Info
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.Switch
import androidx.compose.material3.SwitchDefaults
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
import com.idfm.predictMob.presentation.navigation.Route
import com.idfm.predictMob.ui.theme.PredicMobTheme

class PreferencesState {
    // Alternatives
    var covoiturageInterne by mutableStateOf(true)
    var covoituragePartenaires by mutableStateOf(true)
    var velo by mutableStateOf(false)
    var autopartage by mutableStateOf(false)
    var transportsCommun by mutableStateOf(true)
    var teletravail by mutableStateOf(false)

    // Accessibility
    var activerMode by mutableStateOf(false)
    var eviterAscenseurs by mutableStateOf(true)
    var eviterLes by mutableStateOf(false)
    var prioriserTrajets by mutableStateOf(true)
    var eviterHeuresFort by mutableStateOf(false)
    var proposerAlternatives by mutableStateOf(true)

    // Notifications
    var alerteHotspots by mutableStateOf(true)
    var departRecommande by mutableStateOf(true)
    var alternativeDisponible by mutableStateOf(false)
    var gainCO2 by mutableStateOf(true)
    var badgeDebloque by mutableStateOf(false)

    // Privacy
    var partagerTrajets by mutableStateOf(false)
    var signalerTeletravail by mutableStateOf(false)
}


@Composable
fun rememberPreferencesState(): PreferencesState {
    return remember { PreferencesState() }
}


@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun AccessibilityScreen(
    onNavigateBack: () -> Unit,
    onNavigate: (Route) -> Unit
) {
    val preferencesState = rememberPreferencesState()
    Column(
        modifier = Modifier
            .fillMaxSize()
            .background(PredicMobTheme.color.White)
    ) {
        // Top App Bar
        TopAppBar(
            title = {
                Text(
                    "Accessibilité",
                    color = PredicMobTheme.color.BlueDark,
                    fontSize = 18.sp,
                    fontWeight = FontWeight.Medium
                )
            },
            navigationIcon = {
                IconButton(onClick = onNavigateBack) {
                    Icon(
                        Icons.Default.ArrowBack,
                        contentDescription = "Retour",
                        tint = PredicMobTheme.color.BlueDark
                    )
                }
            },
            colors = TopAppBarDefaults.topAppBarColors(
                containerColor = Color.White
            )
        )

        Column(
            modifier = Modifier
                .fillMaxSize()
                .verticalScroll(rememberScrollState())
                .padding(16.dp)
        ) {
            // Mode section with description
            AccessibilityCard(
                icon = Icons.Default.Accessibility,
                iconColor = Color(0xFF4A9FFF),
                title = "Activer le mode...",
                description = "Personnalisez vos itinéraires pour répondre à vos besoins...",
                checked = preferencesState.activerMode,
                onCheckedChange = { preferencesState.activerMode = it }
            )

            Spacer(modifier = Modifier.height(24.dp))

            // Detailed preferences section
            Text(
                "PRÉFÉRENCES DÉTAILLÉES",
                color = Color.Gray,
                fontSize = 12.sp,
                fontWeight = FontWeight.Medium,
                modifier = Modifier.padding(bottom = 12.dp)
            )

            AccessibilityDetailItem(
                icon = Icons.Default.Elevator,
                title = "Éviter les ascenseurs...",
                description = "Exclut les stations sans ascenseurs fonctionnels.",
                checked = preferencesState.eviterAscenseurs,
                onCheckedChange = { preferencesState.eviterAscenseurs = it }
            )

            AccessibilityDetailItem(
                icon = Icons.Default.AccessibleForward,
                title = "Éviter les...",
                description = "Recherche les itinéraires avec le moins de changements.",
                checked = preferencesState.eviterLes,
                onCheckedChange = { preferencesState.eviterLes = it }
            )

            AccessibilityDetailItem(
                icon = Icons.Default.Info,
                title = "Prioriser les trajets...",
                description = "Met en avant les options sans correspondance.",
                checked = preferencesState.prioriserTrajets,
                onCheckedChange = { preferencesState.prioriserTrajets = it }
            )

            AccessibilityDetailItem(
                icon = Icons.Default.Groups,
                title = "Éviter les heures de fort...",
                description = "Suggère des itinéraires en dehors des pics de trafic.",
                checked = preferencesState.eviterHeuresFort,
                onCheckedChange = { preferencesState.eviterHeuresFort = it }
            )

            AccessibilityDetailItem(
                icon = Icons.Default.DirectionsWalk,
                title = "Proposer des alternativ...",
                description = "Privilégie les trajets avec moins de marche et de...",
                checked = preferencesState.proposerAlternatives,
                onCheckedChange = { preferencesState.proposerAlternatives = it }
            )

            Spacer(modifier = Modifier.height(16.dp))

            // Navigation buttons
            Column (
                modifier = Modifier.fillMaxWidth(),
                verticalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                NavigationButton(
                    text = "Alternatives",
                    onClick = { onNavigateBack() },
                    modifier = Modifier.weight(1f)
                )
                NavigationButton(
                    text = "Notifications",
                    onClick = { onNavigate(Route.Notifications) },
                    modifier = Modifier.weight(1f)
                )
                NavigationButton(
                    text = "Confidentialité",
                    onClick = { onNavigate(Route.Privacy) },
                    modifier = Modifier.weight(1f)
                )
            }
        }
    }
}

@Composable
fun AccessibilityCard(
    icon: ImageVector,
    iconColor: Color,
    title: String,
    description: String,
    checked: Boolean,
    onCheckedChange: (Boolean) -> Unit,
    modifier: Modifier = Modifier
) {
    Row(
        modifier = modifier
            .fillMaxWidth()
            .clip(RoundedCornerShape(12.dp))
            .background(PredicMobTheme.color.BlueDark)
            .padding(16.dp),
        horizontalArrangement = Arrangement.SpaceBetween,
        verticalAlignment = Alignment.Top
    ) {
        Row(
            modifier = Modifier.weight(1f),
            verticalAlignment = Alignment.Top
        ) {
            Box(
                modifier = Modifier
                    .size(40.dp)
                    .clip(RoundedCornerShape(8.dp))
                    .background(iconColor.copy(alpha = 0.2f)),
                contentAlignment = Alignment.Center
            ) {
                Icon(
                    imageVector = icon,
                    contentDescription = null,
                    tint = iconColor,
                    modifier = Modifier.size(24.dp)
                )
            }
            Spacer(modifier = Modifier.width(12.dp))
            Column(
                modifier = Modifier.padding(top = 2.dp)
            ) {
                Text(
                    text = title,
                    color = Color.White,
                    fontSize = 15.sp,
                    fontWeight = FontWeight.Medium
                )
                Spacer(modifier = Modifier.height(4.dp))
                Text(
                    text = description,
                    color = Color.White,
                    fontSize = 13.sp,
                    lineHeight = 18.sp
                )
            }
        }
        Spacer(modifier = Modifier.width(8.dp))
        Switch(
            checked = checked,
            onCheckedChange = onCheckedChange,
            colors = SwitchDefaults.colors(
                checkedThumbColor = Color.White,
                checkedTrackColor = Color(0xFF00D9A5),
                uncheckedThumbColor = Color.White,
                uncheckedTrackColor = Color(0xFF3A3D42)
            )
        )
    }
}

@Composable
fun AccessibilityDetailItem(
    icon: ImageVector,
    title: String,
    description: String,
    checked: Boolean,
    onCheckedChange: (Boolean) -> Unit,
    modifier: Modifier = Modifier
) {
    Row(
        modifier = modifier
            .fillMaxWidth()
            .padding(vertical = 12.dp),
        horizontalArrangement = Arrangement.SpaceBetween,
        verticalAlignment = Alignment.Top
    ) {
        Row(
            modifier = Modifier.weight(1f),
            verticalAlignment = Alignment.Top
        ) {
            Box(
                modifier = Modifier
                    .size(36.dp)
                    .clip(RoundedCornerShape(8.dp))
                    .background(PredicMobTheme.color.Blue),
                contentAlignment = Alignment.Center
            ) {
                Icon(
                    imageVector = icon,
                    contentDescription = null,
                    tint = Color.White,
                    modifier = Modifier.size(20.dp)
                )
            }
            Spacer(modifier = Modifier.width(12.dp))
            Column {
                Text(
                    text = title,
                    color = PredicMobTheme.color.BlueDark,
                    fontSize = 15.sp,
                    fontWeight = FontWeight.Medium
                )
                Spacer(modifier = Modifier.height(4.dp))
                Text(
                    text = description,
                    color = Color.Gray,
                    fontSize = 13.sp,
                    lineHeight = 18.sp
                )
            }
        }
        Spacer(modifier = Modifier.width(8.dp))
        Switch(
            checked = checked,
            onCheckedChange = onCheckedChange,
            colors = SwitchDefaults.colors(
                checkedThumbColor = Color.White,
                checkedTrackColor = PredicMobTheme.color.BlueDark,
                uncheckedThumbColor = Color.White,
                uncheckedTrackColor = PredicMobTheme.color.Blue
            )
        )
    }
}

@Preview
@Composable
fun AccessibilityScreenPreview() {
    AccessibilityScreen(
        onNavigateBack = {},
        onNavigate = {}
    )
}