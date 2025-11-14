package com.idfm.predictMob.presentation.navigation

import androidx.compose.runtime.Composable
import androidx.navigation.NavHostController
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import com.idfm.predictMob.presentation.AccessibilityScreen
import com.idfm.predictMob.presentation.AlternativesScreen
import com.idfm.predictMob.presentation.CommuteScreen
import com.idfm.predictMob.presentation.MainScreen
import com.idfm.predictMob.presentation.PrefAlternativesScreen
import com.idfm.predictMob.presentation.login.LoginScreen

@Composable
fun AppNavHost(
    navController: NavHostController = rememberNavController()
) {
    NavHost(navController = navController, startDestination = Route.Login.route) {
        composable(Route.Login.route) {
            LoginScreen(
                onLoginSuccess = {
                    navController.navigate(Route.Home.route)
                }
            )
        }
        composable(Route.CommuteSetup.route) {
            //   CommuteSetupScreen(
            //       onSaved = { navController.navigate(Route.TripPrediction.route) }
            //   )
        }
        composable(Route.TripPrediction.route) {
            //   TripPredictionScreen(
            //       onSeeAlternatives = { navController.navigate(Route.Alternatives.route) },
            //       onBack = { navController.popBackStack() }
            //   )
        }
        composable(Route.Alternatives.route) {
            AlternativesScreen(
                onNavigateBack = { navController.popBackStack() },
            )
        }
        composable(Route.Home.route) {
            MainScreen(onNavigate = {
                navController.navigate(it.route)
            })
        }

        composable(Route.AddTrip.route) {
            CommuteScreen()
        }
        composable(Route.Accessibility.route) {
            AccessibilityScreen(
                onNavigateBack = {  },
                onNavigate ={
                    navController.navigate(it.route)
                }
            )
        }

        composable(Route.PreferencesAlternatives.route) {
            PrefAlternativesScreen(
                onBackNavigate = {
                    navController.popBackStack()
                },
            )
        }
    }
}