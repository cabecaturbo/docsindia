plugins {
    id("com.android.library")
    id("org.jetbrains.kotlin.android")
}

android {
    namespace = "com.simpledoc.ingest"
    compileSdk = 34

    defaultConfig {
        minSdk = 24
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }

    kotlinOptions {
        jvmTarget = "17"
    }
}

dependencies {
    // TODO: Add CameraX dependencies
    // implementation("androidx.camera:camera-camera2:1.3.0")
    // implementation("androidx.camera:camera-lifecycle:1.3.0")
    // implementation("androidx.camera:camera-view:1.3.0")
}

