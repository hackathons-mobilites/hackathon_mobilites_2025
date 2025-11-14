package com.idfm.predictMob.domain

// Enums
enum class MobilityMode {
    BIKE,
    WALK,
    CARPOOLING,
    PUBLIC_TRANSPORT,
    ELECTRIC_CAR,
    OTHER
}

enum class RiskLevel {
    LOW,
    MEDIUM,
    HIGH,
    CRITICAL
}

enum class AlternativeType {
    PUBLIC_TRANSPORT,
    BIKE,
    CARPOOLING,
    REMOTE_WORK
}

// Data classes
data class User(
    val id: String,
    val name: String,
    val email: String
)

data class Trajectory(
    val id: String = "TRJ-001",
    val originStation: String = "Saint-Ouen",
    val destinationStation: String = "La Défense",
    val departureTime: String = "08:30",
    val date: String = "24/10/2025",
    val mode: MobilityMode = MobilityMode.BIKE,
    val isDefault: Boolean = true
)

data class Prediction(
    val trajectoryId: String,
    val predictedDelayMinutesMin: Int,
    val predictedDelayMinutesMax: Int,
    val riskLevel: RiskLevel,
    val recommendedDepartureTime: String,
    val estimatedDurationMinutes: Int,
    val distanceKm: Int,
    val estimatedArrivalTime: String
)

data class Alternative(
    val id: String,
    val type: AlternativeType,
    val label: String,
    val durationMinutes: Int?,
    val co2Kg: Double?,
    val partnerName: String? = null,
    val deeplink: String? = null
)

data class CommuteLog(
    val id: String,
    val userId: String,
    val date: String,
    val chosenAlternativeType: AlternativeType
)

data class RSEProfile(
    val totalDistanceKm: Int,
    val totalTrips: Int,
    val totalDurationMinutes: Int,
    val co2SavedKg: Double,
    val monthlyGoalProgress: Int, // 0-100
    val treesEquivalent: Int
)

data class Badge(
    val id: String,
    val title: String,
    val type: String,
    val dateEarned: String
)

data class EmployeeSettings(
    val userId: String,
    val shareMobilityWithCompany: Boolean
)
