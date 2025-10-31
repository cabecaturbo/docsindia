pluginManagement {
    repositories {
        google()
        mavenCentral()
        gradlePluginPortal()
    }
}

dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories {
        google()
        mavenCentral()
    }
}

rootProject.name = "SimpleDoc"

include(
    ":app",
    ":ingest",
    ":ocr",
    ":extractors",
    ":billing",
    ":network",
    ":design",
    ":i18n"
)

