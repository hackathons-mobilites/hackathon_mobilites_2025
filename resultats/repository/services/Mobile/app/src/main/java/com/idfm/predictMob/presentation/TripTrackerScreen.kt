package com.idfm.predictMob.presentation

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.filled.BarChart
import androidx.compose.material.icons.filled.ChevronRight
import androidx.compose.material.icons.filled.DirectionsBike
import androidx.compose.material.icons.filled.DirectionsBus
import androidx.compose.material.icons.filled.DirectionsCar
import androidx.compose.material.icons.filled.History
import androidx.compose.material.icons.filled.Home
import androidx.compose.material.icons.filled.Person
import androidx.compose.material.icons.filled.Train
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.FloatingActionButton
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.NavigationBar
import androidx.compose.material3.NavigationBarItem
import androidx.compose.material3.NavigationBarItemDefaults
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.darkColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.idfm.predictMob.domain.RiskLevel
import com.idfm.predictMob.ui.theme.PredicMobTheme

// Data classes
data class Trip(
    val id: Int,
    val title: String,
    val subtitle: String,
    val icon: ImageVector,
    val status: RiskLevel
)


@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun TripTrackerScreen(
    onAddClick: () -> Unit,
    onTripSelected: (Int) -> Unit
) {
    val trips = remember {
        listOf(
            Trip(
                id = 1,
                title = "Domicile → Travail",
                subtitle = "Voiture",
                icon = Icons.Default.DirectionsCar,
                status = RiskLevel.CRITICAL
            ),
            Trip(
                id = 2,
                title = "Travail → Domicile",
                subtitle = "Train, Marche",
                icon = Icons.Default.Train,
                status = RiskLevel.MEDIUM
            ),
            Trip(
                id = 3,
                title = "Visite Client A",
                subtitle = "Vélo",
                icon = Icons.Default.DirectionsBike,
                status = RiskLevel.HIGH
            ),
            Trip(
                id = 4,
                title = "Aéroport",
                subtitle = "Transports en commun",
                icon = Icons.Default.DirectionsBus,
                status = RiskLevel.LOW
            )
        )
    }


    Scaffold(
        floatingActionButton = {
            FloatingActionButton(
                onClick = { onAddClick() },
                containerColor = PredicMobTheme.color.Blue,
                contentColor = Color.White
            ) {
                Icon(
                    imageVector = Icons.Default.Add,
                    contentDescription = "Ajouter un trajet"
                )
            }
        },
        containerColor = PredicMobTheme.color.White
    ) { paddingValues ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(paddingValues)
        ) {
            // Trip list
            LazyColumn(
                modifier = Modifier.fillMaxSize(),
                contentPadding = PaddingValues(horizontal = 16.dp, vertical = 8.dp),
                verticalArrangement = Arrangement.spacedBy(12.dp)
            ) {
                items(trips) { trip ->
                    TripCard(trip, onTripSelected)
                }
            }
        }
    }
}

