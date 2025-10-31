# SimpleDoc Android App

Android-first consumer app for document explanation.

## Package

`com.simpledoc.app`

## Modules

- **app**: Main application module
- **ingest**: CameraX/PDF import for document capture
- **ocr**: ML Kit Text Recognition v2 for on-device OCR
- **extractors**: Template-based field extraction engine
- **billing**: Play Billing v6 for subscriptions
- **network**: Retrofit/OkHttp client for API communication
- **design**: Material Design theme and components
- **i18n**: Localized strings (English, Hindi)

## Setup

1. Open project in Android Studio
2. Sync Gradle files
3. Configure API endpoint in `network` module
4. Add required dependencies (see TODOs in build.gradle.kts files)

## TODO

- Implement CameraX integration in `ingest` module
- Add ML Kit OCR in `ocr` module
- Implement template execution in `extractors` module
- Add Retrofit client in `network` module
- Integrate Play Billing in `billing` module
- Implement WhatsApp share functionality
- Add local reminders
- Complete Hindi localization
