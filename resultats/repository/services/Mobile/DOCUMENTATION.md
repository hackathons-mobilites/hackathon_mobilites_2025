# PredictMob - Technical Documentation

## Overview

PredictMob is an Android application developed in Kotlin (with some Java), using Jetpack Compose for UI and Gradle for build automation. The app provides sustainable transport alternatives, route previews, and eco-friendly suggestions to reduce users' carbon footprint.

## Project Structure

- `app/`: Main Android application module.
  - `src/main/java/com/idfm/predictMob/`: Application source code.
    - `presentation/`: UI screens and composables (e.g., `AlternativesScreen.kt`).
    - `ui/theme/`: Theme and color definitions.
  - `res/`: Resources (layouts, drawables, values).
- `build.gradle`: Project and module build configuration.

## Main Technologies

- **Kotlin**: Primary language for app logic and UI.
- **Java**: Legacy or utility code (if present).
- **Jetpack Compose**: Modern UI toolkit for building native Android interfaces.
- **Material3**: UI components and theming.
- **Gradle**: Build system and dependency management.

## Key Components

### AlternativesScreen

- Displays the user's planned route and sustainable alternatives.
- Uses `Scaffold` and `TopAppBar` for layout.
- Shows a map preview (placeholder), current route, and suggestions.
- Each transport option is a `TransportOptionCard` composable.
- Users can select an alternative and validate their choice.

### TransportOptionCard

- Displays transport mode, duration, emissions, and XP reward.
- Highlights selection and provides a radio button for alternatives.
- Color-codes emissions for quick impact assessment.

## Theming

- Custom theme (`PredicMobTheme`) for consistent colors and styles.
- Uses Material3 theming for modern look and feel.

## Build & Run

1. Clone the repository:
   ```sh
   git clone https://github.com/cap-smarrekchi/PredictMob.git
   ```
2. Open in Android Studio.
3. Sync Gradle and build the project.
4. Run on an emulator or Android device.

## Packaging and Execution

### Packaging

- The project uses Gradle for build automation.
- To generate a release APK:
  1. Open a terminal in the project root.
  2. Run:
     ```sh
     ./gradlew assembleRelease
     ```
  3. The APK will be located in `app/build/outputs/apk/release/`.

### Execution

- To run the app:
  1. Open the project in Android Studio.
  2. Connect an Android device or start an emulator.
  3. Click **Run** or use:
     ```sh
     ./gradlew installDebug
     ```
  4. The app will launch on the selected device.

## Dependencies

- Jetpack Compose
- Material3
- Kotlin stdlib
- (Other dependencies as defined in `build.gradle`)

## Contribution

- Fork the repository and create feature branches.
- Follow Kotlin and Android best practices.
- Submit pull requests for review.

## License

See `LICENSE` file in the repository.