@Composable
fun TripCard(trip: Trip, onTripSelected: (Int) -> Unit) {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .height(80.dp),
        colors = CardDefaults.cardColors(
            containerColor = PredicMobTheme.color.Blue.copy(alpha = 0.3f)
        ),
        onClick = { onTripSelected(trip.id) },
        shape = RoundedCornerShape(12.dp)
    ) {
        Row(
            modifier = Modifier
                .fillMaxSize()
                .padding(16.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            // Icon
            Box(
                modifier = Modifier
                    .size(48.dp)
                    .clip(RoundedCornerShape(8.dp))
                    .background(PredicMobTheme.color.Blue),
                contentAlignment = Alignment.Center
            ) {
                Icon(
                    imageVector = trip.icon,
                    contentDescription = trip.title,
                    tint = Color.White,
                    modifier = Modifier.size(28.dp)
                )
            }

            Spacer(modifier = Modifier.width(16.dp))

            // Title and subtitle
            Column(
                modifier = Modifier.weight(1f)
            ) {
                Text(
                    text = trip.title,
                    style = MaterialTheme.typography.titleMedium,
                    fontWeight = FontWeight.SemiBold,
                    color = PredicMobTheme.color.BlueDark
                )
                Text(
                    text = trip.subtitle,
                    style = MaterialTheme.typography.bodyMedium,
                    color = PredicMobTheme.color.Blue,
                    fontSize = 13.sp
                )
            }

            // Status badge
            Surface(
                color = when (trip.status) {
                    RiskLevel.LOW -> Color(0xB48BC34A)
                    RiskLevel.MEDIUM -> Color(0xFFFFA500)
                    RiskLevel.HIGH -> Color(0xA6FF001E)
                    RiskLevel.CRITICAL -> Color(0xFFE53935)
                },
                shape = RoundedCornerShape(6.dp)
            ) {
                Text(
                    text = when (trip.status) {
                        RiskLevel.LOW -> "Faible"
                        RiskLevel.MEDIUM -> "Moyen"
                        RiskLevel.HIGH -> "Elevé"
                        RiskLevel.CRITICAL -> "Critique"
                    },
                    color = PredicMobTheme.color.White,
                    fontSize = 12.sp,
                    fontWeight = FontWeight.Medium,
                    modifier = Modifier.padding(horizontal = 12.dp, vertical = 6.dp)
                )
            }

            Spacer(modifier = Modifier.width(8.dp))

            // Arrow icon
            Icon(
                imageVector = Icons.Default.ChevronRight,
                contentDescription = "Détails",
                tint = Color.Gray,
                modifier = Modifier.size(20.dp)
            )
        }
    }
}

@Composable
fun BottomNavigationBar(selectedTab: Int, onTabSelected: (Int) -> Unit) {
    NavigationBar(
        containerColor = Color(0xFF0D1F1F),
        contentColor = Color.White
    ) {
        NavigationBarItem(
            selected = selectedTab == 0,
            onClick = { onTabSelected(0) },
            icon = {
                Icon(
                    imageVector = Icons.Default.Home,
                    contentDescription = "Accueil"
                )
            },
            label = { Text("Accueil", fontSize = 12.sp) },
            colors = NavigationBarItemDefaults.colors(
                selectedIconColor = Color(0xFF00BFA5),
                selectedTextColor = Color(0xFF00BFA5),
                unselectedIconColor = Color.Gray,
                unselectedTextColor = Color.Gray,
                indicatorColor = Color.Transparent
            )
        )
        NavigationBarItem(
            selected = selectedTab == 1,
            onClick = { onTabSelected(1) },
            icon = {
                Icon(
                    imageVector = Icons.Default.History,
                    contentDescription = "Historique"
                )
            },
            label = { Text("Historique", fontSize = 12.sp) },
            colors = NavigationBarItemDefaults.colors(
                selectedIconColor = Color(0xFF00BFA5),
                selectedTextColor = Color(0xFF00BFA5),
                unselectedIconColor = Color.Gray,
                unselectedTextColor = Color.Gray,
                indicatorColor = Color.Transparent
            )
        )
        NavigationBarItem(
            selected = selectedTab == 2,
            onClick = { onTabSelected(2) },
            icon = {
                Icon(
                    imageVector = Icons.Default.BarChart,
                    contentDescription = "Stats"
                )
            },
            label = { Text("Stats", fontSize = 12.sp) },
            colors = NavigationBarItemDefaults.colors(
                selectedIconColor = Color(0xFF00BFA5),
                selectedTextColor = Color(0xFF00BFA5),
                unselectedIconColor = Color.Gray,
                unselectedTextColor = Color.Gray,
                indicatorColor = Color.Transparent
            )
        )
        NavigationBarItem(
            selected = selectedTab == 3,
            onClick = { onTabSelected(3) },
            icon = {
                Icon(
                    imageVector = Icons.Default.Person,
                    contentDescription = "Profil"
                )
            },
            label = { Text("Profil", fontSize = 12.sp) },
            colors = NavigationBarItemDefaults.colors(
                selectedIconColor = Color(0xFF00BFA5),
                selectedTextColor = Color(0xFF00BFA5),
                unselectedIconColor = Color.Gray,
                unselectedTextColor = Color.Gray,
                indicatorColor = Color.Transparent
            )
        )
    }
}

@Preview(showBackground = true, showSystemUi = true)
@Composable
fun TripTrackerScreenPreview() {
   
        TripTrackerScreen(
            onAddClick = {},
            onTripSelected = {}
        )
}