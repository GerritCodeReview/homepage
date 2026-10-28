node("jekyll") {
    checkout scm
    stage("generate plugins page") {
        withEnv(['LC_ALL=C.UTF-8', 'LANG=C.UTF-8']) {
            withCredentials([usernamePassword(credentialsId: "gerrit-review.googlesource.com", usernameVariable: "username", passwordVariable: "password")]) {
                sh "pipenv install --dev"
                sh "pipenv run python tools/plugins.py --sleep 15"
            }
        }
    }
    stage("build homepage") {
        sh "bundle install"
        sh "bundle exec jekyll build"
    }
    stage("validate homepage") {
        sh "python3 -m unittest discover -s tests -p test_check_site.py -v"
        sh "python3 tools/check_site.py"
        sh "python3 tools/prepare_test_site.py"
        sh 'export BUNDLE_GEMFILE="$PWD/Gemfile"; cd _test/source; bundle exec jekyll build --destination ../site'
        sh "TEST_SITE=_test/site python3 -m unittest discover -s tests -p test_rendering.py -v"
    }
    stage("browser regression checks") {
        // Do not publish stale results if dependency installation fails.
        dir("test-results") { deleteDir() }
        dir("playwright-report") { deleteDir() }
        try {
            withEnv(["CI=1"]) {
                sh "npm ci"
                sh "npm run test:install-browser"
                sh "npm test"
            }
        } finally {
            junit testResults: "test-results/browser.xml", allowEmptyResults: true
            archiveArtifacts artifacts: "test-results/**,playwright-report/**", allowEmptyArchive: true
        }
    }
    stage("deploy homepage") {
        withCredentials([string(credentialsId: "firebase", variable: "FIREBASE_TOKEN")]) {
            sh "firebase use default"
            sh "firebase deploy"
        }
    }
}
