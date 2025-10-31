plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
}

android {
    namespace = "com.simpledoc.app"
    compileSdk = 34

    defaultConfig {
        applicationId = "com.simpledoc.app"
        minSdk = 24
        targetSdk = 34
        versionCode = 1
        versionName = "1.0.0"
    }

    buildTypes {
        release {
            isMinifyEnabled = false
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro"
            )
        }
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
    // TODO: Add dependencies for ingest, ocr, extractors, billing, network modules
    implementation(project(":ingest"))
    implementation(project(":ocr"))
    implementation(project(":extractors"))
    implementation(project(":billing"))
    implementation(project(":network"))
    implementation(project(":design"))
    implementation(project(":i18n"))
}

