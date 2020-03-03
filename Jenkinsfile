node("jekyll") {
    checkout scm
    stage("plugins") {
        withCredentials([string(credentialsId: "netrc", variable: "netrc")]) {
            sh "echo $netrc > /home/jenkins/.netrc"
        }
        withEnv(['LC_ALL=C.UTF-8', 'LANG=C.UTF-8']) {
            sh "pipenv install --dev"
            sh "pipenv run python tools/plugins.py"
            sh "bundle install"
            sh "bundle exec jekyll build"
            withCredentials([string(credentialsId: "firebase", variable: "FIREBASE_TOKEN")]) {
                sh "firebase deploy"
            }
        }
    }
}