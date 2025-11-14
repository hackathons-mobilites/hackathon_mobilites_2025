package com.idfm.predictMob.domain.utils


import android.content.Context
import android.os.Build
import android.telephony.TelephonyManager
import androidx.annotation.RequiresApi

object DeviceInfoProvider {

    fun getDeviceBrand(): String = Build.BRAND
    fun getDeviceModel(): String = Build.MODEL
    fun getDeviceManufacturer(): String = Build.MANUFACTURER
    fun getOperatingSystem(): String = "Android"
    fun getOsVersion(): String = Build.VERSION.RELEASE

    fun getAppVersion(context: Context): String? {
        return context.packageManager.getPackageInfo(context.packageName, 0).versionName
    }

    @RequiresApi(Build.VERSION_CODES.P)
    fun getAppVersionCode(context: Context): String {
        return context.packageManager.getPackageInfo(context.packageName, 0).longVersionCode.toString()
    }

    fun getDeviceCarrier(context: Context): String {
        val tm = context.getSystemService(Context.TELEPHONY_SERVICE) as TelephonyManager
        return tm.networkOperatorName ?: "unknown"
    }
}
