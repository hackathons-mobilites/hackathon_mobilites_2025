package com.idfm.predictMob.presentation

import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.pager.HorizontalPager
import androidx.compose.foundation.pager.rememberPagerState
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Map
import androidx.compose.material.icons.filled.Notifications
import androidx.compose.material.icons.filled.NotificationsActive
import androidx.compose.material.icons.filled.Person
import androidx.compose.material.icons.filled.Settings
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.NavigationBar
import androidx.compose.material3.NavigationBarItem
import androidx.compose.material3.NavigationBarItemDefaults
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.material3.TopAppBarDefaults
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.tooling.preview.Preview
import com.idfm.predictMob.presentation.navigation.Route
import com.idfm.predictMob.ui.theme.PredicMobTheme


sealed class BottomNavItem(val label: String, val icon: ImageVector) {
    data object Accueil : BottomNavItem("Accueil", Icons.Default.Person)
    data object Trajet : BottomNavItem("Trajets", Icons.Default.Map)
    data object Stat : BottomNavItem("Notifications", Icons.Default.NotificationsActive)
    data object Profil : BottomNavItem("Preferences", Icons.Default.Settings)
}


@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun MainScreen(onNavigate: (Route) -> Unit) {

    val items = listOf(
        BottomNavItem.Accueil,
        BottomNavItem.Trajet,
        BottomNavItem.Stat,
        BottomNavItem.Profil
    )
    val pagerState = rememberPagerState(initialPage = 0, pageCount = { items.size })
    var selectedIndex by rememberSaveable { mutableIntStateOf(1) }
    var targetPage by rememberSaveable { mutableIntStateOf(-1) }


    LaunchedEffect(targetPage) {
        if (targetPage >= 0 && targetPage != pagerState.currentPage) {
            pagerState.animateScrollToPage(targetPage)
            targetPage = -1
        }
    }

    LaunchedEffect(pagerState.currentPage) {
        if (selectedIndex != pagerState.currentPage) {
            selectedIndex = pagerState.currentPage

        }
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text(items[selectedIndex].label, color = PredicMobTheme.color.BlueDark) },
                navigationIcon = {
                    if (selectedIndex == 0)
                    IconButton(onClick = { /* Navigate to profile */ }) {
                        Icon(
                            Icons.Default.Person,
                            contentDescription = "Profile",
                            tint = PredicMobTheme.color.BlueDark
                        )
                    }
                },
                actions = {
                    if (selectedIndex == 0)
                    IconButton(onClick = { /* Show notifications */ }) {
                        Icon(
                            imageVector = Icons.Default.Notifications,
                            contentDescription = "Notifications",
                            tint = PredicMobTheme.color.BlueDark
                        )
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = PredicMobTheme.color.White
                )
            )
        },
        bottomBar = {
            BottomNavigationBar(
                onItemClick = { route ->
                    val index = items.indexOfFirst { it == route }
                        if (index >= 0) {
                            targetPage = index
                    }

                },
                items = items,
                selectedIndex = selectedIndex
            )
        },
        containerColor = PredicMobTheme.color.White
    ) {
        HorizontalPager(
            modifier = Modifier
                .padding(it),
            state = pagerState,
            userScrollEnabled = false
        ) { page ->
            when (items[page]) {
                BottomNavItem.Accueil -> AccueilScreen()
                BottomNavItem.Trajet -> TripTrackerScreen(
                    { onNavigate(Route.AddTrip) },
                    { onNavigate(Route.Alternatives) }

                )
                BottomNavItem.Stat -> TrainAlertsScreen()
                BottomNavItem.Profil -> PreferencesScreen(
                    onAccessibilityClick = { onNavigate(Route.Accessibility) },
                    onAlternativesClick = { onNavigate(Route.PreferencesAlternatives) }
                )


                else -> {}
            }
        }
    }
}

@Composable
fun BottomNavigationBar(
    onItemClick: (BottomNavItem) -> Unit,
    selectedIndex: Int,
    items: List<BottomNavItem>
) {
    NavigationBar(
        containerColor = PredicMobTheme.color.White,
        contentColor = PredicMobTheme.color.White
    ) {
        items.forEachIndexed {

                index, item ->
            NavigationBarItem(
                icon = { Icon(item.icon, contentDescription = item.label) },
                label = { Text(item.label) },
                selected = selectedIndex == index,
                onClick = { onItemClick(item) },
                colors = NavigationBarItemDefaults.colors(
                    selectedIconColor = PredicMobTheme.color.BlueDark,
                    selectedTextColor = PredicMobTheme.color.BlueDark,
                    unselectedIconColor = PredicMobTheme.color.Blue,
                    unselectedTextColor = PredicMobTheme.color.Blue.copy(alpha = 0.6f),
                    indicatorColor = Color.Transparent
                )
            )
        }
    }
}

@Preview
@Composable
fun PreviewMainScreen() {
    MainScreen({})
}