# Build Templates

## Android APK Workflow

[`android_build.yml`](android_build.yml) is a GitHub Actions template for a Node.js application that has a configured [Capacitor](https://capacitorjs.com/) Android project. It installs Java 17 and the Android SDK, synchronizes the Capacitor project, builds a release APK, and uploads the APK as a workflow artifact.

The file is intentionally stored as a **template** rather than under `.github/workflows/`. The current PegaConstellation repositories do not contain a committed `android/` Capacitor project, so enabling this workflow now would create a predictable failing build rather than a useful CI check.

Before copying it into an application repository, confirm that the repository has a committed `package-lock.json`, a working `npm ci` install, Capacitor dependencies and configuration, an `android/` project, a tested Gradle wrapper, and any required signing configuration. The current template builds an unsigned release artifact; production signing should be added only through protected GitHub Secrets and an environment approval process.
