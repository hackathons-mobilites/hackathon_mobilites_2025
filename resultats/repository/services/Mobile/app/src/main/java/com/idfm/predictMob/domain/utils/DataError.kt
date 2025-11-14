package com.idfm.predictMob.domain.utils

sealed interface DataError: Error {
    enum class Remote: DataError {
        REQUEST_TIMEOUT,
        UNAUTHORIZED,
        CONFLICT,
        TOO_MANY_REQUESTS,
        NO_INTERNET,
        PAYLOAD_TOO_LARGE,
        SERVER_ERROR,
        SERIALIZATION,
        INVALID_CREDENTIALS,
        UNKNOWN,
        MHF_SERVER_ERROR,
    }

    enum class Local: DataError {
        DISK_FULL,
        UNKNOWN
    }
}
