package com.idfm.predictMob.presentation

import android.Manifest
import android.location.Location
import android.util.Log
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.background
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
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowForward
import androidx.compose.material.icons.filled.DirectionsCar
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Icon
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.SpanStyle
import androidx.compose.ui.text.buildAnnotatedString
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.BaselineShift
import androidx.compose.ui.text.withStyle
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.google.android.gms.location.LocationServices
import com.google.android.gms.maps.model.BitmapDescriptorFactory
import com.google.android.gms.maps.model.CameraPosition
import com.google.android.gms.maps.model.LatLng
import com.google.maps.android.compose.CameraPositionState
import com.google.maps.android.compose.GoogleMap
import com.google.maps.android.compose.Marker
import com.google.maps.android.compose.MarkerState
import com.google.maps.android.compose.Polyline
import com.google.maps.android.compose.rememberCameraPositionState
import com.idfm.predictMob.ui.theme.PredicMobTheme

data class Reward(val name: String, val requiredXP: Int, val icon: String)

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun AccueilScreen() {
    val context = LocalContext.current
    var userLocation by remember { mutableStateOf<LatLng?>(null) }
    var hasLocationPermission by remember { mutableStateOf(false) }
    val defaultPosition = LatLng(48.8566, 2.3522)
    val cameraPositionState = rememberCameraPositionState {
        position = CameraPosition.fromLatLngZoom(userLocation ?: defaultPosition, 12f)
    }

    fun updateUserLocation() {
        if (hasLocationPermission) {
            val fusedLocationClient = LocationServices.getFusedLocationProviderClient(context)
            fusedLocationClient.lastLocation.addOnSuccessListener { location: Location? ->
                location?.let {
                    Log.d("location","${it.latitude}, ${it.longitude}")
                    userLocation = LatLng(it.latitude, it.longitude)
                    cameraPositionState.position = CameraPosition.fromLatLngZoom(LatLng(it.latitude,it.longitude), 15f)
                }
            }
        }
    }
    val permissionLauncher = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.RequestPermission(),
        onResult = { granted ->
            hasLocationPermission = granted
            updateUserLocation()
        }
    )

    LaunchedEffect(Unit) {
        permissionLauncher.launch(Manifest.permission.ACCESS_FINE_LOCATION)
    }


        LazyColumn(
            modifier = Modifier
                .fillMaxSize()
                .padding(horizontal = 16.dp),
            verticalArrangement = Arrangement.spacedBy(24.dp)
        ) {
            item {
                Spacer(modifier = Modifier.height(8.dp))
                Row {
                    Text(
                        text = "Bonjour Alex!",
                        fontSize = 32.sp,
                        fontWeight = FontWeight.Bold,
                        color = PredicMobTheme.color.BlueDark,
                      modifier =   Modifier.weight(1f)
                    )
                    Text(
                        text = "⭐ 1200 XP",
                        color = PredicMobTheme.color.BlueDark,
                        fontWeight = FontWeight.SemiBold,
                        fontSize = 16.sp
                    )

                }

            }
            
            item {
                NextTripCard(cameraPositionState = cameraPositionState, userLocation = userLocation)
            }
            
            item {
                RecentActivitySection()
            }
            
            item {
                PositiveImpactSection()
            }
            
            item {
                Spacer(modifier = Modifier.height(16.dp))
            }
        }
    }

