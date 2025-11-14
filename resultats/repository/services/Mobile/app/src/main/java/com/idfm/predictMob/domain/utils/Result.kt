package com.idfm.predictMob.domain.utils


sealed interface Result<out D, out E : Error> {
    data class Success<out D>(val data: D) : Result<D, Nothing>
    data class Error<out E : com.idfm.predictMob.domain.utils.Error>(val error: E, val code:Int = -1, val message: String = "") :
        Result<Nothing, E>

    data object SuccessEmpty : Result<Nothing, Nothing>
}

inline fun <T, E : Error, R> Result<T, E>.map(map: (T) -> R): Result<R, E> {
    return when (this) {
        is Result.Error -> Result.Error(error, code, message)
        is Result.Success -> Result.Success(map(data))
        is Result.SuccessEmpty -> Result.SuccessEmpty
    }
}

fun <T, E : Error> Result<T, E>.asEmptyDataResult(): EmptyResult<E> {
    return map { }
}

inline fun <T, E : Error> Result<T, E>.onSuccess(action: (T) -> Unit): Result<T, E> {
    return when (this) {
        is Result.Error -> this
        is Result.SuccessEmpty -> this
        is Result.Success -> {
            action(data)
            this
        }
    }
}

inline fun <T, E : Error, R : Error> Result<T, E>.switchError(switch: (E, String) -> Result<T, R>): Result<T, R> {
    return when (this) {
        is Result.Error -> switch(this.error, this.message)
        is Result.Success -> this
        is Result.SuccessEmpty -> this
    }
}

inline fun <T, E : Error> Result<T, E>.onError(action: (E) -> Unit): Result<T, E> {
    return when (this) {
        is Result.Error -> {
            action(error)
            this
        }

        is Result.Success -> this
        is Result.SuccessEmpty -> this
    }
}

typealias EmptyResult<E> = Result<Unit, E>