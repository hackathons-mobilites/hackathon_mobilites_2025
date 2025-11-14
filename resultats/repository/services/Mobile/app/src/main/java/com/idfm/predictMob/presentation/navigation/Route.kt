package com.idfm.predictMob.presentation.navigation

sealed class Route(val route: String) {
    data object Login : Route("login")
    data object CommuteSetup : Route("commute_setup")

    data object TripPrediction : Route("trip_prediction")
    data object Alternatives : Route("alternatives")
    data object Home : Route("home")

    data object AddTrip : Route("add_trip")

    object PreferencesAlternatives : Route("PreferencesAlternatives")
    object Accessibility : Route("accessibility")
    object Notifications : Route("notifications")
    object Privacy : Route("privacy")
}