@Composable
fun NextTripCard(cameraPositionState: CameraPositionState, userLocation: LatLng?) {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .height(320.dp),
        colors = CardDefaults.cardColors(containerColor = PredicMobTheme.color.Blue.copy(alpha = 0.6f)),
        shape = RoundedCornerShape(16.dp)
    ) {
        Column(modifier = Modifier.fillMaxSize()) {
            // Map placeholder
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .height(180.dp)
                    .background(Color(0xFF4A6B5A))
            ) {
                MapContent(cameraPositionState = cameraPositionState, userLocation = userLocation)
            }
            
            Column(modifier = Modifier.padding(16.dp)) {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Icon(
                        imageVector = Icons.Default.DirectionsCar,
                        contentDescription = null,
                        tint = PredicMobTheme.color.White,
                        modifier = Modifier.size(24.dp)
                    )
                    Spacer(modifier = Modifier.width(8.dp))
                    Text(
                        text = "Prochain Trajet",
                        color = PredicMobTheme.color.White,
                        fontSize = 14.sp
                    )
                }
                
                Spacer(modifier = Modifier.height(8.dp))
                
                Text(
                    text = "Destination: Siège Social",
                    color = PredicMobTheme.color.White,
                    fontSize = 20.sp,
                    fontWeight = FontWeight.SemiBold
                )
                
                Spacer(modifier = Modifier.height(12.dp))
                
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Column {
                        Text(
                            text = "10:30 - Durée estimée:",
                            color = PredicMobTheme.color.White,
                            fontSize = 14.sp
                        )
                        Text(
                            text = "25 min",
                            color = PredicMobTheme.color.White,
                            fontSize = 16.sp,
                            fontWeight = FontWeight.Medium
                        )
                    }
                    
                    Button(
                        onClick = { /* Navigate to trip details */ },
                        colors = ButtonDefaults.buttonColors(
                            containerColor = PredicMobTheme.color.BlueDark
                        ),
                        shape = RoundedCornerShape(12.dp)
                    ) {
                        Text(
                            text = "Voir les ...",
                            color = Color.White,
                            fontWeight = FontWeight.SemiBold
                        )
                        Spacer(modifier = Modifier.width(4.dp))
                        Icon(
                            imageVector = Icons.AutoMirrored.Filled.ArrowForward,
                            contentDescription = null,
                            tint = Color.Black
                        )
                    }
                }
            }
        }
    }
}


@Composable
fun RewardsSection(userXP: Int) {
    val rewards = listOf(
        Reward("1-Day Metro Pass", 500, "🚇"),
        Reward("Bike Rental Voucher", 1000, "🚲"),
        Reward("E-Scooter Credit", 1500, "🛴"),
        Reward("Carpool Discount", 2000, "🚗"),
        Reward("Train Ticket Upgrade", 3000, "🚆")
    )
    Column {
        Text(
            text = "Your Mobility Rewards",
            fontSize = 24.sp,
            fontWeight = FontWeight.Bold,
            color = PredicMobTheme.color.BlueDark
        )
        Spacer(modifier = Modifier.height(12.dp))
        LazyRow (
            horizontalArrangement = Arrangement.spacedBy(12.dp),
            modifier = Modifier.fillMaxWidth()
        ) {
            rewards.forEach { reward ->
                item {
                Card(
                    shape = RoundedCornerShape(12.dp),
                    colors = CardDefaults.cardColors(
                        containerColor = if (userXP >= reward.requiredXP) PredicMobTheme.color.Blue else Color.LightGray
                    ),
                    modifier = Modifier.weight(1f)
                ) {
                    Column(
                        modifier = Modifier.padding(12.dp),
                        horizontalAlignment = Alignment.CenterHorizontally
                    ) {
                        Text(reward.icon, fontSize = 32.sp)
                        Text(
                            text = reward.name,
                            fontWeight = FontWeight.SemiBold,
                            color = Color.White
                        )
                        Text(
                            text = "${reward.requiredXP} XP",
                            fontSize = 12.sp,
                            color = Color.White.copy(alpha = 0.7f)
                        )
                        if (userXP >= reward.requiredXP) {
                            Text(
                                text = "Claimable!",
                                fontSize = 12.sp,
                                color = Color.Yellow,
                                fontWeight = FontWeight.Bold
                            )
                        }
                    }
                }
            }}
        }
    }
}


