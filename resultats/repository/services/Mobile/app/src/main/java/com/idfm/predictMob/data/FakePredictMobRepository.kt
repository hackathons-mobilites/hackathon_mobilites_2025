package com.idfm.predictMob.data


import com.idfm.predictMob.domain.Alternative
import com.idfm.predictMob.domain.AlternativeType
import com.idfm.predictMob.domain.Badge
import com.idfm.predictMob.domain.CommuteLog
import com.idfm.predictMob.domain.Prediction
import com.idfm.predictMob.domain.RSEProfile
import com.idfm.predictMob.domain.RiskLevel
import com.idfm.predictMob.domain.Trajectory
import com.idfm.predictMob.domain.User

class FakePredictMobRepository : PredictMobRepository {
    
    private var currentUser: User? = null
    private var currentTrajectory: Trajectory? = null
    private var rseProfile: RSEProfile = RSEProfile(
        totalDistanceKm = 84,
        totalTrips = 12,
        totalDurationMinutes = 405,
        co2SavedKg = 11.2,
        monthlyGoalProgress = 75,
        treesEquivalent = 2
    )
    
    private val badges = listOf(
        Badge(
            id = "badge-1",
            title = "Eco-Commute Champion",
            type = "RSE Achievement",
            dateEarned = "15/10/2025"
        ),
        Badge(
            id = "badge-2",
            title = "Bike Lover",
            type = "Transport Mode",
            dateEarned = "20/10/2025"
        ),
        Badge(
            id = "badge-3",
            title = "Remote Hero",
            type = "Flexibility",
            dateEarned = "22/10/2025"
        )
    )
    
    override fun loginWithProvider(provider: String): User {
        val user = User(
            id = "user-001",
            name = "Alex",
            email = "alex@example.com"
        )
        currentUser = user
        return user
    }
    
    override fun saveTrajectory(trajectory: Trajectory) {
        currentTrajectory = trajectory
    }
    
    override fun getCurrentTrajectory(): Trajectory? {
        return currentTrajectory ?: Trajectory()
    }
    
    override fun getPredictionForUser(userId: String): Prediction {
        return Prediction(
            trajectoryId = "TRJ-001",
            predictedDelayMinutesMin = 5,
            predictedDelayMinutesMax = 10,
            riskLevel = RiskLevel.HIGH,
            recommendedDepartureTime = "08:00",
            estimatedDurationMinutes = 45,
            distanceKm = 22,
            estimatedArrivalTime = "08:45"
        )
    }
    
    override fun getAlternativesForTrajectory(trajectoryId: String): List<Alternative> {
        return listOf(
            Alternative(
                id = "alt-1",
                type = AlternativeType.PUBLIC_TRANSPORT,
                label = "Transports en commun",
                durationMinutes = 70,
                co2Kg = 13.5
            ),
            Alternative(
                id = "alt-2",
                type = AlternativeType.BIKE,
                label = "Vélo électrique",
                durationMinutes = 65,
                co2Kg = 1.5
            ),
            Alternative(
                id = "alt-3",
                type = AlternativeType.CARPOOLING,
                label = "Covoiturage",
                durationMinutes = 55,
                co2Kg = 7.6
            ),
            Alternative(
                id = "alt-4",
                type = AlternativeType.REMOTE_WORK,
                label = "Télétravail",
                durationMinutes = null,
                co2Kg = 0.0
            )
        )
    }
    
    override fun saveCommuteLog(log: CommuteLog) {
        // Mock: just update RSE profile
        rseProfile = rseProfile.copy(
            totalTrips = rseProfile.totalTrips + 1
        )
    }
    
    override fun getRSEProfile(userId: String): RSEProfile {
        return rseProfile
    }
    
    override fun getBadges(userId: String): List<Badge> {
        return badges
    }
    
    override fun getCurrentUser(): User? {
        return currentUser
    }
    
    override fun updateRSEPoints(userId: String, alternative: Alternative) {
        // Mock: update CO2 saved based on alternative
        val co2Saved = when (alternative.type) {
            AlternativeType.PUBLIC_TRANSPORT -> 1.7
            AlternativeType.BIKE -> 13.7
            AlternativeType.CARPOOLING -> 7.6
            AlternativeType.REMOTE_WORK -> 15.2
        }
        
        rseProfile = rseProfile.copy(
            co2SavedKg = rseProfile.co2SavedKg + co2Saved,
            totalTrips = rseProfile.totalTrips + 1,
            monthlyGoalProgress = minOf(100, rseProfile.monthlyGoalProgress + 5)
        )
    }
}
