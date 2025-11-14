"""Composants d'affichage pour la météo."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict

import streamlit as st

from .constants import WEATHER_CODE_DESCRIPTIONS, WEATHER_CODE_EMOJIS


def display_weather_forecast(forecast: Dict[str, Any], requested_datetime: datetime | None) -> None:
    """Affiche les informations météorologiques dans l'interface utilisateur."""
    if not forecast:
        return

    st.markdown("---")

    temperature = forecast.get("temp2m")
    weather_code = forecast.get("weather")
    weather_description = WEATHER_CODE_DESCRIPTIONS.get(weather_code, "Conditions indisponibles")
    weather_emoji = WEATHER_CODE_EMOJIS.get(weather_code, "🌈")

    summary_parts = []
    if temperature is not None:
        summary_parts.append(f"🌡️ {temperature}°C")
    summary_parts.append(f"{weather_emoji} {weather_description}")
    summary_text = " • ".join(summary_parts)

    summary_label = f"🌤️ Météo prévue : {summary_text}"

    with st.expander(summary_label):
        if requested_datetime:
            try:
                requested_local = requested_datetime.astimezone()
                st.markdown(
                    f"**Pour le {requested_local.strftime('%d/%m/%Y %H:%M')} ({requested_local.tzinfo})**"
                )
            except Exception:
                st.markdown(
                    f"**Pour le {requested_datetime.strftime('%d/%m/%Y %H:%M')}**"
                )

        try:
            raw_datetime = forecast["datetime"]
            try:
                forecast_dt = datetime.strptime(raw_datetime, "%Y-%m-%dT%H:%M:%S%z")
            except ValueError:
                forecast_dt = datetime.fromisoformat(raw_datetime)
            st.caption(f"Prévision fournie pour {forecast_dt.strftime('%d/%m/%Y %H:%M %Z')}")
        except (KeyError, ValueError):
            pass

        col_temp, col_weather = st.columns(2)
        with col_temp:
            if temperature is not None:
                st.metric("Température", f"{temperature}°C")
        with col_weather:
            st.metric("Conditions", f"{weather_emoji} {weather_description}")

        prob_rain = forecast.get("probarain")
        wind = forecast.get("wind10m")
        gust = forecast.get("gust10m")
        humidity = forecast.get("rh2m")

        details = []
        if prob_rain is not None:
            details.append(f"Probabilité de pluie : {prob_rain}%")
        if humidity is not None:
            details.append(f"Humidité : {humidity}%")
        if wind is not None:
            details.append(f"Vent moyen : {wind} km/h")
        if gust is not None:
            details.append(f"Rafales : {gust} km/h")

        if details:
            st.write(" • ".join(details))