@Composable
private fun MapContent(
    cameraPositionState: CameraPositionState,
    userLocation: LatLng?,
) {

    LaunchedEffect(userLocation) {
        userLocation?.let {
            cameraPositionState.position = CameraPosition.fromLatLngZoom(it, 15f)
        }
    }
    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(Color(0xFFEFF3F8))
    ) {
        GoogleMap(
            modifier = Modifier.fillMaxSize(), cameraPositionState = cameraPositionState
        ) {
            val routeCoordinates = listOf(
                    LatLng(48.8579356, 2.3887146),
            LatLng(48.90221793481658, 2.4005930875358197),
            LatLng(48.900187528771056, 2.4121097032938903),
            LatLng(48.89687231373944, 2.4229136857494735),
            LatLng(48.89237326394321, 2.4326761423348535),
            LatLng(48.88682813026311, 2.4410990991669047),
            LatLng(48.88040683438414, 2.447922184285259),
            LatLng(48.873306387977726, 2.452929639038536),
            LatLng(48.86574429625975, 2.455956241877516),
            LatLng(48.857952417370755, 2.4568893576386074),
            LatLng(48.85017061772323, 2.4556710324510853),
            LatLng(48.84264122001275, 2.452298197249892),
            LatLng(48.83560341046516, 2.446822029998771),
            LatLng(48.82928783370276, 2.4393454419348683),
            LatLng(48.82390968323466, 2.430020872613582),
            LatLng(48.81966350585768, 2.4190464539485077),
            LatLng(48.81671980728262, 2.406662844762883),
            LatLng(48.815220557012865, 2.393147826283997),
            LatLng(48.8152667057754, 2.378809797849801),
            LatLng(48.81691616137385, 2.3639793820335645),
            LatLng(48.82018237267703, 2.348999369080812),
            LatLng(48.82503347262693, 2.3342154103548084),
            LatLng(48.83139204458686, 2.319964762704315),
            LatLng(48.83913744524239, 2.3065654887585116),
            LatLng(48.84810869854382, 2.2943064366630944),
            LatLng(48.85810785340476, 2.283437207702951),
            LatLng(48.86890657775865, 2.274169291176859),
            LatLng(48.88025180016239, 2.2666714428267717),
            LatLng(48.89187241363771, 2.261066599183109),
            LatLng(48.90348566558713, 2.2575285848768346),
            LatLng(48.91480311411221, 2.256174757196609),
            LatLng(48.92553896871709, 2.257124666253876),
            LatLng(48.93541865477721, 2.2605118057133937),
            LatLng(48.94418737674076, 2.2664025840992053),
            LatLng(48.95161772787875, 2.2748677141543353),
            LatLng(48.95751405315249, 2.285970992005474) // Ending point
            )
            Polyline(
                points = routeCoordinates,
                clickable = true,
                color = Color.Blue,
                width = 5f
            )

            userLocation?.let {
                Marker(
                    state = MarkerState(position = it),
                    title = "Ma position",
                    icon = BitmapDescriptorFactory.defaultMarker(BitmapDescriptorFactory.HUE_AZURE)
                )
            }
        }

    }
}

@Composable
fun RecentActivitySection() {
    Column {
        Text(
            text = "Votre Activité Récente",
            fontSize = 24.sp,
            fontWeight = FontWeight.Bold,
            color = PredicMobTheme.color.BlueDark
        )
        
        Spacer(modifier = Modifier.height(16.dp))
        
        var selectedPeriod by remember { mutableStateOf("Semaine") }
        
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .clip(RoundedCornerShape(12.dp))
                .background(PredicMobTheme.color.Blue)
                .padding(4.dp)
        ) {
            PeriodTab(
                text = "Semaine",
                selected = selectedPeriod == "Semaine",
                onClick = { selectedPeriod = "Semaine" },
                modifier = Modifier.weight(1f)
            )
            PeriodTab(
                text = "Mois",
                selected = selectedPeriod == "Mois",
                onClick = { selectedPeriod = "Mois" },
                modifier = Modifier.weight(1f)
            )
        }
        
        Spacer(modifier = Modifier.height(16.dp))
        
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            StatCard(
                value = "84",
                unit = "km",
                label = "Distance",
                modifier = Modifier.weight(1f)
            )
            StatCard(
                value = "12",
                unit = "",
                label = "Trajets",
                modifier = Modifier.weight(1f)
            )
            StatCard(
                value = "6h45",
                unit = "",
                label = "Temps total",
                modifier = Modifier.weight(1f)
            )
        }
    }
}

@Composable
fun PeriodTab(
    text: String,
    selected: Boolean,
    onClick: () -> Unit,
    modifier: Modifier = Modifier
) {
    Box(
        modifier = modifier
            .clip(RoundedCornerShape(8.dp))
            .background(if (selected) PredicMobTheme.color.BlueDark else Color.Transparent)
            .clickable(onClick = onClick)
            .padding(vertical = 12.dp),
        contentAlignment = Alignment.Center
    ) {
        Text(
            text = text,
            color = if (selected) Color.White else Color.White.copy(alpha = 0.6f),
            fontWeight = if (selected) FontWeight.SemiBold else FontWeight.Normal
        )
    }
}

