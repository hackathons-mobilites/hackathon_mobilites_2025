package com.idfm.predictMob.data

import com.idfm.predictMob.domain.Alternative
import com.idfm.predictMob.domain.Badge
import com.idfm.predictMob.domain.CommuteLog
import com.idfm.predictMob.domain.Prediction
import com.idfm.predictMob.domain.RSEProfile
import com.idfm.predictMob.domain.Trajectory
import com.idfm.predictMob.domain.User

interface PredictMobRepository {
    fun loginWithProvider(provider: String): User
    fun saveTrajectory(trajectory: Trajectory)
    fun getCurrentTrajectory(): Trajectory?
    fun getPredictionForUser(userId: String): Prediction
    fun getAlternativesForTrajectory(trajectoryId: String): List<Alternative>
    fun saveCommuteLog(log: CommuteLog)
    fun getRSEProfile(userId: String): RSEProfile
    fun getBadges(userId: String): List<Badge>
    fun getCurrentUser(): User?
    fun updateRSEPoints(userId: String, alternative: Alternative)
}
