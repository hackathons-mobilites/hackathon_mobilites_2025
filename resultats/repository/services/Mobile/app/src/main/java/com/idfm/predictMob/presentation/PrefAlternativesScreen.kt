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
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.idfm.predictMob.presentation.navigation.Route
import com.idfm.predictMob.ui.theme.PredicMobTheme

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun PrefAlternativesScreen(
    preferencesState: PreferencesState = rememberPreferencesState(),
    onBackNavigate: () -> Unit
) {
    Column(
        modifier = Modifier
            .fillMaxSize()
            .background(PredicMobTheme.color.White)
    ) {
        // Top App Bar
        TopAppBar(
            title = {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Text(
                        "Préférences de trajet",
                        color = Color.White,
                        fontSize = 18.sp,
                        fontWeight = FontWeight.Medium
                    )
                    Text(
                        "Enregistrer",
                        color = Color(0xFF00D9A5),
                        fontSize = 16.sp,
                        modifier = Modifier.padding(start = 8.dp)
                    )
                }
            },
            navigationIcon = {
                IconButton(onClick = { onBackNavigate() }) {
                    Icon(
                        Icons.Default.ArrowBack,
                        contentDescription = "Retour",
                        tint = Color.White
                    )
                }
            },
            colors = TopAppBarDefaults.topAppBarColors(
                containerColor = Color(0xFF1A1D21)
            )
        )

        Column(
            modifier = Modifier
                .fillMaxSize()
                .verticalScroll(rememberScrollState())
                .padding(16.dp)
        ) {
            // Alternatives section
            Text(
                "Mes alternatives préférées",
                color = PredicMobTheme.color.Blue,
                fontSize = 16.sp,
                fontWeight = FontWeight.Medium,
                modifier = Modifier.padding(bottom = 12.dp)
            )

            PreferenceItem(
                icon = Icons.Default.Group,
                title = "Covoiturage interne",
                checked = preferencesState.covoiturageInterne,
                onCheckedChange = { preferencesState.covoiturageInterne = it }
            )

            PreferenceItem(
                icon = Icons.Default.People,
                title = "Covoiturage partenaires",
                checked = preferencesState.covoituragePartenaires,
                onCheckedChange = { preferencesState.covoituragePartenaires = it }
            )

            PreferenceItem(
                icon = Icons.Default.DirectionsBike,
                title = "Vélo",
                checked = preferencesState.velo,
                onCheckedChange = { preferencesState.velo = it }
            )

            PreferenceItem(
                icon = Icons.Default.DirectionsCar,
                title = "Autopartage",
                checked = preferencesState.autopartage,
                onCheckedChange = { preferencesState.autopartage = it }
            )

            PreferenceItem(
                icon = Icons.Default.DirectionsBus,
                title = "Transports en commun",
                checked = preferencesState.transportsCommun,
                onCheckedChange = { preferencesState.transportsCommun = it }
            )

            PreferenceItem(
                icon = Icons.Default.Home,
                title = "Télétravail (si aléa majeur)",
                checked = preferencesState.teletravail,
                onCheckedChange = { preferencesState.teletravail = it }
            )

            Spacer(modifier = Modifier.height(24.dp))

            // Priorities section
            Text(
                "Mes priorités",
                color = PredicMobTheme.color.Blue,
                fontSize = 16.sp,
                fontWeight = FontWeight.Medium,
                modifier = Modifier.padding(bottom = 8.dp)
            )

            Text(
                "Classez vos priorités pour optimiser vos trajets.",
                color = Color.Gray,
                fontSize = 13.sp,
                modifier = Modifier.padding(bottom = 12.dp)
            )

            PriorityItem(
                number = 1,
                title = "Réduire mon empreinte CO₂",
                color = PredicMobTheme.color.Blue.copy(alpha = 0.8f)
            )

            PriorityItem(
                number = 2,
                title = "Minimiser mon temps de trajet",
                color = PredicMobTheme.color.Blue.copy(alpha = 0.8f)
            )

            PriorityItem(
                number = 3,
                title = "Minimiser le coût",
                color = PredicMobTheme.color.Blue.copy(alpha = 0.8f)
            )

            PriorityItem(
                number = 4,
                title = "Limiter le temps de marche",
                color = PredicMobTheme.color.Blue.copy(alpha = 0.8f)
            )

            PriorityItem(
                number = 5,
                title = "Éviter la météo défavorable",
                color = PredicMobTheme.color.Blue.copy(alpha = 0.8f)
            )

            Spacer(modifier = Modifier.height(16.dp))
        }
    }
}

@Composable
fun PreferenceItem(
    icon: ImageVector,
    title: String,
    checked: Boolean,
    onCheckedChange: (Boolean) -> Unit,
    modifier: Modifier = Modifier
) {
    Row(
        modifier = modifier
            .fillMaxWidth()
            .padding(vertical = 8.dp),
        horizontalArrangement = Arrangement.SpaceBetween,
        verticalAlignment = Alignment.CenterVertically
    ) {
        Row(
            verticalAlignment = Alignment.CenterVertically,
            modifier = Modifier.weight(1f)
        ) {
            Icon(
                imageVector = icon,
                contentDescription = null,
                tint = PredicMobTheme.color.BlueDark,
                modifier = Modifier.size(24.dp)
            )
            Spacer(modifier = Modifier.width(12.dp))
            Text(
                text = title,
                color = PredicMobTheme.color.BlueDark,
                fontSize = 15.sp
            )
        }
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

@Composable
fun PriorityItem(
    number: Int,
    title: String,
    color: Color,
    modifier: Modifier = Modifier
) {
    Row(
        modifier = modifier
            .fillMaxWidth()
            .clip(RoundedCornerShape(8.dp))
            .background(color)
            .padding(horizontal = 16.dp, vertical = 12.dp),
        horizontalArrangement = Arrangement.SpaceBetween,
        verticalAlignment = Alignment.CenterVertically
    ) {
        Row(
            verticalAlignment = Alignment.CenterVertically,
            modifier = Modifier.weight(1f)
        ) {
            Box(
                modifier = Modifier
                    .size(24.dp)
                    .clip(RoundedCornerShape(4.dp))
                    .background(Color.White.copy(alpha = 0.2f)),
                contentAlignment = Alignment.Center
            ) {
                Text(
                    text = number.toString(),
                    color = Color.White,
                    fontSize = 14.sp,
                    fontWeight = FontWeight.Bold
                )
            }
            Spacer(modifier = Modifier.width(12.dp))
            Text(
                text = title,
                color = Color.White,
                fontSize = 14.sp
            )
        }
        Icon(
            imageVector = Icons.Default.DragHandle,
            contentDescription = "Réorganiser",
            tint = Color.White.copy(alpha = 0.5f),
            modifier = Modifier.size(20.dp)
        )
    }
    Spacer(modifier = Modifier.height(8.dp))
}

@Composable
fun NavigationButton(
    text: String,
    onClick: () -> Unit,
    modifier: Modifier = Modifier
) {
    Button(
        onClick = onClick,
        modifier = modifier.height(48.dp),
        colors = ButtonDefaults.buttonColors(
            containerColor = PredicMobTheme.color.Blue.copy(alpha = 0.8f)
        ),
        shape = RoundedCornerShape(8.dp)
    ) {
        Text(
            text = text,
            fontSize = 12.sp,
            color = Color.White
        )
    }
}

@Preview
@Composable
fun PrefAlternativesScreenPreview() {
    PrefAlternativesScreen(
        preferencesState = PreferencesState(),
        onBackNavigate = {}
    )
}