@Composable
fun StatCard(
    value: String,
    unit: String,
    label: String,
    modifier: Modifier = Modifier
) {
    Card(
        modifier = modifier.height(100.dp),
        colors = CardDefaults.cardColors(containerColor = PredicMobTheme.color.Blue),
        shape = RoundedCornerShape(12.dp)
    ) {
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(12.dp),
            verticalArrangement = Arrangement.Center,
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            Row(verticalAlignment = Alignment.Bottom) {
                Text(
                    text = value,
                    fontSize = 28.sp,
                    fontWeight = FontWeight.Bold,
                    color = Color.White
                )
                if (unit.isNotEmpty()) {
                    Text(
                        text = " $unit",
                        fontSize = 16.sp,
                        color = Color.White.copy(alpha = 0.7f)
                    )
                }
            }
            Text(
                text = label,
                fontSize = 12.sp,
                color = Color.White.copy(alpha = 0.7f)
            )
        }
    }
}

@Composable
fun PositiveImpactSection() {
    Column {
        Text(
            text = "Votre Impact Positif",
            fontSize = 24.sp,
            fontWeight = FontWeight.Bold,
            color = PredicMobTheme.color.BlueDark
        )
        
        Spacer(modifier = Modifier.height(16.dp))
        
        Card(
            modifier = Modifier.fillMaxWidth(),
            colors = CardDefaults.cardColors(containerColor = PredicMobTheme.color.Blue),
            shape = RoundedCornerShape(16.dp)
        ) {
            Column(modifier = Modifier.padding(20.dp)) {
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    // Progress circle
                    Box(
                        modifier = Modifier.size(80.dp),
                        contentAlignment = Alignment.Center
                    ) {
                        CircularProgressIndicator(
                            progress = 0.75f,
                            modifier = Modifier.size(80.dp),
                            strokeWidth = 6.dp,
                            color = PredicMobTheme.color.BlueDark,
                            trackColor = Color(0xFF1E3A2E)
                        )
                        Text(
                            text = "75%",
                            color = Color.White,
                            fontSize = 20.sp,
                            fontWeight = FontWeight.Bold
                        )
                    }
                    
                    Spacer(modifier = Modifier.width(16.dp))
                    
                    Column {
                        Text(
                            text = "Objectif du mois atteint",
                            color = Color.White,
                            fontSize = 16.sp,
                            fontWeight = FontWeight.SemiBold
                        )
                        Text(
                            text = buildAnnotatedString {
                                append("Vous avez économisé ")
                                withStyle(style = SpanStyle(fontWeight = FontWeight.Bold)) {
                                    append("11.2kg")
                                }
                                append(" de\nCO")
                                withStyle(style = SpanStyle(fontSize = 10.sp, baselineShift = BaselineShift.Subscript)) {
                                    append("2")
                                }
                                append(" !")
                            },
                            color = Color.White.copy(alpha = 0.9f),
                            fontSize = 14.sp
                        )
                    }
                }
                
                Spacer(modifier = Modifier.height(16.dp))
                
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.spacedBy(12.dp)
                ) {
                    ImpactCard(
                        icon = "CO₂",
                        value = "11.2 kg",
                        label = "CO₂ évités",
                        modifier = Modifier.weight(1f)
                    )
                    ImpactCard(
                        icon = "🌲",
                        value = "2",
                        label = "Arbres sauvés",
                        modifier = Modifier.weight(1f)
                    )
                }
                
                Spacer(modifier = Modifier.height(16.dp))
                
                Text(
                    text = "En savoir plus sur nos objectifs RSE",
                    color = PredicMobTheme.color.White,
                    fontSize = 14.sp,
                    fontWeight = FontWeight.Medium,
                    modifier = Modifier.clickable { /* Navigate to RSE info */ }
                )
            }
        }
        RewardsSection(userXP = 1200)
    }
}

@Composable
fun ImpactCard(
    icon: String,
    value: String,
    label: String,
    modifier: Modifier = Modifier
) {
    Card(
        modifier = modifier.height(80.dp),
        colors = CardDefaults.cardColors(containerColor = PredicMobTheme.color.White.copy(alpha = 0.5f)),
        shape = RoundedCornerShape(12.dp)
    ) {
        Row(
            modifier = Modifier
                .fillMaxSize()
                .padding(12.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Text(
                text = icon,
                fontSize = 24.sp,
                color = PredicMobTheme.color.BlueDark
            )
            Spacer(modifier = Modifier.width(8.dp))
            Column {
                Text(
                    text = value,
                    fontSize = 18.sp,
                    fontWeight = FontWeight.Bold,
                    color = Color.White
                )
                Text(
                    text = label,
                    fontSize = 11.sp,
                    color = Color.White.copy(alpha = 0.7f)
                )
            }
        }
    }
}



@Preview
@Composable
fun AccueilScreenPreview() {
    AccueilScreen()
}

